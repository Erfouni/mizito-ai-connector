# صفحه‌های میزیتو (office.mizito.ir)

هر صفحه (state) با آدرس، قالب HTML، پارامترها، و چیزهایی که در قالبش هست: متن‌ها، دکمه‌ها و عمل‌ها (`ng-click`)،
فیلدها (`ng-model`)، لینک‌ها (`ui-sref`)، کنترلرها و endpointهایی که آن کنترلرها صدا می‌زنند.
جزئیات هر قالب در [views.md](views.md) و هر endpoint در [api.md](api.md) آمده است.

## پوسته‌ی اپ

### `ws` (انتزاعی)

- آدرس: `#/ws`
- قالب: `workspace`
- متن‌ها: «پرونده مشتری»، «پروژه»، «گفتگو»، اتصال به اینترنت برقرار نیست، جهت اشتراک‌گذاری فایل(ها) انتخاب کنید، و یا، یک
- عمل‌ها: `cancelAppShareContent`
- کنترلرها: `AppNotificationHistoryController` `AppWorkspaceController`
- endpointهای این کنترلرها: `dashboard.demoGuide` `profile.setWallpaper`

## ورود، ثبت‌نام و حساب کاربری

### `login_sso`

- آدرس: `#/login_sso/:token`
- قالب: `login/login_sso`
- متن‌ها: —
- عمل‌ها: —
- کنترلرها: `AppLoginSSOController`
- endpointهای این کنترلرها: `session.createSSO`

### `login` (انتزاعی)

- آدرس: `#/lg`
- قالب: `login/login_container`
- متن‌ها: دانلود اپلیکیشن، دانلود اپلیکیشن میزیتو
- عمل‌ها: —
- کنترلرها: `AppLoginController`
- endpointهای این کنترلرها: `session.userInfo` `workspace.userId`

### `login.login`

- آدرس: `#/login`
- قالب: `login/login`
- متن‌ها: ثبت‌نام، حساب کاربری ندارید؟، شماره همراه خود را وارد نمایید، ورود، ورود بیومتریک، کلمه عبور، کلمه عبور را فراموش کرده‌ام
- عمل‌ها: `forgotPassword` `login` `loginBiometric` `showRegisterForm` `showUserNameInput`
- فیلدها: `user.password` `user.username`

### `login.profile`

- آدرس: `#/profile`
- قالب: `login/profile`
- متن‌ها: «به میزیتو خوش آمدید»، انتخاب کلمه عبور، انصراف، تکرار کلمه عبور، شما برای اولین بار است که از میزیتو استفاده می‌کنید. برای شروع به کار، لطفاً اطلاعات خود را کامل نمایید.، قوانین و مقررات، موجود در سایت را می‌پذیرم.، نام، نام خانوادگی
- عمل‌ها: `cancelSendMyInfo` `sendMyInfo`
- فیلدها: `register.accept_terms` `register.firstname` `register.lastname` `register.password` `register.repassword`
- زیرقالب‌ها: `login/partial/partial-password-complexity-hint`
- کنترلرها: `AppLoginProfileController`
- endpointهای این کنترلرها: `profile.activate` `session.forgot`

### `login.forgot`

- آدرس: `#/forgot`
- قالب: `login/forgot`
- متن‌ها: انصراف، درخواست کد ریست، شماره همراه خود را وارد نمایید، شماره همراه خود را وارد کنید، تا کد ریست برای شما ارسال شود.، فراموشی کلمه عبور
- عمل‌ها: `cancelSendResetCodeRequest` `sendResetCodeRequest`
- فیلدها: `forgot_username.username`

### `login.forgot_reset`

- آدرس: `#/forgot_reset`
- قالب: `login/forgot_reset`
- متن‌ها: انتخاب کلمه عبور، به‌روزرسانی کلمه عبور، تکرار کلمه عبور، درخواست مجدد، کد ریست، کد ریست ارسال شده را در کادر زیر وارد نمایید:
- عمل‌ها: `cancelResetPassword` `resetPassword`
- فیلدها: `reset_password.password` `reset_password.repassword` `reset_password.reset_code`
- زیرقالب‌ها: `login/partial/partial-password-complexity-hint`
- کنترلرها: `AppLoginRegisterController`
- endpointهای این کنترلرها: `session.forgotReset`

### `register` (انتزاعی)

- آدرس: `#/register/p=:phone`
- قالب: `login/register_container`
- پارامترها: `phone`
- متن‌ها: به میزیتو خوش آمدید، در حال آماده‌سازی میزِکار شما...، سپاسگزاریم که میزیتو را انتخاب نمودید
- عمل‌ها: —
- کنترلرها: `AppRegisterController`
- endpointهای این کنترلرها: `session.register` `session.username`

### `register.step1`

- آدرس: `#/s1`
- قالب: `login/reg_1`
- متن‌ها: آدرس ایمیل خود را وارد نمایید، از طریق ایمیل، از طریق پیامک، با ثبت‌نام در میزیتو، شما با، ثبت‌نام، شرایط استفاده و قوانین حریم شخصی، شماره همراه خود را وارد نمایید، قبلاً ثبت‌نام کرده‌اید؟، ملحق شدن به، میزیتو، میزیتو موافقت کرده‌اید.، ورود
- عمل‌ها: `sendActivateCode` `showLoginForm`
- فیلدها: `register.activate_method` `register.email` `register.phone`

### `register.step2`

- آدرس: `#/s2`
- قالب: `login/reg_2`
- متن‌ها: بررسی کد فعال‌سازی، درخواست مجدد، کد فعال‌سازی، کد فعال‌سازی دریافت شده را در کادر زیر وارد کنید:
- عمل‌ها: `checkPinCode` `showActivateSelector`
- فیلدها: `register.pin_code`

### `register.step3`

- آدرس: `#/s3`
- قالب: `login/reg_3`
- متن‌ها: * توجه داشته باشید برای ورودهای بعدی به میزیتو، باید در قسمت، انتخاب کلمه عبور، تنظیمات اولیه، تکرار کلمه عبور، را وارد نمایید.، عبارت، قوانین و مقررات، موجود در سایت را می‌پذیرم.، نام، نام خانوادگی، نام شرکت و یا تیم، نام کاربری، نام کاربری شما
- عمل‌ها: `sendMyInfo`
- فیلدها: `register.accept_terms` `register.firstname` `register.lastname` `register.password` `register.repassword` `register.username` `register.workspace_name`
- زیرقالب‌ها: `login/partial/partial-password-complexity-hint`
- کنترلرها: `AppRegisterCompleteController`
- endpointهای این کنترلرها: `session.register`

### `register.step4`

- آدرس: `#/s4`
- قالب: `login/reg_4`
- متن‌ها: بعداً همکارانم را معرفی می‌کنم، جهت شروع، همکاران را به میزکار خود دعوت کنید:، دعوت همکاران به میزکار، شماره همراه، نام همکار، ورود به میزیتو
- عمل‌ها: `addTeammate` `createWorkspace` `removeTeammate`
- فیلدها: `user.email_phone` `user.name`

### `workspace_switching`

- آدرس: `#/workspace_switching`
- قالب: `workspace/switching`
- متن‌ها: لطفاً منتظر بمانید...
- عمل‌ها: —
- کنترلرها: `AppWorkspaceSwitchingController`

### `delete_account.request`

- آدرس: (کنترلر AppDeleteAccountRequest…)
- قالب: —

### `delete_account.validation`

- آدرس: (کنترلر AppDeleteAccountController)
- قالب: —

## داشبورد

### `ws.home`

- آدرس: `#/home`
- قالب: `home/home`
- متن‌ها: ... مشاهده همه ( )، «تنظیمات»، «مجوزها»، ارتقاء طرح، انصراف، ایجاد میزِکار جدید، ایجاد میزکار جدید، این میزکار دارای پلن پیشرفته می‌باشد، این نسخه از میزیتو بر روی سرور اختصاصی نصب شده است، بخیر، بخیر؛، برای استفاده از دیگر امکانات میزیتو، به بخش، به میزِکار، به میزیتو خوش اومدی؛، تأیید درخواست، دعوت شده‌اید، راهنما، سایر میزِکارها، سایر میزِکارهای شما:، شما توسط، شما میزِکار فعالی ندارید. لطفاً جهت ادامه، یک میزِکار جدید برای خود بسازید:، فضای میزِکار شما در حال تمام شدن است. لطفاً قبل از اتمام نسبت به ارتقاء طرح خود اقدام نمایید.، فعال‌سازی امکانات، مخفی شدن میزِکارها، مراجعه کنید.، میزکار «، نوتیفیکیشن‌های مرورگر را غیرفعال کرده‌اید، پشتیبانی
- عمل‌ها: `acceptInvite` `activatePermissions` `cancelInvite` `createNewWorkspace` `profileSettings` `sendSupportRequest` `showAllOtherWorkspaces` `showHelp` `showOnlineStatusSelector` `showProfileSettings` `showSettingsPlansTab` `toggleCollapseWorkspaces`
- زیرقالب‌ها: `home/workspace-widget` `home/workspace-widget-active`
- کنترلرها: `AppDashboardController`
- endpointهای این کنترلرها: `dashboard.acceptInviteRequest` `dashboard.cancelInviteRequest` `dashboard.getAllSummary` `dashboard.getAllWorkspacesUsers` `dashboard.getPending` `dashboard.notifySeen` `meeting.endCall` `projects.allSummary`

## گفتگو

### `ws.im`

- آدرس: `#/im/:dialog/:message`
- قالب: `chat/chat`
- پارامترها: `dialog`
- متن‌ها: برای شروع مکالمه یک مخاطب را انتخاب کنید، در حال بارگذاری، هنوز پیغامی وجود ندارد ...
- عمل‌ها: `gotoRepliedBaseMessage`
- زیرقالب‌ها: `chat/chat-dialog-list` `chat/chat-header` `chat/chat-input` `chat/chat-pinned-message-viewer` `chat/chat-viewer`
- کنترلرها: `AppImController` `AppImDialogsController` `ChatViewCtrl`
- endpointهای این کنترلرها: `chat.setTyping` `chat.updateSentMessage` `projects.allSummary` `projects.chatSummary`

## پروژه‌ها

### `ws.projects` (انتزاعی)

- آدرس: `#/projects`
- قالب: `projects/projects`
- متن‌ها: در حال بارگذاری، هنوز پیغامی وجود ندارد ...
- عمل‌ها: `gotoRepliedBaseMessage`
- زیرقالب‌ها: `chat/chat-input` `chat/chat-pinned-message-viewer` `chat/chat-viewer` `projects/calendar/calendar-viewer` `projects/gantt/gantt-viewer` `projects/kanban-viewer` `projects/partial/chat-header-project` `projects/partial/project-pane` `projects/projects-list` `tasks/project-viewer`
- کنترلرها: `AppCalendarViewerController` `AppGanttViewerController` `AppImController` `AppImDialogsController` `AppKanbanViewerController` `AppProjectFilesController` `AppProjectPaneController` `AppTasksController` `AppTasksInboxController` `ChatProjectStatisticsCtrl` `ChatViewCtrl`
- endpointهای این کنترلرها: `chat.setTyping` `chat.updateSentMessage` `projects.allSummary` `projects.chatSummary` `projects.getProjectFiles` `projects.getProjectTaskFileIds` `projects.getProjectsUserAdmin` `projects.removeKanbanBoard` `projects.setKanbanBoardOrder` `tasks.print` `tasks.setKanbanWeight` `tasks.setKanbanWeightSort`

### `ws.projects.all`

- آدرس: `#/all`
- قالب: —

### `ws.projects.dialog`

- آدرس: `#/dialog/:dialog/:message`
- قالب: —
- پارامترها: `dialog`

### `ws.projects_monitor`

- آدرس: `#/projects/monitor`
- قالب: `monitoring/monitoring_projects`
- متن‌ها: * وظیفه دارای بیشترین تاخیر:، * کاربر دارای بیشترین تعداد وظیفه در کارتابل:، آرشیو شده، آرشیو نشده، انتخاب گروه‌بندی پروژه:، تعداد:، جهت مانیتورینگ باید در پروژه‌ها دسترسی مدیریت داشته باشید.، در این صفحه، وضعیت پروژه‌هایی که مدیر آن‌ها هستید نمایش داده می‌شود.، مانیتورینگ وظایف، مانیتورینگ پروژه‌ها، مانیتورینگ پروژه‌های کاربر، مرتب‌سازی پروژه‌ها:، مورد، نمایش تقویم وظایف، نمودار کارهای انجام شده در ۳۰ روز گذشته، همه پروژه‌ها، همه پروژه‌های میزکار، همه پروژه‌های کاربر، وضعیت آرشیو، وضعیت پیشرفت پروژه‌ها:، چاپ گزارش، کارهای انجام شده در ۳۰ روز گذشته، کاری انجام نشده است، گزارش شامل پروژه‌های:
- عمل‌ها: `$mdMenu.open` `print` `setSortType` `showCalendarPage` `showMonitorTasksPage` `showPrevPage` `showProjectDetails`
- فیلدها: `filter.archive_status` `filter.str` `selected_project_label.selected`
- کنترلرها: `AppMonitoringProjectsController`
- endpointهای این کنترلرها: `monitor.chart.getPast30DoneTasksPercents` `monitor.projectsSummary` `projects.getProjectsUserAdmin` `projects.monitor.chart.getPast30DoneTasksPercents` `projects.monitor.projectsSummary`

### `ws.projects_monitoring_project`

- آدرس: `#/project/monitor/project/:projectId`
- قالب: `monitoring/monitoring_project`
- متن‌ها: از برچسبی استفاده نشده است، انجام آخرین وظیفه:، انجام اولین وظیفه:، زمان ایجاد پروژه:، زمان یادآوری آخرین وظیفه:، مانیتورینگ پروژه، مورد، میزان استفاده از برچسب‌ها در پروژه، نمودار میزان استفاده از برچسب‌ها در پروژه، نمودار وظایف انجام شده توسط همکاران، وضعیت پیشرفت پروژه:، وظایف انجام شده توسط همکاران، چاپ گزارش
- عمل‌ها: `print` `showMonitorProjectsPage` `showProject`
- کنترلرها: `AppMonitoringProjectController`
- endpointهای این کنترلرها: `monitor.project` `projects.monitor.project`

### `ws.projects_monitoring_tasks`

- آدرس: `#/project/monitor/tasks`
- قالب: `monitoring/monitoring_tasks`
- متن‌ها: انتخاب، انجام شده، انجام نشده، ایجاد کننده، بازه زمانی، برچسب‌ها، بیشتر...، در حال بارگذاری، شماره پیگیری فرم، فقط دارای تاخیر، فیلتر، لیست بورد، لیست وظایف خالی است، مانیتورینگ وظایف، متن، مسؤول انجام، نامشخص، همه وظایف، وضعیت انجام، وضعیت تاخیر، پرونده مشتری، پروژه \| دسته‌بندی، چاپ نتایج، گروه‌بندی پروژه‌ها
- عمل‌ها: `doFilter` `filter.date_range` `filter.dialog` `filter.labels=[]` `filter.project_labels=[]` `filterClearAssignee` `filterClearOwner` `filterClearProject` `filterClearProjectList` `filterSelectAssignee` `filterSelectDateRange` `filterSelectDialog` `filterSelectLabels` `filterSelectOwner` `filterSelectProject` `filterSelectProjectLabels` `filterSelectProjectList` `loadMore` `printResult` `showMonitorPage`
- فیلدها: `filter.done_status` `filter.form_request_tracking_code` `filter.overdue_status` `filter.title`
- زیرقالب‌ها: `tasks/partial-inbox-sort-selection`
- کنترلرها: `AppMonitoringTasksController`
- endpointهای این کنترلرها: `projects.getProjectsUserAdmin` `tasks.print`

### `ws.projects_monitoring_calendar`

- آدرس: `#/project/monitor/calendar`
- قالب: `projects/monitoring_calendar`
- متن‌ها: مانیتورینگ پروژه‌های زیر:
- عمل‌ها: `showMonitorPage` `toggleSelectProject`
- زیرقالب‌ها: `projects/calendar/calendar-viewer`
- کنترلرها: `AppCalendarViewerController` `AppMonitoringProjectsForUserCalendarController`
- endpointهای این کنترلرها: `projects.getProjectsUserAdmin`

### `ws.import_project`

- آدرس: `#/import_project`
- قالب: `projects/import_project`
- متن‌ها: انتخاب، انتخاب فایل، انتخاب لیست وظایف انجام شده، انتقال اطلاعات، انتقال اطلاعات (Import) وظایف به میزیتو، انتقال اطلاعات از ترلو، انتقال اطلاعات از فایل CSV، انتقال اطلاعات از فایل اکسل، تعداد خطا:، تعیین اعضا:، تعیین برچسب‌ها:، توجه! در حالت دمو، فقط تعداد، دانلود فایل نمونه csv، دانلود فایل نمونه excel، راهنما، راهنمای انتقال اطلاعات از ترلو، ردیف، عنوان پروژه، قابل انتقال می‌باشد.، مرحله قبل، مرحله ۱: انتخاب فایل، مرحله ۲: نمایش، مرحله ۳: تبدیل، مشاهده پروژه، هیچکدام، پروژه " " با موفقیت ایجاد گردید.، ۵ رکورد اطلاعاتی
- عمل‌ها: `cancel` `downloadSampleFile` `importTasks` `selectLabel` `selectMember` `showFinalProject` `showImportHelp` `uploadFile`
- فیلدها: `fieldIndexes[$index]` `kanbanDoneListTitle` `projectTitle`
- کنترلرها: `AppImportProjectController`
- endpointهای این کنترلرها: `projects.import` `projects.importPrepare`

## وظایف و تقویم

### `ws.tasks` (انتزاعی)

- آدرس: `#/tasks`
- قالب: `tasks/tasks`
- متن‌ها: —
- عمل‌ها: `newTask`
- کنترلرها: `AppTasksController`

### `ws.tasks.calendar`

- آدرس: `#/calendar`
- قالب: `projects/calendar/calendar-viewer`
- متن‌ها: تعداد وظایف بیشتر از ۱۰۰ مورد ...، امروز، امروز:، ایجاد وظیفه جدید، تعداد وظایف این روز، جمعه، دوشنبه، زمان یادآوری، سه‌شنبه، شنبه، فیلتر نمایش، مهلت انجام، نحوه نمایش وظایف، نمایش بر اساس:، نمایش وظایف بدون زمان، نمایش وظایف بدون مهلت، نمایش کامل عناوین، وظایف همه کاربران، وظیفه، پنجشنبه، چهارشنبه، یکشنبه
- عمل‌ها: `$mdMenu.open` `addTask` `goToday` `nextMonth` `prevMonth` `setVisibilityType` `showMobileDayTasks` `toggleFilterOptions`
- فیلدها: `show_all_users` `show_complete_task_title_tmp` `show_no_time_tasks`
- زیرقالب‌ها: `projects/calendar/partial-calendar-view-task` `projects/calendar/partial-task-filter`
- کنترلرها: `AppCalendarViewerController`
- endpointهای این کنترلرها: `projects.getProjectsUserAdmin`

### `ws.tasks.inbox`

- آدرس: `#/inbox/:task`
- قالب: `tasks/inbox-viewer`
- پارامترها: `task`
- متن‌ها: —
- عمل‌ها: —
- زیرقالب‌ها: `tasks/partial-tasks-viewer` `tasks/partial_inbox_viewer_header`
- کنترلرها: `AppTasksInboxController`
- endpointهای این کنترلرها: `tasks.print`

### `ws.tasks.project`

- آدرس: `#/project/:project`
- قالب: `tasks/project-viewer`
- متن‌ها: ایجاد وظیفه، بدون انجام دهنده، فیلتر، مشاهده فایل‌ها، مشاهده مشخصات، نمایش:، چاپ نتایج، کارهای انجام شده، کارهای انجام نشده، کارهای بدون زمان، کارهای دارای تاخیر، کارهای دارای زمان، کارهای دارای پیشرفت، کارهای دیگران، کارهای من
- عمل‌ها: `$mdMenu.open` `addTaskFromTasksView` `editProjectInfo` `printResult` `show_project_files.active` `toggleFilterOptions`
- فیلدها: `only_project_filter.type`
- زیرقالب‌ها: `tasks/partial-inbox-sort-selection` `tasks/partial-tasks-viewer` `tasks/partial_inbox_viewer_header` `tasks/project-files-viewer`
- کنترلرها: `AppProjectFilesController` `AppTasksInboxController`
- endpointهای این کنترلرها: `projects.getProjectFiles` `projects.getProjectTaskFileIds` `tasks.print`

### `ws.tasks.label`

- آدرس: `#/label/:label`
- قالب: `tasks/label-viewer`
- متن‌ها: مشاهده مشخصات
- عمل‌ها: `$mdMenu.open` `editLabelInfo`
- زیرقالب‌ها: `tasks/partial-tasks-viewer` `tasks/partial_inbox_viewer_header`
- کنترلرها: `AppTasksInboxController`
- endpointهای این کنترلرها: `tasks.print`

### `ws.tasks.outbox`

- آدرس: `#/outbox`
- قالب: `tasks/outbox-viewer`
- متن‌ها: —
- عمل‌ها: —
- زیرقالب‌ها: `tasks/partial-tasks-viewer` `tasks/partial_inbox_viewer_header`
- کنترلرها: `AppTasksInboxController`
- endpointهای این کنترلرها: `tasks.print`

### `ws.tasks.done`

- آدرس: `#/done`
- قالب: `tasks/done-viewer`
- متن‌ها: انتخاب، انصراف، ایجاد کننده، بیشتر...، در حال بارگذاری، فیلتر، فیلتر نمایش، فیلتر نمایش وظایف، مسؤول انجام، نامشخص، وظیفه‌ای در این بخش وجود ندارد، پروژه (دسته‌بندی)، چاپ نتایج، کارهای انجام شده بر اساس زمان
- عمل‌ها: `doFilter` `filterDoneClearAssignee` `filterDoneClearOwner` `filterDoneClearProject` `filterDoneSelectAssignee` `filterDoneSelectOwner` `filterDoneSelectProject` `loadMore` `printDoneResult` `showTask` `toggleFilterDoneOptions`
- کنترلرها: `AppTasksDoneController`
- endpointهای این کنترلرها: `tasks.print`

## کارتابل نامه‌ها

### `ws.inbox`

- آدرس: `#/inbox`
- قالب: `inbox/inbox`
- متن‌ها: ایجاد نامه، در حال بارگذاری، فیلتر نمایش نامه‌ها
- عمل‌ها: `compose` `toggleFilterOptions`
- زیرقالب‌ها: `inbox/inbox-message-viewer` `inbox/inbox-viewer`
- کنترلرها: `AppInboxController`
- endpointهای این کنترلرها: `inbox.deleteMessage` `inbox.getMessageDialogs`

### `ws.inbox.label`

- آدرس: `#/inbox/label/:label`
- قالب: `inbox/inbox`
- پارامترها: `label`
- متن‌ها: ایجاد نامه، در حال بارگذاری، فیلتر نمایش نامه‌ها
- عمل‌ها: `compose` `toggleFilterOptions`
- زیرقالب‌ها: `inbox/inbox-message-viewer` `inbox/inbox-viewer`
- کنترلرها: `AppInboxController`
- endpointهای این کنترلرها: `inbox.deleteMessage` `inbox.getMessageDialogs`

### `ws.inbox.thread`

- آدرس: `#/inbox/:thread/:message`
- قالب: `inbox/inbox`
- پارامترها: `thread`
- متن‌ها: ایجاد نامه، در حال بارگذاری، فیلتر نمایش نامه‌ها
- عمل‌ها: `compose` `toggleFilterOptions`
- زیرقالب‌ها: `inbox/inbox-message-viewer` `inbox/inbox-viewer`
- کنترلرها: `AppInboxController`
- endpointهای این کنترلرها: `inbox.deleteMessage` `inbox.getMessageDialogs`

## یادداشت‌ها

### `ws.notes` (انتزاعی)

- آدرس: `#/notes`
- قالب: `notes/notes`
- متن‌ها: —
- عمل‌ها: —

### `ws.notes.view`

- آدرس: `#/view`
- قالب: `notes/view_all`
- متن‌ها: در حال بارگذاری
- عمل‌ها: —
- فیلدها: `filter.str`
- زیرقالب‌ها: `notes/notes-input` `notes/notes-sheet`
- کنترلرها: `AppNotesController`
- endpointهای این کنترلرها: `notes.setLabels`

### `ws.notes.label`

- آدرس: `#/label/:label`
- قالب: `notes/label-viewer`
- متن‌ها: مشاهده مشخصات
- عمل‌ها: `$mdMenu.open` `editLabelInfo`
- زیرقالب‌ها: `notes/notes-input` `notes/notes-sheet`
- کنترلرها: `AppNotesController`
- endpointهای این کنترلرها: `notes.setLabels`

### `ws.notes.deleted`

- آدرس: `#/trash`
- قالب: `notes/view_no_input`
- متن‌ها: توجه! یادداشت‌های حذف شده پس از ۳۰ روز به صورت کامل حذف خواهند شد.، یادداشت آرشیو شده‌ای ندارید.، یادداشت حذف شده‌ای ندارید.
- عمل‌ها: —
- زیرقالب‌ها: `notes/notes-sheet`
- کنترلرها: `AppNotesController`
- endpointهای این کنترلرها: `notes.setLabels`

### `ws.notes.archived`

- آدرس: `#/archived`
- قالب: `notes/view_no_input`
- متن‌ها: توجه! یادداشت‌های حذف شده پس از ۳۰ روز به صورت کامل حذف خواهند شد.، یادداشت آرشیو شده‌ای ندارید.، یادداشت حذف شده‌ای ندارید.
- عمل‌ها: —
- زیرقالب‌ها: `notes/notes-sheet`
- کنترلرها: `AppNotesController`
- endpointهای این کنترلرها: `notes.setLabels`

## CRM: مشتریان، معاملات، پرداخت‌ها

### `ws.customer` (انتزاعی)

- آدرس: `#/cu`
- قالب: `crm/crm`
- متن‌ها: در حال بارگذاری، هنوز پیغامی وجود ندارد ...
- عمل‌ها: `gotoRepliedBaseMessage`
- زیرقالب‌ها: `chat/chat-input` `chat/chat-pinned-message-viewer` `chat/chat-viewer` `crm/chat-header-crm` `crm/crm-customers-list` `crm/customer-pane` `sales/monitoring-deals` `sales/monitoring-payments`
- کنترلرها: `AppCustomerPaneController` `AppDealsMonitoringController` `AppImController` `AppImDialogsController` `AppPaymentsMonitoringAllController` `AppPaymentsMonitoringChartsController` `AppPaymentsMonitoringController` `AppPaymentsMonitoringDetailsController` `ChatViewCtrl` `CrmHeaderCtrl`
- endpointهای این کنترلرها: `chat.getDialogUnDoneTasksCount` `chat.setTyping` `chat.updateSentMessage` `projects.allSummary` `projects.chatSummary`

### `ws.customer.all`

- آدرس: `#/all`
- قالب: —

### `ws.customer.label`

- آدرس: `#/label/:label`
- قالب: —

### `ws.customer.dialog`

- آدرس: `#/dialog/:label/:dialog/:message`
- قالب: —
- پارامترها: `label`

### `ws.customer.deals`

- آدرس: `#/deals`
- قالب: —

### `ws.customer.payments`

- آدرس: `#/payments`
- قالب: —

### `ws.import_customers`

- آدرس: `#/import_customers`
- قالب: `crm/import_customers`
- متن‌ها: * پس از Import اطلاعات مشتریان، کاربران زیر دسترسی مشاهده به این پرونده‌ها را دارند:، افزودن، انتخاب، انتخاب فایل، انتقال اطلاعات، انتقال اطلاعات (Import) مشتریان به میزیتو، انتقال اطلاعات از اکسل، تعداد خطا:، تعیین برچسب‌ها:، توجه! در حالت دمو، فقط تعداد، دانلود فایل نمونه، دسترسی مشاهده، راهنما، ردیف، قابل انتقال می‌باشد.، مرحله قبل، مرحله ۱: انتخاب فایل، مرحله ۲: نمایش، مرحله ۳: تبدیل، مشاهده، هیچکدام، پرونده مشتریان با موفقیت ایجاد شدند.، ۵ رکورد اطلاعاتی
- عمل‌ها: `addMember` `cancel` `downloadSampleFile` `importCustomers` `removeMember` `selectLabel` `showCustomers` `showImportHelp` `uploadFile`
- فیلدها: `fieldIndexes[$index]`
- کنترلرها: `AppImportCustomersController`
- endpointهای این کنترلرها: `customer.import` `customer.importPrepare`

## مانیتورینگ و گزارش‌ها

### `ws.monitoring`

- آدرس: `#/monitoring`
- قالب: `monitoring/monitoring`
- متن‌ها: آخرین نامه ارسال شده توسط:، آخرین وظیفه انجام شده توسط:، آخرین وظیفه ایجاد شده توسط:، آخرین پرونده ایجاد شده توسط:، آخرین گفتگو توسط:، آخرین یادداشت ایجاد شده توسط:، اعضا:، تعداد کارهای انجام شده:، حذف:، دعوت:، زمان ایجاد میزِکار، زمان:، صورتجلسات سازمانی، فضای مصرف شده، فعال:، مالک میزِکار، مانیتورینگ، مانیتورینگ اعضا، مانیتورینگ میزِکار «، مانیتورینگ وظایف، مانیتورینگ پرونده مشتریان، مانیتورینگ پروژه‌ها، مهمان:، مورد، میزان انجام کارها در ۳۰ روز گذشته، نامه‌ها (۳۰ روز گذشته)، نامه‌ها در ۳۰ روز گذشته:، نفر، وظایف انجام شده (۱۲ ماه گذشته)، وظایف انجام شده در ۱۲ ماه گذشته:، … (+19)
- عمل‌ها: `showCustomersMonitoring` `showMonitorTasks` `showMonitoringMinutes` `showMonitoringUsers` `showNotesMonitoring` `showProjectsMonitoring` `showTasksDoneMonitoring`
- کنترلرها: `AppMonitoringController`
- endpointهای این کنترلرها: `monitor.chart.chatMessages` `monitor.chart.customers` `monitor.chart.getPast30DoneTasksPercents` `monitor.chart.inboxMessages` `monitor.chart.notes` `monitor.chart.tasksCreated` `monitor.chart.tasksDone` `monitor.workspace`

### `ws.monitoring_users`

- آدرس: `#/monitoring/users`
- قالب: `monitoring/monitoring_users`
- متن‌ها: اعضای میزِکار، مانیتورینگ اعضای میزِکار «، مشاهده مانیتورینگ، مشاهده مانیتورینگ کاربر
- عمل‌ها: `members_filter.filter=''` `showMonitorPage` `showMonitoringUser`
- فیلدها: `members_filter.filter`
- کنترلرها: `AppMonitoringUsersController`

### `ws.monitoring_user`

- آدرس: `#/monitoring/user/:uid`
- قالب: `monitoring/monitoring_user`
- متن‌ها: (کل وظایف بدون احتساب وظایف ایجاد شده توسط خود کاربر)، زمان آخرین نامه:، زمان آخرین وظیفه:، زمان آخرین پرونده:، زمان آخرین پیام:، زمان آخرین یادداشت:، سابقه آنلاین، مانیتورینگ پروژه‌های کاربر، مشاهده کارتابل وظایف، نامه‌ها (۳۰ روز گذشته)، نامه‌ها در ۳۰ روز گذشته:، وضعیت عملکرد کاربر، وظایف انجام شده توسط کاربر (۱۲ ماه گذشته)، وظایف انجام شده در ۱۲ ماه گذشته:، وظایف ایجاد شده توسط کاربر (۱۲ ماه گذشته)، وظایف ایجاد شده در ۱۲ ماه گذشته:، وظایف تعیین شده از طرف دیگران به کاربر (۱۲ ماه گذشته)، وظایف در ۱۲ ماه گذشته:، وظایف کاربر (۱۲ ماه گذشته)، وظایف کاربر در ۱۲ ماه گذشته:، پرونده‌های ایجاد شده (۱۲ ماه گذشته)، پرونده‌های ایجاد شده در ۱۲ ماه گذشته:، کل نامه‌ها:، کل وظایف انجام شده:، کل وظایف ایجاد شده:، کل وظایف کاربر:، کل پرونده‌های ایجاد شده توسط کاربر:، کل گفتگوها:، کل یادداشت‌های کاربر:، گفتگوها (۳۰ روز گذشته)، … (+3)
- عمل‌ها: `showMonitorUserProjects` `showMonitorUsersPage` `showUserAttendance` `showUserTasks`
- کنترلرها: `AppMonitoringUserController`
- endpointهای این کنترلرها: `monitor.chart.chatMessages` `monitor.chart.customers` `monitor.chart.inboxMessages` `monitor.chart.notes` `monitor.chart.tasksAssigned` `monitor.chart.tasksCreated` `monitor.chart.tasksDone` `monitor.user`

### `ws.monitoring_tasks`

- آدرس: `#/monitoring/tasks`
- قالب: `monitoring/monitoring_tasks`
- متن‌ها: انتخاب، انجام شده، انجام نشده، ایجاد کننده، بازه زمانی، برچسب‌ها، بیشتر...، در حال بارگذاری، شماره پیگیری فرم، فقط دارای تاخیر، فیلتر، لیست بورد، لیست وظایف خالی است، مانیتورینگ وظایف، متن، مسؤول انجام، نامشخص، همه وظایف، وضعیت انجام، وضعیت تاخیر، پرونده مشتری، پروژه \| دسته‌بندی، چاپ نتایج، گروه‌بندی پروژه‌ها
- عمل‌ها: `doFilter` `filter.date_range` `filter.dialog` `filter.labels=[]` `filter.project_labels=[]` `filterClearAssignee` `filterClearOwner` `filterClearProject` `filterClearProjectList` `filterSelectAssignee` `filterSelectDateRange` `filterSelectDialog` `filterSelectLabels` `filterSelectOwner` `filterSelectProject` `filterSelectProjectLabels` `filterSelectProjectList` `loadMore` `printResult` `showMonitorPage`
- فیلدها: `filter.done_status` `filter.form_request_tracking_code` `filter.overdue_status` `filter.title`
- زیرقالب‌ها: `tasks/partial-inbox-sort-selection`
- کنترلرها: `AppMonitoringTasksController`
- endpointهای این کنترلرها: `projects.getProjectsUserAdmin` `tasks.print`

### `ws.monitoring_customers`

- آدرس: `#/monitoring_customers`
- قالب: `monitoring/monitoring_customers`
- متن‌ها: - ایجاد:، «ایجادکننده:، انتخاب، ایجاد از تاریخ، ایجاد تا تاریخ، ایجاد شده توسط، تعداد کل:، جستجو، داشتن برچسب، عدم مشاهده، قابل مشاهده برای، نامشخص، نداشتن برچسب، چاپ نتایج، گزارش وضعیت پرونده مشتریان
- عمل‌ها: `clearFromDate` `clearToDate` `filter.labels=[]` `filter.labels_not=[]` `filterSelectCreatedBy` `filterSelectCreatedByRemove` `filterSelectHasAccess` `filterSelectHasAccessNot` `filterSelectHasAccessNotRemove` `filterSelectHasAccessRemove` `filterSelectLabels` `filterSelectLabelsNot` `load` `null` `printResult` `showMonitorPage`
- فیلدها: `filter.from_date` `filter.to_date`
- کنترلرها: `AppMonitoringCustomersController`
- endpointهای این کنترلرها: `monitor.customers`

### `ws.monitoring_minutes`

- آدرس: `#/monitoring_minutes`
- قالب: `monitoring/monitoring_minutes`
- متن‌ها: انتخاب، برچسب‌ها، دارای مصوبه انجام نشده، رئیس جلسه، عضو جلسه، فیلتر، لیست صورتجلسات خالی است.، مانیتورینگ صورتجلسات سازمانی، متن، ناظر اجرا، نامشخص، همه مصوبات انجام شده، وضعیت، پروژه \| دسته‌بندی، کارشناس جلسه
- عمل‌ها: `doFilter` `filter.labels=[]` `filterClearProject` `filterClearUser` `filterSelectLabels` `filterSelectProject` `filterSelectUser` `showMinute` `showMonitorPage`
- فیلدها: `filter.content` `filter.state`
- کنترلرها: `AppMonitoringMinutesController`
- endpointهای این کنترلرها: `monitor.minutes`

### `ws.monitoring_projects`

- آدرس: `#/monitoring/projects/:uid/:project_label`
- قالب: `monitoring/monitoring_projects`
- پارامترها: `uid`
- متن‌ها: * وظیفه دارای بیشترین تاخیر:، * کاربر دارای بیشترین تعداد وظیفه در کارتابل:، آرشیو شده، آرشیو نشده، انتخاب گروه‌بندی پروژه:، تعداد:، جهت مانیتورینگ باید در پروژه‌ها دسترسی مدیریت داشته باشید.، در این صفحه، وضعیت پروژه‌هایی که مدیر آن‌ها هستید نمایش داده می‌شود.، مانیتورینگ وظایف، مانیتورینگ پروژه‌ها، مانیتورینگ پروژه‌های کاربر، مرتب‌سازی پروژه‌ها:، مورد، نمایش تقویم وظایف، نمودار کارهای انجام شده در ۳۰ روز گذشته، همه پروژه‌ها، همه پروژه‌های میزکار، همه پروژه‌های کاربر، وضعیت آرشیو، وضعیت پیشرفت پروژه‌ها:، چاپ گزارش، کارهای انجام شده در ۳۰ روز گذشته، کاری انجام نشده است، گزارش شامل پروژه‌های:
- عمل‌ها: `$mdMenu.open` `print` `setSortType` `showCalendarPage` `showMonitorTasksPage` `showPrevPage` `showProjectDetails`
- فیلدها: `filter.archive_status` `filter.str` `selected_project_label.selected`
- کنترلرها: `AppMonitoringProjectsController`
- endpointهای این کنترلرها: `monitor.chart.getPast30DoneTasksPercents` `monitor.projectsSummary` `projects.getProjectsUserAdmin` `projects.monitor.chart.getPast30DoneTasksPercents` `projects.monitor.projectsSummary`

### `ws.monitoring_project`

- آدرس: `#/monitoring/project/:projectId`
- قالب: `monitoring/monitoring_project`
- متن‌ها: از برچسبی استفاده نشده است، انجام آخرین وظیفه:، انجام اولین وظیفه:، زمان ایجاد پروژه:، زمان یادآوری آخرین وظیفه:، مانیتورینگ پروژه، مورد، میزان استفاده از برچسب‌ها در پروژه، نمودار میزان استفاده از برچسب‌ها در پروژه، نمودار وظایف انجام شده توسط همکاران، وضعیت پیشرفت پروژه:، وظایف انجام شده توسط همکاران، چاپ گزارش
- عمل‌ها: `print` `showMonitorProjectsPage` `showProject`
- کنترلرها: `AppMonitoringProjectController`
- endpointهای این کنترلرها: `monitor.project` `projects.monitor.project`

### `ws.monitoring_user_tasks`

- آدرس: `#/monitoring/monitoring_user_tasks/:uid`
- قالب: `monitoring/monitoring_user_tasks`
- متن‌ها: —
- عمل‌ها: `showMonitorUsersPage`
- زیرقالب‌ها: `tasks/inbox-viewer`
- کنترلرها: `AppMonitoringUserTasksController` `AppTasksController` `AppTasksInboxController`
- endpointهای این کنترلرها: `tasks.print`

## جستجو و نشان‌شده‌ها

### `ws.search`

- آدرس: `#/search/:search_str`
- قالب: `search/search`
- پارامترها: `search_str`
- متن‌ها: در، نامه‌ها، نمایش نتایج بیشتر، وظایف، وظایف تکمیل شده، پرونده مشتریان، گفتگوها
- عمل‌ها: `chatShowMore` `customersShowMore` `inboxShowMore` `tasksCompletedShowMore` `tasksShowMore`
- کنترلرها: `AppSearchController`

### `ws.bookmarks`

- آدرس: `#/bookmarks`
- قالب: `search/search`
- متن‌ها: در، نامه‌ها، نمایش نتایج بیشتر، وظایف، وظایف تکمیل شده، پرونده مشتریان، گفتگوها
- عمل‌ها: `chatShowMore` `customersShowMore` `inboxShowMore` `tasksCompletedShowMore` `tasksShowMore`
- کنترلرها: `AppSearchController`

## تنظیمات میزکار

### `ws.settings`

- آدرس: `#/settings/:page`
- قالب: —
- پارامترها: `page`
- زیرصفحه‌ها (`:page`): `invite` (دعوت عضو جدید)، `members` (اعضا)، `perms` (مجوزها)، `plan` (طرح فعلی)، `plans` (خرید/ارتقای طرح)، `removed` (اعضای حذف‌شده)؛ به‌علاوه‌ی تب «عمومی» و «مالی» در خود قالب

### `ws.settings_mobile`

- آدرس: `#/settings/mobile/:page`
- قالب: `workspace/settings_mobile_pages`
- پارامترها: `page`
- متن‌ها: صفحه تنظیمات
- عمل‌ها: `backToSettingsMobile`
- زیرقالب‌ها: `workspace/setting_tabs/settings_tab_info` `workspace/setting_tabs/settings_tab_invite` `workspace/setting_tabs/settings_tab_members` `workspace/setting_tabs/settings_tab_permissions` `workspace/setting_tabs/settings_tab_plans` `workspace/setting_tabs/settings_tab_removed`
- کنترلرها: `AppWorkspaceSettingsController`
- endpointهای این کنترلرها: `payment.checkDiscountCode` `payment.requestTrial` `payment.uploadLastWaitingInvoicePayment` `workspace.changeRole` `workspace.delete` `workspace.reJoinMember` `workspace.removeMember` `workspace.setWorkspaceSettings` `workspace.updateDedicatedLogoPhoto` `workspace.updateTitle` `workspace.updateWorkspaceRoleName`

## جلسه‌ی تصویری

### `ws.meeting`

- آدرس: `#/meeting/:meetingId`
- قالب: `meeting/meeting-viewer`
- متن‌ها: اشتراک صفحه، اعضا، جزئیات جلسه، درخواست صحبت، گفتگو
- عمل‌ها: `endCall` `mobileToggleUserFullScreen` `shareScreen` `showMeetingChat` `showMeetingMembers` `showUserFullScreen` `showUserFullScreenOff` `toggleHandUp` `toggleMyAudio` `toggleMyVideo` `toggleShowDetailsFrame`
- زیرقالب‌ها: `meeting/partial/members`
- کنترلرها: `AppMeetingViewerController`
- endpointهای این کنترلرها: `meeting.endCall` `meeting.get`

## پشتیبانی

### `ws.support`

- آدرس: `#/support/:sid`
- قالب: `support/admin/support_admin`
- پارامترها: `sid`
- متن‌ها: «دمو»، آخرین بازخورد، آزاد کردن قفل، این گفتگو بدون ارسال پاسخ خاتمه می‌یابد، برای شروع مکالمه یک مخاطب را انتخاب کنید، تمدید قفل برای ۳ دقیقه، حس اخیر مشتری:، خاتمه گفتگو، در اختیار شما، در حال بارگذاری، سابقه بازخورد مشتری، طرح، طرح رایگان، علت‌های اخیر نارضایتی، قفل گفتگو، مالک میزکار، مثبت، مدیر میزکار، مشاهده میزکار، مشاهده کاربر، منفی، منقضی شده ·، مهمان، نرخ رضایت، نیازمند اصلاح، هنوز پیغامی وجود ندارد ...، پاسخ‌های شما:، پرونده باز، کپی نام کاربر
- عمل‌ها: `closeSupportDialogResponse` `copySupportUserName` `extendSupportDialogLock` `lockSupportDialog` `showMonitorPage` `showMonitorUserPage` `showUserPhone` `show_mobile_support_details=!show_mobile_support_details` `show_support_feedback_context=!show_support_feedback_context` `unlockSupportDialog` `unselectDialog`
- زیرقالب‌ها: `support/admin/support-chat-input` `support/admin/support-chat-viewer` `support/admin/support-dialog-list` `support/admin/support-feedback-monitor` `support/admin/support-search-content`
- کنترلرها: `AppAdminSupportChatController`
- endpointهای این کنترلرها: `support.getSupportInfo` `support.searchContent` `support.setTypingAdmin`

## چاپ

### `ws.print`

- آدرس: `#/print`
- قالب: `print/print-content`
- متن‌ها: —
- عمل‌ها: —

## ابزارهای اصلاح داده (مدیر)

### `ws.fix_customers`

- آدرس: `#/fix/customers`
- قالب: `workspace/fix/fix_customers`
- متن‌ها: (انتخاب شده: )، «آرشیو شده»، «ایجادکننده:، آرشیو شده، آرشیو نشده، اصلاح دسترسی پرونده مشتریان، افزودن، انتخاب، انتخاب همه، بازیابی از آرشیو، تعداد کل:، جستجو، حذف، داشتن برچسب، دسترسی از فرد، دسترسی به فرد، عدم مشاهده، فیلتر، قابل مشاهده برای، مشاهده اعضا، نامشخص، نداشتن برچسب، وضعیت
- عمل‌ها: `filter.labels=[]` `filter.labels_not=[]` `filterSelectHasAccess` `filterSelectHasAccessNot` `filterSelectHasAccessNotRemove` `filterSelectHasAccessRemove` `filterSelectLabels` `filterSelectLabelsNot` `grantAccessToUser` `load` `markAll` `null` `showMembers` `toggleSelect`
- فیلدها: `dialog_filter` `filter.archive_status`
- کنترلرها: `AppFixCustomersController`
- endpointهای این کنترلرها: `fix.customer.getAll` `fix.customer.getMembers` `fix.customer.grantAccess`

### `ws.fix_projects`

- آدرس: `#/fix/projects`
- قالب: `workspace/fix/fix_projects`
- متن‌ها: (انتخاب شده: )، «آرشیو شده»، «ایجادکننده:، آرشیو شده، آرشیو نشده، اصلاح دسترسی پروژه‌ها، افزودن، انتخاب، انتخاب همه، بازیابی ( ) وظایف آرشیو شده، بازیابی از آرشیو، تعداد کل:، جستجو، حذف، دسترسی از فرد، دسترسی به فرد، عدم مشاهده، فیلتر، قابل مشاهده برای، مشاهده اعضا، نامشخص، وضعیت، گروه‌بندی پروژه‌ها
- عمل‌ها: `filter.project_labels=[]` `filterSelectHasAccess` `filterSelectHasAccessNot` `filterSelectHasAccessNotRemove` `filterSelectHasAccessRemove` `filterSelectProjectLabels` `grantAccessToUser` `load` `markAll` `null` `restoreArchiveTasks` `showMembers` `toggleSelect`
- فیلدها: `dialog_filter` `filter.archive_status`
- کنترلرها: `AppFixProjectsController`
- endpointهای این کنترلرها: `fix.projects.getAll` `fix.projects.getMembers` `fix.projects.grantAccess` `projects.restoreArchivedTasks`

### `ws.fix_chat_groups`

- آدرس: `#/fix/chat_groups`
- قالب: `workspace/fix/fix_chat_groups`
- متن‌ها: (انتخاب شده: )، «آرشیو شده»، «ایجادکننده:، «کانال»، آرشیو شده، آرشیو نشده، اصلاح دسترسی گروه‌های گفتگو، افزودن، انتخاب همه، بازیابی از آرشیو، تعداد کل:، جستجو، حذف، دسترسی از فرد، دسترسی به فرد، عدم مشاهده، فیلتر، قابل مشاهده برای، مشاهده اعضا، نامشخص، وضعیت
- عمل‌ها: `filterSelectHasAccess` `filterSelectHasAccessNot` `filterSelectHasAccessNotRemove` `filterSelectHasAccessRemove` `grantAccessToUser` `load` `markAll` `null` `showMembers` `toggleSelect`
- فیلدها: `dialog_filter` `filter.archive_status`
- کنترلرها: `AppFixChatGroupsController`
- endpointهای این کنترلرها: `fix.chatGroups.getAll` `fix.chatGroups.getMembers` `fix.chatGroups.grantAccess`

