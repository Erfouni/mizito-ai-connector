# Mizito internal API map

Reverse-engineered on 2026-09-27 from the office.mizito.ir web app (AngularJS bundle `a_.js`,
`services.invokeApi`). Not an official or stable API: it can change when Mizito ships a new client.

## Transport

| | |
|---|---|
| Base URL | `https://app.mizito.ir` (`Config.App.api_url`) |
| Call | `POST /api/<module>/<method>`; the client's `"chat.getHistory"` maps to `/api/chat/getHistory` |
| Auth header | `x-token: <token>` (the web app keeps it in `localStorage.token`) |
| Body | JSON; `{}` when there are no params |
| Expired token | HTTP 401 → the web app goes to `login.login` |
| Login | `POST /capi/session/create` `{username, password: md5hex(pw) + "|" + sha256hex(pw), loginCode, regId}` → `{status, token}`; status 1 or 5 means success |
| Workspace | Each token is scoped to one workspace. `workspace.switch {workspace_id}` → `{token}` for the other workspace |
| Realtime | socket.io (not used here) |

## Verified request/response shapes

| Endpoint | Request | Response (abridged) |
|---|---|---|
| `workspace.userId` | `{}` | `{uid, wid, workspaces:[{_id,title,active}], is_guest, access_admin, remain_days, …}` |
| `workspace.getUsers` | `{}` | `{users:[{_id, first_name, last_name, role, status:{was_online}, deleted, invited}], user_status}` |
| `dashboard.getAllSummary` | `{}` | `[{workspace_id, workspace_title, inbox, chat, task:{today, overdue, with_time, no_time}, meetings}]` |
| `chat.getDialogs` | `{}` | `{dialogs:[{_id, is_group, is_customer_entity, unread_count, messages_count, last_message_date, peer_user}], pin_dialogs}` |
| `chat.getFullChat` | `{dialog}` | `{_id, title, is_group, is_project_group, participants, settings}` |
| `chat.getChatView` | `{dialog}` | `{unread_count, messages_count, last_message_date, seen, peer_user}` |
| `chat.getHistory` | `{dialog, offset}` | up to 15 messages `[{_id, from, date, message(html), msg_index, media, reply_to, mention, edited, deleted}]`. `offset` = number of newest messages to skip, so 0 returns the latest 15 |
| `chat.search` | `{mode:"chat"\|"customers", search_str, offset}` | messages plus `chat_full` (dialog) and `from_user` |
| `projects.getList` | `{}` | `{projects, project_status}` |
| `projects.allSummary` | `{}` or `{with_details:true}` | `{summaries}` |
| `tasks.upcoming` | `{inbox:true}` (mine) / `{outbox:true}` (following) / `{project_id, all:true}` + `{sort_type:"default", filter:null, from}`; completed tasks only via `{done_timeline:true, filter:{}, from}` | open (or done) task list, each with `access_token` |
| `tasks.getAll` | `{inbox:true, sort_type, filter}` | task list |
| `tasks.get` | `{token: access_token}` (share links: `{taskId:"sl…"}`) | full task: `{_id, title, notes(plain text), assignee:[ids], project, checklist:[{_id,title,checked}], progress, deadline, completed, access_token, …}` |
| `tasks.getComments` | `{token}` | `[{_id, comment(html), comment_at, comment_owner, edited, deleted}]` |
| `inbox.getInbox` | `{mode:"inbox", offset}` or `{mode:"outbox", offset, outbox_mode:"all"\|"only_created"}` | `[{_id, thread, subject, from, send_date, unread, count, short_content, raw_content, attachments_count}]` |
| `inbox.getHistory` | `{thread}` | the first letter itself `{_id(=thread), from, to:[{user,unread,seen_date}], receivers:[ids], subject, content(html), send_date, attachments, messages:[replies]}` |
| `labels.getAll` | `{type:"task"}` | labels |

**Security:** a task's `access_token` is a JWT whose payload embeds the user's session token (`x-token`) in plain base64. Never pass it to a model or log it.

## Verified write calls (2026-09-28)

| Endpoint | Request | Notes |
|---|---|---|
| `chat.send` | the web client's local message object `{_:"message", _id, local, dialog, out:true, message(html), media:null, from, date(ms), reply_to, mention:[], seen_count:1, randomId, pending:true}` | returns nothing useful; confirm via `chat.getHistory` |
| `chat.seen` | `{dialog, seen_count}` | marks read (sends read receipts) |
| `chat.createDialog` | `{user}` | the client only calls it when no private dialog with that user exists (not exercised) |
| `tasks.add` | `{title, notes(plain), assignee:[ids], project, kanban_board:null, labels:[], attachments:[], deleted:false, alarm_options:null, progress:0, weight:1, responsible:null, checklist:[{title, checked:false}], from_chat:false, from_minute:false, insert_to_chat_group:false}` + `deadline` only when set | **`project` is required**: without it the API answers `false` (the web form says «please select project») |
| `tasks.save` | same fields as `tasks.add` + `task_id`, `token` | whole editable task, not a diff |
| `tasks.newComment` | `{token, comment(html), attachments:[], mention:[], reply_id:null}` | endpoint name is built dynamically in the client, so it is missing from the list below |
| `tasks.setCompleted` | `{token, completed, project}` | completing sets progress to 100 |
| `tasks.updateDeadline` | `{token, project, deadline}` | ISO 8601 string, `null` clears |
| `tasks.updateProgress` | `{token, progress}` | |
| `tasks.setChecklistCheckedValue` | `{token, checklistId, checked}` | |
| `inbox.send` | `{to:[ids], subject, content(html), attachments:[], tasks_insert_to_chat_groups:[], labels:[]}`; reply adds `reply_to` (letter id) and `thread` | returns `true` |
| `notes.create` | `{title, note, photo:null, color, checklist:[{title, checked}], labels:[]}` | colors: white red orange yellow grey blue cyan green |
| `projects.add` | `{title, color:"grey", members:[ids]}` | returns `true`; find the id via `projects.getList` |

Names can use Arabic `ي` instead of Persian `ی` (e.g. the bot «دستيار ميزيتو»); normalise before matching.

## Parameters read from the client code (not yet exercised)

- `tasks.history {token, tid}`, `chat.getMessages {mids, dialog}`, `chat.getMessageByDate {dialog, date}`
- `projects.full {project_id}`, `projects.get {projectId, token}`, `projects.history {project_id}`, `projects.chatSummary {dialog, project, withBoards}`, `projects.save {project_id, title, color, members}`
- `inbox.expandInboxRow {thread, mode}`, `notes.update` (a note object with `_id`)
- `monitor.user {uid}`, `monitor.workspace {}` (HTTP 400 with `{}`), `session.userInfo {uid}`

## All 336 endpoints found in the client

**attendance**: delete, start, stop
**chat**: addPinMessage, archiveProject, convertDialogToNotPublic, convertMentionToUnProcessed, createDialog, deleteDialog, deleteUser, fixDialogs, getChatView, getDialogUnDoneTasksCount, getDialogs, getFullChat, getHistory, getMessageByDate, getMessageIndex, getMessages, getStatusDetails, inviteUser, loadSettings, pinDialog, removeMentionMessage, removePhoto, removePinMessage, removeTaskSnoozeMessage, saveSettings, search, seen, send, setAdmin, setTyping, toggleBookmark, unpinDialog, updatePhoto, updateSentMessage, updateTitle
**content**: getCroppedPhoto
**customer**: add, history, import, importPrepare, suggestParticipants, update, updateLabel
**dashboard**: acceptInviteRequest, cancelInviteRequest, checkWhatsNew, demoGuide, getAllBadges, getAllSummary, getAllWorkspacesUsers, getPending, notifySeen, setWhatsNewSeen
**deal**: add, getAll, getCustomerDeals, getReportStatistics, history, info, update
**device**: register
**feedback**: checkRequireParticipant, sendFeedback
**fix**: changeUser.changeChatGroups, changeUser.changeCustomers, changeUser.changeTasks, changeUser.history, chatGroups.getAll, chatGroups.getMembers, chatGroups.grantAccess, customer.getAll, customer.getMembers, customer.grantAccess, projects.getAll, projects.getMembers, projects.grantAccess
**formRequestTemplate**: add, getAll, getAllForms, getHistory, remove, save, submit, view
**inbox**: archive, archive.sender, changeMessageDialogs, changeMessageLabels, deleteMessage, expandInboxRow, getHistory, getInbox, getLastSecretariatStatus, getMessageDialogs, getMessageLabels, getSeenDetails, seen, send, setTyping, toggleBookmark, unArchive, unArchive.sender
**labels**: add, delete, getAll, history, save, sendUsage
**meeting**: broadcastMeetingMessage, create, endCall, get, ping, reject
**minute**: getTemplate, getTemplates, history, setMinuteAsTemplate, update
**minuteAdvanced**: deleteComment, editComment, get, getComments, getSmsHistory, getTemplates, newComment, sendDraft, sendForSign, sendSms, setMinuteAsTemplate, sign, update
**monitor**: chart.chatMessages, chart.customers, chart.getPast30DoneTasksPercents, chart.inboxMessages, chart.notes, chart.tasksAssigned, chart.tasksCreated, chart.tasksDone, customers, minutes, user, workspace
**notes**: archiveNote, create, deleteNote, getAll, setChecklistValue, setColor, setLabels, update, updatePinState
**payment**: add, checkDiscountCode, createUpgradeInvoice, getAllPayments, getCustomerPayments, getInvoice, getReportDetails, getReportStatistics, history, info, requestTrial, setWantToPay, update, uploadLastWaitingInvoicePayment
**polling**: getTemplates, printPollingResults, retractVote, setPollingAsTemplate, setPollingVote, stopPolling
**profile**: activate, changePhoneNumber, getEmailInfo, getProfileSecurity, removePhoto, setDontDisturbUntil, setOnlineStatus, setUserOptions, setWallpaper, terminateOneSession, terminateOtherSessions, turnTwoStepLoginOff, update, updateEmail, updatePassword, updatePhoto, verifyEmail
**projectAutomation**: buttonClicked, customParam.add, customParam.delete, customParam.getAll, customParam.getHistory, customParam.getValuesHistory, customParam.restore, customParam.update, customParam.updateOrder, delete, getAll, getHistory, getTaskAutomateButtons, loadConstants, updateOrder
**projectAutomationWorkflow**: add, delete, getAll, getOne, update
**projects**: activateAdvancedFeatures, add, addKanbanBoard, allSummary, archive, chatSummary, clone, full, ganttRemoveTask, get, getAdvancedFeaturesHistory, getList, getListAdmin, getListAdminForMember, getProjectFiles, getProjectTaskFileIds, getProjectsUserAdmin, history, import, importPrepare, removeKanbanBoard, restoreArchivedTasks, save, setAdvancedFeatures, setChatProjectColor, setChatProjectLabels, setKanbanBoardOrder, undoArchive, updateKanbanBoard
**session**: createSSO, deleteAccount, deleteAccountRequest, forgot, forgotReset, iOSAppIsAlive, register, userInfo, username
**support**: clientOnlineHistory, closeResponse, deleteFromClient, deleteResponse, deleteResponseFeedback, editFromClient, editResponse, extendDialogLock, getAdminHistory, getClientUnreadCount, getDialog, getDialogs, getFeedbackMonitor, getFeedbackMonitorOpenCount, getFeedbackMonitorStats, getFeedbackReviewCase, getSupportInfo, lockDialog, markClientSeen, markSupportSeen, reopenFeedbackReview, resolveFeedbackReview, searchContent, sendFromClient, sendResponse, sendSuggestion, setResponseFeedbackVote, setTyping, setTypingAdmin, startFeedbackReview, unlockDialog, updateResponseFeedbackDetails
**taskTemplates**: add, getAll, getAllTemplates, remove, save
**tasks**: add, checkToken, createShareLink, deleteComment, editComment, ganttGetTaskInfo, get, getAll, getComments, getSeenDetails, history, print, removeFromBoard, removeFromTracking, removeTask, removeTaskUndo, save, setChecklistCheckedValue, setCompleted, setKanbanWeight, setKanbanWeightSort, snooze, toggleBookmark, upcoming, updateDeadline, updateProgress
**workspace**: add, changeOwner, changeRole, delete, getPermissions, getPlans, getUsers, ignoreBusinessTypeModal, inviteMember, name, planInfo, reJoinMember, removeMember, sendContactUsage, setWorkspaceSettings, switch, updateBusinessType, updateDedicatedLogoPhoto, updateTitle, updateUserPermission, updateWorkspaceRoleName, userId
