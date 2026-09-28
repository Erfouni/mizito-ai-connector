# همه‌ی endpointهای API میزیتو

369 endpoint از کد وب‌اپ، از جمله آن‌هایی که اسمشان با عبارت شرطی ساخته می‌شود. همه `POST {api_url}/api/<ماژول>/<متد>` با هدر `x-token` هستند.
«پارامترها» کلیدهای payload در محل فراخوانی‌اند (`var:x` یعنی شیء از قبل ساخته شده، `-` یعنی بدون payload).
«محل فراخوانی» سرویس یا کنترلر و تابعی در کد وب است که آن را صدا می‌زند.

| وضعیت در MCP | تعداد |
|---|---|
| ⛔ رد شد | 8 |
| ✅ تست‌شده | 56 |
| ➖ پیاده‌نشده | 223 |
| 🔎 با `mizito_api_read` | 74 |
| 🟡 پیاده‌شده، تست‌نشده | 8 |

## `attendance` — حضور و غیاب (5)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `attendance.delete` | `attendanceId` | service:AppAttendanceManager › removeRow | ➖ پیاده‌نشده | حضور و غیاب: پیاده نشد |
| `attendance.getHistory` | `var:A` | service:AppAttendanceManager › showManualLog | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `attendance.getOnlineHistory` | `var:A` | service:AppAttendanceManager › showOnlineLog | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `attendance.start` | `-` | service:AppAttendanceManager › start | ➖ پیاده‌نشده | حضور و غیاب: پیاده نشد |
| `attendance.stop` | `-` | service:AppAttendanceManager › stop | ➖ پیاده‌نشده | حضور و غیاب: پیاده نشد |

## `chat` — گفتگو (37)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `chat.addPinMessage` | `dialog,message` | service:AppChatsManager › confirmAddPingMessage | ✅ تست‌شده | `mizito_manage_message` |
| `chat.archiveProject` | `dialog,project,withArchiveTasks` | service:AppProjectsManager › showArchiveProjectSelectorDialog | ✅ تست‌شده | `mizito_archive_project` |
| `chat.convertDialogToNotPublic` | `dialog` | service:AppChatsManager › convertToNotPublicGroup | ➖ پیاده‌نشده | پیاده نشد |
| `chat.convertMentionToUnProcessed` | `dialog,mid` | service:AppImManager › convertMentionToUnProcessed | ➖ پیاده‌نشده | پیاده نشد |
| `chat.createDialog` | `user` \| `var:b` | service:AppPeersManager › onDomRemoved<br>service:AppPeersManager › showChatWithRoute | ✅ تست‌شده | `mizito_create_group`, `mizito_create_project`, `mizito_start_conversation` |
| `chat.deleteDialog` | `dialog` | service:AppChatsManager › deleteGroup | ➖ پیاده‌نشده | پیاده نشد |
| `chat.deleteUser` | `dialog,user` | service:AppChatsManager › deleteUser | ➖ پیاده‌نشده | پیاده نشد |
| `chat.fixDialogs` | `dialog` | service:AppPeersManager › reset | ➖ پیاده‌نشده | پیاده نشد |
| `chat.getChatView` | `dialog` | service:AppImManager › getHistory | ✅ تست‌شده | `mizito_get_messages`, `mizito_manage_message`, `mizito_mark_conversation_read` |
| `chat.getDialogUnDoneTasksCount` | `dialog` | controller:CrmHeaderCtrl › toggleShowPayments | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `chat.getDialogs` | `-` | service:AppPeersManager › reset | ✅ تست‌شده | `mizito_list_conversations`, `mizito_start_conversation` |
| `chat.getFullChat` | `dialog` | service:AppChatProfileManager › forceFullChatUpdate<br>service:AppChatProfileManager › handleEscapeKey | ✅ تست‌شده | `mizito_api_read` |
| `chat.getHistory` | `var:d` | service:AppImManager › getHistory | ✅ تست‌شده | `mizito_get_messages`, `mizito_send_message` |
| `chat.getMessageByDate` | `dialog,date` | service:AppImManager › getMessageByDate | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `chat.getMessageIndex` | `dialog,mid` | service:AppImManager › getMessageIndex | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `chat.getMessages` | `mids,dialog` | directive:myPeerOnlineStatusLink › setVote<br>service:AppImManager › ? | ✅ تست‌شده | `mizito_manage_message` |
| `chat.getStatusDetails` | `dialog,mid` | service:AppImManager › convertMentionToUnProcessed | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `chat.inviteUser` | `dialog,user` | service:AppChatsManager › inviteUser | 🟡 پیاده‌شده، تست‌نشده | `mizito_add_project_members`, `mizito_manage_conversation` — به همکار واقعی اعلان می‌رود؛ تست نشد |
| `chat.loadSettings` | `-` | service:AppPeersManager › loadNotificationSettings | ➖ پیاده‌نشده | پیاده نشد |
| `chat.pinDialog` | `dialog` | service:AppPeersManager › toggleSetPin | ✅ تست‌شده | `mizito_manage_conversation` |
| `chat.removeMentionMessage` | `mid,dialog` | service:AppImManager › removeMentionMessage | ➖ پیاده‌نشده | پیاده نشد |
| `chat.removePhoto` | `dialog` | service:AppChatsManager › removePhoto | ➖ پیاده‌نشده | پیاده نشد |
| `chat.removePinMessage` | `dialog,message` | service:AppChatsManager › confirmRemovePingMessage | ➖ پیاده‌نشده | پیاده نشد |
| `chat.removeSentMessage` | `dialog,mid` | service:AppImManager › removeMessage | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_message` — حذف است؛ تست نشد |
| `chat.removeSentMessageAdmin` | `dialog,mid` | service:AppImManager › removeMessage | ➖ پیاده‌نشده | پیاده نشد |
| `chat.removeTaskSnoozeMessage` | `mid,dialog,task_id` | service:AppImManager › removeSnoozeMessage | ➖ پیاده‌نشده | پیاده نشد |
| `chat.saveSettings` | `dialog,mute` | service:AppChatsManager › showProjectAdvancedFeaturesModal | ➖ پیاده‌نشده | پیاده نشد |
| `chat.search` | `var:f` | service:AppImManager › searchMessages | ✅ تست‌شده | `mizito_search_messages` |
| `chat.seen` | `dialog,seen_count` | service:AppImManager › markSeen | ✅ تست‌شده | `mizito_mark_conversation_read` |
| `chat.send` | `var:b` | service:AppImManager › ? | ✅ تست‌شده | `mizito_send_message` |
| `chat.setAdmin` | `dialog,user,isAdmin` | service:AppChatsManager › setAdminUser | ➖ پیاده‌نشده | پیاده نشد |
| `chat.setTyping` | `dialog` | controller:ChatViewCtrl › showRobotHelp | ➖ پیاده‌نشده | پیاده نشد |
| `chat.toggleBookmark` | `dialog,mid,bookmarked` | service:AppImManager › ? | ✅ تست‌شده | `mizito_manage_message` |
| `chat.unpinDialog` | `dialog` | service:AppPeersManager › toggleUnPin | ✅ تست‌شده | `mizito_manage_conversation` |
| `chat.updatePhoto` | `dialog,photo` | service:AppChatsManager › changePhoto | ➖ پیاده‌نشده | پیاده نشد |
| `chat.updateSentMessage` | `dialog,mid,log` \| `dialog,mid,newMessage` | controller:ChatViewCtrl › ?<br>service:AppCallLogManager › createLog<br>service:AppImManager › update | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_message` — فقط برای پیام دیده‌نشده؛ مسیر موفق تست نشد |
| `chat.updateTitle` | `dialog,title` | service:AppChatsManager › updateTitle | ✅ تست‌شده | `mizito_manage_conversation` |

## `content` — فایل و محتوا (2)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `content.getCroppedPhoto` | `base,points` | service:AppFilesManager › showUploaderWithCropper | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `content.getDownloadLink` | `content` | factory:services › closeToast | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |

## `customer` — CRM – مشتریان (7)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `customer.add` | `var:d` | service:AppCustomersManager › createCustomer | ⛔ رد شد | 400 حتی با payload دقیق فرم وب (CRM در پلن نیست) — `mizito_create_customer` |
| `customer.history` | `customer_id` | service:AppCustomersManager › showChangesHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `customer.import` | `contentId,members,labelAssign,fieldIndexes` | controller:AppImportCustomersController › importCustomers | ➖ پیاده‌نشده | CRM: پلن حساب تست شامل آن نبود |
| `customer.importPrepare` | `contentId` | controller:AppImportCustomersController › prepareRows | ➖ پیاده‌نشده | CRM: پلن حساب تست شامل آن نبود |
| `customer.suggestParticipants` | `-` | service:AppCustomersManager › reset | ➖ پیاده‌نشده | CRM: پلن حساب تست شامل آن نبود |
| `customer.update` | `var:d` | service:AppCustomersManager › createCustomer | ➖ پیاده‌نشده | CRM: پلن حساب تست شامل آن نبود |
| `customer.updateLabel` | `customer_id,is_add,label_id` | service:AppCustomersManager › updateLabel | ➖ پیاده‌نشده | CRM: پلن حساب تست شامل آن نبود |

## `dashboard` — داشبورد (11)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `dashboard.acceptInviteRequest` | `workspace` | controller:AppDashboardController › acceptInvite | ➖ پیاده‌نشده | پیاده نشد |
| `dashboard.cancelInviteRequest` | `workspace` | controller:AppDashboardController › cancelInvite | ➖ پیاده‌نشده | پیاده نشد |
| `dashboard.checkWhatsNew` | `-` | controller:HeaderController › showBookmarksPage | ➖ پیاده‌نشده | پیاده نشد |
| `dashboard.demoGuide` | `-` | controller:AppWorkspaceController › showDemoGuide | ➖ پیاده‌نشده | پیاده نشد |
| `dashboard.getAllBadges` | `only_badges` | service:AppWorkspaceManager › cancel | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `dashboard.getAllSummary` | `-` | controller:AppDashboardController › setWallpaper | ✅ تست‌شده | `mizito_dashboard` |
| `dashboard.getAllWorkspacesUsers` | `-` | controller:AppDashboardController › setWallpaper | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `dashboard.getPending` | `-` | controller:AppDashboardController › dashboardMeetingCallRemove<br>controller:AppDashboardController › setWallpaper | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `dashboard.notifySeen` | `-` | controller:AppDashboardController › setWallpaper | ➖ پیاده‌نشده | پیاده نشد |
| `dashboard.setWhatsNewSeen` | `-` | controller:HeaderController › showWhatsNew | ➖ پیاده‌نشده | پیاده نشد |
| `dashboard.whatsNew` | `-` | factory:services › showWhatsNew | ➖ پیاده‌نشده | پیاده نشد |

## `deal` — CRM – معاملات (7)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `deal.add` | `var:c` | service:AppDealsManager › createDeal | ➖ پیاده‌نشده | CRM فروش: پلن حساب تست شامل آن نبود |
| `deal.getAll` | `var:a` | service:AppDealsManager › getAllDeals | ⛔ رد شد | 400 (فروش در پلن نیست) |
| `deal.getCustomerDeals` | `customer` | service:AppDealsManager › getCustomerSales | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `deal.getReportStatistics` | `filter` | service:AppDealsManager › getReportStatistics | ⛔ رد شد | 400 (فروش در پلن نیست) |
| `deal.history` | `deal_id` | service:AppDealsManager › showChangesHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `deal.info` | `deal_id` | service:AppDealsManager › showDeal | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `deal.update` | `var:c` | service:AppDealsManager › createDeal | ➖ پیاده‌نشده | CRM فروش: پلن حساب تست شامل آن نبود |

## `device` — دستگاه و اعلان (1)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `device.register` | `subscription,iOS,regId,deviceName,deviceId,versionCode,versionName` | factory:notificationIOSService › isFirefox | ➖ پیاده‌نشده | ثبت دستگاه برای اعلان: خارج از محدوده |

## `feedback` — بازخورد (2)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `feedback.checkRequireParticipant` | `-` | service:AppProfileManager › snooze | ➖ پیاده‌نشده | بازخورد به میزیتو: خارج از محدوده |
| `feedback.sendFeedback` | `feedback` | service:AppProfileManager › close<br>service:AppProfileManager › noAnswer<br>service:AppProfileManager › snooze | ➖ پیاده‌نشده | بازخورد به میزیتو: خارج از محدوده |

## `fix` — ابزار اصلاح داده (مدیر) (13)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `fix.changeUser.changeChatGroups` | `fromUser,toUser` | service:AppFixChangeUserManager › update | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |
| `fix.changeUser.changeCustomers` | `fromUser,toUser` | service:AppFixChangeUserManager › update | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |
| `fix.changeUser.changeTasks` | `fromUser,toUser` | service:AppFixChangeUserManager › update | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |
| `fix.changeUser.history` | `-` | service:AppFixChangeUserManager › wrapForHistory | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |
| `fix.chatGroups.getAll` | `filter` | controller:AppFixChatGroupsController › load | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |
| `fix.chatGroups.getMembers` | `dialog` | controller:AppFixChatGroupsController › showMembers | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |
| `fix.chatGroups.grantAccess` | `dialogIds,userId,access` \| `dialogIds,users,access` | controller:AppFixChatGroupsController › addMember<br>controller:AppFixChatGroupsController › grantAccessToUser<br>controller:AppFixChatGroupsController › removeMember | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |
| `fix.customer.getAll` | `filter` | controller:AppFixCustomersController › load | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |
| `fix.customer.getMembers` | `customer` | controller:AppFixCustomersController › showMembers | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |
| `fix.customer.grantAccess` | `customerIds,userId,access` \| `customerIds,users,access` | controller:AppFixCustomersController › addMember<br>controller:AppFixCustomersController › grantAccessToUser<br>controller:AppFixCustomersController › removeMember | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |
| `fix.projects.getAll` | `filter` | controller:AppFixProjectsController › load | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |
| `fix.projects.getMembers` | `project` | controller:AppFixProjectsController › showMembers | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |
| `fix.projects.grantAccess` | `projectIds,userId,access` \| `projectIds,users,access` | controller:AppFixProjectsController › addMember<br>controller:AppFixProjectsController › grantAccessToUser<br>controller:AppFixProjectsController › removeMember<br>service:AppProjectsManager › showArchiveProjectSelectorDialog | ➖ پیاده‌نشده | ابزار اصلاح دسترسی مدیر: خارج از محدوده |

## `formRequestTemplate` — فرم‌های درخواست (10)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `formRequestTemplate.add` | `projectId,form` | service:AppProjectAutomationFormRequestsManager › cancel | ➖ پیاده‌نشده | فرم‌های درخواست (پلن سازمانی): پیاده نشد |
| `formRequestTemplate.getAll` | `projectId` | service:AppProjectAutomationFormRequestsManager › cancel | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `formRequestTemplate.getAllForms` | `-` | service:AppProjectAutomationFormRequestsManager › getAllForms | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `formRequestTemplate.getHistory` | `projectId,templateId` | service:AppProjectAutomationFormRequestsManager › ? | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `formRequestTemplate.getTaskWorkflow` | `token` | service:AppProjectAutomationWorkflowManager › ensureFormTemplateForWorkflowKey | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `formRequestTemplate.newComment` | `token,comment,attachments,mention,reply_id` | service:AppTasksManager › sendNewComment | ➖ پیاده‌نشده | فرم‌های درخواست (پلن سازمانی): پیاده نشد |
| `formRequestTemplate.remove` | `projectId,formId` | service:AppProjectAutomationFormRequestsManager › delete | ➖ پیاده‌نشده | فرم‌های درخواست (پلن سازمانی): پیاده نشد |
| `formRequestTemplate.save` | `projectId,form` | service:AppProjectAutomationFormRequestsManager › cancel | ➖ پیاده‌نشده | فرم‌های درخواست (پلن سازمانی): پیاده نشد |
| `formRequestTemplate.submit` | `templateId,custom_params_values` | service:AppProjectAutomationFormRequestsManager › showFormInput | ➖ پیاده‌نشده | فرم‌های درخواست (پلن سازمانی): پیاده نشد |
| `formRequestTemplate.view` | `templateId` | service:AppProjectAutomationFormRequestsManager › showFormInput | ➖ پیاده‌نشده | فرم‌های درخواست (پلن سازمانی): پیاده نشد |

## `inbox` — کارتابل نامه‌ها (21)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `inbox.archive` | `thread` | service:AppInboxManager › archive | ✅ تست‌شده | `mizito_manage_letter` |
| `inbox.archive.sender` | `thread` | service:AppInboxManager › archive | ➖ پیاده‌نشده | پیاده نشد |
| `inbox.badge` | `-` | factory:services › getInboxBadge | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `inbox.changeMessageDialogs` | `thread,dialogs` | service:AppInboxManager › onDone | ➖ پیاده‌نشده | پیاده نشد |
| `inbox.changeMessageLabels` | `thread,labels` | service:AppInboxManager › changeLabels | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_letter` — تست نشد |
| `inbox.deleteMessage` | `mid,isDeleteThread` | controller:AppInboxController › deleteMessage | ➖ پیاده‌نشده | پیاده نشد |
| `inbox.expandInboxRow` | `thread,mode` | service:AppInboxManager › expandInboxRow | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `inbox.getHistory` | `thread` | service:AppInboxManager › getHistory | ✅ تست‌شده | `mizito_get_letter_thread`, `mizito_reply_letter` |
| `inbox.getInbox` | `var:d` | service:AppInboxManager › loadInbox | ✅ تست‌شده | `mizito_list_letters` |
| `inbox.getLastSecretariatStatus` | `-` | service:AppSecretariatManager › reset | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `inbox.getMessageDialogs` | `thread` | controller:AppInboxController › togglePinNote | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `inbox.getMessageLabels` | `thread` | service:AppInboxManager › getHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `inbox.getSeenDetails` | `thread,msgId` | service:AppInboxManager › showSeenDetails | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `inbox.registerInLetter` | `thread,letterOptions` | service:AppSecretariatManager › setCustomNumber | ➖ پیاده‌نشده | پیاده نشد |
| `inbox.registerOutLetter` | `thread,letterOptions` | service:AppSecretariatManager › setCustomNumber | ➖ پیاده‌نشده | پیاده نشد |
| `inbox.seen` | `thread` | service:AppInboxManager › markAsSeen | ✅ تست‌شده | `mizito_manage_letter` |
| `inbox.send` | `var:b` | service:AppInboxManager › send | ✅ تست‌شده | `mizito_reply_letter`, `mizito_send_letter` |
| `inbox.setTyping` | `thread` | service:AppInboxManager › setTyping | ➖ پیاده‌نشده | پیاده نشد |
| `inbox.toggleBookmark` | `thread,bookmarked` | service:AppInboxManager › toggleBookmark | ✅ تست‌شده | `mizito_manage_letter` |
| `inbox.unArchive` | `thread` | service:AppInboxManager › unArchive | ✅ تست‌شده | `mizito_manage_letter` |
| `inbox.unArchive.sender` | `thread` | service:AppInboxManager › unArchive | ➖ پیاده‌نشده | پیاده نشد |

## `labels` — برچسب‌ها (6)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `labels.add` | `title,color,type` | service:AppLabelManager › isVisible | ✅ تست‌شده | `mizito_create_label` |
| `labels.delete` | `label_id,label_type` | service:AppLabelManager › isVisible | ➖ پیاده‌نشده | پیاده نشد |
| `labels.getAll` | `type` | service:AppLabelManager › isVisible | ✅ تست‌شده | `mizito_create_label`, `mizito_list_labels` |
| `labels.history` | `label_id` | service:AppLabelManager › showChangesHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `labels.save` | `label_id,type,title,color` | service:AppLabelManager › isVisible | ➖ پیاده‌نشده | پیاده نشد |
| `labels.sendUsage` | `label_id,type` | service:AppLabelManager › isVisible | ➖ پیاده‌نشده | پیاده نشد |

## `meeting` — جلسه‌ی تصویری (6)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `meeting.broadcastMeetingMessage` | `meeting,message` | service:AppMeetingManager › sendBroadcast | ➖ پیاده‌نشده | تماس تصویری (WebRTC): از طریق MCP قابل استفاده نیست |
| `meeting.create` | `dialog,members,tab` | service:AppMeetingManager › resetWorkspace | ➖ پیاده‌نشده | تماس تصویری (WebRTC): از طریق MCP قابل استفاده نیست |
| `meeting.endCall` | `meeting,socket,tab` | controller:AppDashboardController › dashboardMeetingCallRemove<br>controller:AppMeetingViewerController › mobileToggleUserFullScreen | ➖ پیاده‌نشده | تماس تصویری (WebRTC): از طریق MCP قابل استفاده نیست |
| `meeting.get` | `meeting,socket,tab` | controller:AppMeetingViewerController › createMeeting | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `meeting.ping` | `meeting,socket,tab` | service:AppMeetingManager › ping | ➖ پیاده‌نشده | تماس تصویری (WebRTC): از طریق MCP قابل استفاده نیست |
| `meeting.reject` | `meeting` | service:AppMeetingManager › rejectCall | ➖ پیاده‌نشده | تماس تصویری (WebRTC): از طریق MCP قابل استفاده نیست |

## `minute` — صورتجلسه (5)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `minute.getTemplate` | `template` | service:AppMinutesManager › selectTemplate<br>service:AppMinutesManager › showMinute | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `minute.getTemplates` | `-` | service:AppMinutesManager › clickOutsideToClose | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `minute.history` | `minute_id` | service:AppMinutesManager › showChangesHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `minute.setMinuteAsTemplate` | `var:d` | service:AppMinutesManager › toggleTemplate | ➖ پیاده‌نشده | صورتجلسه (به‌صورت پیوست چت ساخته می‌شود): پیاده نشد |
| `minute.update` | `dialog,minute` | service:AppMinutesManager › createMinute | ➖ پیاده‌نشده | صورتجلسه (به‌صورت پیوست چت ساخته می‌شود): پیاده نشد |

## `minuteAdvanced` — صورتجلسه‌ی پیشرفته (13)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `minuteAdvanced.deleteComment` | `minuteId,commentId` | service:AppMinutesAdvancedManager › deleteComment | ➖ پیاده‌نشده | صورتجلسه‌ی پیشرفته: پیاده نشد |
| `minuteAdvanced.editComment` | `minuteId,commentId,newComment` | service:AppMinutesAdvancedManager › update | ➖ پیاده‌نشده | صورتجلسه‌ی پیشرفته: پیاده نشد |
| `minuteAdvanced.get` | `minuteId` | service:AppMinutesAdvancedManager › sendForSign | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `minuteAdvanced.getComments` | `minuteId` | service:AppMinutesAdvancedManager › reset | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `minuteAdvanced.getSmsHistory` | `minuteId` | service:AppMinutesAdvancedManager › reset | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `minuteAdvanced.getTemplates` | `-` | service:AppMinutesAdvancedManager › sendForSign | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `minuteAdvanced.newComment` | `minuteId,comment,attachments` | service:AppMinutesAdvancedManager › sendNewComment | ➖ پیاده‌نشده | صورتجلسه‌ی پیشرفته: پیاده نشد |
| `minuteAdvanced.sendDraft` | `minuteId,dialog,project` | service:AppMinutesAdvancedManager › sendDraft | ➖ پیاده‌نشده | صورتجلسه‌ی پیشرفته: پیاده نشد |
| `minuteAdvanced.sendForSign` | `minuteId,dialog,project` | service:AppMinutesAdvancedManager › sendForSign | ➖ پیاده‌نشده | صورتجلسه‌ی پیشرفته: پیاده نشد |
| `minuteAdvanced.sendSms` | `minuteId,dialog,project,template` | service:AppMinutesAdvancedManager › sendNewSms | ➖ پیاده‌نشده | صورتجلسه‌ی پیشرفته: پیاده نشد |
| `minuteAdvanced.setMinuteAsTemplate` | `minuteId,isActive` | service:AppMinutesAdvancedManager › toggleTemplate | ➖ پیاده‌نشده | صورتجلسه‌ی پیشرفته: پیاده نشد |
| `minuteAdvanced.sign` | `mid,dialog,minuteId` | service:AppMinutesAdvancedManager › signMinute | ➖ پیاده‌نشده | صورتجلسه‌ی پیشرفته: پیاده نشد |
| `minuteAdvanced.update` | `minute,dialog,project` | service:AppMinutesAdvancedManager › removeMembersOther | ➖ پیاده‌نشده | صورتجلسه‌ی پیشرفته: پیاده نشد |

## `monitor` — گزارش و مانیتورینگ (16)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `monitor.attendanceUserHistory` | `-` | service:AppAttendanceManager › showManualLog | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.attendanceUserOnlineHistory` | `-` | service:AppAttendanceManager › showOnlineLog | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.chart.chatMessages` | `-` \| `uid` | controller:AppMonitoringController › reload<br>controller:AppMonitoringUserController › reload | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.chart.customers` | `-` \| `uid` | controller:AppMonitoringController › reload<br>controller:AppMonitoringUserController › reload | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.chart.getPast30DoneTasksPercents` | `-` \| `var:e` | controller:AppMonitoringController › showTasksDoneMonitoring<br>controller:AppMonitoringProjectsController › showCalendarPage | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.chart.inboxMessages` | `-` \| `uid` | controller:AppMonitoringController › reload<br>controller:AppMonitoringUserController › reload | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.chart.notes` | `-` \| `uid` | controller:AppMonitoringController › reload<br>controller:AppMonitoringUserController › reload | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.chart.tasksAssigned` | `uid` \| `uid,not_owner` | controller:AppMonitoringUserController › reload | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.chart.tasksCreated` | `-` \| `uid` | controller:AppMonitoringController › reload<br>controller:AppMonitoringUserController › reload | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.chart.tasksDone` | `-` \| `uid` | controller:AppMonitoringController › reload<br>controller:AppMonitoringUserController › reload | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.customers` | `filter` | controller:AppMonitoringCustomersController › load | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.minutes` | `filter` | controller:AppMonitoringMinutesController › doFilter | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.project` | `projectId` | controller:AppMonitoringProjectController › print | ⛔ رد شد | 400 (دسترسی مدیر/پلن) |
| `monitor.projectsSummary` | `var:e` | controller:AppMonitoringProjectsController › showCalendarPage | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.user` | `uid` | controller:AppMonitoringUserController › reload | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `monitor.workspace` | `-` | controller:AppMonitoringController › reload | ⛔ رد شد | 400 (دسترسی مدیر/پلن) |

## `notes` — یادداشت‌ها (9)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `notes.archiveNote` | `note_id,archived` | service:AppNotesManager › archiveNote<br>service:AppNotesManager › unArchiveNote | ✅ تست‌شده | `mizito_manage_note` |
| `notes.create` | `var:b` | service:AppNotesManager › addNote | ✅ تست‌شده | `mizito_create_note` |
| `notes.deleteNote` | `note_id,deleted` | service:AppNotesManager › deleteNote<br>service:AppNotesManager › unDeleteNote | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_note` — حذف است؛ تست نشد |
| `notes.getAll` | `var:a` | service:AppNotesManager › loadNotes | ✅ تست‌شده | `_find_note`, `mizito_list_notes` |
| `notes.setChecklistValue` | `note_id,check_index,checked` | service:AppNotesManager › setNoteChecklistValue | ✅ تست‌شده | `mizito_manage_note` |
| `notes.setColor` | `note_id,color` | service:AppNotesManager › setNoteColor | ➖ پیاده‌نشده | پیاده نشد |
| `notes.setLabels` | `note_id,labels` | controller:AppNotesController › showLabelSelector | ➖ پیاده‌نشده | پیاده نشد |
| `notes.update` | `var:b` | service:AppNotesManager › addNote | ✅ تست‌شده | `mizito_update_note` |
| `notes.updatePinState` | `pinned,noteId` | service:AppNotesManager › updatePinState | ✅ تست‌شده | `mizito_manage_note` |

## `payment` — پرداخت و صورتحساب (14)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `payment.add` | `payment` | service:AppPaymentsManager › createPayment | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.checkDiscountCode` | `discountCode,planId` | controller:AppWorkspaceSettingsController › checkCouponCode | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.createUpgradeInvoice` | `plan_id,discount_code,request_enterprise,is_online` | service:AppWorkspaceManager › close | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.getAllPayments` | `var:a` | service:AppPaymentsManager › getAllPayments | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.getCustomerPayments` | `customer` | service:AppPaymentsManager › getCustomerPayments | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.getInvoice` | `invoice` | service:AppWorkspaceManager › close<br>service:AppWorkspaceManager › showInvoice | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.getReportDetails` | `var:a` | service:AppPaymentsManager › getReportDetails | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.getReportStatistics` | `filter` | service:AppPaymentsManager › getReportStatistics | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.history` | `payment_id` | service:AppPaymentsManager › showChangesHistory | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.info` | `payment_id` | service:AppPaymentsManager › showPayment | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.requestTrial` | `planId,request_enterprise` | controller:AppWorkspaceSettingsController › requestTrial | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.setWantToPay` | `invoice` | service:AppWorkspaceManager › manualPayment | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.update` | `var:f` | service:AppPaymentsManager › createPayment | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |
| `payment.uploadLastWaitingInvoicePayment` | `invoice,photo` | controller:AppWorkspaceSettingsController › uploadLastWaitingInvoicePayment | ➖ پیاده‌نشده | مالی و پرداخت: عمداً کنار گذاشته شد |

## `polling` — نظرسنجی (6)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `polling.getTemplates` | `-` | service:AppPollingManager › cancel | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `polling.printPollingResults` | `dialog,polling` | service:AppPollingManager › printPollingResults | ➖ پیاده‌نشده | نظرسنجی (پیوست چت، نیازمند ادمین گروه): پیاده نشد |
| `polling.retractVote` | `dialog,polling` | service:AppImManager › retractVote | ➖ پیاده‌نشده | نظرسنجی (پیوست چت، نیازمند ادمین گروه): پیاده نشد |
| `polling.setPollingAsTemplate` | `var:d` | service:AppImManager › togglePollingTemplate | ➖ پیاده‌نشده | نظرسنجی (پیوست چت، نیازمند ادمین گروه): پیاده نشد |
| `polling.setPollingVote` | `dialog,polling,my_votes` | service:AppPollingManager › setVote | ➖ پیاده‌نشده | نظرسنجی (پیوست چت، نیازمند ادمین گروه): پیاده نشد |
| `polling.stopPolling` | `dialog,polling` | service:AppImManager › stopPolling | ➖ پیاده‌نشده | نظرسنجی (پیوست چت، نیازمند ادمین گروه): پیاده نشد |

## `profile` — پروفایل و امنیت حساب (17)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `profile.activate` | `firstname,lastname,pass` | controller:AppLoginProfileController › sendMyInfo | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.changePhoneNumber` | `step,password` \| `step,token,phone,pin` | service:AppProfileManager › update | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.getEmailInfo` | `-` | service:AppProfileManager › terminateSession | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.getProfileSecurity` | `-` | service:AppProfileManager › showProfileSettings | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.removePhoto` | `-` | service:AppProfileManager › removePhoto | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.setDontDisturbUntil` | `hours` | service:AppProfileManager › setDontDisturb | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.setOnlineStatus` | `status` | service:AppUsersManager › update | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.setUserOptions` | `optionTitle,value` | service:AppProfileManager › setProfileOptions | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.setWallpaper` | `wallpaper` | controller:AppWorkspaceController › setWallpaper | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.terminateOneSession` | `regId,terminateSid` | service:AppProfileManager › terminateSession | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.terminateOtherSessions` | `regId` | service:AppProfileManager › terminateOtherSessions | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.turnTwoStepLoginOff` | `-` \| `pinCode` | service:AppProfileManager › twoStepLoginSwitchChanged | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.update` | `var:b.profile` | service:AppProfileManager › update | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.updateEmail` | `email` | service:AppProfileManager › setEmail | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.updatePassword` | `current,pass,pinCode` | service:AppProfileManager › changePassword | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.updatePhoto` | `base,points` | service:AppProfileManager › setPhoto | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |
| `profile.verifyEmail` | `code` | service:AppProfileManager › checkEmailVerificationCode | ➖ پیاده‌نشده | رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد |

## `projectAutomation` — اتوماسیون پروژه (17)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `projectAutomation.add` | `projectId,automateItem` | service:AppProjectAutomationManager › update | ➖ پیاده‌نشده | اتوماسیون پروژه‌های پیشرفته: پیاده نشد |
| `projectAutomation.buttonClicked` | `var:g` | service:AppProjectAutomationManager › automateButtonClicked | ➖ پیاده‌نشده | اتوماسیون پروژه‌های پیشرفته: پیاده نشد |
| `projectAutomation.customParam.add` | `projectId,paramItem` | service:AppProjectAutomationCustomParamsManager › applyTemplateEnsureAndSelect<br>service:AppProjectAutomationFormRequestsManager › ensureFormTemplateForWorkflowKey | ➖ پیاده‌نشده | اتوماسیون پروژه‌های پیشرفته: پیاده نشد |
| `projectAutomation.customParam.delete` | `projectId,paramId` | service:AppProjectAutomationCustomParamsManager › delete | ➖ پیاده‌نشده | اتوماسیون پروژه‌های پیشرفته: پیاده نشد |
| `projectAutomation.customParam.getAll` | `projectId,token,automateButtonId,isAdminMode` | service:AppProjectAutomationCustomParamsManager › automateButtonClicked | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projectAutomation.customParam.getHistory` | `projectId,paramId` | service:AppProjectAutomationCustomParamsManager › cancel | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projectAutomation.customParam.getValuesHistory` | `token` | service:AppProjectAutomationCustomParamsManager › showTaskParamValuesHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projectAutomation.customParam.restore` | `projectId,paramId` | service:AppProjectAutomationCustomParamsManager › restoreParam | ➖ پیاده‌نشده | اتوماسیون پروژه‌های پیشرفته: پیاده نشد |
| `projectAutomation.customParam.update` | `projectId,paramId,paramItem` | service:AppProjectAutomationFormRequestsManager › cancel | ➖ پیاده‌نشده | اتوماسیون پروژه‌های پیشرفته: پیاده نشد |
| `projectAutomation.customParam.updateOrder` | `projectId,items` | service:AppProjectAutomationCustomParamsManager › updateOrder | ➖ پیاده‌نشده | اتوماسیون پروژه‌های پیشرفته: پیاده نشد |
| `projectAutomation.delete` | `projectId,automateItemId` | service:AppProjectAutomationManager › delete | ➖ پیاده‌نشده | اتوماسیون پروژه‌های پیشرفته: پیاده نشد |
| `projectAutomation.getAll` | `projectId` | service:AppProjectAutomationManager › close | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projectAutomation.getHistory` | `automateId,projectId` | service:AppProjectAutomationManager › close | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projectAutomation.getTaskAutomateButtons` | `token` | service:AppProjectAutomationManager › getTaskAutomateButtons | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projectAutomation.loadConstants` | `-` | service:AppProjectAutomationManager › ? | ➖ پیاده‌نشده | اتوماسیون پروژه‌های پیشرفته: پیاده نشد |
| `projectAutomation.update` | `projectId,automateItem` | service:AppProjectAutomationManager › update | ➖ پیاده‌نشده | اتوماسیون پروژه‌های پیشرفته: پیاده نشد |
| `projectAutomation.updateOrder` | `projectId,type,items` | service:AppProjectAutomationManager › saveOrder | ➖ پیاده‌نشده | اتوماسیون پروژه‌های پیشرفته: پیاده نشد |

## `projectAutomationWorkflow` — گردش‌کار اتوماسیون (6)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `projectAutomationWorkflow.add` | `projectId,workflow` | service:AppProjectAutomationWorkflowManager › ensureFormTemplateForWorkflowKey | ➖ پیاده‌نشده | گردش‌کار اتوماسیون: پیاده نشد |
| `projectAutomationWorkflow.delete` | `projectId,workflowId` | service:AppProjectAutomationWorkflowManager › ensureFormTemplateForWorkflowKey | ➖ پیاده‌نشده | گردش‌کار اتوماسیون: پیاده نشد |
| `projectAutomationWorkflow.getAll` | `projectId` | service:AppProjectAutomationWorkflowManager › getAll | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projectAutomationWorkflow.getOne` | `projectId,workflowId` | service:AppProjectAutomationWorkflowManager › ensureFormTemplateForWorkflowKey | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projectAutomationWorkflow.getTaskWorkflow` | `token` | service:AppProjectAutomationWorkflowManager › ensureFormTemplateForWorkflowKey | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projectAutomationWorkflow.update` | `projectId,workflow` | service:AppProjectAutomationWorkflowManager › ensureFormTemplateForWorkflowKey | ➖ پیاده‌نشده | گردش‌کار اتوماسیون: پیاده نشد |

## `projects` — پروژه‌ها (41)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `projects.activateAdvancedFeatures` | `project,dialog,advanced` | service:AppChatsManager › toggleProjectAdvancedFeatures | ➖ پیاده‌نشده | پیاده نشد |
| `projects.add` | `title,color,members` | service:AppProjectsManager › cancel | ✅ تست‌شده | `mizito_api_read` |
| `projects.addKanbanBoard` | `projectId,kanbanBoard` | service:AppKanbanManager › update | ✅ تست‌شده | `mizito_add_project_board` |
| `projects.allSummary` | `-` \| `with_details` | controller:AppDashboardController › showAllTrackingItems<br>controller:AppImDialogsController › callDialog | ✅ تست‌شده | `_projects_tab` |
| `projects.archive` | `project_id` | service:AppProjectsManager › archiveProject | ⛔ رد شد | 405 برای غیرمدیر (در وب «حذف با امکان بازگشت» است) |
| `projects.chatSummary` | `dialog,project,withBoards` | controller:AppImDialogsController › callDialog<br>controller:ChatProjectStatisticsCtrl › handleVoiceRecordFile | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.clone` | `projectId,projectName,ignoreTaskIds` | service:AppProjectDuplicateManager › duplicateProject | ➖ پیاده‌نشده | پیاده نشد |
| `projects.full` | `project_id` | service:AppProjectsManager › cancel | ✅ تست‌شده | `_project_overview`, `mizito_add_project_board`, `mizito_add_project_members`, `mizito_archive_project`, `mizito_update_project` |
| `projects.ganttGroupAddTasks` | `var:P` | service:AppGanttManager › showAddExistingTaskModal | ➖ پیاده‌نشده | پیاده نشد |
| `projects.ganttLoadMoreTasks` | `project,taskIds` | service:AppGanttManager › cancel | ➖ پیاده‌نشده | پیاده نشد |
| `projects.ganttMoveTask` | `var:Q` | service:AppGanttManager › onDomRemoved | ➖ پیاده‌نشده | پیاده نشد |
| `projects.ganttRemoveGroup` | `project,phaseId` | service:AppGanttManager › delete | ➖ پیاده‌نشده | پیاده نشد |
| `projects.ganttRemoveTask` | `project,taskId` | service:AppTasksManager › removeFromGantt | ➖ پیاده‌نشده | پیاده نشد |
| `projects.ganttSaveGroup` | `project,phase` | service:AppGanttManager › create | ➖ پیاده‌نشده | پیاده نشد |
| `projects.ganttSetTaskTimeline` | `project,tasks` | service:AppGanttManager › ? | ➖ پیاده‌نشده | پیاده نشد |
| `projects.ganttTaskLinkAdd` | `var:R` | service:AppGanttManager › onDomRemoved | ➖ پیاده‌نشده | پیاده نشد |
| `projects.ganttTaskLinkRemove` | `var:S` | service:AppGanttManager › onDomRemoved | ➖ پیاده‌نشده | پیاده نشد |
| `projects.get` | `projectId,token` | service:AppProjectsManager › selectHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.getAdvancedFeaturesHistory` | `dialog,project` | service:AppProjectAdvancedHistoryManager › showChangesHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.getGanttData` | `project` | service:AppGanttManager › cancel | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.getList` | `-` | service:AppProjectsManager › selectHistory | ✅ تست‌شده | `_refresh_task_tokens`, `mizito_archive_project`, `mizito_create_project`, `mizito_list_projects` |
| `projects.getListAdmin` | `-` | service:AppProjectsManager › selectHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.getListAdminForMember` | `user` | service:AppProjectsManager › selectHistory | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.getProjectFiles` | `var:a` | controller:AppProjectFilesController › printResult | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.getProjectTaskFileIds` | `project,task` | controller:AppProjectFilesController › showTask | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.getProjectsUserAdmin` | `-` | controller:AppCalendarViewerController › filterSelectProject<br>controller:AppMonitoringProjectsController › projectLabelChanged<br>controller:AppMonitoringProjectsForUserCalendarController › showMonitorPage<br>controller:AppMonitoringTasksController › filterSelectProjectList | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.history` | `project_id` | service:AppProjectsManager › showChangesHistory | ✅ تست‌شده | `mizito_get_history` |
| `projects.import` | `contentId,importType,projectTitle,memberAssign,labelAssign,fieldIndexes,kanbanDoneListTitle` | controller:AppImportProjectController › importTasks | ➖ پیاده‌نشده | پیاده نشد |
| `projects.importPrepare` | `contentId,importType` | controller:AppImportProjectController › prepareRows | ➖ پیاده‌نشده | پیاده نشد |
| `projects.monitor.chart.getPast30DoneTasksPercents` | `var:e` | controller:AppMonitoringProjectsController › showCalendarPage | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `projects.monitor.project` | `projectId` | controller:AppMonitoringProjectController › print | ⛔ رد شد | 400 (دسترسی مدیر/پلن) |
| `projects.monitor.projectsSummary` | `var:e` | controller:AppMonitoringProjectsController › showCalendarPage | ➖ پیاده‌نشده | پیاده نشد |
| `projects.removeKanbanBoard` | `projectId,boardId` | controller:AppKanbanViewerController › removeBoard | ➖ پیاده‌نشده | پیاده نشد |
| `projects.restoreArchivedTasks` | `project` | controller:AppFixProjectsController › restoreArchiveTasks | ➖ پیاده‌نشده | پیاده نشد |
| `projects.save` | `project_id,title,color,members` | service:AppProjectsManager › cancel | ✅ تست‌شده | `mizito_add_project_members`, `mizito_update_project` |
| `projects.setAdvancedFeatures` | `dialog,advanced` | service:AppChatsManager › setAdminUser<br>service:AppProjectsManager › cancel | ➖ پیاده‌نشده | پیاده نشد |
| `projects.setChatProjectColor` | `project,dialog,color` | service:AppProjectsManager › showColorSelector | ➖ پیاده‌نشده | پیاده نشد |
| `projects.setChatProjectLabels` | `project,dialog,labels` | service:AppProjectsManager › setProjectLabel | ➖ پیاده‌نشده | پیاده نشد |
| `projects.setKanbanBoardOrder` | `projectId,boardId,oldPosition,newPosition` | controller:AppKanbanViewerController › invalidTarget | ➖ پیاده‌نشده | پیاده نشد |
| `projects.undoArchive` | `project_id` | service:AppProjectsManager › archiveProject | ⛔ رد شد | 405 برای غیرمدیر |
| `projects.updateKanbanBoard` | `projectId,kanbanBoardId,kanbanBoard` | service:AppKanbanManager › update | ➖ پیاده‌نشده | پیاده نشد |

## `session` — نشست و حساب کاربری (10)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `session.createSSO` | `token` | controller:AppLoginSSOController › link | ➖ پیاده‌نشده | ورود، ثبت‌نام و حذف حساب: عمداً کنار گذاشته شد |
| `session.deleteAccount` | `validationCode` | controller:AppDeleteAccountController › deleteAccount | ➖ پیاده‌نشده | ورود، ثبت‌نام و حذف حساب: عمداً کنار گذاشته شد |
| `session.deleteAccountRequest` | `username` | controller:AppDeleteAccountRequestController › sendDeleteAccountCodeRequest | ➖ پیاده‌نشده | ورود، ثبت‌نام و حذف حساب: عمداً کنار گذاشته شد |
| `session.forgot` | `username` | controller:AppLoginProfileController › sendResetCodeRequest | ➖ پیاده‌نشده | ورود، ثبت‌نام و حذف حساب: عمداً کنار گذاشته شد |
| `session.forgotReset` | `reset_code,pass` | controller:AppLoginRegisterController › resetPassword | ➖ پیاده‌نشده | ورود، ثبت‌نام و حذف حساب: عمداً کنار گذاشته شد |
| `session.iOSAppIsAlive` | `deviceId,isAlive` | factory:notificationIOSService › onmessage | ➖ پیاده‌نشده | ورود، ثبت‌نام و حذف حساب: عمداً کنار گذاشته شد |
| `session.logout` | `var:t` | factory:services › logout | ➖ پیاده‌نشده | ورود، ثبت‌نام و حذف حساب: عمداً کنار گذاشته شد |
| `session.register` | `var:e` \| `var:l` | controller:AppRegisterCompleteController › createWorkspace<br>controller:AppRegisterCompleteController › sendMyInfo<br>controller:AppRegisterController › checkPinCode<br>controller:AppRegisterController › sendActivateCode | ➖ پیاده‌نشده | ورود، ثبت‌نام و حذف حساب: عمداً کنار گذاشته شد |
| `session.userInfo` | `uid` | controller:AppLoginController › link | ➖ پیاده‌نشده | ورود، ثبت‌نام و حذف حساب: عمداً کنار گذاشته شد |
| `session.username` | `var:null` | controller:AppRegisterController › removeTeammate | ➖ پیاده‌نشده | ورود، ثبت‌نام و حذف حساب: عمداً کنار گذاشته شد |

## `support` — پشتیبانی میزیتو (32)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `support.clientOnlineHistory` | `-` | service:AppSupportManager › loadOnlineSupportHistory | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.closeResponse` | `supportId` | service:AppSupportManager › closeResponse | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.deleteFromClient` | `messageId` | service:AppSupportManager › deleteFromClient | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.deleteResponse` | `supportId,messageId` | service:AppSupportManager › deleteResponse | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.deleteResponseFeedback` | `messageId` | service:AppSupportManager › deleteResponseFeedback | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.editFromClient` | `messageId,message` | service:AppSupportManager › editFromClient | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.editResponse` | `supportId,messageId,message` | service:AppSupportManager › editResponse | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.extendDialogLock` | `supportId` | service:AppSupportManager › extendDialogLock | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.getAdminHistory` | `supportId` | service:AppSupportManager › getAdminHistory | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.getClientUnreadCount` | `-` | service:AppSupportManager › getClientBadge | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.getDialog` | `dialog` | service:AppSupportManager › getDialogOrLoad | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.getDialogs` | `filter,filterIsLastMessageIsRequest,skip,limit` | service:AppSupportManager › registerLetter | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.getFeedbackMonitor` | `var:a` | service:AppSupportManager › getFeedbackMonitor | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.getFeedbackMonitorOpenCount` | `{}` | service:AppSupportManager › getFeedbackMonitorOpenCount | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.getFeedbackMonitorStats` | `var:a` | service:AppSupportManager › getFeedbackMonitorStats | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.getFeedbackReviewCase` | `caseId` | service:AppSupportManager › getFeedbackReviewCase | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.getSupportInfo` | `supportId` | controller:AppAdminSupportChatController › close<br>controller:AppAdminSupportChatController › openSupportDialogAtMessage | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.lockDialog` | `supportId` | service:AppSupportManager › lockDialog | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.markClientSeen` | `seenCount` | service:AppSupportManager › markClientSeen | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.markSupportSeen` | `supportId,seenCount` | service:AppSupportManager › markSupportSeen | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.reopenFeedbackReview` | `caseId` | service:AppSupportManager › reopenFeedbackReview | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.resolveFeedbackReview` | `caseId,result,dissatisfactionReason,note` | service:AppSupportManager › resolveFeedbackReview | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.searchContent` | `searchStr,messageType,supportUser,fromDate,toDate,skip` | controller:AppAdminSupportChatController › searchContents | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.sendFromClient` | `message,media,replyTo` | service:AppSupportManager › sendFromClient | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.sendResponse` | `supportId,message,media,replyTo` | service:AppSupportManager › sendResponse | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.sendSuggestion` | `var:a.suggestion` | service:AppSupportManager › send | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.setResponseFeedbackVote` | `messageId,value,reason,comment` | service:AppSupportManager › setResponseFeedbackVote | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.setTyping` | `-` | controller:AppSupportChatController › keyPressed | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.setTypingAdmin` | `supportId` | controller:AppAdminSupportChatController › sendDraftMessage | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.startFeedbackReview` | `caseId` | service:AppSupportManager › startFeedbackReview | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.unlockDialog` | `supportId` | service:AppSupportManager › unlockDialog | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |
| `support.updateResponseFeedbackDetails` | `messageId,reason,comment` | service:AppSupportManager › updateResponseFeedbackDetails | ➖ پیاده‌نشده | گفتگوی پشتیبانی خود میزیتو: خارج از محدوده |

## `taskTemplates` — قالب‌های وظیفه (5)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `taskTemplates.add` | `var:a` | service:AppTaskTemplatesManager › updateRepeatingTask | ➖ پیاده‌نشده | قالب وظیفه: پیاده نشد |
| `taskTemplates.getAll` | `projectId` | service:AppTaskTemplatesManager › getAll | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `taskTemplates.getAllTemplates` | `projectId` | service:AppTaskTemplatesManager › getAllForUser | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `taskTemplates.remove` | `projectId,templateId` | service:AppTaskTemplatesManager › remove | ➖ پیاده‌نشده | قالب وظیفه: پیاده نشد |
| `taskTemplates.save` | `var:a` | service:AppTaskTemplatesManager › updateRepeatingTask | ➖ پیاده‌نشده | قالب وظیفه: پیاده نشد |

## `tasks` — وظایف (28)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `tasks.add` | `var:l` \| `var:o` | service:AppMinutesManager › selectTemplate<br>service:AppTasksManager › show | ✅ تست‌شده | `mizito_create_task` |
| `tasks.badge` | `-` | factory:services › getTasksBadge | ✅ تست‌شده | `mizito_api_read` |
| `tasks.checkToken` | `tid,token` | service:AppTasksManager › ? | ➖ پیاده‌نشده | پیاده نشد |
| `tasks.createShareLink` | `token` | service:AppTasksManager › copyTaskLink | ➖ پیاده‌نشده | پیاده نشد |
| `tasks.deleteComment` | `token,commentId` | service:AppTasksManager › deleteComment | ➖ پیاده‌نشده | پیاده نشد |
| `tasks.editComment` | `token,commentId,newComment` | service:AppTasksManager › update | ➖ پیاده‌نشده | پیاده نشد |
| `tasks.ganttGetTaskInfo` | `project,token` | service:AppTasksManager › gotoProjectPage | ➖ پیاده‌نشده | پیاده نشد |
| `tasks.get` | `var:a` | service:AppTasksManager › clickOutsideToClose | ✅ تست‌شده | `_load_task` |
| `tasks.getAll` | `var:e` | service:AppTasksManager › getAll | ✅ تست‌شده | `mizito_api_read` |
| `tasks.getComments` | `token` | service:AppTasksManager › ? | ✅ تست‌شده | `mizito_comment_on_task`, `mizito_get_task_comments` |
| `tasks.getSeenDetails` | `token` | service:AppTasksManager › ? | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `tasks.history` | `token,tid` | service:AppTasksManager › toggleSortOrder | ✅ تست‌شده | `mizito_get_history` |
| `tasks.newComment` | `token,comment,attachments,mention,reply_id` | service:AppTasksManager › sendNewComment | ✅ تست‌شده | `mizito_comment_on_task` |
| `tasks.print` | `done_timeline,filter` \| `var:a` \| `var:e` | controller:AppMonitoringTasksController › printResult<br>controller:AppTasksDoneController › printDoneResult<br>controller:AppTasksInboxController › printResult | ➖ پیاده‌نشده | پیاده نشد |
| `tasks.removeFromBoard` | `token,project_id` | service:AppTasksManager › removeTaskFromBoard | ➖ پیاده‌نشده | پیاده نشد |
| `tasks.removeFromTracking` | `token` | service:AppTasksManager › removeTaskFromTracking | ➖ پیاده‌نشده | پیاده نشد |
| `tasks.removeTask` | `token` | service:AppTasksManager › removeTask | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_task` — حذف است؛ تست نشد |
| `tasks.removeTaskUndo` | `token` | service:AppTasksManager › removeTaskUndo | 🟡 پیاده‌شده، تست‌نشده | `mizito_manage_task` — برگرداندن حذف؛ تست نشد |
| `tasks.save` | `var:o` | service:AppTasksManager › show | ✅ تست‌شده | `_save_task` |
| `tasks.setChecklistCheckedValue` | `token,checklistId,checked` | service:AppTasksManager › checklistCheckedChanged | ✅ تست‌شده | `mizito_check_task_item` |
| `tasks.setCompleted` | `token,completed,project` \| `token,project,completed,progress,undone_user_id` | service:AppTasksManager › clickOutsideToClose | ✅ تست‌شده | `mizito_set_task_completed` |
| `tasks.setKanbanWeight` | `token,projectId,kanbanBoardId,kanbanWeight` | controller:AppKanbanViewerController › invalidTarget | ➖ پیاده‌نشده | پیاده نشد |
| `tasks.setKanbanWeightSort` | `projectId,kanbanBoardId,sortField,sortOrder` | controller:AppKanbanViewerController › sortTasks | ➖ پیاده‌نشده | پیاده نشد |
| `tasks.snooze` | `token,project,alarm_at,update_repeat_base` | service:AppTasksManager › snoozeTask | ✅ تست‌شده | `mizito_create_task`, `mizito_set_task_reminder` |
| `tasks.toggleBookmark` | `token,bookmarked` | service:AppTasksManager › toggleBookmark | ✅ تست‌شده | `mizito_manage_task` |
| `tasks.upcoming` | `var:e` | service:AppTasksManager › loadUpcoming | ✅ تست‌شده | `_refresh_task_tokens`, `mizito_calendar`, `mizito_list_tasks` |
| `tasks.updateDeadline` | `token,project,deadline` | service:AppTasksManager › updateTaskDeadline | ✅ تست‌شده | `mizito_set_task_deadline` |
| `tasks.updateProgress` | `token,progress` | service:AppTasksManager › updateProgress | ✅ تست‌شده | `mizito_set_task_progress` |

## `workspace` — میزکار (22)

| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |
|---|---|---|---|---|
| `workspace.add` | `name,members` | service:AppWorkspaceManager › create | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.changeOwner` | `owner,pinCode,password` | service:AppWorkspaceManager › update | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.changeRole` | `user_id,role` | controller:AppWorkspaceSettingsController › changeRole | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.delete` | `-` | controller:AppWorkspaceSettingsController › deleteWorkspace | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.getPermissions` | `-` | service:AppWorkspaceManager › getPermissions | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `workspace.getPlans` | `-` | service:AppWorkspaceManager › getPlanTypes | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `workspace.getUsers` | `-` | service:AppUsersManager › endCall | ✅ تست‌شده | `mizito_list_users` |
| `workspace.ignoreBusinessTypeModal` | `-` | service:AppWorkspaceManager › close | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.inviteMember` | `name,email_phone,is_guest` | service:AppUsersManager › endCall | 🟡 پیاده‌شده، تست‌نشده | `mizito_invite_workspace_member` — دعوت واقعی می‌فرستد؛ تست نشد |
| `workspace.name` | `-` | service:AppWorkspaceManager › loadWorkspaceName | 🔎 با `mizito_api_read` | خواندنی؛ ابزار اختصاصی ندارد |
| `workspace.planInfo` | `details` | service:AppWorkspaceManager › close | ✅ تست‌شده | `mizito_api_read` |
| `workspace.reJoinMember` | `member_id` | controller:AppWorkspaceSettingsController › reJoinMember | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.removeMember` | `member_id` | controller:AppWorkspaceSettingsController › removeMember | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.sendContactUsage` | `user_id` | service:AppCustomersManager › createCustomer<br>service:AppInboxManager › send<br>service:AppUsersManager › endCall | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.setWorkspaceSettings` | `title,value` | controller:AppWorkspaceSettingsController › setWorkspaceSettings | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.switch` | `workspace_id` | service:AppWorkspaceManager › cancel | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.updateBusinessType` | `business_type` | service:AppWorkspaceManager › close | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.updateDedicatedLogoPhoto` | `photo` | controller:AppWorkspaceSettingsController › uploadDedicatedLoginPhoto | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.updateTitle` | `title` | controller:AppWorkspaceSettingsController › updateWorkspaceTitle | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.updateUserPermission` | `user,permission,access` | service:AppWorkspaceManager › updateUserPermission | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.updateWorkspaceRoleName` | `user_id,workspaceRoleName` | controller:AppWorkspaceSettingsController › workspaceRoleNameEditableOk | ➖ پیاده‌نشده | پیاده نشد |
| `workspace.userId` | `regId` | controller:AppLoginController › link | ✅ تست‌شده | `mizito_whoami` |

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

