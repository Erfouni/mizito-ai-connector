# همه‌ی endpointهای API میزیتو

369 endpoint از کد وب‌اپ، از جمله آن‌هایی که اسمشان با عبارت شرطی ساخته می‌شود. همه `POST {api_url}/api/<ماژول>/<متد>` با هدر `x-token` هستند.
«پارامترها» کلیدهای payload در محل فراخوانی‌اند (`var:x` یعنی شیء از قبل ساخته شده، `-` یعنی بدون payload).
«محل فراخوانی» سرویس یا کنترلر و تابعی در کد وب است که آن را صدا می‌زند.

| وضعیت در MCP | تعداد |
|---|---|
| ⛔ رد شد | 24 |
| ✅ تست‌شده | 103 |
| ➖ پیاده‌نشده | 84 |
| 🔎 با `mizito_api_read` | 29 |
| 🟡 پیاده‌شده، تست‌نشده | 129 |

## `attendance` — حضور و غیاب (5)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `attendance.delete` | `attendanceId` | service:AppAttendanceManager › removeRow | 🟡 پیاده‌شده، تست‌نشده | `mizito_attendance` — به انتخاب کاربر تست نشد |
| `attendance.getHistory` | `var:A` | service:AppAttendanceManager › showManualLog | ⛔ رد شد | 405 (حضور دستی در این میزکار خاموش است) — `mizito_attendance_history` |
| `attendance.getOnlineHistory` | `var:A` | service:AppAttendanceManager › showOnlineLog | ✅ تست‌شده | `mizito_attendance_history` |
| `attendance.start` | `-` | service:AppAttendanceManager › start | 🟡 پیاده‌شده، تست‌نشده | `mizito_attendance` — به انتخاب کاربر تست نشد |
| `attendance.stop` | `-` | service:AppAttendanceManager › stop | 🟡 پیاده‌شده، تست‌نشده | `mizito_attendance` — به انتخاب کاربر تست نشد |

## `chat` — گفتگو (37)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `chat.addPinMessage` | `dialog,message` | service:AppChatsManager › confirmAddPingMessage | ✅ تست‌شده | `mizito_manage_message` |
| `chat.archiveProject` | `dialog,project,withArchiveTasks` | service:AppProjectsManager › showArchiveProjectSelectorDialog | ✅ تست‌شده | `mizito_archive_project` |
| `chat.convertDialogToNotPublic` | `dialog` | service:AppChatsManager › convertToNotPublicGroup | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_conversation` |
| `chat.convertMentionToUnProcessed` | `dialog,mid` | service:AppImManager › convertMentionToUnProcessed | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_message` |
| `chat.createDialog` | `user` \| `var:b` | service:AppPeersManager › onDomRemoved<br>service:AppPeersManager › showChatWithRoute | ✅ تست‌شده | `mizito_create_group`, `mizito_create_project`, `mizito_start_conversation` |
| `chat.deleteDialog` | `dialog` | service:AppChatsManager › deleteGroup | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_conversation` — حذف برگشت‌ناپذیر گروه؛ با confirm محافظت می‌شود؛ تست نشد |
| `chat.deleteUser` | `dialog,user` | service:AppChatsManager › deleteUser | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_conversation`, `mizito_update_project` — روی گروه واقعی اثر دارد؛ تست نشد |
| `chat.fixDialogs` | `dialog` | service:AppPeersManager › reset | ➖ پیاده‌نشده | تعمیر داخلی فهرست گفتگو |
| `chat.getChatView` | `dialog` | service:AppImManager › getHistory | ✅ تست‌شده | `messages_count` |
| `chat.getDialogUnDoneTasksCount` | `dialog` | controller:CrmHeaderCtrl › toggleShowPayments | ✅ تست‌شده | `mizito_get_conversation` |
| `chat.getDialogs` | `-` | service:AppPeersManager › reset | ✅ تست‌شده | `dialog_row`, `mizito_list_conversations`, `mizito_list_customers`, `mizito_start_conversation` |
| `chat.getFullChat` | `dialog` | service:AppChatProfileManager › forceFullChatUpdate<br>service:AppChatProfileManager › handleEscapeKey | ✅ تست‌شده | `chat_full`, `dialog_title` |
| `chat.getHistory` | `var:d` | service:AppImManager › getHistory | ✅ تست‌شده | `_first_index_since`, `mizito_get_messages`, `send_chat` |
| `chat.getMessageByDate` | `dialog,date` | service:AppImManager › getMessageByDate | ✅ تست‌شده | `mizito_get_messages` |
| `chat.getMessageIndex` | `dialog,mid` | service:AppImManager › getMessageIndex | ✅ تست‌شده | `mizito_get_messages` |
| `chat.getMessages` | `mids,dialog` | directive:myPeerOnlineStatusLink › setVote<br>service:AppImManager › ? | ✅ تست‌شده | `load_message` |
| `chat.getStatusDetails` | `dialog,mid` | service:AppImManager › convertMentionToUnProcessed | ✅ تست‌شده | `mizito_get_message_info`, `mizito_manage_message` |
| `chat.inviteUser` | `dialog,user` | service:AppChatsManager › inviteUser | 🟡 پیاده‌شده، تست‌نشده | `mizito_add_project_members`, `mizito_manage_conversation`, `mizito_update_project` — به همکار واقعی اعلان می‌رود؛ تست نشد |
| `chat.loadSettings` | `-` | service:AppPeersManager › loadNotificationSettings | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `chat.pinDialog` | `dialog` | service:AppPeersManager › toggleSetPin | ✅ تست‌شده | `mizito_manage_conversation` |
| `chat.removeMentionMessage` | `mid,dialog` | service:AppImManager › removeMentionMessage | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_message` |
| `chat.removePhoto` | `dialog` | service:AppChatsManager › removePhoto | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_conversation` |
| `chat.removePinMessage` | `dialog,message` | service:AppChatsManager › confirmRemovePingMessage | ✅ تست‌شده | `mizito_manage_message` |
| `chat.removeSentMessage` | `dialog,mid` | service:AppImManager › removeMessage | ✅ تست‌شده | `mizito_manage_message` |
| `chat.removeSentMessageAdmin` | `dialog,mid` | service:AppImManager › removeMessage | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_message` |
| `chat.removeTaskSnoozeMessage` | `mid,dialog,task_id` | service:AppImManager › removeSnoozeMessage | ➖ پیاده‌نشده | پیام یادآوری ربات؛ داخلی |
| `chat.saveSettings` | `dialog,mute` | service:AppChatsManager › showProjectAdvancedFeaturesModal | ✅ تست‌شده | `mizito_manage_conversation` |
| `chat.search` | `var:f` | service:AppImManager › searchMessages | ✅ تست‌شده | `mizito_search_messages` |
| `chat.seen` | `dialog,seen_count` | service:AppImManager › markSeen | ✅ تست‌شده | `mizito_mark_conversation_read` |
| `chat.send` | `var:b` | service:AppImManager › ? | ✅ تست‌شده | `send_chat` |
| `chat.setAdmin` | `dialog,user,isAdmin` | service:AppChatsManager › setAdminUser | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_conversation` — روی گروه واقعی اثر دارد؛ تست نشد |
| `chat.setTyping` | `dialog` | controller:ChatViewCtrl › showRobotHelp | ➖ پیاده‌نشده | نشانگر «در حال نوشتن» |
| `chat.toggleBookmark` | `dialog,mid,bookmarked` | service:AppImManager › ? | ✅ تست‌شده | `mizito_manage_message` |
| `chat.unpinDialog` | `dialog` | service:AppPeersManager › toggleUnPin | ✅ تست‌شده | `mizito_manage_conversation` |
| `chat.updatePhoto` | `dialog,photo` | service:AppChatsManager › changePhoto | ➖ پیاده‌نشده | برش تصویر در مرورگر |
| `chat.updateSentMessage` | `dialog,mid,log` \| `dialog,mid,newMessage` | controller:ChatViewCtrl › ?<br>service:AppCallLogManager › createLog<br>service:AppImManager › update | ✅ تست‌شده | `mizito_manage_message` |
| `chat.updateTitle` | `dialog,title` | service:AppChatsManager › updateTitle | ✅ تست‌شده | `mizito_manage_conversation`, `mizito_update_project` |

## `content` — فایل و محتوا (2)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `content.getCroppedPhoto` | `base,points` | service:AppFilesManager › showUploaderWithCropper | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `content.getDownloadLink` | `content` | factory:services › closeToast | ✅ تست‌شده | `_download_url` |

## `customer` — CRM – مشتریان (7)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `customer.add` | `var:d` | service:AppCustomersManager › createCustomer | ⛔ رد شد | 400 (CRM در پلن نیست) — `mizito_create_customer` |
| `customer.history` | `customer_id` | service:AppCustomersManager › showChangesHistory | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_customer` |
| `customer.import` | `contentId,members,labelAssign,fieldIndexes` | controller:AppImportCustomersController › importCustomers | ➖ پیاده‌نشده | ورود از Excel: ویزارد وب |
| `customer.importPrepare` | `contentId` | controller:AppImportCustomersController › prepareRows | ➖ پیاده‌نشده | ورود از Excel: ویزارد وب |
| `customer.suggestParticipants` | `-` | service:AppCustomersManager › reset | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `customer.update` | `var:d` | service:AppCustomersManager › createCustomer | 🟡 پیاده‌شده، تست‌نشده | `mizito_update_customer` |
| `customer.updateLabel` | `customer_id,is_add,label_id` | service:AppCustomersManager › updateLabel | 🟡 پیاده‌شده، تست‌نشده | `mizito_update_customer` |

## `dashboard` — داشبورد (11)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `dashboard.acceptInviteRequest` | `workspace` | controller:AppDashboardController › acceptInvite | 🟡 پیاده‌شده، تست‌نشده | `mizito_respond_workspace_invitation` — دعوتی در حساب تست نبود |
| `dashboard.cancelInviteRequest` | `workspace` | controller:AppDashboardController › cancelInvite | 🟡 پیاده‌شده، تست‌نشده | `mizito_respond_workspace_invitation` — دعوتی در حساب تست نبود |
| `dashboard.checkWhatsNew` | `-` | controller:HeaderController › showBookmarksPage | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `dashboard.demoGuide` | `-` | controller:AppWorkspaceController › showDemoGuide | ➖ پیاده‌نشده | راهنمای نسخه‌ی دمو |
| `dashboard.getAllBadges` | `only_badges` | service:AppWorkspaceManager › cancel | ✅ تست‌شده | `mizito_workspace_info` |
| `dashboard.getAllSummary` | `-` | controller:AppDashboardController › setWallpaper | ✅ تست‌شده | `mizito_dashboard` |
| `dashboard.getAllWorkspacesUsers` | `-` | controller:AppDashboardController › setWallpaper | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `dashboard.getPending` | `-` | controller:AppDashboardController › dashboardMeetingCallRemove<br>controller:AppDashboardController › setWallpaper | ✅ تست‌شده | `mizito_workspace_info` |
| `dashboard.notifySeen` | `-` | controller:AppDashboardController › setWallpaper | ➖ پیاده‌نشده | داخلی رابط وب |
| `dashboard.setWhatsNewSeen` | `-` | controller:HeaderController › showWhatsNew | ➖ پیاده‌نشده | اعلان «چه خبر؟» رابط وب |
| `dashboard.whatsNew` | `-` | factory:services › showWhatsNew | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |

## `deal` — CRM – معاملات (7)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `deal.add` | `var:c` | service:AppDealsManager › createDeal | 🟡 پیاده‌شده، تست‌نشده | `mizito_save_deal` |
| `deal.getAll` | `var:a` | service:AppDealsManager › getAllDeals | ⛔ رد شد | 400 (فروش در پلن نیست) — `mizito_list_deals` |
| `deal.getCustomerDeals` | `customer` | service:AppDealsManager › getCustomerSales | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_customer` |
| `deal.getReportStatistics` | `filter` | service:AppDealsManager › getReportStatistics | ⛔ رد شد | 400 (فروش در پلن نیست) — `mizito_list_deals` |
| `deal.history` | `deal_id` | service:AppDealsManager › showChangesHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `deal.info` | `deal_id` | service:AppDealsManager › showDeal | 🟡 پیاده‌شده، تست‌نشده | `mizito_save_deal` |
| `deal.update` | `var:c` | service:AppDealsManager › createDeal | 🟡 پیاده‌شده، تست‌نشده | `mizito_save_deal` |

## `device` — دستگاه و اعلان (1)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `device.register` | `subscription,iOS,regId,deviceName,deviceId,versionCode,versionName` | factory:notificationIOSService › isFirefox | ➖ پیاده‌نشده | ثبت دستگاه برای اعلان: داخلی |

## `feedback` — بازخورد (2)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `feedback.checkRequireParticipant` | `-` | service:AppProfileManager › snooze | ➖ پیاده‌نشده | نظرسنجی رضایت میزیتو: خارج از محدوده |
| `feedback.sendFeedback` | `feedback` | service:AppProfileManager › close<br>service:AppProfileManager › noAnswer<br>service:AppProfileManager › snooze | ➖ پیاده‌نشده | نظرسنجی رضایت میزیتو: خارج از محدوده |

## `fix` — ابزار اصلاح داده (مدیر) (13)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `fix.changeUser.changeChatGroups` | `fromUser,toUser` | service:AppFixChangeUserManager › update | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_transfer_member_work` |
| `fix.changeUser.changeCustomers` | `fromUser,toUser` | service:AppFixChangeUserManager › update | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_transfer_member_work` |
| `fix.changeUser.changeTasks` | `fromUser,toUser` | service:AppFixChangeUserManager › update | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_transfer_member_work` |
| `fix.changeUser.history` | `-` | service:AppFixChangeUserManager › wrapForHistory | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_transfer_member_work` |
| `fix.chatGroups.getAll` | `filter` | controller:AppFixChatGroupsController › load | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_list_all` |
| `fix.chatGroups.getMembers` | `dialog` | controller:AppFixChatGroupsController › showMembers | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_list_all` |
| `fix.chatGroups.grantAccess` | `dialogIds,userId,access` \| `dialogIds,users,access` | controller:AppFixChatGroupsController › addMember<br>controller:AppFixChatGroupsController › grantAccessToUser<br>controller:AppFixChatGroupsController › removeMember | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_grant_access` |
| `fix.customer.getAll` | `filter` | controller:AppFixCustomersController › load | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_list_all` |
| `fix.customer.getMembers` | `customer` | controller:AppFixCustomersController › showMembers | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_list_all` |
| `fix.customer.grantAccess` | `customerIds,userId,access` \| `customerIds,users,access` | controller:AppFixCustomersController › addMember<br>controller:AppFixCustomersController › grantAccessToUser<br>controller:AppFixCustomersController › removeMember | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_grant_access` |
| `fix.projects.getAll` | `filter` | controller:AppFixProjectsController › load | ⛔ رد شد | 400 برای غیرمدیر — `mizito_admin_list_all` |
| `fix.projects.getMembers` | `project` | controller:AppFixProjectsController › showMembers | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_list_all` |
| `fix.projects.grantAccess` | `projectIds,userId,access` \| `projectIds,users,access` | controller:AppFixProjectsController › addMember<br>controller:AppFixProjectsController › grantAccessToUser<br>controller:AppFixProjectsController › removeMember<br>service:AppProjectsManager › showArchiveProjectSelectorDialog | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_grant_access`, `mizito_admin_restore_project` |

## `formRequestTemplate` — فرم‌های درخواست (10)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `formRequestTemplate.add` | `projectId,form` | service:AppProjectAutomationFormRequestsManager › cancel | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `formRequestTemplate.getAll` | `projectId` | service:AppProjectAutomationFormRequestsManager › cancel | ✅ تست‌شده | `mizito_get_project_automation` |
| `formRequestTemplate.getAllForms` | `-` | service:AppProjectAutomationFormRequestsManager › getAllForms | ✅ تست‌شده | `mizito_list_request_forms` |
| `formRequestTemplate.getHistory` | `projectId,templateId` | service:AppProjectAutomationFormRequestsManager › ? | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `formRequestTemplate.getTaskWorkflow` | `token` | service:AppProjectAutomationWorkflowManager › ensureFormTemplateForWorkflowKey | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_task_extras` |
| `formRequestTemplate.newComment` | `token,comment,attachments,mention,reply_id` | service:AppTasksManager › sendNewComment | 🟡 پیاده‌شده، تست‌نشده | `mizito_comment_on_task` |
| `formRequestTemplate.remove` | `projectId,formId` | service:AppProjectAutomationFormRequestsManager › delete | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `formRequestTemplate.save` | `projectId,form` | service:AppProjectAutomationFormRequestsManager › cancel | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `formRequestTemplate.submit` | `templateId,custom_params_values` | service:AppProjectAutomationFormRequestsManager › showFormInput | 🟡 پیاده‌شده، تست‌نشده | `mizito_submit_request_form` |
| `formRequestTemplate.view` | `templateId` | service:AppProjectAutomationFormRequestsManager › showFormInput | 🟡 پیاده‌شده، تست‌نشده | `mizito_list_request_forms`, `mizito_submit_request_form` |

## `inbox` — کارتابل نامه‌ها (21)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `inbox.archive` | `thread` | service:AppInboxManager › archive | ✅ تست‌شده | `mizito_manage_letter` |
| `inbox.archive.sender` | `thread` | service:AppInboxManager › archive | ✅ تست‌شده | `mizito_manage_letter` |
| `inbox.badge` | `-` | factory:services › getInboxBadge | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `inbox.changeMessageDialogs` | `thread,dialogs` | service:AppInboxManager › onDone | ✅ تست‌شده | `mizito_manage_letter` |
| `inbox.changeMessageLabels` | `thread,labels` | service:AppInboxManager › changeLabels | ✅ تست‌شده | `mizito_manage_letter` |
| `inbox.deleteMessage` | `mid,isDeleteThread` | controller:AppInboxController › deleteMessage | ✅ تست‌شده | `mizito_manage_letter` |
| `inbox.expandInboxRow` | `thread,mode` | service:AppInboxManager › expandInboxRow | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `inbox.getHistory` | `thread` | service:AppInboxManager › getHistory | ✅ تست‌شده | `_locate`, `mizito_get_letter_thread`, `mizito_manage_letter`, `mizito_reply_letter` |
| `inbox.getInbox` | `var:d` | service:AppInboxManager › loadInbox | ✅ تست‌شده | `mizito_list_letters` |
| `inbox.getLastSecretariatStatus` | `-` | service:AppSecretariatManager › reset | ⛔ رد شد | 400 (دبیرخانه در پلن نیست) — `mizito_register_letter` |
| `inbox.getMessageDialogs` | `thread` | controller:AppInboxController › togglePinNote | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_letter_thread` |
| `inbox.getMessageLabels` | `thread` | service:AppInboxManager › getHistory | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_letter_thread` |
| `inbox.getSeenDetails` | `thread,msgId` | service:AppInboxManager › showSeenDetails | ✅ تست‌شده | `mizito_get_letter_thread` |
| `inbox.registerInLetter` | `thread,letterOptions` | service:AppSecretariatManager › setCustomNumber | 🟡 پیاده‌شده، تست‌نشده | `mizito_register_letter` |
| `inbox.registerOutLetter` | `thread,letterOptions` | service:AppSecretariatManager › setCustomNumber | 🟡 پیاده‌شده، تست‌نشده | `mizito_register_letter` |
| `inbox.seen` | `thread` | service:AppInboxManager › markAsSeen | ✅ تست‌شده | `mizito_manage_letter` |
| `inbox.send` | `var:b` | service:AppInboxManager › send | ✅ تست‌شده | `mizito_reply_letter`, `mizito_send_letter` |
| `inbox.setTyping` | `thread` | service:AppInboxManager › setTyping | ➖ پیاده‌نشده | نشانگر «در حال نوشتن» |
| `inbox.toggleBookmark` | `thread,bookmarked` | service:AppInboxManager › toggleBookmark | ✅ تست‌شده | `mizito_manage_letter` |
| `inbox.unArchive` | `thread` | service:AppInboxManager › unArchive | ✅ تست‌شده | `mizito_manage_letter` |
| `inbox.unArchive.sender` | `thread` | service:AppInboxManager › unArchive | ✅ تست‌شده | `mizito_manage_letter` |

## `labels` — برچسب‌ها (6)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `labels.add` | `title,color,type` | service:AppLabelManager › isVisible | ✅ تست‌شده | `mizito_create_label` |
| `labels.delete` | `label_id,label_type` | service:AppLabelManager › isVisible | ✅ تست‌شده | `mizito_manage_label` |
| `labels.getAll` | `type` | service:AppLabelManager › isVisible | ✅ تست‌شده | `mizito_create_label`, `mizito_list_labels`, `mizito_manage_label` |
| `labels.history` | `label_id` | service:AppLabelManager › showChangesHistory | ✅ تست‌شده | `mizito_manage_label` |
| `labels.save` | `label_id,type,title,color` | service:AppLabelManager › isVisible | ✅ تست‌شده | `mizito_manage_label` |
| `labels.sendUsage` | `label_id,type` | service:AppLabelManager › isVisible | ➖ پیاده‌نشده | آمار استفاده‌ی داخلی وب |

## `meeting` — جلسه‌ی تصویری (6)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `meeting.broadcastMeetingMessage` | `meeting,message` | service:AppMeetingManager › sendBroadcast | ➖ پیاده‌نشده | تماس تصویری (WebRTC): از طریق MCP قابل استفاده نیست |
| `meeting.create` | `dialog,members,tab` | service:AppMeetingManager › resetWorkspace | ➖ پیاده‌نشده | تماس تصویری (WebRTC): از طریق MCP قابل استفاده نیست |
| `meeting.endCall` | `meeting,socket,tab` | controller:AppDashboardController › dashboardMeetingCallRemove<br>controller:AppMeetingViewerController › mobileToggleUserFullScreen | ➖ پیاده‌نشده | تماس تصویری (WebRTC): از طریق MCP قابل استفاده نیست |
| `meeting.get` | `meeting,socket,tab` | controller:AppMeetingViewerController › createMeeting | ➖ پیاده‌نشده | تماس تصویری (WebRTC): از طریق MCP قابل استفاده نیست |
| `meeting.ping` | `meeting,socket,tab` | service:AppMeetingManager › ping | ➖ پیاده‌نشده | تماس تصویری (WebRTC): از طریق MCP قابل استفاده نیست |
| `meeting.reject` | `meeting` | service:AppMeetingManager › rejectCall | ➖ پیاده‌نشده | تماس تصویری (WebRTC): از طریق MCP قابل استفاده نیست |

## `minute` — صورتجلسه (5)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `minute.getTemplate` | `template` | service:AppMinutesManager › selectTemplate<br>service:AppMinutesManager › showMinute | 🟡 پیاده‌شده، تست‌نشده | `mizito_create_minute` |
| `minute.getTemplates` | `-` | service:AppMinutesManager › clickOutsideToClose | ✅ تست‌شده | `mizito_list_templates` |
| `minute.history` | `minute_id` | service:AppMinutesManager › showChangesHistory | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_minute` |
| `minute.setMinuteAsTemplate` | `var:d` | service:AppMinutesManager › toggleTemplate | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_minute` |
| `minute.update` | `dialog,minute` | service:AppMinutesManager › createMinute | ✅ تست‌شده | `mizito_manage_minute` |

## `minuteAdvanced` — صورتجلسه‌ی پیشرفته (13)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `minuteAdvanced.deleteComment` | `minuteId,commentId` | service:AppMinutesAdvancedManager › deleteComment | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_advanced_minute` |
| `minuteAdvanced.editComment` | `minuteId,commentId,newComment` | service:AppMinutesAdvancedManager › update | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_advanced_minute` |
| `minuteAdvanced.get` | `minuteId` | service:AppMinutesAdvancedManager › sendForSign | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_minute`, `mizito_manage_advanced_minute` |
| `minuteAdvanced.getComments` | `minuteId` | service:AppMinutesAdvancedManager › reset | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_minute` |
| `minuteAdvanced.getSmsHistory` | `minuteId` | service:AppMinutesAdvancedManager › reset | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_minute` |
| `minuteAdvanced.getTemplates` | `-` | service:AppMinutesAdvancedManager › sendForSign | ✅ تست‌شده | `mizito_list_templates` |
| `minuteAdvanced.newComment` | `minuteId,comment,attachments` | service:AppMinutesAdvancedManager › sendNewComment | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_advanced_minute` |
| `minuteAdvanced.sendDraft` | `minuteId,dialog,project` | service:AppMinutesAdvancedManager › sendDraft | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_advanced_minute` |
| `minuteAdvanced.sendForSign` | `minuteId,dialog,project` | service:AppMinutesAdvancedManager › sendForSign | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_advanced_minute` |
| `minuteAdvanced.sendSms` | `minuteId,dialog,project,template` | service:AppMinutesAdvancedManager › sendNewSms | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_advanced_minute` |
| `minuteAdvanced.setMinuteAsTemplate` | `minuteId,isActive` | service:AppMinutesAdvancedManager › toggleTemplate | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_advanced_minute` |
| `minuteAdvanced.sign` | `mid,dialog,minuteId` | service:AppMinutesAdvancedManager › signMinute | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_advanced_minute` |
| `minuteAdvanced.update` | `minute,dialog,project` | service:AppMinutesAdvancedManager › removeMembersOther | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_advanced_minute` |

## `monitor` — گزارش و مانیتورینگ (16)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `monitor.attendanceUserHistory` | `-` | service:AppAttendanceManager › showManualLog | 🟡 پیاده‌شده، تست‌نشده | `mizito_attendance_history` |
| `monitor.attendanceUserOnlineHistory` | `-` | service:AppAttendanceManager › showOnlineLog | 🟡 پیاده‌شده، تست‌نشده | `mizito_attendance_history` |
| `monitor.chart.chatMessages` | `-` \| `uid` | controller:AppMonitoringController › reload<br>controller:AppMonitoringUserController › reload | 🟡 پیاده‌شده، تست‌نشده | `mizito_reports` |
| `monitor.chart.customers` | `-` \| `uid` | controller:AppMonitoringController › reload<br>controller:AppMonitoringUserController › reload | 🟡 پیاده‌شده، تست‌نشده | `mizito_reports` |
| `monitor.chart.getPast30DoneTasksPercents` | `-` \| `var:e` | controller:AppMonitoringController › showTasksDoneMonitoring<br>controller:AppMonitoringProjectsController › showCalendarPage | 🟡 پیاده‌شده، تست‌نشده | `mizito_reports` |
| `monitor.chart.inboxMessages` | `-` \| `uid` | controller:AppMonitoringController › reload<br>controller:AppMonitoringUserController › reload | 🟡 پیاده‌شده، تست‌نشده | `mizito_reports` |
| `monitor.chart.notes` | `-` \| `uid` | controller:AppMonitoringController › reload<br>controller:AppMonitoringUserController › reload | 🟡 پیاده‌شده، تست‌نشده | `mizito_reports` |
| `monitor.chart.tasksAssigned` | `uid` \| `uid,not_owner` | controller:AppMonitoringUserController › reload | 🟡 پیاده‌شده، تست‌نشده | `mizito_reports` |
| `monitor.chart.tasksCreated` | `-` \| `uid` | controller:AppMonitoringController › reload<br>controller:AppMonitoringUserController › reload | 🟡 پیاده‌شده، تست‌نشده | `mizito_reports` |
| `monitor.chart.tasksDone` | `-` \| `uid` | controller:AppMonitoringController › reload<br>controller:AppMonitoringUserController › reload | ⛔ رد شد | 400 (دسترسی مدیر/پلن) — `mizito_reports` |
| `monitor.customers` | `filter` | controller:AppMonitoringCustomersController › load | 🟡 پیاده‌شده، تست‌نشده | `mizito_reports` |
| `monitor.minutes` | `filter` | controller:AppMonitoringMinutesController › doFilter | ⛔ رد شد | 400 (دسترسی مدیر/پلن) — `mizito_reports` |
| `monitor.project` | `projectId` | controller:AppMonitoringProjectController › print | ⛔ رد شد | 400 (دسترسی مدیر/پلن) — `mizito_reports` |
| `monitor.projectsSummary` | `var:e` | controller:AppMonitoringProjectsController › showCalendarPage | ⛔ رد شد | 400 (دسترسی مدیر/پلن) — `mizito_reports` |
| `monitor.user` | `uid` | controller:AppMonitoringUserController › reload | ⛔ رد شد | 400 (دسترسی مدیر/پلن) — `mizito_reports` |
| `monitor.workspace` | `-` | controller:AppMonitoringController › reload | ⛔ رد شد | 400 (دسترسی مدیر/پلن) — `mizito_reports` |

## `notes` — یادداشت‌ها (9)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `notes.archiveNote` | `note_id,archived` | service:AppNotesManager › archiveNote<br>service:AppNotesManager › unArchiveNote | ✅ تست‌شده | `mizito_manage_note` |
| `notes.create` | `var:b` | service:AppNotesManager › addNote | ✅ تست‌شده | `mizito_create_note` |
| `notes.deleteNote` | `note_id,deleted` | service:AppNotesManager › deleteNote<br>service:AppNotesManager › unDeleteNote | ✅ تست‌شده | `mizito_manage_note` |
| `notes.getAll` | `var:a` | service:AppNotesManager › loadNotes | ✅ تست‌شده | `_find_note`, `mizito_list_notes` |
| `notes.setChecklistValue` | `note_id,check_index,checked` | service:AppNotesManager › setNoteChecklistValue | ✅ تست‌شده | `mizito_manage_note` |
| `notes.setColor` | `note_id,color` | service:AppNotesManager › setNoteColor | ➖ پیاده‌نشده | با notes.update انجام می‌شود (mizito_update_note) |
| `notes.setLabels` | `note_id,labels` | controller:AppNotesController › showLabelSelector | 🟡 پیاده‌شده، تست‌نشده | `mizito_update_note` |
| `notes.update` | `var:b` | service:AppNotesManager › addNote | ✅ تست‌شده | `mizito_update_note` |
| `notes.updatePinState` | `pinned,noteId` | service:AppNotesManager › updatePinState | ✅ تست‌شده | `mizito_manage_note` |

## `payment` — پرداخت و صورتحساب (14)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `payment.add` | `payment` | service:AppPaymentsManager › createPayment | 🟡 پیاده‌شده، تست‌نشده | `mizito_save_payment` |
| `payment.checkDiscountCode` | `discountCode,planId` | controller:AppWorkspaceSettingsController › checkCouponCode | ➖ پیاده‌نشده | خرید و پرداخت اشتراک: عمداً ابزار ندارد (تراکنش مالی) |
| `payment.createUpgradeInvoice` | `plan_id,discount_code,request_enterprise,is_online` | service:AppWorkspaceManager › close | ➖ پیاده‌نشده | خرید و پرداخت اشتراک: عمداً ابزار ندارد (تراکنش مالی) |
| `payment.getAllPayments` | `var:a` | service:AppPaymentsManager › getAllPayments | ➖ پیاده‌نشده | فهرست جزئی پرداخت‌ها با فیلتر پیچیده‌ی وب؛ آمار و پرداخت‌های هر مشتری ابزار دارند |
| `payment.getCustomerPayments` | `customer` | service:AppPaymentsManager › getCustomerPayments | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_customer` |
| `payment.getInvoice` | `invoice` | service:AppWorkspaceManager › close<br>service:AppWorkspaceManager › showInvoice | ➖ پیاده‌نشده | خرید و پرداخت اشتراک: عمداً ابزار ندارد (تراکنش مالی) |
| `payment.getReportDetails` | `var:a` | service:AppPaymentsManager › getReportDetails | ➖ پیاده‌نشده | جزئیات ماهانه‌ی گزارش؛ آمار کلی ابزار دارد |
| `payment.getReportStatistics` | `filter` | service:AppPaymentsManager › getReportStatistics | 🟡 پیاده‌شده، تست‌نشده | `mizito_payment_report` |
| `payment.history` | `payment_id` | service:AppPaymentsManager › showChangesHistory | ➖ پیاده‌نشده | سابقه‌ی تغییر سند مالی |
| `payment.info` | `payment_id` | service:AppPaymentsManager › showPayment | 🟡 پیاده‌شده، تست‌نشده | `mizito_save_payment` |
| `payment.requestTrial` | `planId,request_enterprise` | controller:AppWorkspaceSettingsController › requestTrial | ➖ پیاده‌نشده | خرید و پرداخت اشتراک: عمداً ابزار ندارد (تراکنش مالی) |
| `payment.setWantToPay` | `invoice` | service:AppWorkspaceManager › manualPayment | ➖ پیاده‌نشده | خرید و پرداخت اشتراک: عمداً ابزار ندارد (تراکنش مالی) |
| `payment.update` | `var:f` | service:AppPaymentsManager › createPayment | 🟡 پیاده‌شده، تست‌نشده | `mizito_save_payment` |
| `payment.uploadLastWaitingInvoicePayment` | `invoice,photo` | controller:AppWorkspaceSettingsController › uploadLastWaitingInvoicePayment | ➖ پیاده‌نشده | خرید و پرداخت اشتراک: عمداً ابزار ندارد (تراکنش مالی) |

## `polling` — نظرسنجی (6)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `polling.getTemplates` | `-` | service:AppPollingManager › cancel | ✅ تست‌شده | `mizito_list_templates` |
| `polling.printPollingResults` | `dialog,polling` | service:AppPollingManager › printPollingResults | ⛔ رد شد | 400 (گزارش چاپی، پلن سازمانی) — `mizito_get_poll_results` |
| `polling.retractVote` | `dialog,polling` | service:AppImManager › retractVote | ✅ تست‌شده | `mizito_poll_action` |
| `polling.setPollingAsTemplate` | `var:d` | service:AppImManager › togglePollingTemplate | 🟡 پیاده‌شده، تست‌نشده | `mizito_poll_action` |
| `polling.setPollingVote` | `dialog,polling,my_votes` | service:AppPollingManager › setVote | ✅ تست‌شده | `mizito_poll_action` |
| `polling.stopPolling` | `dialog,polling` | service:AppImManager › stopPolling | ✅ تست‌شده | `mizito_poll_action` |

## `profile` — پروفایل و امنیت حساب (17)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `profile.activate` | `firstname,lastname,pass` | controller:AppLoginProfileController › sendMyInfo | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.changePhoneNumber` | `step,password` \| `step,token,phone,pin` | service:AppProfileManager › update | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.getEmailInfo` | `-` | service:AppProfileManager › terminateSession | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.getProfileSecurity` | `-` | service:AppProfileManager › showProfileSettings | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.removePhoto` | `-` | service:AppProfileManager › removePhoto | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.setDontDisturbUntil` | `hours` | service:AppProfileManager › setDontDisturb | 🟡 پیاده‌شده، تست‌نشده | `mizito_set_presence` — به انتخاب کاربر تست نشد |
| `profile.setOnlineStatus` | `status` | service:AppUsersManager › update | 🟡 پیاده‌شده، تست‌نشده | `mizito_set_presence` — به انتخاب کاربر تست نشد |
| `profile.setUserOptions` | `optionTitle,value` | service:AppProfileManager › setProfileOptions | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.setWallpaper` | `wallpaper` | controller:AppWorkspaceController › setWallpaper | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.terminateOneSession` | `regId,terminateSid` | service:AppProfileManager › terminateSession | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.terminateOtherSessions` | `regId` | service:AppProfileManager › terminateOtherSessions | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.turnTwoStepLoginOff` | `-` \| `pinCode` | service:AppProfileManager › twoStepLoginSwitchChanged | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.update` | `var:b.profile` | service:AppProfileManager › update | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.updateEmail` | `email` | service:AppProfileManager › setEmail | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.updatePassword` | `current,pass,pinCode` | service:AppProfileManager › changePassword | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.updatePhoto` | `base,points` | service:AppProfileManager › setPhoto | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |
| `profile.verifyEmail` | `code` | service:AppProfileManager › checkEmailVerificationCode | ➖ پیاده‌نشده | رمز، شماره، ایمیل، ورود دومرحله‌ای و نشست‌ها: عمداً ابزار ندارد (امنیت حساب) |

## `projectAutomation` — اتوماسیون پروژه (17)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `projectAutomation.add` | `projectId,automateItem` | service:AppProjectAutomationManager › update | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `projectAutomation.buttonClicked` | `var:g` | service:AppProjectAutomationManager › automateButtonClicked | 🟡 پیاده‌شده، تست‌نشده | `mizito_run_task_automation` |
| `projectAutomation.customParam.add` | `projectId,paramItem` | service:AppProjectAutomationCustomParamsManager › applyTemplateEnsureAndSelect<br>service:AppProjectAutomationFormRequestsManager › ensureFormTemplateForWorkflowKey | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `projectAutomation.customParam.delete` | `projectId,paramId` | service:AppProjectAutomationCustomParamsManager › delete | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `projectAutomation.customParam.getAll` | `projectId,token,automateButtonId,isAdminMode` | service:AppProjectAutomationCustomParamsManager › automateButtonClicked | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_project_automation` |
| `projectAutomation.customParam.getHistory` | `projectId,paramId` | service:AppProjectAutomationCustomParamsManager › cancel | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projectAutomation.customParam.getValuesHistory` | `token` | service:AppProjectAutomationCustomParamsManager › showTaskParamValuesHistory | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_task_extras` |
| `projectAutomation.customParam.restore` | `projectId,paramId` | service:AppProjectAutomationCustomParamsManager › restoreParam | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `projectAutomation.customParam.update` | `projectId,paramId,paramItem` | service:AppProjectAutomationFormRequestsManager › cancel | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `projectAutomation.customParam.updateOrder` | `projectId,items` | service:AppProjectAutomationCustomParamsManager › updateOrder | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `projectAutomation.delete` | `projectId,automateItemId` | service:AppProjectAutomationManager › delete | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `projectAutomation.getAll` | `projectId` | service:AppProjectAutomationManager › close | ⛔ رد شد | 400 (پروژه‌ی پیشرفته با اتوماسیون لازم است) — `mizito_get_project_automation` |
| `projectAutomation.getHistory` | `automateId,projectId` | service:AppProjectAutomationManager › close | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projectAutomation.getTaskAutomateButtons` | `token` | service:AppProjectAutomationManager › getTaskAutomateButtons | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_task_extras` |
| `projectAutomation.loadConstants` | `-` | service:AppProjectAutomationManager › ? | ✅ تست‌شده | `mizito_get_project_automation` |
| `projectAutomation.update` | `projectId,automateItem` | service:AppProjectAutomationManager › update | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `projectAutomation.updateOrder` | `projectId,type,items` | service:AppProjectAutomationManager › saveOrder | ➖ پیاده‌نشده | ترتیب قوانین: از وب |

## `projectAutomationWorkflow` — گردش‌کار اتوماسیون (6)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `projectAutomationWorkflow.add` | `projectId,workflow` | service:AppProjectAutomationWorkflowManager › ensureFormTemplateForWorkflowKey | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `projectAutomationWorkflow.delete` | `projectId,workflowId` | service:AppProjectAutomationWorkflowManager › ensureFormTemplateForWorkflowKey | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |
| `projectAutomationWorkflow.getAll` | `projectId` | service:AppProjectAutomationWorkflowManager › getAll | ⛔ رد شد | 400 (پروژه‌ی پیشرفته لازم است) — `mizito_get_project_automation` |
| `projectAutomationWorkflow.getOne` | `projectId,workflowId` | service:AppProjectAutomationWorkflowManager › ensureFormTemplateForWorkflowKey | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projectAutomationWorkflow.getTaskWorkflow` | `token` | service:AppProjectAutomationWorkflowManager › ensureFormTemplateForWorkflowKey | 🟡 پیاده‌شده، تست‌نشده | `mizito_get_task_extras` |
| `projectAutomationWorkflow.update` | `projectId,workflow` | service:AppProjectAutomationWorkflowManager › ensureFormTemplateForWorkflowKey | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_automation` |

## `projects` — پروژه‌ها (41)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `projects.activateAdvancedFeatures` | `project,dialog,advanced` | service:AppChatsManager › toggleProjectAdvancedFeatures | ⛔ رد شد | 400 روی پلن آزمایشی (پروژه‌ی پیشرفته) — `mizito_set_project_advanced` |
| `projects.add` | `title,color,members` | service:AppProjectsManager › cancel | ✅ تست‌شده | `mizito_api_read` |
| `projects.addKanbanBoard` | `projectId,kanbanBoard` | service:AppKanbanManager › update | ✅ تست‌شده | `mizito_add_project_board` |
| `projects.allSummary` | `-` \| `with_details` | controller:AppDashboardController › showAllTrackingItems<br>controller:AppImDialogsController › callDialog | ✅ تست‌شده | `projects_tab` |
| `projects.archive` | `project_id` | service:AppProjectsManager › archiveProject | ⛔ رد شد | 405 برای غیرمدیر — `mizito_admin_archive_category` |
| `projects.chatSummary` | `dialog,project,withBoards` | controller:AppImDialogsController › callDialog<br>controller:ChatProjectStatisticsCtrl › handleVoiceRecordFile | ✅ تست‌شده | `mizito_get_project` |
| `projects.clone` | `projectId,projectName,ignoreTaskIds` | service:AppProjectDuplicateManager › duplicateProject | ⛔ رد شد | 400 روی پلن آزمایشی — `mizito_clone_project` |
| `projects.full` | `project_id` | service:AppProjectsManager › cancel | ✅ تست‌شده | `project_full` |
| `projects.ganttGroupAddTasks` | `var:P` | service:AppGanttManager › showAddExistingTaskModal | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_gantt` |
| `projects.ganttLoadMoreTasks` | `project,taskIds` | service:AppGanttManager › cancel | 🟡 پیاده‌شده، تست‌نشده | `_gantt` |
| `projects.ganttMoveTask` | `var:Q` | service:AppGanttManager › onDomRemoved | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_gantt` |
| `projects.ganttRemoveGroup` | `project,phaseId` | service:AppGanttManager › delete | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_gantt` |
| `projects.ganttRemoveTask` | `project,taskId` | service:AppTasksManager › removeFromGantt | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_gantt` |
| `projects.ganttSaveGroup` | `project,phase` | service:AppGanttManager › create | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_gantt` |
| `projects.ganttSetTaskTimeline` | `project,tasks` | service:AppGanttManager › ? | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_gantt` |
| `projects.ganttTaskLinkAdd` | `var:R` | service:AppGanttManager › onDomRemoved | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_gantt` |
| `projects.ganttTaskLinkRemove` | `var:S` | service:AppGanttManager › onDomRemoved | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_gantt` |
| `projects.get` | `projectId,token` | service:AppProjectsManager › selectHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.getAdvancedFeaturesHistory` | `dialog,project` | service:AppProjectAdvancedHistoryManager › showChangesHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.getGanttData` | `project` | service:AppGanttManager › cancel | ⛔ رد شد | 400 (پروژه‌ی پیشرفته با گانت لازم است) — `_gantt` |
| `projects.getList` | `-` | service:AppProjectsManager › selectHistory | ✅ تست‌شده | `_refresh_task_tokens`, `mizito_archive_project`, `mizito_clone_project`, `mizito_create_project`, `mizito_list_projects` |
| `projects.getListAdmin` | `-` | service:AppProjectsManager › selectHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.getListAdminForMember` | `user` | service:AppProjectsManager › selectHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.getProjectFiles` | `var:a` | controller:AppProjectFilesController › printResult | ✅ تست‌شده | `mizito_list_project_files` |
| `projects.getProjectTaskFileIds` | `project,task` | controller:AppProjectFilesController › showTask | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.getProjectsUserAdmin` | `-` | controller:AppCalendarViewerController › filterSelectProject<br>controller:AppMonitoringProjectsController › projectLabelChanged<br>controller:AppMonitoringProjectsForUserCalendarController › showMonitorPage<br>controller:AppMonitoringTasksController › filterSelectProjectList | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.history` | `project_id` | service:AppProjectsManager › showChangesHistory | ✅ تست‌شده | `mizito_get_history` |
| `projects.import` | `contentId,importType,projectTitle,memberAssign,labelAssign,fieldIndexes,kanbanDoneListTitle` | controller:AppImportProjectController › importTasks | ➖ پیاده‌نشده | ورود از Excel: ویزارد وب |
| `projects.importPrepare` | `contentId,importType` | controller:AppImportProjectController › prepareRows | ➖ پیاده‌نشده | ورود از Excel: ویزارد وب |
| `projects.monitor.chart.getPast30DoneTasksPercents` | `var:e` | controller:AppMonitoringProjectsController › showCalendarPage | 🟡 پیاده‌شده، تست‌نشده | `mizito_reports` |
| `projects.monitor.project` | `projectId` | controller:AppMonitoringProjectController › print | ⛔ رد شد | 400 (دسترسی مدیر/پلن) — `mizito_reports` |
| `projects.monitor.projectsSummary` | `var:e` | controller:AppMonitoringProjectsController › showCalendarPage | 🟡 پیاده‌شده، تست‌نشده | `mizito_reports` |
| `projects.removeKanbanBoard` | `projectId,boardId` | controller:AppKanbanViewerController › removeBoard | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_project_board` |
| `projects.restoreArchivedTasks` | `project` | controller:AppFixProjectsController › restoreArchiveTasks | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_restore_project` |
| `projects.save` | `project_id,title,color,members` | service:AppProjectsManager › cancel | ✅ تست‌شده | `mizito_add_project_members`, `mizito_update_project` |
| `projects.setAdvancedFeatures` | `dialog,advanced` | service:AppChatsManager › setAdminUser<br>service:AppProjectsManager › cancel | 🟡 پیاده‌شده، تست‌نشده | `mizito_set_project_advanced` |
| `projects.setChatProjectColor` | `project,dialog,color` | service:AppProjectsManager › showColorSelector | ✅ تست‌شده | `mizito_update_project` |
| `projects.setChatProjectLabels` | `project,dialog,labels` | service:AppProjectsManager › setProjectLabel | 🟡 پیاده‌شده، تست‌نشده | `mizito_update_project` |
| `projects.setKanbanBoardOrder` | `projectId,boardId,oldPosition,newPosition` | controller:AppKanbanViewerController › invalidTarget | ✅ تست‌شده | `mizito_manage_project_board` |
| `projects.undoArchive` | `project_id` | service:AppProjectsManager › archiveProject | ⛔ رد شد | 405 برای غیرمدیر — `mizito_admin_archive_category` |
| `projects.updateKanbanBoard` | `projectId,kanbanBoardId,kanbanBoard` | service:AppKanbanManager › update | ✅ تست‌شده | `mizito_manage_project_board` |

## `session` — نشست و حساب کاربری (10)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `session.createSSO` | `token` | controller:AppLoginSSOController › link | ➖ پیاده‌نشده | ورود، ثبت‌نام، خروج و حذف حساب: عمداً ابزار ندارد (امنیت حساب) |
| `session.deleteAccount` | `validationCode` | controller:AppDeleteAccountController › deleteAccount | ➖ پیاده‌نشده | ورود، ثبت‌نام، خروج و حذف حساب: عمداً ابزار ندارد (امنیت حساب) |
| `session.deleteAccountRequest` | `username` | controller:AppDeleteAccountRequestController › sendDeleteAccountCodeRequest | ➖ پیاده‌نشده | ورود، ثبت‌نام، خروج و حذف حساب: عمداً ابزار ندارد (امنیت حساب) |
| `session.forgot` | `username` | controller:AppLoginProfileController › sendResetCodeRequest | ➖ پیاده‌نشده | ورود، ثبت‌نام، خروج و حذف حساب: عمداً ابزار ندارد (امنیت حساب) |
| `session.forgotReset` | `reset_code,pass` | controller:AppLoginRegisterController › resetPassword | ➖ پیاده‌نشده | ورود، ثبت‌نام، خروج و حذف حساب: عمداً ابزار ندارد (امنیت حساب) |
| `session.iOSAppIsAlive` | `deviceId,isAlive` | factory:notificationIOSService › onmessage | ➖ پیاده‌نشده | اعلان iOS |
| `session.logout` | `var:t` | factory:services › logout | ➖ پیاده‌نشده | ورود، ثبت‌نام، خروج و حذف حساب: عمداً ابزار ندارد (امنیت حساب) |
| `session.register` | `var:e` \| `var:l` | controller:AppRegisterCompleteController › createWorkspace<br>controller:AppRegisterCompleteController › sendMyInfo<br>controller:AppRegisterController › checkPinCode<br>controller:AppRegisterController › sendActivateCode | ➖ پیاده‌نشده | ورود، ثبت‌نام، خروج و حذف حساب: عمداً ابزار ندارد (امنیت حساب) |
| `session.userInfo` | `uid` | controller:AppLoginController › link | ➖ پیاده‌نشده | ورود، ثبت‌نام، خروج و حذف حساب: عمداً ابزار ندارد (امنیت حساب) |
| `session.username` | `var:null` | controller:AppRegisterController › removeTeammate | ➖ پیاده‌نشده | ورود، ثبت‌نام، خروج و حذف حساب: عمداً ابزار ندارد (امنیت حساب) |

## `support` — پشتیبانی میزیتو (32)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `support.clientOnlineHistory` | `-` | service:AppSupportManager › loadOnlineSupportHistory | ✅ تست‌شده | `mizito_support_history` |
| `support.closeResponse` | `supportId` | service:AppSupportManager › closeResponse | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.deleteFromClient` | `messageId` | service:AppSupportManager › deleteFromClient | 🟡 پیاده‌شده، تست‌نشده | `mizito_contact_support` |
| `support.deleteResponse` | `supportId,messageId` | service:AppSupportManager › deleteResponse | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.deleteResponseFeedback` | `messageId` | service:AppSupportManager › deleteResponseFeedback | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.editFromClient` | `messageId,message` | service:AppSupportManager › editFromClient | 🟡 پیاده‌شده، تست‌نشده | `mizito_contact_support` |
| `support.editResponse` | `supportId,messageId,message` | service:AppSupportManager › editResponse | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.extendDialogLock` | `supportId` | service:AppSupportManager › extendDialogLock | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.getAdminHistory` | `supportId` | service:AppSupportManager › getAdminHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `support.getClientUnreadCount` | `-` | service:AppSupportManager › getClientBadge | ✅ تست‌شده | `mizito_support_history` |
| `support.getDialog` | `dialog` | service:AppSupportManager › getDialogOrLoad | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `support.getDialogs` | `filter,filterIsLastMessageIsRequest,skip,limit` | service:AppSupportManager › registerLetter | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `support.getFeedbackMonitor` | `var:a` | service:AppSupportManager › getFeedbackMonitor | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `support.getFeedbackMonitorOpenCount` | `{}` | service:AppSupportManager › getFeedbackMonitorOpenCount | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `support.getFeedbackMonitorStats` | `var:a` | service:AppSupportManager › getFeedbackMonitorStats | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `support.getFeedbackReviewCase` | `caseId` | service:AppSupportManager › getFeedbackReviewCase | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `support.getSupportInfo` | `supportId` | controller:AppAdminSupportChatController › close<br>controller:AppAdminSupportChatController › openSupportDialogAtMessage | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `support.lockDialog` | `supportId` | service:AppSupportManager › lockDialog | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.markClientSeen` | `seenCount` | service:AppSupportManager › markClientSeen | ➖ پیاده‌نشده | داخلی گفتگوی پشتیبانی |
| `support.markSupportSeen` | `supportId,seenCount` | service:AppSupportManager › markSupportSeen | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.reopenFeedbackReview` | `caseId` | service:AppSupportManager › reopenFeedbackReview | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.resolveFeedbackReview` | `caseId,result,dissatisfactionReason,note` | service:AppSupportManager › resolveFeedbackReview | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.searchContent` | `searchStr,messageType,supportUser,fromDate,toDate,skip` | controller:AppAdminSupportChatController › searchContents | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `support.sendFromClient` | `message,media,replyTo` | service:AppSupportManager › sendFromClient | 🟡 پیاده‌شده، تست‌نشده | `mizito_contact_support` — به پشتیبانی واقعی میزیتو می‌رود؛ تست نشد |
| `support.sendResponse` | `supportId,message,media,replyTo` | service:AppSupportManager › sendResponse | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.sendSuggestion` | `var:a.suggestion` | service:AppSupportManager › send | 🟡 پیاده‌شده، تست‌نشده | `mizito_contact_support` — به پشتیبانی واقعی میزیتو می‌رود؛ تست نشد |
| `support.setResponseFeedbackVote` | `messageId,value,reason,comment` | service:AppSupportManager › setResponseFeedbackVote | ➖ پیاده‌نشده | امتیاز به پاسخ پشتیبانی |
| `support.setTyping` | `-` | controller:AppSupportChatController › keyPressed | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.setTypingAdmin` | `supportId` | controller:AppAdminSupportChatController › sendDraftMessage | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.startFeedbackReview` | `caseId` | service:AppSupportManager › startFeedbackReview | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.unlockDialog` | `supportId` | service:AppSupportManager › unlockDialog | ➖ پیاده‌نشده | پنل کارکنان پشتیبانی میزیتو: فقط برای کارمندان شرکت |
| `support.updateResponseFeedbackDetails` | `messageId,reason,comment` | service:AppSupportManager › updateResponseFeedbackDetails | ➖ پیاده‌نشده | امتیاز به پاسخ پشتیبانی |

## `taskTemplates` — قالب‌های وظیفه (5)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `taskTemplates.add` | `var:a` | service:AppTaskTemplatesManager › updateRepeatingTask | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_task_template` |
| `taskTemplates.getAll` | `projectId` | service:AppTaskTemplatesManager › getAll | ⛔ رد شد | 400 (پروژه‌ی پیشرفته لازم است) — `mizito_get_project_automation` |
| `taskTemplates.getAllTemplates` | `projectId` | service:AppTaskTemplatesManager › getAllForUser | ⛔ رد شد | 400 (پروژه‌ی پیشرفته لازم است) — `_template`, `mizito_list_templates` |
| `taskTemplates.remove` | `projectId,templateId` | service:AppTaskTemplatesManager › remove | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_task_template` |
| `taskTemplates.save` | `var:a` | service:AppTaskTemplatesManager › updateRepeatingTask | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_task_template` |

## `tasks` — وظایف (28)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `tasks.add` | `var:l` \| `var:o` | service:AppMinutesManager › selectTemplate<br>service:AppTasksManager › show | ✅ تست‌شده | `mizito_create_minute`, `mizito_create_task` |
| `tasks.badge` | `-` | factory:services › getTasksBadge | ✅ تست‌شده | `mizito_api_read` |
| `tasks.checkToken` | `tid,token` | service:AppTasksManager › ? | ➖ پیاده‌نشده | داخلی |
| `tasks.createShareLink` | `token` | service:AppTasksManager › copyTaskLink | ✅ تست‌شده | `mizito_manage_task` |
| `tasks.deleteComment` | `token,commentId` | service:AppTasksManager › deleteComment | ✅ تست‌شده | `mizito_manage_task_comment` |
| `tasks.editComment` | `token,commentId,newComment` | service:AppTasksManager › update | ✅ تست‌شده | `mizito_manage_task_comment` |
| `tasks.ganttGetTaskInfo` | `project,token` | service:AppTasksManager › gotoProjectPage | ✅ تست‌شده | `mizito_get_task_extras` |
| `tasks.get` | `var:a` | service:AppTasksManager › clickOutsideToClose | ✅ تست‌شده | `load_task` |
| `tasks.getAll` | `var:e` | service:AppTasksManager › getAll | ✅ تست‌شده | `mizito_api_read` |
| `tasks.getComments` | `token` | service:AppTasksManager › ? | ✅ تست‌شده | `mizito_comment_on_task`, `mizito_get_task_comments` |
| `tasks.getSeenDetails` | `token` | service:AppTasksManager › ? | ✅ تست‌شده | `mizito_get_task_extras` |
| `tasks.history` | `token,tid` | service:AppTasksManager › toggleSortOrder | ✅ تست‌شده | `mizito_get_history` |
| `tasks.newComment` | `token,comment,attachments,mention,reply_id` | service:AppTasksManager › sendNewComment | ✅ تست‌شده | `mizito_comment_on_task` |
| `tasks.print` | `done_timeline,filter` \| `var:a` \| `var:e` | controller:AppMonitoringTasksController › printResult<br>controller:AppTasksDoneController › printDoneResult<br>controller:AppTasksInboxController › printResult | ➖ پیاده‌نشده | نمای چاپی |
| `tasks.removeFromBoard` | `token,project_id` | service:AppTasksManager › removeTaskFromBoard | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_task` |
| `tasks.removeFromTracking` | `token` | service:AppTasksManager › removeTaskFromTracking | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_task` |
| `tasks.removeTask` | `token` | service:AppTasksManager › removeTask | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_task` — برگشت‌پذیر (سطل زباله)؛ تست نشد |
| `tasks.removeTaskUndo` | `token` | service:AppTasksManager › removeTaskUndo | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_task` — تست نشد |
| `tasks.save` | `var:o` | service:AppTasksManager › show | ✅ تست‌شده | `save_task` |
| `tasks.setChecklistCheckedValue` | `token,checklistId,checked` | service:AppTasksManager › checklistCheckedChanged | ✅ تست‌شده | `mizito_check_task_item` |
| `tasks.setCompleted` | `token,completed,project` \| `token,project,completed,progress,undone_user_id` | service:AppTasksManager › clickOutsideToClose | ✅ تست‌شده | `mizito_set_task_completed` |
| `tasks.setKanbanWeight` | `token,projectId,kanbanBoardId,kanbanWeight` | controller:AppKanbanViewerController › invalidTarget | ✅ تست‌شده | `mizito_move_task_to_board` |
| `tasks.setKanbanWeightSort` | `projectId,kanbanBoardId,sortField,sortOrder` | controller:AppKanbanViewerController › sortTasks | ✅ تست‌شده | `mizito_manage_project_board` |
| `tasks.snooze` | `token,project,alarm_at,update_repeat_base` | service:AppTasksManager › snoozeTask | ✅ تست‌شده | `mizito_create_task`, `mizito_set_task_reminder` |
| `tasks.toggleBookmark` | `token,bookmarked` | service:AppTasksManager › toggleBookmark | ✅ تست‌شده | `mizito_manage_task` |
| `tasks.upcoming` | `var:e` | service:AppTasksManager › loadUpcoming | ✅ تست‌شده | `_gantt`, `_refresh_task_tokens`, `mizito_calendar`, `mizito_list_tasks`, `mizito_move_task_to_board` |
| `tasks.updateDeadline` | `token,project,deadline` | service:AppTasksManager › updateTaskDeadline | ✅ تست‌شده | `mizito_set_task_deadline` |
| `tasks.updateProgress` | `token,progress` | service:AppTasksManager › updateProgress | ✅ تست‌شده | `mizito_set_task_progress` |

## `workspace` — میزکار (22)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `workspace.add` | `name,members` | service:AppWorkspaceManager › create | ➖ پیاده‌نشده | ساخت میزکار جدید: از وب |
| `workspace.changeOwner` | `owner,pinCode,password` | service:AppWorkspaceManager › update | ➖ پیاده‌نشده | تغییر مالک با رمز و کد: از وب |
| `workspace.changeRole` | `user_id,role` | controller:AppWorkspaceSettingsController › changeRole | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_manage_member` |
| `workspace.delete` | `-` | controller:AppWorkspaceSettingsController › deleteWorkspace | ➖ پیاده‌نشده | حذف میزکار: برگشت‌ناپذیر، از وب |
| `workspace.getPermissions` | `-` | service:AppWorkspaceManager › getPermissions | ⛔ رد شد | 400 برای غیرمدیر — `mizito_admin_workspace_settings`, `mizito_workspace_info` |
| `workspace.getPlans` | `-` | service:AppWorkspaceManager › getPlanTypes | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `workspace.getUsers` | `-` | service:AppUsersManager › endCall | ✅ تست‌شده | `mizito_list_users`, `users` |
| `workspace.ignoreBusinessTypeModal` | `-` | service:AppWorkspaceManager › close | ➖ پیاده‌نشده | پنجره‌ی نوع کسب‌وکار در وب |
| `workspace.inviteMember` | `name,email_phone,is_guest` | service:AppUsersManager › endCall | 🟡 پیاده‌شده، تست‌نشده | `mizito_invite_workspace_member` — دعوت واقعی می‌فرستد؛ تست نشد |
| `workspace.name` | `-` | service:AppWorkspaceManager › loadWorkspaceName | ✅ تست‌شده | `mizito_admin_workspace_settings`, `mizito_workspace_info` |
| `workspace.planInfo` | `details` | service:AppWorkspaceManager › close | ✅ تست‌شده | `mizito_workspace_info` |
| `workspace.reJoinMember` | `member_id` | controller:AppWorkspaceSettingsController › reJoinMember | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_manage_member` |
| `workspace.removeMember` | `member_id` | controller:AppWorkspaceSettingsController › removeMember | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_manage_member` |
| `workspace.sendContactUsage` | `user_id` | service:AppCustomersManager › createCustomer<br>service:AppInboxManager › send<br>service:AppUsersManager › endCall | ➖ پیاده‌نشده | آمار استفاده‌ی داخلی وب |
| `workspace.setWorkspaceSettings` | `title,value` | controller:AppWorkspaceSettingsController › setWorkspaceSettings | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_workspace_settings` |
| `workspace.switch` | `workspace_id` | service:AppWorkspaceManager › cancel | 🟡 پیاده‌شده، تست‌نشده | `switch_workspace` — حساب تست فقط یک میزکار داشت |
| `workspace.updateBusinessType` | `business_type` | service:AppWorkspaceManager › close | ➖ پیاده‌نشده | پنجره‌ی نوع کسب‌وکار در وب |
| `workspace.updateDedicatedLogoPhoto` | `photo` | controller:AppWorkspaceSettingsController › uploadDedicatedLoginPhoto | ➖ پیاده‌نشده | لوگوی سرور اختصاصی؛ آپلود با برش تصویر |
| `workspace.updateTitle` | `title` | controller:AppWorkspaceSettingsController › updateWorkspaceTitle | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_workspace_settings` |
| `workspace.updateUserPermission` | `user,permission,access` | service:AppWorkspaceManager › updateUserPermission | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_manage_member` |
| `workspace.updateWorkspaceRoleName` | `user_id,workspaceRoleName` | controller:AppWorkspaceSettingsController › workspaceRoleNameEditableOk | 🟡 پیاده‌شده، تست‌نشده | `mizito_admin_manage_member` |
| `workspace.userId` | `regId` | controller:AppLoginController › link | ✅ تست‌شده | `_me`, `my_user_id` |

## درخواست‌های دیگر (غیر از `invokeApi`)

| مسیر | کاربرد |
|---|---|
| `POST {api_url}/capi/session/create` | ورود: `{username, password: md5\|sha256, loginCode, regId}` → `{status, token}` |
| `POST {api_url}/capi/<module>/<method>` | فراخوانی بدون توکن (گزینه‌ی `no_token` در `invokeApi`) |
| `POST {api_url}/api/content/upload` | آپلود فایل و عکس (مسیر از `getUploadPath`) |
| `POST {api_url}/api/crm/report` | گزارش چاپی CRM با فرم HTML (برچسب‌ها و فیلترها) |
| `GET {cdn_url}/cdn/<jwt>` | نمایش فایل و عکس (JWT شامل شناسه‌ی محتوا و میزکار) |
| `GET {cdn_url}/cdn/dl/…` | دانلود فایل |
| `GET {cdn_url}/cdn/de/logo/…` | لوگوی سرور اختصاصی |
| `socket.io {io_url}` | کانال لحظه‌ای؛ جزئیات در [realtime-and-types.md](realtime-and-types.md) |

