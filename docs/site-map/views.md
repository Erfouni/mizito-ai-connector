# قالب‌ها، مودال‌ها و پنل‌های میزیتو

همه‌ی 322 قالب HTML: آن‌هایی که از `https://office.mizito.ir/views/<نام>.html` بار می‌شوند، به‌علاوه‌ی قالب‌هایی
که داخل کد مبهم‌شده‌ی `a_.js` جاسازی شده‌اند و با `my-include` بار می‌شوند (منوی کناری، هدر، ورودی چت، کانبان، گانت، ...).
برای هر قالب: کجا استفاده می‌شود (صفحه، یا سرویس/کنترلر و تابعی که مودال را باز می‌کند)، متن‌ها، عمل‌ها، فیلدها،
کنترلرها و عناصر سفارشی.

## `(ریشه)/` (1)

### `workspace`

- منبع: views/ only
- استفاده: صفحه‌ی `ws`؛ `service:IdleManager / start / state`
- متن‌ها: «پرونده مشتری»، «پروژه»، «گفتگو»، اتصال به اینترنت برقرار نیست، جهت اشتراک‌گذاری فایل(ها) انتخاب کنید، و یا، یک
- عمل‌ها: `cancelAppShareContent`
- کنترلر: `AppNotificationHistoryController` `AppWorkspaceController`
- عناصر سفارشی: `ui-view`

## `attendance/` (1)

### `attendance/modal-attendance-history`

- منبع: views/ + embedded
- استفاده: `service:AppAttendanceManager / cancel / modal/panel`
- متن‌ها: اطلاعات قدیمی این بازه ممکن است کامل نباشد.، بازه نمایش، بازه‌های آنلاین این روز ( بازه)، بیشتر...، در حال بارگذاری، روز، روزهای آنلاین در این بازه، سابقه آنلاین قابل نمایش ثبت نشده است.، سابقه‌ای هنوز وجود ندارد، ساعت حضور، ساعت نمایش داده شده بر اساس زمان محلی سیستم است.، شروع، مجموع زمان آنلاین در این بازه، مدت، نمایش، نمایش روزهای قبل، نمایش زمان‌های آنلاین در میزکار، پایان، ۰۰، ۰۶، ۱۲، ۱۸، ۲۴
- عمل‌ها: `cancel` `day.times.length` `editRow` `loadMore` `removeRow`
- عناصر سفارشی: `md-table-container`

## `bookmark/` (1)

### `bookmark/partial-bookmark-toggle-icon-container`

- منبع: views/ + embedded
- استفاده: `directive:myBookmarkToggleContainer / getMultiOptionLabels / directive/other`
- متن‌ها: :'حذف از لیست نشان‌شده‌ها'}}، ? 'افزودن به لیست نشان‌شده‌ها'
- عمل‌ها: `callBack`
- راهنماها: {{!bookmarked ? 'افزودن به لیست نشان‌شده‌ها' :'حذف از لیست نشان‌شده‌ها'}}

## `chat/` (26)

### `chat/chat`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.im`؛ `service:IdleManager / start / state`
- متن‌ها: برای شروع مکالمه یک مخاطب را انتخاب کنید، در حال بارگذاری، هنوز پیغامی وجود ندارد ...
- عمل‌ها: `gotoRepliedBaseMessage`
- کنترلر: `AppImController` `AppImDialogsController` `ChatViewCtrl`
- زیرقالب: `chat/chat-dialog-list` `chat/chat-header` `chat/chat-input` `chat/chat-pinned-message-viewer` `chat/chat-viewer`

### `chat/chat-dialog-list`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/chat`
- متن‌ها: ارسال پیام شخصی، اعضا، ایجاد کانال، ایجاد گروه گفتگو، دعوت عضو جدید، فیلتر، همه، پیام شخصی، گروه جدید، گروه‌ها
- عمل‌ها: `$mdMenu.open` `dialog_filter=''` `inviteNewUser` `null` `setActiveFolder` `showSelectUserForNewChat` `showSelectUsersForNewGroupChat` `toggleShowDeletedUsers`
- فیلدها: `dialog_filter`
- راهنماها: {{'dialogs_filter' \| translate}}، اعضا، ایجاد کانال، ایجاد گروه گفتگو، همه، پیام شخصی، گروه‌ها
- زیرقالب: `chat/partial-dialog` `chat/partial-dialog-start`

### `chat/chat-header`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/chat`
- متن‌ها: جلسه آنلاین
- عمل‌ها: `callDialog` `showDialogsList`
- زیرقالب: `chat/partial-chat-dialog-header-filter-buttons` `chat/partial-chat-dialog-header-menu` `chat/partial-chat-header-back-callout`

### `chat/chat-input`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/chat`؛ داخل قالب `crm/crm`؛ داخل قالب `projects/projects`
- متن‌ها: + صورتجلسه، + وظیفه، ارسال، انصراف، ثبت گزارش تماس با مشتری، حذف پیام صوتی، در حال نمایش محتوای فیلتر شده ...، در حال ویرایش پیام، ذخیره، ذخیره تغییرات، راهنمای دستورات، شکلک، صورتجلسه، صورتجلسه ساده، صورتجلسه سازمانی، فایل، لغو، منشن پیام برای ...، منشن:، نظرسنجی، وظیفه، پیام خود را بگذارید...، پیام صوتی، گزارش تماس
- عمل‌ها: `$mdMenu.open` `addCallLog` `addFile` `addMinutes` `addPolling` `addTask` `cancelEditMessage` `cancelFilter` `cancelVoiceRecorder` `clearReply` `gotoMessage` `removeMention` `sendDraftMessage` `showEmojiPicker` `showMentionSelector` `showRobotHelp` `startVoiceRecord`
- فیلدها: `draftMessage.message`
- راهنماها: {{editing.active ? 'ویرایش پیام...' : ('write_your_msg' \| translate)}}، ارسال، ثبت گزارش تماس با مشتری، حذف پیام صوتی، ذخیره تغییرات، راهنمای دستورات، شکلک، صورتجلسه، فایل، منشن پیام برای ...، نظرسنجی، وظیفه، پیام صوتی

### `chat/chat-pinned-message-viewer`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/chat`؛ داخل قالب `crm/crm`؛ داخل قالب `projects/projects`
- متن‌ها: حذف پیام سنجاق شده
- عمل‌ها: `gotoMessage` `removePin`
- راهنماها: حذف پیام سنجاق شده

### `chat/chat-viewer`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/chat`؛ داخل قالب `crm/crm`؛ داخل قالب `projects/projects`
- متن‌ها: —

### `chat/modal-chat-message-details-info`

- منبع: views/ + embedded
- استفاده: `service:AppImManager / toggleBookmark / modal/panel`
- متن‌ها: ارسال شده توسط:، این پیام هنوز مشاهده نشده است.، تبدیل به مشاهده نشده، تبدیل پیام به وظیفه، تعریف الگوی نظرسنجی، جزئیات پیام، حذف الگوی نظرسنجی، حذف سنجاق پیام، حذف شده توسط:، حذف پیام، خوانده شده توسط:، زمان ارسال پیام، سنجاق پیام، نتایج نظرسنجی، ویرایش متن پیام، پایان نظرسنجی، پس گرفتن نظر، کپی متن پیام
- عمل‌ها: `convertMentionToUnProcessed` `convertToTask` `copyMessage` `removeMessage` `retractVote` `stopPolling` `togglePinMessage` `togglePollingTemplate` `updateMessage` `viewPollingResults`
- راهنماها: حذف سنجاق پیام، حذف پیام، سنجاق پیام، ویرایش متن پیام، کپی متن پیام

### `chat/modal-dashboard-all-teammates`

- منبع: views/ + embedded
- استفاده: `service:AppUsersManager / cancel / modal/panel`
- متن‌ها: بستن
- عمل‌ها: `cancel` `startChat`
- فیلدها: `user_filter`
- راهنماها: فیلتر ...

### `chat/modal-dialog-info`

- منبع: views/ + embedded
- استفاده: `service:AppChatsManager / showProjectAdvancedFeaturesModal / modal/panel`
- متن‌ها: ( نفر)، : (chatFull.is_customer_entity ? 'آرشیو پرونده (حذف)' : 'حذف گروه')، ? 'حذف کانال'، آرشیو پروژه، از اینجا می‌توانید اولین جریان‌کار را بسازید.، از اینجا می‌توانید اولین قانون، دکمه یا پارامتر سفارشی را بسازید.، اعضای گروه، افزودن اعضا، به-->، تبدیل به عادی، تعیین شده است.، تغییر تصویر، تغییر دهد و به تنظیمات پروژه پیشرفته نیز دسترسی دارد.، تغییر رنگ پروژه، تنظیمات، تنظیمات پروژه پیشرفته، جریان‌کارها:، حالت جریان‌کار، حالت کلاسیک، حذف تصویر، حذف مدیریت گروه، حذف کاربر از گروه، خودکارسازی پروژه، دسترسی کامل به مدیریت اعضا، ویرایش عنوان و تصویر گروه دارد و می‌تواند وضعیت پروژه را بین حالت، دکمه‌های خودکار:، … (+27)
- عمل‌ها: `archiveProject` `cancelEditMode` `changePhoto` `chatFull.settings.not_mute` `close` `convertToNotPublicGroup` `deleteGroup` `deleteUser` `inviteUser` `removePhoto` `setAdminUser` `setEditMode` `setProjectColor` `setProjectLabel` `showProjectAdvancedFeaturesModal` `showProjectAutomationsModal` `toggleProjectAdvancedFeatures` `updateTitle`
- فیلدها: `chatFull.project.is_advanced` `chatFull.settings.not_mute` `newTitle.title`
- راهنماها: عنوان جدید گروه یا پروژه...، تغییر رنگ پروژه، حذف کاربر از گروه

### `chat/modal-filter-robot-mention-type`

- منبع: views/ + embedded
- استفاده: `service:AppImManager / select / modal/panel`
- متن‌ها: منشن‌های مشاهده نشده، کلیه منشن‌ها
- عمل‌ها: `select`

### `chat/modal-mark-dialogs-as-seen`

- منبع: views/ + embedded
- استفاده: `service:AppPeersManager / cancel / modal/panel`
- متن‌ها: انصراف، تبدیل به خوانده شده، تعداد :، توصیه:، پیشنهاد می‌شود پیام‌های دریافتی را در همان لحظه مشاهده کنید تا مدیریت کارها به بهترین شکل ممکن انجام شود.
- عمل‌ها: `cancel` `ok` `toggleSelect`
- زیرقالب: `crm/partial-dialog`

### `chat/modal-newchat-dialog-group`

- منبع: views/ + embedded
- استفاده: `service:AppPeersManager / createGroup / modal/panel`
- متن‌ها: انتخاب اعضا:، انتخاب تصویر نشانه، انتخاب رنگ نماد پروژه، انصراف، ایجاد پروژه، ایجاد کانال، ایجاد گروه، ایجاد گروه گفتگو، این کانال برای تمامی اعضای این میزِکار قابل مشاهده خواهد بود.، این گروه برای تمامی اعضای این میزِکار قابل مشاهده خواهد بود.، در صورت استفاده از پروژه، همکاران شما می‌توانند به صورت چابک و سریع با یکدیگر ارتباط داشته باشند. از امکانات تقویم و بورد استفاده کرده و برای همکاران وظایف ایجاد کنید و در صورت نیاز صورتجلسات خود را ثبت نمایید.، ضمناً به ازای ایجاد هر پروژه یک "دسته‌بندی" هم در قسمت وظایف به صورت خودکار ایجاد خواهد شد.، عنوان پروژه، عنوان کانال، عنوان گروه، قابل مشاهده برای تمامی اعضای میزکار، کاربران مهمان
- عمل‌ها: `cancel` `createGroup` `group.color=color` `setPhoto` `toggleUser`
- فیلدها: `group.is_public` `group.title` `user_filter`
- راهنماها: فیلتر ...

### `chat/modal-newchat-user`

- منبع: views/ + embedded
- استفاده: `service:AppPeersManager / cancel / modal/panel`
- متن‌ها: انتخاب اعضا:، انصراف، جهت ارسال پیام خصوصی، یک نفر را انتخاب کنید:، دعوت عضو جدید
- عمل‌ها: `cancel` `inviteNewUser` `startChat`
- فیلدها: `user_filter`
- راهنماها: فیلتر ...

### `chat/modal-update-message-text`

- منبع: views/ + embedded
- استفاده: `service:AppImManager / update / modal/panel`
- متن‌ها: انصراف، ویرایش متن پیام
- عمل‌ها: `cancel` `update`
- فیلدها: `newMessage`

### `chat/partial-chat-dialog-header-filter-buttons`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/chat-header`؛ داخل قالب `crm/chat-header-crm`؛ داخل قالب `projects/partial/chat-header-project`
- متن‌ها: برو به تاریخ، جستجو در متن پیام‌ها، فیلتر امضای صورتجلسات، فیلتر بر اساس کاربر، فیلتر تصاویر، فیلتر صورتجلسات، فیلتر فایل‌ها، فیلتر فیلم‌ها، فیلتر نظرسنجی، فیلتر وظایف، فیلتر پیام‌ها:، فیلتر پیام‌های صوتی، فیلتر گزارش تماس‌ها، منشن‌ها
- عمل‌ها: `doFilter` `gotoDate` `showRobotMentionFilter` `showSearchFilter` `showSenderFilter` `toggleShowMobileFilterButtons`
- راهنماها: برو به تاریخ، جستجو در متن پیام‌ها، فیلتر امضای صورتجلسات، فیلتر بر اساس کاربر، فیلتر تصاویر، فیلتر صورتجلسات، فیلتر فایل‌ها، فیلتر فیلم‌ها، فیلتر نظرسنجی، فیلتر وظایف، فیلتر پیام‌های صوتی، فیلتر گزارش تماس‌ها، منشن‌ها

### `chat/partial-chat-dialog-header-menu`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/chat-header`؛ داخل قالب `crm/chat-header-crm`؛ داخل قالب `projects/partial/chat-header-project`
- متن‌ها: اطلاعات پرونده، تنظیمات، حذف پین، فیلتر پیام‌ها، پین کردن پرونده، پین کردن پروژه، پین کردن گفتگو، کپی پروژه
- عمل‌ها: `$mdMenu.open` `duplicateProject` `showCustomerInfo` `showGroupInfo` `toggleSetPin` `toggleShowMobileFilterButtons` `toggleUnPin`
- راهنماها: تنظیمات

### `chat/partial-chat-header-back-callout`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/chat-header`؛ داخل قالب `crm/chat-header-crm`؛ داخل قالب `projects/partial/chat-header-project`
- متن‌ها: بازگشت به صفحه منشن‌ها، بستن
- عمل‌ها: `dismissGotoBackPageBox` `gotoDialogPageBackPage`
- راهنماها: بستن

### `chat/partial-dialog`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/chat-dialog-list`
- متن‌ها: —
- عمل‌ها: `dialogSelect`

### `chat/partial-dialog-start`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/chat-dialog-list`
- متن‌ها: —
- عمل‌ها: `startChat`

### `chat/partial-message`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / link / directive/other`
- متن‌ها: مشاهده پیغام، مشخصات، نفر دیده، پاسخ
- عمل‌ها: `gotoMessage` `gotoMessageLink` `null` `replyMessage` `showMessageDetails` `showTask` `startChat`
- راهنماها: مشاهده پیغام

### `chat/partial-message-commands`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / openLink / directive/other`
- متن‌ها: —
- زیرقالب: `chat/partial-message-commands-command` `chat/partial-message-commands-link`

### `chat/partial-message-commands-command`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/partial-message-commands`
- متن‌ها: —
- عمل‌ها: `sendCommand`

### `chat/partial-message-commands-link`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/partial-message-commands`
- متن‌ها: —
- عمل‌ها: `openLink`

### `chat/partial-message-media`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / openLink / directive/other`
- متن‌ها: —

### `chat/partial-reply-message`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / showTask / directive/other`
- متن‌ها: در حال بارگذاری

### `chat/partial-short-message`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / showTask / directive/other`
- متن‌ها: تصویر، صورتجلسه، نظرسنجی، وظیفه، گزارش تماس

## `crm/` (11)

### `crm/chat-header-crm`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `crm/crm`
- متن‌ها: مشتری:
- عمل‌ها: `mobileShowCustomersList`
- کنترلر: `CrmHeaderCtrl`
- زیرقالب: `chat/partial-chat-dialog-header-filter-buttons` `chat/partial-chat-dialog-header-menu` `chat/partial-chat-header-back-callout`

### `crm/crm`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.customer`؛ `service:IdleManager / start / state`
- متن‌ها: در حال بارگذاری، هنوز پیغامی وجود ندارد ...
- عمل‌ها: `gotoRepliedBaseMessage`
- کنترلر: `AppImController` `ChatViewCtrl`
- زیرقالب: `chat/chat-input` `chat/chat-pinned-message-viewer` `chat/chat-viewer` `crm/chat-header-crm` `crm/crm-customers-list` `crm/customer-pane` `sales/monitoring-deals` `sales/monitoring-payments`

### `crm/crm-customers-list`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `crm/crm`
- متن‌ها: انتقال اطلاعات (Import) مشتریان به میزیتو، تبدیل وضعیت پرونده‌ها به خوانده شده، ثبت اطلاعات مشتری جدید، فیلتر، فیلتر نمایش، چاپ اطلاعات پرونده مشتریان
- عمل‌ها: `$mdMenu.open` `createCustomer` `dialog_filter=''` `importCustomersFromFile` `markAllAsSeen` `null` `printResult` `toggleFilterOptions`
- فیلدها: `dialog_filter`
- راهنماها: تبدیل وضعیت پرونده‌ها به خوانده شده
- کنترلر: `AppImDialogsController`
- زیرقالب: `crm/partial-customers-filter` `crm/partial-dialog`

### `crm/customer-pane`

- منبع: views/ + embedded
- استفاده: `service:AppCustomersManager / close / modal/panel`؛ داخل قالب `crm/crm`
- متن‌ها: آدرس، آدرس ایمیل، آدرس سایت، اطلاعات نمایندگان، برچسب‌ها: +، سمت، شماره تماس، شماره همراه، قابل مشاهده برای:، مشاهده نامه‌ها، نام نماینده، ویرایش اطلاعات
- عمل‌ها: `editCustomer` `showCustomerInboxMessages` `showCustomersList` `showLabelSelector` `startChat`
- راهنماها: —
- کنترلر: `AppCustomerPaneController`
- زیرقالب: `sales/customer-pane-sales`

### `crm/import_customers`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.import_customers`؛ `service:IdleManager / None / state`
- متن‌ها: * پس از Import اطلاعات مشتریان، کاربران زیر دسترسی مشاهده به این پرونده‌ها را دارند:، افزودن، انتخاب، انتخاب فایل، انتقال اطلاعات، انتقال اطلاعات (Import) مشتریان به میزیتو، انتقال اطلاعات از اکسل، تعداد خطا:، تعیین برچسب‌ها:، توجه! در حالت دمو، فقط تعداد، دانلود فایل نمونه، دسترسی مشاهده، راهنما، ردیف، قابل انتقال می‌باشد.، مرحله قبل، مرحله ۱: انتخاب فایل، مرحله ۲: نمایش، مرحله ۳: تبدیل، مشاهده، هیچکدام، پرونده مشتریان با موفقیت ایجاد شدند.، ۵ رکورد اطلاعاتی
- عمل‌ها: `addMember` `cancel` `downloadSampleFile` `importCustomers` `removeMember` `selectLabel` `showCustomers` `showImportHelp` `uploadFile`
- فیلدها: `fieldIndexes[$index]`
- کنترلر: `AppImportCustomersController`

### `crm/modal-call-log-new`

- منبع: views/ + embedded
- استفاده: `service:AppCallLogManager / cancel / modal/panel`
- متن‌ها: ارسال گزارش، انصراف، این فیلد الزامی است.، به‌روزرسانی، تاریخ، درج گزارش ...، ساعت، ساعت را صحیح وارد نمایید.، نوع تماس:، گزارش، گزارش تماس
- عمل‌ها: `cancel` `createLog`
- فیلدها: `log.date` `log.is_out_call` `log.notes` `log.time`
- راهنماها: {{'add_call_log_description_here' \| translate}}، {{'time' \| translate}}
- عناصر سفارشی: `md-persian-datepicker`

### `crm/modal-customer-inbox-messages`

- منبع: views/ + embedded
- استفاده: `controller:AppCustomerPaneController / cancel / modal/panel`
- متن‌ها: بازگشت، نامه‌های در کارتابل، نامه‌های صادره، نامه‌های مربوط به پرونده مشتری، نامه‌های وارده
- عمل‌ها: `cancel`

### `crm/modal-new-customer`

- منبع: views/ + embedded
- استفاده: `service:AppCustomersManager / createCustomer / modal/panel`
- متن‌ها: ( ) توسط:، آدرس، آدرس ایمیل، آدرس سایت، اطلاعات بیشتر، اطلاعات مشتری، اطلاعات نمایندگان، انصراف، ایجاد، این فیلد الزامی است.، بازیابی از سابقه، توضیحات، سابقه تغییرات اطلاعات مشتری، سمت، شماره تماس، شماره همراه، شناسه ملی، عنوان، فکس، قابل مشاهده برای، نام تجاری مشتری، نام مشتری، نام نماینده، کد اقتصادی، کد پستی
- عمل‌ها: `addMobile` `addPhone` `addRepresentative` `cancel` `createCustomer` `moreInfo` `removeMobile` `removePhone` `removeRepresentative` `selectHistory` `setPhoto` `showChangesHistory` `showRepresentatives`
- فیلدها: `customer.address` `customer.economic_code` `customer.email` `customer.fax` `customer.name` `customer.national_code` `customer.notes` `customer.postal_code` `customer.short_name` `customer.website` `members` `mobile.phone_number` `phone.label` `phone.phone_number` `user.email` `user.mobile` `user.name` `user.phone` `user.title`
- راهنماها: {{'phone_label' \| translate}}، {{'viewable_for' \| translate}}
- زیرقالب: `partial/partial-chip-user-selector` `partial/partial-chip-user-template`

### `crm/partial-customers-filter`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `crm/crm-customers-list`
- متن‌ها: انتخاب، انصراف، بستن حالت فیلتر، تعداد نتایج:، جستجو مشخصات، داشتن برچسب، فیلتر، فیلتر نمایش، نداشتن برچسب، پرونده)، چاپ نتایج
- عمل‌ها: `cancelFilterInfo` `doFilterInfo` `filterSelectLabels` `filterSelectLabelsClear` `filterSelectLabelsNot` `filterSelectLabelsNotClear` `printResult` `toggleFilterOptions`
- فیلدها: `filter.typed_search_info`
- راهنماها: بستن حالت فیلتر

### `crm/partial-dialog`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `chat/modal-mark-dialogs-as-seen`؛ داخل قالب `crm/crm-customers-list`
- متن‌ها: —
- عمل‌ها: `dialogSelect`

### `crm/workspace-submenu`

- منبع: views/ + embedded
- استفاده: —
- متن‌ها: برچسب‌ها، مانیتورینگ فروش، مانیتورینگ مالی، همه مشتریان، پرونده مشتریان
- عمل‌ها: `selectLabelToRoute` `showAllCustomers` `showDealsMonitoring` `showPaymentsMonitoring`

## `home/` (12)

### `home/home`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.home`؛ `service:IdleManager / start / state`
- متن‌ها: ... مشاهده همه ( )، «تنظیمات»، «مجوزها»، ارتقاء طرح، انصراف، ایجاد میزِکار جدید، ایجاد میزکار جدید، این میزکار دارای پلن پیشرفته می‌باشد، این نسخه از میزیتو بر روی سرور اختصاصی نصب شده است، بخیر، بخیر؛، برای استفاده از دیگر امکانات میزیتو، به بخش، به میزِکار، به میزیتو خوش اومدی؛، تأیید درخواست، دعوت شده‌اید، راهنما، سایر میزِکارها، سایر میزِکارهای شما:، شما توسط، شما میزِکار فعالی ندارید. لطفاً جهت ادامه، یک میزِکار جدید برای خود بسازید:، فضای میزِکار شما در حال تمام شدن است. لطفاً قبل از اتمام نسبت به ارتقاء طرح خود اقدام نمایید.، فعال‌سازی امکانات، مخفی شدن میزِکارها، مراجعه کنید.، … (+3)
- عمل‌ها: `acceptInvite` `activatePermissions` `cancelInvite` `createNewWorkspace` `profileSettings` `sendSupportRequest` `showAllOtherWorkspaces` `showHelp` `showOnlineStatusSelector` `showProfileSettings` `showSettingsPlansTab` `toggleCollapseWorkspaces`
- راهنماها: این میزکار دارای پلن پیشرفته می‌باشد، این نسخه از میزیتو بر روی سرور اختصاصی نصب شده است، مخفی شدن میزِکارها، نوتیفیکیشن‌های مرورگر را غیرفعال کرده‌اید
- کنترلر: `AppDashboardController`
- زیرقالب: `home/workspace-widget` `home/workspace-widget-active`

### `home/nowrouz_infos_modal`

- منبع: views/ + embedded
- استفاده: `service:AppNowrouzManager / downloadStory / modal/panel`
- متن‌ها: اشتراک‌گذاری، در حال دانلود تصویر...
- عمل‌ها: `close` `downloadStory` `next` `pause` `play` `prev`

### `home/partial/partial_max_delay_task`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `home/workspace-widget-active`
- متن‌ها: * وظیفه دارای بیشترین تاخیر:، * کاربر دارای بیشترین تعداد وظیفه در کارتابل:، تبریک! در حال حاضر وظیفه دارای تاخیر ندارید.، تعداد:، طبق برنامه پیش می‌ره!، همه، کارهای تیم

### `home/project_summary_details`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / getRepeatSummary / directive/other`
- متن‌ها: «تعداد کارهای باقیمانده:، آخرین وظیفه انجام شده:، انجام شده:، انجام شده: % درصد، باقیمانده:، باقیمانده: % درصد، بدون زمان:، دارای تاخیر:، دارای تاخیر: % درصد، دارای زمان:، دارای پیشرفت:، دارای پیشرفت: % درصد، پروژه:، کارهای انجام شده: مورد، کارهای بدون زمان: مورد، کارهای دارای تاخیر: مورد، کارهای دارای زمان: مورد
- عمل‌ها: `showProject`
- راهنماها: انجام شده: %{{status_done_percent \| persian_digits_with_zero}} درصد، باقیمانده: %{{status_remain_percent \| persian_digits_with_zero}} درصد، دارای تاخیر: %{{status_overdue_percent \| persian_digits_with_zero}} درصد، دارای پیشرفت: %{{status_partial_completed_percent \| persian_digits_with_zero}} درصد، کارهای انجام شده: {{status_done \| persian_digits_with_zero}} مورد، کارهای بدون زمان: {{status_no_time \| persian_digits_with_zero}} مورد، کارهای دارای تاخیر: {{status_overdue \| persian_digits_with_zero}} مورد، کارهای دارای زمان: {{status_with_time \| persian_digits_with_zero}} مورد

### `home/report-widget-item`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `home/workspace-widget-active`
- متن‌ها: —
- عمل‌ها: `toggleReportValueVisibility`
- راهنماها: {{user_options.hide_dashboard_late_income_value ? 'نمایش مبلغ' : 'مخفی کردن مبلغ'}}

### `home/whats_new_modal`

- منبع: views/ + embedded
- استفاده: `factory:services / isAdvanced / modal/panel`
- متن‌ها: آخرین تغییرات، تغییری برای نمایش وجود ندارد.، جدید، در حال بارگذاری...، مشاهده ویدیوی آپدیت جدید، پلن پیشرفته
- عمل‌ها: `close` `showNewFeatureHelp`

### `home/widget_parts/my_projects`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: —
- عمل‌ها: `showProject`

### `home/widget_parts/my_tasks`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: ( مورد)، مشاهده همه، کارهای من، کاری برای انجام ندارید
- عمل‌ها: `showAllMyTasks`

### `home/widget_parts/tracking_tasks`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: مشاهده همه، کاری برای پیگیری ندارید
- عمل‌ها: `showAllTrackingItems`

### `home/workspace-submenu`

- منبع: views/ + embedded
- استفاده: —
- متن‌ها: فضای استفاده شده

### `home/workspace-widget`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `home/home`
- متن‌ها: —
- عمل‌ها: `switchWorkspace`

### `home/workspace-widget-active`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `home/home`
- متن‌ها: بزن بریم!، بیا ببین تا حالا چه مسیر شگفت‌انگیزی رو توی میزیتو طی کردی!، سال نو مبارک!، شما عضو مهمان این میزِکار هستید، نامه‌ها، نامه‌های جدید، همکاران من:، وضعیت پیشرفت پروژه‌ها:، وظایف امروز، وظایف بدون زمان، وظایف دارای تاخیر، وظایف دارای زمان، وظایف شما، پرونده مشتریان، پروژه‌ها، پیام‌های جدید، گفتگو
- عمل‌ها: `inviteNewUser` `reportWidgetClicked` `showAllTeammates` `showChats` `showCrm` `showInbox` `showNowrouzInfos` `showProject` `showProjects` `showTasks` `startChat`
- راهنماها: —
- زیرقالب: `home/partial/partial_max_delay_task` `home/report-widget-item` `meeting/partial/workspace-meeting-pending-dashboard`

## `inbox/` (11)

### `inbox/inbox`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.inbox`؛ صفحه‌ی `ws.inbox.label`؛ صفحه‌ی `ws.inbox.thread`؛ `service:IdleManager / start / state`
- متن‌ها: ایجاد نامه، در حال بارگذاری، فیلتر نمایش نامه‌ها
- عمل‌ها: `compose` `toggleFilterOptions`
- کنترلر: `AppInboxController`
- زیرقالب: `inbox/inbox-message-viewer` `inbox/inbox-viewer`

### `inbox/inbox-message-viewer`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `inbox/inbox`
- متن‌ها: آرشیو نامه، اتصال نامه به پرونده مشتریان، ارجاع پیام به نفرات دیگر، بازگشت به کارتابل، برچسب‌ها: +، به، تاریخ ثبت:، تاریخ نامه:، تغییر اتصال پرونده مشتریان به:، تغییر برچسب به:، ثبت شماره نامه، حذف این پاراف، حذف کامل نامه، شماره نامه:، موضوع:، نوع نامه:، پاراف‌ها:، پاسخ، پاسخ به این پاراف، پرونده‌ها:، چاپ
- عمل‌ها: `$mdMenu.open` `archive` `attachCustomers` `deleteMessage` `forward` `printInboxMessage` `registerLetter` `reply` `showCustomer` `showInbox` `showLabelSelector` `showSeenDetails`
- راهنماها: اتصال نامه به پرونده مشتریان، چاپ

### `inbox/inbox-viewer`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `inbox/inbox`
- متن‌ها: بیشتر...، در حال بارگذاری
- عمل‌ها: `loadMoreInbox`
- زیرقالب: `inbox/partial-inbox-filter`

### `inbox/modal-compose`

- منبع: views/ + embedded
- استفاده: `service:AppInboxManager / send / modal/panel`
- متن‌ها: ارسال، افزودن فایل، افزودن وظیفه، انصراف، این فیلد الزامی است.، برچسب‌ها، به، متن، پیوست‌ها
- عمل‌ها: `$mdMenu.open` `addFile` `addReceiver` `addTask` `cancel` `removeAttachment` `send` `showLabelSelector`
- فیلدها: `message.content` `message.subject` `message.to`
- راهنماها: موضوع
- عناصر سفارشی: `ng-wig`
- زیرقالب: `partial/partial-chip-user-selector` `partial/partial-chip-user-template`

### `inbox/modal-inbox-message-seen-details`

- منبع: views/ + embedded
- استفاده: `service:AppInboxManager / showSeenDetails / modal/panel`
- متن‌ها: جزئیات پیام، خوانده شده توسط:، زمان ارسال پیام

### `inbox/modal-secretariat-register-letter`

- منبع: views/ + embedded
- استفاده: `service:AppSecretariatManager / cancel / modal/panel`
- متن‌ها: انصراف، تاریخ ثبت:، تاریخ نامه قبلی:، تاریخ نامه وارده:، تایید، ثبت شماره دبیرخانه، ثبت شماره نامه، شماره ثبت شده قبلی:، شماره نامه قبلی:، شماره نامه وارده:، شماره پیشنهادی برای این نامه:، نامه صادره، نامه وارده
- عمل‌ها: `cancel` `ok` `setCustomNumber` `showCustomNumber`
- فیلدها: `letter.custom_number` `letter.inbox_message_in_date` `letter.inbox_message_in_number` `letter.next_sec_postfix` `letter.next_sec_prefix` `letter.sec_register_date` `letter.type`
- راهنماها: شماره نامه، پسوند، پیشوند
- عناصر سفارشی: `md-persian-datepicker`

### `inbox/partial-inbox-filter`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `inbox/inbox-viewer`
- متن‌ها: انتخاب، انصراف، با پیوست، بازه زمانی، بدون پیوست، برچسب، تاریخ نامه از، تاریخ نامه تا، خوانده شده، خوانده نشده، دریافت کننده، شماره نامه، فرستنده، فیلتر، فیلتر نمایش نامه‌ها، متن، نامشخص، نامه صادره، نامه وارده، نوع نامه، وضعیت خوانده شده، پرونده مشتری، پیوست
- عمل‌ها: `doFilter` `filter.date_range` `filter.dialog` `filter.labels=[]` `filterClearFrom` `filterClearTo` `filterSelectDateRange` `filterSelectDialog` `filterSelectFrom` `filterSelectLabels` `filterSelectTo` `toggleFilterOptions`
- فیلدها: `filter.has_attach_status` `filter.read_unread_status` `filter.search_str` `filter.secretariat_letter_type` `filter.secretariat_register_from` `filter.secretariat_register_to` `filter.secretariat_sec_num`

### `inbox/partial-inbox-row`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / showTask / directive/other`
- متن‌ها: - \| صادره، - \| وارده، جدید
- عمل‌ها: `showInboxMessage`

### `inbox/partial-message-reply-viewer`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / None / directive/other`
- متن‌ها: —
- عمل‌ها: `gotoMessage`

### `inbox/toast_sent_message`

- منبع: views/ + embedded
- استفاده: `service:AppInboxManager / show / modal/panel`
- متن‌ها: مشاهده
- عمل‌ها: `show`
- عناصر سفارشی: `md-toast`

### `inbox/workspace-submenu`

- منبع: views/ + embedded
- استفاده: —
- متن‌ها: برچسب‌ها، صندوق خروجی، صندوق ورودی، نامه‌های ثبتی صادره، نامه‌های ثبتی وارده، ورودی آرشیو شده، پاراف‌های من، کارتابل
- عمل‌ها: `selectLabelToRoute` `setMode` `setOutboxMode`

## `login/` (13)

### `login/forgot`

- منبع: views/ only
- استفاده: صفحه‌ی `login.forgot`؛ `service:IdleManager / start / state`
- متن‌ها: انصراف، درخواست کد ریست، شماره همراه خود را وارد نمایید، شماره همراه خود را وارد کنید، تا کد ریست برای شما ارسال شود.، فراموشی کلمه عبور
- عمل‌ها: `cancelSendResetCodeRequest` `sendResetCodeRequest`
- فیلدها: `forgot_username.username`
- راهنماها: {{'enter_your_phone_number' \| translate}}

### `login/forgot_reset`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `login.forgot_reset`؛ `service:IdleManager / start / state`
- متن‌ها: انتخاب کلمه عبور، به‌روزرسانی کلمه عبور، تکرار کلمه عبور، درخواست مجدد، کد ریست، کد ریست ارسال شده را در کادر زیر وارد نمایید:
- عمل‌ها: `cancelResetPassword` `resetPassword`
- فیلدها: `reset_password.password` `reset_password.repassword` `reset_password.reset_code`
- کنترلر: `AppLoginRegisterController`
- زیرقالب: `login/partial/partial-password-complexity-hint`

### `login/login`

- منبع: views/ only
- استفاده: صفحه‌ی `login.login`؛ `service:IdleManager / start / state`
- متن‌ها: ثبت‌نام، حساب کاربری ندارید؟، شماره همراه خود را وارد نمایید، ورود، ورود بیومتریک، کلمه عبور، کلمه عبور را فراموش کرده‌ام
- عمل‌ها: `forgotPassword` `login` `loginBiometric` `showRegisterForm` `showUserNameInput`
- فیلدها: `user.password` `user.username`

### `login/login_container`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `login`؛ `service:IdleManager / start / state`
- متن‌ها: دانلود اپلیکیشن، دانلود اپلیکیشن میزیتو
- کنترلر: `AppLoginController`
- عناصر سفارشی: `ui-view`

### `login/login_sso`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `login_sso`؛ `service:IdleManager / start / state`
- متن‌ها: —
- کنترلر: `AppLoginSSOController`

### `login/partial/partial-password-complexity-hint`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `login/forgot_reset`؛ داخل قالب `login/profile`؛ داخل قالب `login/reg_3`؛ داخل قالب `workspace/change_password`
- متن‌ها: دارای حداقل یک حرف بزرگ، دارای حداقل یک حرف کوچک، دارای حداقل یک عدد، دارای حداقل یک کاراکتر خاص، دارای حداقل ۱۰ کاراکتر

### `login/profile`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `login.profile`؛ `service:IdleManager / start / state`
- متن‌ها: «به میزیتو خوش آمدید»، انتخاب کلمه عبور، انصراف، تکرار کلمه عبور، شما برای اولین بار است که از میزیتو استفاده می‌کنید. برای شروع به کار، لطفاً اطلاعات خود را کامل نمایید.، قوانین و مقررات، موجود در سایت را می‌پذیرم.، نام، نام خانوادگی
- عمل‌ها: `cancelSendMyInfo` `sendMyInfo`
- فیلدها: `register.accept_terms` `register.firstname` `register.lastname` `register.password` `register.repassword`
- کنترلر: `AppLoginProfileController`
- زیرقالب: `login/partial/partial-password-complexity-hint`

### `login/reg_1`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `register.step1`؛ `service:IdleManager / start / state`
- متن‌ها: آدرس ایمیل خود را وارد نمایید، از طریق ایمیل، از طریق پیامک، با ثبت‌نام در میزیتو، شما با، ثبت‌نام، شرایط استفاده و قوانین حریم شخصی، شماره همراه خود را وارد نمایید، قبلاً ثبت‌نام کرده‌اید؟، ملحق شدن به، میزیتو، میزیتو موافقت کرده‌اید.، ورود
- عمل‌ها: `sendActivateCode` `showLoginForm`
- فیلدها: `register.activate_method` `register.email` `register.phone`
- راهنماها: {{'enter_your_email' \| translate}}، {{'enter_your_phone_number' \| translate}}

### `login/reg_2`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `register.step2`؛ `service:IdleManager / start / state`
- متن‌ها: بررسی کد فعال‌سازی، درخواست مجدد، کد فعال‌سازی، کد فعال‌سازی دریافت شده را در کادر زیر وارد کنید:
- عمل‌ها: `checkPinCode` `showActivateSelector`
- فیلدها: `register.pin_code`
- راهنماها: {{'enter_pin_code_2' \| translate}}

### `login/reg_3`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `register.step3`؛ `service:IdleManager / start / state`
- متن‌ها: * توجه داشته باشید برای ورودهای بعدی به میزیتو، باید در قسمت، انتخاب کلمه عبور، تنظیمات اولیه، تکرار کلمه عبور، را وارد نمایید.، عبارت، قوانین و مقررات، موجود در سایت را می‌پذیرم.، نام، نام خانوادگی، نام شرکت و یا تیم، نام کاربری، نام کاربری شما
- عمل‌ها: `sendMyInfo`
- فیلدها: `register.accept_terms` `register.firstname` `register.lastname` `register.password` `register.repassword` `register.username` `register.workspace_name`
- کنترلر: `AppRegisterCompleteController`
- زیرقالب: `login/partial/partial-password-complexity-hint`

### `login/reg_4`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `register.step4`؛ `service:IdleManager / start / state`
- متن‌ها: بعداً همکارانم را معرفی می‌کنم، جهت شروع، همکاران را به میزکار خود دعوت کنید:، دعوت همکاران به میزکار، شماره همراه، نام همکار، ورود به میزیتو
- عمل‌ها: `addTeammate` `createWorkspace` `removeTeammate`
- فیلدها: `user.email_phone` `user.name`

### `login/register_container`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `register`؛ `service:IdleManager / start / state`
- متن‌ها: به میزیتو خوش آمدید، در حال آماده‌سازی میزِکار شما...، سپاسگزاریم که میزیتو را انتخاب نمودید
- کنترلر: `AppRegisterController`
- عناصر سفارشی: `ui-view`

### `login/slider`

- منبع: views/ + embedded
- استفاده: `directive:myWorkspaceName / link / directive/other`
- متن‌ها: بورد پروژه و گانت چارت، ثبت اسناد مالی و فرصت‌های فروش، مانیتورینگ، چت و گفتگوی آنلاین
- عمل‌ها: `openSlide`

## `meeting/` (6)

### `meeting/meeting-starter`

- منبع: views/ + embedded
- استفاده: `service:AppMeetingManager / prepareCallDialog / modal/panel`
- متن‌ها: افزودن کاربر به جلسه، انتخاب همه، انصراف، تعداد انتخاب شده:، شروع تماس، مشارکت کنندگان در جلسه آنلاین را انتخاب کنید، نفر
- عمل‌ها: `addUser` `close` `createMeeting` `toggleMarkAll` `toggleSelected`

### `meeting/meeting-viewer`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.meeting`؛ `service:IdleManager / None / state`
- متن‌ها: اشتراک صفحه، اعضا، جزئیات جلسه، درخواست صحبت، گفتگو
- عمل‌ها: `endCall` `mobileToggleUserFullScreen` `shareScreen` `showMeetingChat` `showMeetingMembers` `showUserFullScreen` `showUserFullScreenOff` `toggleHandUp` `toggleMyAudio` `toggleMyVideo` `toggleShowDetailsFrame`
- کنترلر: `AppMeetingViewerController`
- زیرقالب: `meeting/partial/members`

### `meeting/modal-meeting-video-mic-status`

- منبع: views/ + embedded
- استفاده: `service:AppMeetingManager / cancel / modal/panel`
- متن‌ها: وضعیت دوربین و میکروفون شما، برای ورود به جلسه
- عمل‌ها: `constraints.audio` `constraints.video` `ok`

### `meeting/partial/members`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `meeting/meeting-viewer`
- متن‌ها: —

### `meeting/partial/workspace-meeting-pending`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: درخواست پیوستن به جلسه، رد تماس، پاسخ به تماس
- عمل‌ها: `meetingCallAccept` `meetingCallReject`
- راهنماها: رد تماس، پاسخ به تماس

### `meeting/partial/workspace-meeting-pending-dashboard`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `home/workspace-widget-active`
- متن‌ها: حذف، پیوستن به جلسه
- عمل‌ها: `dashboardMeetingCallRemove` `meetingCallAccept`

## `minute/` (10)

### `minute/modal-new-advanced-minute`

- منبع: views/ + embedded
- استفاده: `service:AppMinutesAdvancedManager / sendForSign / modal/panel`
- متن‌ها: ارسال جهت امضای صورتجلسه و مصوبات، استفاده از الگوی صورتجلسه سازمانی، الگوی صورتجلسه‌ی سازمانی، انصراف، بازگشت، تعریف به عنوان الگو، تنظیمات صورتجلسه، حذف حالت الگو، دعوت از اعضا، صورتجلسه، چاپ
- عمل‌ها: `$mdMenu.open` `cancel` `createMinute` `printMinute` `sendDraft` `sendForSign` `toggleTemplate` `useTemplate`
- راهنماها: تنظیمات صورتجلسه، چاپ

### `minute/modal-new-minute`

- منبع: views/ + embedded
- استفاده: `service:AppMinutesManager / removeTask / modal/panel`
- متن‌ها: ( ) توسط:، «ویرایش شده توسط:، استفاده از الگوی صورتجلسه، افزودن مصوبه، الگوی صورتجلسه، انصراف، ایجاد صورتجلسه، بستن، به‌روزرسانی، تاریخ، تعریف به عنوان الگو، تنظیمات صورتجلسه، حذف حالت الگو، در:، سابقه تغییرات متن صورتجلسه، ساعت، ساعت را صحیح وارد نمایید.، صورتجلسه، مشروح جلسه (اختیاری)، مصوبات، موضوع جلسه، مکان، وظایف، ویرایش صورتجلسه، پیوست، … (+1)
- عمل‌ها: `$mdMenu.open` `addFile` `addTask` `cancel` `createMinute` `editMinute` `printMinute` `removeAttachment` `removeTask` `selectHistory` `showChangesHistory` `toggleTemplate` `useTemplate`
- فیلدها: `minute.date` `minute.location` `minute.notes` `minute.subject` `minute.time`
- راهنماها: تنظیمات صورتجلسه، سابقه تغییرات متن صورتجلسه، چاپ
- عناصر سفارشی: `md-persian-datepicker`

### `minute/tabs/minute-attendance`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: حضور و غیاب
- فیلدها: `member.attendance` `member.attendance_comments`
- راهنماها: توضیحات...

### `minute/tabs/minute-comments`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: ثبت گزارش، حذف گزارش، در حال بارگذاری، متن گزارش، ویرایش گزارش، پیوست فایل به گزارش
- عمل‌ها: `addCommentAttachment` `deleteComment` `editComment` `removeCommentFile` `sendNewComment`
- فیلدها: `minute.newComment`
- راهنماها: درج گزارش و یا نظر شما ...، حذف گزارش، ویرایش گزارش، پیوست فایل به گزارش

### `minute/tabs/minute-info`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: امضا کنندگان، بدون امضا، برچسب‌ها:، تاریخ، دستور جلسه، ساعت، ساعت را صحیح وارد نمایید.، موضوع جلسه، مکان، یادآوری به اعضا چند ساعت قبل از زمان شروع جلسه باشد؟، یادآوری جلسه
- عمل‌ها: `showLabelSelector`
- فیلدها: `minute.date` `minute.has_reminder` `minute.location` `minute.notes_pre` `minute.reminder_hours_before` `minute.subject` `minute.time`

### `minute/tabs/minute-members`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: اعضای جلسه، اعضای جلسه *، انتخاب، حذف، دبیر جلسه:، رئیس جلسه:، سایر مدعوین، شماره همراه، ناظر اجرا:، نام و نام خانوادگی، کارشناس جلسه:
- عمل‌ها: `addMember` `addMembersOther` `changeMemberExecutive` `changeMemberExecutive2` `changeMemberObserver` `changeMemberOwner` `minute.member_executive2` `minute.member_observer` `removeMembersOther`
- فیلدها: `minute.member_users` `user.name` `user.phone`
- راهنماها: افزودن عضو...، حذف
- زیرقالب: `partial/partial-chip-user-selector` `partial/partial-chip-user-template`

### `minute/tabs/minute-note`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: متن صورتجلسه، مشروح جلسه
- فیلدها: `minute.notes`

### `minute/tabs/minute-sms`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: ارسال پیامک، ارسال پیامک به اعضا، امضای صورتجلسه، انتخاب الگوی پیام جهت ارسال، تغییر زمان جلسه، تغییر زمان و مکان جلسه، تغییر مکان جلسه، در حال بارگذاری، لغو جلسه، پیش نمایش متن:، یادآوری تکمیل وظایف مربوط به مصوبات
- عمل‌ها: `sendNewSms`
- فیلدها: `minute.newSmsTemplate`

### `minute/tabs/minute-tasks`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: افزودن مصوبه، مصوبات
- عمل‌ها: `addTask` `removeTask`

### `minute/template-selector`

- منبع: views/ + embedded
- استفاده: `service:AppMinutesAdvancedManager / showMinute / modal/panel`؛ `service:AppMinutesManager / showMinute / modal/panel`
- متن‌ها: فیلتر الگوی صورتجلسه
- عمل‌ها: `selectTemplate` `showMinute`
- فیلدها: `filter`
- راهنماها: {{'search_for_minute_templates' \| translate}}

## `monitoring/` (9)

### `monitoring/monitoring`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.monitoring`؛ `service:IdleManager / start / state`
- متن‌ها: آخرین نامه ارسال شده توسط:، آخرین وظیفه انجام شده توسط:، آخرین وظیفه ایجاد شده توسط:، آخرین پرونده ایجاد شده توسط:، آخرین گفتگو توسط:، آخرین یادداشت ایجاد شده توسط:، اعضا:، تعداد کارهای انجام شده:، حذف:، دعوت:، زمان ایجاد میزِکار، زمان:، صورتجلسات سازمانی، فضای مصرف شده، فعال:، مالک میزِکار، مانیتورینگ، مانیتورینگ اعضا، مانیتورینگ میزِکار «، مانیتورینگ وظایف، مانیتورینگ پرونده مشتریان، مانیتورینگ پروژه‌ها، مهمان:، مورد، میزان انجام کارها در ۳۰ روز گذشته، … (+24)
- عمل‌ها: `showCustomersMonitoring` `showMonitorTasks` `showMonitoringMinutes` `showMonitoringUsers` `showNotesMonitoring` `showProjectsMonitoring` `showTasksDoneMonitoring`
- کنترلر: `AppMonitoringController`

### `monitoring/monitoring_customers`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.monitoring_customers`؛ `service:IdleManager / start / state`
- متن‌ها: - ایجاد:، «ایجادکننده:، انتخاب، ایجاد از تاریخ، ایجاد تا تاریخ، ایجاد شده توسط، تعداد کل:، جستجو، داشتن برچسب، عدم مشاهده، قابل مشاهده برای، نامشخص، نداشتن برچسب، چاپ نتایج، گزارش وضعیت پرونده مشتریان
- عمل‌ها: `clearFromDate` `clearToDate` `filter.labels=[]` `filter.labels_not=[]` `filterSelectCreatedBy` `filterSelectCreatedByRemove` `filterSelectHasAccess` `filterSelectHasAccessNot` `filterSelectHasAccessNotRemove` `filterSelectHasAccessRemove` `filterSelectLabels` `filterSelectLabelsNot` `load` `null` `printResult` `showMonitorPage`
- فیلدها: `filter.from_date` `filter.to_date`
- کنترلر: `AppMonitoringCustomersController`
- عناصر سفارشی: `md-persian-datepicker`

### `monitoring/monitoring_minutes`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.monitoring_minutes`؛ `service:IdleManager / start / state`
- متن‌ها: انتخاب، برچسب‌ها، دارای مصوبه انجام نشده، رئیس جلسه، عضو جلسه، فیلتر، لیست صورتجلسات خالی است.، مانیتورینگ صورتجلسات سازمانی، متن، ناظر اجرا، نامشخص، همه مصوبات انجام شده، وضعیت، پروژه \| دسته‌بندی، کارشناس جلسه
- عمل‌ها: `doFilter` `filter.labels=[]` `filterClearProject` `filterClearUser` `filterSelectLabels` `filterSelectProject` `filterSelectUser` `showMinute` `showMonitorPage`
- فیلدها: `filter.content` `filter.state`
- کنترلر: `AppMonitoringMinutesController`

### `monitoring/monitoring_project`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.projects_monitoring_project`؛ صفحه‌ی `ws.monitoring_project`؛ `service:IdleManager / start / state`
- متن‌ها: از برچسبی استفاده نشده است، انجام آخرین وظیفه:، انجام اولین وظیفه:، زمان ایجاد پروژه:، زمان یادآوری آخرین وظیفه:، مانیتورینگ پروژه، مورد، میزان استفاده از برچسب‌ها در پروژه، نمودار میزان استفاده از برچسب‌ها در پروژه، نمودار وظایف انجام شده توسط همکاران، وضعیت پیشرفت پروژه:، وظایف انجام شده توسط همکاران، چاپ گزارش
- عمل‌ها: `print` `showMonitorProjectsPage` `showProject`
- راهنماها: چاپ گزارش
- کنترلر: `AppMonitoringProjectController`

### `monitoring/monitoring_projects`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.projects_monitor`؛ صفحه‌ی `ws.monitoring_projects`؛ `service:IdleManager / start / state`
- متن‌ها: * وظیفه دارای بیشترین تاخیر:، * کاربر دارای بیشترین تعداد وظیفه در کارتابل:، آرشیو شده، آرشیو نشده، انتخاب گروه‌بندی پروژه:، تعداد:، جهت مانیتورینگ باید در پروژه‌ها دسترسی مدیریت داشته باشید.، در این صفحه، وضعیت پروژه‌هایی که مدیر آن‌ها هستید نمایش داده می‌شود.، مانیتورینگ وظایف، مانیتورینگ پروژه‌ها، مانیتورینگ پروژه‌های کاربر، مرتب‌سازی پروژه‌ها:، مورد، نمایش تقویم وظایف، نمودار کارهای انجام شده در ۳۰ روز گذشته، همه پروژه‌ها، همه پروژه‌های میزکار، همه پروژه‌های کاربر، وضعیت آرشیو، وضعیت پیشرفت پروژه‌ها:، چاپ گزارش، کارهای انجام شده در ۳۰ روز گذشته، کاری انجام نشده است، گزارش شامل پروژه‌های:
- عمل‌ها: `$mdMenu.open` `print` `setSortType` `showCalendarPage` `showMonitorTasksPage` `showPrevPage` `showProjectDetails`
- فیلدها: `filter.archive_status` `filter.str` `selected_project_label.selected`
- راهنماها: فیلتر عنوان پروژه...، چاپ گزارش
- کنترلر: `AppMonitoringProjectsController`

### `monitoring/monitoring_tasks`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.projects_monitoring_tasks`؛ صفحه‌ی `ws.monitoring_tasks`؛ `service:IdleManager / start / state`
- متن‌ها: انتخاب، انجام شده، انجام نشده، ایجاد کننده، بازه زمانی، برچسب‌ها، بیشتر...، در حال بارگذاری، شماره پیگیری فرم، فقط دارای تاخیر، فیلتر، لیست بورد، لیست وظایف خالی است، مانیتورینگ وظایف، متن، مسؤول انجام، نامشخص، همه وظایف، وضعیت انجام، وضعیت تاخیر، پرونده مشتری، پروژه \| دسته‌بندی، چاپ نتایج، گروه‌بندی پروژه‌ها
- عمل‌ها: `doFilter` `filter.date_range` `filter.dialog` `filter.labels=[]` `filter.project_labels=[]` `filterClearAssignee` `filterClearOwner` `filterClearProject` `filterClearProjectList` `filterSelectAssignee` `filterSelectDateRange` `filterSelectDialog` `filterSelectLabels` `filterSelectOwner` `filterSelectProject` `filterSelectProjectLabels` `filterSelectProjectList` `loadMore` `printResult` `showMonitorPage`
- فیلدها: `filter.done_status` `filter.form_request_tracking_code` `filter.overdue_status` `filter.title`
- راهنماها: —
- کنترلر: `AppMonitoringTasksController`
- زیرقالب: `tasks/partial-inbox-sort-selection`

### `monitoring/monitoring_user`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.monitoring_user`؛ `service:IdleManager / start / state`
- متن‌ها: (کل وظایف بدون احتساب وظایف ایجاد شده توسط خود کاربر)، زمان آخرین نامه:، زمان آخرین وظیفه:، زمان آخرین پرونده:، زمان آخرین پیام:، زمان آخرین یادداشت:، سابقه آنلاین، مانیتورینگ پروژه‌های کاربر، مشاهده کارتابل وظایف، نامه‌ها (۳۰ روز گذشته)، نامه‌ها در ۳۰ روز گذشته:، وضعیت عملکرد کاربر، وظایف انجام شده توسط کاربر (۱۲ ماه گذشته)، وظایف انجام شده در ۱۲ ماه گذشته:، وظایف ایجاد شده توسط کاربر (۱۲ ماه گذشته)، وظایف ایجاد شده در ۱۲ ماه گذشته:، وظایف تعیین شده از طرف دیگران به کاربر (۱۲ ماه گذشته)، وظایف در ۱۲ ماه گذشته:، وظایف کاربر (۱۲ ماه گذشته)، وظایف کاربر در ۱۲ ماه گذشته:، پرونده‌های ایجاد شده (۱۲ ماه گذشته)، پرونده‌های ایجاد شده در ۱۲ ماه گذشته:، کل نامه‌ها:، کل وظایف انجام شده:، کل وظایف ایجاد شده:، … (+8)
- عمل‌ها: `showMonitorUserProjects` `showMonitorUsersPage` `showUserAttendance` `showUserTasks`
- راهنماها: (کل وظایف بدون احتساب وظایف ایجاد شده توسط خود کاربر)
- کنترلر: `AppMonitoringUserController`

### `monitoring/monitoring_user_tasks`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.monitoring_user_tasks`؛ `service:IdleManager / start / state`
- متن‌ها: —
- عمل‌ها: `showMonitorUsersPage`
- کنترلر: `AppMonitoringUserTasksController` `AppTasksController`
- زیرقالب: `tasks/inbox-viewer`

### `monitoring/monitoring_users`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.monitoring_users`؛ `service:IdleManager / start / state`
- متن‌ها: اعضای میزِکار، مانیتورینگ اعضای میزِکار «، مشاهده مانیتورینگ، مشاهده مانیتورینگ کاربر
- عمل‌ها: `members_filter.filter=''` `showMonitorPage` `showMonitoringUser`
- فیلدها: `members_filter.filter`
- راهنماها: فیلتر ... (نام کاربر، سِمت کاربر)
- کنترلر: `AppMonitoringUsersController`

## `notes/` (9)

### `notes/color-selector`

- منبع: views/ + embedded
- استفاده: `service:AppNotesManager / setNoteColor / modal/panel`
- متن‌ها: —
- عمل‌ها: `setNoteColor`

### `notes/label-viewer`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.notes.label`؛ `service:IdleManager / start / state`
- متن‌ها: مشاهده مشخصات
- عمل‌ها: `$mdMenu.open` `editLabelInfo`
- کنترلر: `AppNotesController`
- زیرقالب: `notes/notes-input` `notes/notes-sheet`

### `notes/note`

- منبع: views/ + embedded
- استفاده: `service:AppNotesManager / reset / directive/other`
- متن‌ها: روز قبل، آرشیو، انتخاب برچسب، بازیابی، تغییر رنگ، حذف، ویرایش، کپی محتوا
- عمل‌ها: `$parent.$parent.$parent.archiveNote` `$parent.$parent.$parent.copyNoteToClipboard` `$parent.$parent.$parent.deleteNote` `$parent.$parent.$parent.openPhoto` `$parent.$parent.$parent.showColorSelector` `$parent.$parent.$parent.showLabelSelector` `$parent.$parent.$parent.startEditNote` `$parent.$parent.$parent.togglePinNote` `$parent.$parent.$parent.unArchiveNote` `$parent.$parent.$parent.unDeleteNote`
- فیلدها: `item.checked`
- راهنماها: آرشیو، انتخاب برچسب، تغییر رنگ، حذف، ویرایش، کپی محتوا

### `notes/notes`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.notes`؛ `service:IdleManager / start / state`
- متن‌ها: —
- عناصر سفارشی: `ui-view`

### `notes/notes-input`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `notes/label-viewer`؛ داخل قالب `notes/view_all`
- متن‌ها: انتخاب تصویر، انصراف، عنوان یادداشت، چک لیست، یادداشت خود را بنویسید...، یادداشت خود را قرار دهید ...
- عمل‌ها: `addChecklistItem` `addNote` `closeEditNote` `new_note.checklist.splice` `removePhoto` `setNewNoteColor` `setPhoto` `showNoteEditMode` `toggleChecklistShow` `togglePinNote`
- فیلدها: `item.checked` `item.title` `new_checklist.title` `new_note.note` `new_note.title`
- راهنماها: عنوان چک لیست، عنوان چک لیست جدید، انتخاب تصویر، چک لیست

### `notes/notes-sheet`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `notes/label-viewer`؛ داخل قالب `notes/view_all`؛ داخل قالب `notes/view_no_input`
- متن‌ها: —

### `notes/view_all`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.notes.view`؛ `service:IdleManager / start / state`
- متن‌ها: در حال بارگذاری
- فیلدها: `filter.str`
- راهنماها: فیلتر...
- کنترلر: `AppNotesController`
- زیرقالب: `notes/notes-input` `notes/notes-sheet`

### `notes/view_no_input`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.notes.deleted`؛ صفحه‌ی `ws.notes.archived`؛ `service:IdleManager / start / state`
- متن‌ها: توجه! یادداشت‌های حذف شده پس از ۳۰ روز به صورت کامل حذف خواهند شد.، یادداشت آرشیو شده‌ای ندارید.، یادداشت حذف شده‌ای ندارید.
- کنترلر: `AppNotesController`
- زیرقالب: `notes/notes-sheet`

### `notes/workspace-submenu`

- منبع: views/ + embedded
- استفاده: —
- متن‌ها: آرشیو یادداشت‌ها، برچسب‌ها، همه یادداشت‌ها، یادداشت‌های حذف شده، یادداشت‌های من
- عمل‌ها: `selectLabelToRoute`

## `notification/` (2)

### `notification/notification_history`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: بستن نمایش سابقه نوتیفیکیشن‌ها، حذف تمام سابقه‌ها، سابقه نوتیفیکیشن‌ها، سابقه‌ای جهت نمایش وجود ندارد.
- عمل‌ها: `clear` `close` `showLogItem`
- راهنماها: بستن نمایش سابقه نوتیفیکیشن‌ها، حذف تمام سابقه‌ها
- زیرقالب: `notification/partial_notification_history_row_title`

### `notification/partial_notification_history_row_title`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `notification/notification_history`
- متن‌ها: —

## `partial/` (55)

### `partial/component-rating-field`

- منبع: views/ + embedded
- استفاده: `directive:myBookmarkToggleContainer / toggle / directive/other`
- متن‌ها: مقداری ندارد
- عمل‌ها: `nextRating` `setRating`
- فیلدها: `value`
- عناصر سفارشی: `md-slider-container`

### `partial/emoji-picker`

- منبع: views/ + embedded
- استفاده: `controller:ChatViewCtrl / showEmojiPicker / modal/panel`؛ `factory:services / showEmojiPicker / modal/panel`
- متن‌ها: —
- عناصر سفارشی: `emoji-picker`

### `partial/entity-audio`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / link / directive/other`
- متن‌ها: —
- عمل‌ها: `media.audio.downloadStarted?` `media.audio.isPlaying` `save` `shareDocument`
- فیلدها: `currentTime.val`

### `partial/entity-call-log`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / shareDocument / directive/other`
- متن‌ها: تماس خروجی، تماس ورودی، نوع تماس:
- راهنماها: نوع تماس: تماس خروجی، نوع تماس: تماس ورودی

### `partial/entity-document`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / link / directive/other`
- متن‌ها: حجم فایل:
- عمل‌ها: `shareDocument`

### `partial/entity-drag-drop`

- منبع: views/ + embedded
- استفاده: `service:AppDraggedFilesManager / addDropContainer / directive/other`
- متن‌ها: ارسال سریع‌تر (به همراه فشرده‌سازی تصاویر)، ارسال نسخه اصلی (بدون فشرده‌سازی تصاویر)، فایل‌ها را اینجا رها کنید

### `partial/entity-mention-in-chat`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / link / directive/other`
- متن‌ها: در، شما خود را در، شما را در، مشاهده پیام
- عمل‌ها: `showMessage`

### `partial/entity-mention-in-task`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / showMessage / directive/other`
- متن‌ها: این منشن مربوط به موردی بوده که حذف شده، حذف شده، در، در پروژه، شما خود را در گزارش، شما را در گزارش
- عمل‌ها: `showTask`

### `partial/entity-minute`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / link / directive/other`
- متن‌ها: «منتظر تأیید»، صورتجلسه، مصوبات، وظیفه تکرارشونده، وظیفه دارای پیوست، وظیفه دارای گزارش
- راهنماها: --> --> <!--، وظیفه تکرارشونده، وظیفه دارای پیوست، وظیفه دارای گزارش

### `partial/entity-minute-advanced`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / link / directive/other`
- متن‌ها: مصوبات جلسه:، اطلاعات جلسه:، اعضای جلسه:، دستور جلسه:، زمان جلسه، صورتجلسه، متن صورتجلسه:، مصوبات، مکان جلسه، وظیفه تکرارشونده، وظیفه دارای گزارش
- راهنماها: وظیفه تکرارشونده، وظیفه دارای گزارش

### `partial/entity-minute-sign`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / setVote / directive/other`
- متن‌ها: امضای صورتجلسه، در صورت تأیید، صورتجلسه را امضا بفرمایید:، صورتجلسه، مشاهده صورتجلسه
- عمل‌ها: `showMinute` `signMinute`

### `partial/entity-minute-sign-processed`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / signMinute / directive/other`
- متن‌ها: «پردازش شد»

### `partial/entity-minute-task-change`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: تغییر وضعیت وظیفه در صورتجلسه:، وظیفه دارای گزارش، وظیفه:
- راهنماها: وظیفه دارای گزارش

### `partial/entity-photo`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / link / directive/other`
- متن‌ها: —
- عمل‌ها: `shareDocument`

### `partial/entity-polling`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / link / directive/other`
- متن‌ها: از، بدون مشارکت، ثبت نظر، سؤال، سؤال بعدی، سؤال قبلی، مشارکت:، نتایج نهایی:
- عمل‌ها: `nextPage` `prevPage` `setVote`
- راهنماها: سؤال بعدی، سؤال قبلی

### `partial/entity-task`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / shareDocument / directive/other`
- متن‌ها: «منتظر تأیید»، حذف شده، حذف وظیفه از بورد، لغو تکرار، مهلت:، وظیفه دارای پیوست، وظیفه دارای گزارش
- عمل‌ها: `cancelTaskRepeat` `removeTaskFromBoard` `setTaskDone` `setTaskUnDone`
- راهنماها: حذف وظیفه از بورد، وظیفه دارای پیوست، وظیفه دارای گزارش

### `partial/entity-task-automation-message`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / showTask / directive/other`
- متن‌ها: در نتیجه فعالیت، روی :، پیام فوق به صورت خودکار برای شما ارسال شده است.
- عمل‌ها: `showTask`

### `partial/entity-task-reminder-owner`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / cancelTaskRepeat / directive/other`
- متن‌ها: —
- راهنماها: —

### `partial/entity-task-schedule`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / link / directive/other`
- متن‌ها: امروز، انجام شد، این کار رو امروز انجام می‌دم، این کار رو انجام دادم، این کار رو بعداً انجام می‌دم، بعداً، بی‌خیال، درآینده
- عمل‌ها: `backFromLaterSelector` `backFromTodaySelector` `cancelSnooze` `setSnoozeDate` `setSnoozeFuture` `setSnoozeLater` `setTaskDone` `showLaterSelector` `showTodaySelector`
- راهنماها: این کار رو امروز انجام می‌دم، این کار رو انجام دادم، این کار رو بعداً انجام می‌دم

### `partial/entity-task-schedule-processed`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / setSnoozeFuture / directive/other`
- متن‌ها: «پردازش شد»

### `partial/entity-video`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / shareDocument / directive/other`
- متن‌ها: —
- عمل‌ها: `shareDocument`

### `partial/header`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: ارتباط با پشتیبانی، امکانات پلن پیشرفته، انتخاب میزِکار و تنظیمات، اپلیکیشن iOS، اپلیکیشن اندروید، ایجاد میزِکار جدید، بستن، تا، تمدید / ارتقاء طرح، تنظیمات، تنظیمات حساب کاربری، تنظیمات شخصی، تنظیمات میزِکار، توقف نوتیفیکیشن‌ها، جدید، جستجو، جستجو ...، حالت روز، حالت شب، حالت نمایش، حالت نمایش و پس‌زمینه، حالت پیش‌فرض سیستم، خروج، خرید پلن، در حال حاضر پلن فعالی ندارید.، … (+16)
- عمل‌ها: `$mdMenu.open` `applyDarkMode` `closeThemePanel` `downloadAndroid` `downloadiOS` `loadWorkspaceBadges` `logout` `newWorkspace` `openSideNavPanel` `openThemePanel` `profileSettings` `searchIconClicked` `sendSuggestion` `sendSupportRequest` `setDontDisturb` `setWallpaper` `showBookmarksPage` `showDashboard` `showDemoGuide` `showDsExGuide` `showHelp` `showHelpCenterMenu` `showSearchPage` `showWhatsNew` `switchWorkspace` `toggleShowNotificationCenter` `upgradePlan` `workspaceSettings`
- فیلدها: `searchStr` `workspaceFilter.title`
- راهنماها: {{'search' \| translate}}، عنوان میزکار ...، ارتباط با پشتیبانی، بستن، حالت روز، حالت شب، حالت پیش‌فرض سیستم، راهنما، نمایش موارد نشان‌شده
- کنترلر: `HeaderController`

### `partial/help-inline`

- منبع: views/ + embedded
- استفاده: `directive:myBookmarkToggleContainer / getMultiOptionLabels / directive/other`
- متن‌ها: بستن راهنما، راهنما ...
- عمل‌ها: `close`
- راهنماها: راهنما ...

### `partial/in-app-notification`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: —
- عمل‌ها: `inAppNotificationAction`
- کنترلر: `AppiOSNotificationController`

### `partial/label-editor`

- منبع: views/ + embedded
- استفاده: `service:AppLabelManager / deleteLabel / modal/panel`
- متن‌ها: انتخاب رنگ، انصراف، ایجاد، به‌روزرسانی، عنوان برچسب، مشخصات برچسب
- عمل‌ها: `cancel` `deleteLabel` `editLabel.color=color` `updateLabel`
- فیلدها: `editLabel.title`

### `partial/label-selector`

- منبع: views/ + embedded
- استفاده: `service:AppLabelManager / selectHistory / modal/panel`
- متن‌ها: ( ) توسط:، انتخاب رنگ، انصراف، ایجاد، ایجاد برچسب جدید، بازیابی از سابقه، سابقه تغییرات برچسب، عنوان برچسب، فیلتر برچسب، مشخصات برچسب
- عمل‌ها: `deleteLabel` `editLabel.color=color` `selectHistory` `selectLabel` `showChangesHistory` `showNewLabelPanel` `showSelector` `showUpdateLabelPanel` `updateLabel`
- فیلدها: `editLabel.title` `filter.title` `labelselector_selection[label]`
- راهنماها: {{'search_for_label' \| translate \| strReplace:'برچسب':labelName}}، {{'label_history' \| translate \| strReplace:'برچسب':labelName}}

### `partial/modal-archive-project-dialog`

- منبع: views/ + embedded
- استفاده: `service:AppProjectsManager / cancel / modal/panel`
- متن‌ها: آرشیو پروژه، آرشیو پروژه و حذف وظایف از کارتابل کاربران، انصراف، روش بازیابی پروژه:، فقط آرشیو پروژه، لطفاً نوع آرشیو را انتخاب کنید، وظایف این پروژه در کارتابل وظایف کاربران همچنان باقی می‌مانند.، وظایف این پروژه نیز آرشیو می‌شوند و از لیست کارتابل کاربران حذف می‌گردند.، پیشنهاد: اگر مطمئن نیستید، «فقط آرشیو پروژه» را انتخاب کنید.
- عمل‌ها: `cancel` `ok`
- فیلدها: `archiveMode`

### `partial/modal-confirm-dialog`

- منبع: views/ + embedded
- استفاده: `factory:services / cancel / modal/panel`
- متن‌ها: انصراف
- عمل‌ها: `cancel` `ok`

### `partial/modal-dont-disturb-dialog`

- منبع: views/ + embedded
- استفاده: `service:AppProfileManager / cancel / modal/panel`
- متن‌ها: انتخاب مدت، انصراف، با انتخاب مدت، نوتیفیکیشن‌های مرورگر موقتاً غیرفعال می‌شوند.، تایید، توقف نوتیفیکیشن‌ها، ساعت، پیش‌فرض
- عمل‌ها: `cancel` `ok` `selectHours`

### `partial/modal-file-downloader`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: در حال دانلود…، لغو

### `partial/modal-file-uploader`

- منبع: views/ + embedded
- استفاده: `service:AppFilesManager / removeFile / modal/panel`
- متن‌ها: ارسال به صورت فایل، انصراف، خطا در آپلود، در حال پردازش…، مورد
- عمل‌ها: `cancel` `removeFile` `selectFile` `send`
- فیلدها: `caption` `sendAsFile`

### `partial/modal-filter-search`

- منبع: views/ + embedded
- استفاده: `factory:services / keyPressed / modal/panel`
- متن‌ها: جستجو
- عمل‌ها: `doSearch`
- فیلدها: `searchStr.str`

### `partial/modal-get-date-dialog`

- منبع: views/ + embedded
- استفاده: `factory:services / onSelect / modal/panel`
- متن‌ها: —
- فیلدها: `calendarDate`
- عناصر سفارشی: `md-persian-calendar`

### `partial/modal-input-number-dialog`

- منبع: views/ + embedded
- استفاده: `factory:services / cancel / modal/panel`
- متن‌ها: انصراف
- عمل‌ها: `cancel`
- فیلدها: `otpValidatorFormInputsDigit1` `otpValidatorFormInputsDigit2` `otpValidatorFormInputsDigit3` `otpValidatorFormInputsDigit4` `otpValidatorFormInputsDigit5`

### `partial/modal-input-password-dialog`

- منبع: views/ + embedded
- استفاده: `factory:services / cancel / modal/panel`
- متن‌ها: ارسال، انصراف، کلمه عبور
- عمل‌ها: `cancel` `ok`
- فیلدها: `password`

### `partial/modal-message-dialog-demo-activated`

- منبع: views/ + embedded
- استفاده: `factory:services / showSupport / modal/panel`
- متن‌ها: «پلن پیشرفته برای میزکار شما به مدت محدود فعال گردیده است»، ارتباط با پشتیبانی، امکانات زیر در قالب دمو برای شما فعال شده است:، تنظیمات میزکار > مجوزها، جهت آشنایی با امکانات میزیتو، سامانه آموزشی میزیتو در اختیار شماست:، جهت استفاده از امکانات کامل پلن پیشرفته، اقدامات زیر را انجام دهید:، در، در صورت سؤال و یا نیاز به آموزش و راهنمایی، از قسمت پشتیبانی با ما در ارتباط باشید.، دسترسی امکانات را برای خود ایجاد کنید.، راهنمای میزیتو، قدم اول:، قدم دوم:، ویدئوهای آموزشی، ویرایش پروژه > تنظیمات پروژه، پروژه را به پیشرفته تبدیل کنید و تنظمیات پروژه پیشرفته را نیز انجام دهید.
- عمل‌ها: `ok` `showSupport`

### `partial/modal-notification-feature-dialog`

- منبع: views/ + embedded
- استفاده: `factory:notificationIOSService / isFirefox / modal/panel`
- متن‌ها: امکان دریافت نوتیفیکشن بر روی iPhone فراهم شده است. لطفا جهت فعال‌سازی، ابتدا نسخه وب‌اپلیکیشن (PWA) فعلی، تایید، تمایلی ندارم!، قابلیت دریافت نوتیفیکیشن فعال شد، میزیتو را حذف نمایید و مجدد اقدام به نصب آن فرمایید.
- عمل‌ها: `cancel` `ok`

### `partial/modal-notification-permission-dialog`

- منبع: views/ + embedded
- استفاده: `factory:notificationIOSService / isFirefox / modal/panel`
- متن‌ها: برای دریافت نوتیفیکیشن، گزینه‌ی زیر را انتخاب کنید.، فعال‌سازی نوتیفیکیشن
- عمل‌ها: `ok`

### `partial/modal-photo-cropper`

- منبع: views/ + embedded
- استفاده: `service:AppFilesManager / cancel / modal/panel`
- متن‌ها: انصراف
- عمل‌ها: `cancel` `setImage`

### `partial/modal-photo-viewer`

- منبع: views/ + embedded
- استفاده: `service:AppPhotosManager / photoClicked / modal/panel`
- متن‌ها: از، اشتراک گذاری، بزرگ‌نمایی، در حال بارگزاری، ذخیره، چرخش به راست، چرخش به چپ، کوچک‌نمایی
- عمل‌ها: `$event.stopPropagation` `close` `photoClicked` `rotate` `save` `share` `zoomIn` `zoomOut`
- راهنماها: اشتراک گذاری، بزرگ‌نمایی، ذخیره، چرخش به راست، چرخش به چپ، کوچک‌نمایی

### `partial/modal-report-get-dates-dialog`

- منبع: views/ + embedded
- استفاده: `factory:services / cancel / modal/panel`
- متن‌ها: از تاریخ، انتخاب بازه زمانی جهت گزارش، انتخاب سریع، انصراف، بر اساس، تا تاریخ
- عمل‌ها: `cancel` `ok` `setQuickDateRange`
- فیلدها: `filter.from_date` `filter.to_date` `filter.type`
- عناصر سفارشی: `md-persian-datepicker`

### `partial/modal-video-viewer`

- منبع: views/ + embedded
- استفاده: `service:AppFilesManager / close / modal/panel`
- متن‌ها: اشتراک گذاری، ذخیره
- عمل‌ها: `close` `save` `share`
- راهنماها: اشتراک گذاری، ذخیره

### `partial/partial-chip-user-selector`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `crm/modal-new-customer`؛ داخل قالب `inbox/modal-compose`؛ داخل قالب `minute/tabs/minute-members`؛ داخل قالب `projects/modal-project-advanced-features`؛ داخل قالب `tasks/partial/partial-modal-new-project-main`
- متن‌ها: —

### `partial/partial-chip-user-template`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `crm/modal-new-customer`؛ داخل قالب `inbox/modal-compose`؛ داخل قالب `minute/tabs/minute-members`؛ داخل قالب `projects/modal-project-advanced-features`؛ داخل قالب `tasks/partial/partial-modal-new-project-main`
- متن‌ها: —

### `partial/peer-selector`

- منبع: views/ + embedded
- استفاده: `service:AppPeersManager / cancel / modal/panel`
- متن‌ها: انتخاب پرونده مشتری:، انصراف، در حال بارگذاری
- عمل‌ها: `cancel` `null` `ok` `removeDialog` `selectDialog` `selectUser`
- فیلدها: `dialog_filter` `dialogselector_selection[item.d._id]`

### `partial/project-selector`

- منبع: views/ + embedded
- استفاده: `service:AppProjectsManager / showUpdateProject / modal/panel`
- متن‌ها: دسته‌بندی جدید، فیلتر دسته‌بندی
- عمل‌ها: `selectProject` `showNewProject` `showUpdateProject`
- فیلدها: `filter`
- راهنماها: {{'search_for_projects' \| translate}}

### `partial/schedule-selector`

- منبع: views/ + embedded
- استفاده: `service:AppTaskSchedulerManager / setFinalResult / modal/panel`
- متن‌ها: روزانه، ? 'بدون تکرار - برای تعیین تکرار کلیک کنید'، آخرین، آخرین روز ماه، الگوی تکرار، امروز، انتخاب تاریخ و زمان، انتخاب تاریخ و ساعت دلخواه، اولین، اولین روز ماه، اولین یا آخرین، اولین/آخرینِ ...شنبه، بدون پایان، بعد از … بار، تا تاریخ، تاریخ پایان، تعداد تکرار، تکرار خاص، تکرار خاص…، تکرار نمی‌شود، حالت روزانه، روز ...ام (۱ تا ۳۰)، روز هفته، روزهای هفته، روزِ ماه، … (+24)
- عمل‌ها: `closeQuickTimePopup` `custom_date.repeat_options.week_days[$index]` `custom_repeat_popup` `isOpenDateSelector=true` `null` `selectCustomDate` `selectTodayCustomTime` `setCustomRepeat` `setCustomRepeatBase` `setCustomTime` `setDailyMode` `setDate` `setFinalResult` `setMonthlyDayOfWeek` `setMonthlyInterval` `setMonthlyMode` `setMonthlyWeekdayPos` `setQuickDayTime` `setRepeatUntilType` `setWeeklyInterval` `showCustomRepeatSelector` `showCustomTimeSelector` `showDaysSelector` `showQuickTimeSelector` `showRepeatUntilDatePicker` `special_day_in_month` `stepRepeatUntilDays` `stepSpecialDayInMonth`
- فیلدها: `custom_date.date` `custom_date.repeat_options.repeat_until_date` `custom_date.repeat_options.repeat_until_days` `custom_date.time` `specialDayInMonthValue`
- راهنماها: ساعت (مثال: 14:00)
- عناصر سفارشی: `md-persian-datepicker`

### `partial/side-nav`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: —
- عمل‌ها: `profileSettings` `toggleOpenWorkspaceSelector`
- کنترلر: `SideNavController`
- زیرقالب: `partial/side-nav-menu` `partial/side-nav-workspaces`

### `partial/side-nav-menu`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `partial/side-nav`
- متن‌ها: تبریک تولد!!، تنظیمات، داشبورد، دعوت عضو جدید، مانیتورینگ، نامه‌ها، همکارانم، وظایف، پرونده مشتریان، پروژه‌ها، پشتیبان آنلاین، گفتگو، یادداشت‌های من
- عمل‌ها: `inviteNewUser` `sayBirthdayCongratulation` `startChat` `workspaceSettings`
- راهنماها: تبریک تولد!!

### `partial/side-nav-workspaces`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `partial/side-nav`
- متن‌ها: ایجاد میزِکار جدید، تنظیمات
- عمل‌ها: `newWorkspace` `switchWorkspace` `workspaceSettings`
- فیلدها: `workspaceFilter.title`
- راهنماها: عنوان میزکار ...

### `partial/toast_error`

- منبع: views/ + embedded
- استفاده: `factory:services / cancel / modal/panel`
- متن‌ها: —
- عناصر سفارشی: `md-toast`

### `partial/toast_success`

- منبع: views/ + embedded
- استفاده: `factory:services / showToast / modal/panel`
- متن‌ها: —
- عناصر سفارشی: `md-toast`

### `partial/toast_undo_with_close`

- منبع: views/ + embedded
- استفاده: `factory:services / closeToast / modal/panel`
- متن‌ها: لغو
- عمل‌ها: `closeToast` `undo`
- عناصر سفارشی: `md-toast`

### `partial/toast_warning_reload_after_disconnect`

- منبع: views/ + embedded
- استفاده: `factory:services / closeToast / modal/panel`
- متن‌ها: بارگذاری مجدد، برای نمایش صحیح اطلاعات، لطفاً صفحه را مجدداً بارگذاری کنید.، توجه: ارتباط اینترنتی یا شبکه شما برای مدتی قطع بوده است.
- عمل‌ها: `closeToast` `refresh`
- عناصر سفارشی: `md-toast`

### `partial/user-selector`

- منبع: views/ + embedded
- استفاده: `service:AppUsersManager / cancel / modal/panel`
- متن‌ها: (حذف شده)، انصراف، لیست اعضای مهمان، لیست همکاران، نام کاربر را وارد نمایید، کاربران حذف شده
- عمل‌ها: `cancel` `ok` `selectUser` `toggleGuests`
- فیلدها: `selected_text` `showDeleted` `userselector_selection[user._id]`
- راهنماها: {{'enter_user_name' \| translate}}، لیست اعضای مهمان لیست همکاران

## `polling/` (3)

### `polling/modal-new-polling`

- منبع: views/ + embedded
- استفاده: `service:AppPollingManager / cancel / modal/panel`
- متن‌ها: پاسخ صحیح این سوال را مشخص کنید.، استفاده از الگوی نظرسنجی، انتخاب چند پاسخ، انتقال سؤال به بالا، انتقال سؤال به پایین، انصراف، ایجاد نظرسنجی، این فیلد الزامی است.، تنظیمات، توضیحات (اختیاری)، حالت آزمون، حذف این سؤال، در حالت آزمون، اعضا فقط می‌توانند یک پاسخ درست انتخاب کنند. اعضا قادر به تغییر پاسخ نخواهند بود.، سؤال جدید، عدم افشای نظر هر عضو، عنوان پرسش، نمایش نظر هر عضو به مدیر، پرسشنامه چند سؤاله، گزینه جدید، گزینه‌ها
- عمل‌ها: `$mdMenu.open` `addQuestion` `cancel` `createPolling` `moveQuestionDown` `moveQuestionUp` `newOption` `removeOption` `removeQuestion` `useTemplate`
- فیلدها: `item.text` `polling.admin_visible` `polling.anonymous` `polling.multiple_answers` `polling.multiple_questions` `polling.quiz_mode` `question.correct_answer` `question.description` `question.subject`
- راهنماها: عنوان گزینه، انتقال سؤال به بالا، انتقال سؤال به پایین، حذف این سؤال

### `polling/modal-polling-result`

- منبع: views/ + embedded
- استفاده: `service:AppPollingManager / cancel / modal/panel`
- متن‌ها: بازگشت، رأی، نتایج نظرسنجی، پاسخ صحیح، چاپ نتایج، گزینه :
- عمل‌ها: `cancel` `printPollingResults`

### `polling/template-selector`

- منبع: views/ + embedded
- استفاده: `service:AppPollingManager / selectTemplate / modal/panel`
- متن‌ها: —
- عمل‌ها: `selectTemplate`
- فیلدها: `filter`
- راهنماها: فیلتر الگوی نظرسنجی

## `print/` (1)

### `print/print-content`

- دانلود نشد (HTTP 404); این قالب پویا ساخته می‌شود.

## `projects/` (62)

### `projects/automation/components/project-automation-param-field-input`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / getActionTypeTitle / directive/other`
- متن‌ها: (مقداری ندارد)، \| حداکثر حجم: مگابایت، آپلود تصویر، آپلود فایل، انتخاب، فرمت‌های مجاز:، نوع فیلد « » پشتیبانی نمی‌شود.، — بدون انتخاب —
- عمل‌ها: `removeFile` `removeUser` `selectUser` `toggleCheckbox` `upload`
- فیلدها: `values[p._id]`
- راهنماها: انتخاب تاریخ
- عناصر سفارشی: `md-persian-datepicker` `my-rating-field` `my-toggle-switch`

### `projects/automation/components/project-automation-param-value-viewer`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / toggleCheckbox / directive/other`
- متن‌ها: —
- راهنماها: {{p.description}}
- عناصر سفارشی: `my-rating-field`

### `projects/automation/modal-project-automation-custom-param-item`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationCustomParamsManager / cancel / modal/panel`
- متن‌ها: (کد پارامتر: # )، آخرین استفاده:، احساسی 😊، از * برای پذیرش تمام فرمت‌ها استفاده کنید.، از طریق، اسلایدر 🎚️، اطلاعات کلی، افزودن گزینه جدید، انتخاب حالت پیش‌فرض، انتخاب کاربران مجاز، انصراف، انواع مجاز تصویر (با کاما جدا کنید)، انواع مجاز فایل (با کاما جدا کنید)، اگر این گزینه فعال باشد، پارامتر فقط در صورت داشتن مقدار در پنجره وظایف نمایش داده می‌شود.، اگر هیچ کاربری انتخاب نشود، انتخاب کاربر آزاد خواهد بود.، این متن در کنار چک‌باکس نمایش داده می‌شود و مفهوم گزینه را برای کاربر مشخص می‌کند.، این نمایی از فیلدی است که کاربر هنگام ورود اطلاعات مشاهده خواهد کرد:، به‌طور پیش‌فرض jpg و png مجاز هستند. از * برای پذیرش همه‌ی فرمت‌ها استفاده کنید.، تعداد استفاده از پارامتر:، تعریف دکمه خودکار، تعریف پارامتر سفارشی، تنظیمات خاص فیلد انتخاب‌شده، توسط:، توضیح، توضیح کنار چک‌باکس، … (+40)
- عمل‌ها: `addFileTypeSuggestion` `addOption` `cancel` `delete` `param.color` `removeAllowedUser` `removeOption` `save` `selectAllowedUsers` `setParamType` `showHistory`
- فیلدها: `opt.label` `param.allowed_file_types_string` `param.checkbox_label` `param.description` `param.hide_if_empty` `param.is_enabled` `param.max_file_size_mb` `param.price_unit` `param.rating_max` `param.rating_style` `param.title` `param.toggle_default_value` `param.toggle_left_value` `param.toggle_right_value`
- راهنماها: توضیح کاربرد پارامتر را وارد کنید...، مثلاً 10، مثلاً 5، مثلاً jpg, png, webp یا * برای همه، مثلاً pdf, docx, xlsx یا * برای همه، مثلاً بله یا فعال یا نهایی‌شده، مثلاً تأیید انجام شده؟، مثلاً تومان، دلار، €، مثلاً خیر یا غیرفعال یا پیش‌نویس، مشاهده سابقه تغییرات
- عناصر سفارشی: `my-project-automation-param-field-input`

### `projects/automation/modal-project-automation-form-request-editor`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationFormRequestsManager / save / modal/panel`
- متن‌ها: ( مورد)، (فیلد واردشده در فرم)، «ارجاع برای بررسی نهایی»، «به‌روزرسانی درصد پیشرفت»، «تغییر مسؤول انجام یا تأییدکننده»، «در انتظار پاسخ کاربر»، «مدارک ناقص»، آخرین استفاده، آمار استفاده از فرم، اطلاعات کلی فرم، افزودن تاریخ ثبت درخواست، افزودن ساعت ثبت درخواست، افزودن نام درخواست‌دهنده، الگوی عنوان وظیفه هنگام ثبت درخواست، الگوی وظیفه مرتبط با این فرم، انتخاب / ویرایش فیلدها، انصراف، اگر این درخواست در قالب جریان کار انجام شود، کل مراحل رسیدگی و مرحله فعال به صورت گرافیکی به کاربر نمایش داده می‌شود.، این بخش چک‌لیست وظیفهٔ مرتبط با فرم است و مراحل انجام درخواست را برای کاربر نهایی نمایش می‌دهد.، این مجوز فقط در صورتی اثر دارد که درخواست با جریان کار انجام شود.، با کلیک روی آیکن‌های چشم داخل پیش‌نمایش، نمایش/عدم‌نمایش هر بخش برای کاربر نهایی تغییر می‌کند.، بخش پیام‌ها برای این فرم نمایش داده نخواهد شد.، بخشی از عنوان بر اساس اطلاعات فرم و کاربر تکمیل می‌شود.، برای مدیریت مجوز نمایش، روی آیکن‌های چشم کلیک کنید، برچسب‌های پیش‌فرض:، بورد مقصد:، … (+89)
- عمل‌ها: `!isParamSelected` `cancel` `delete` `form.visibility_settings.allow_comment_submit` `form.visibility_settings.show_alarm_time` `form.visibility_settings.show_checklist` `form.visibility_settings.show_current_step` `form.visibility_settings.show_history` `form.visibility_settings.show_labels` `form.visibility_settings.show_last_update` `form.visibility_settings.show_progress` `form.visibility_settings.show_responsible` `form.visibility_settings.show_workflow` `openParamSelector` `openTaskTemplateEditor` `removeParam` `save` `showHistory`
- فیلدها: `form.description` `form.is_active` `form.title` `form.title_pattern.include_date` `form.title_pattern.include_requester` `form.title_pattern.include_time` `form.visibility_settings.comments_mode` `param.required`
- راهنماها: با کلیک روی آیکن‌های چشم داخل پیش‌نمایش، نمایش/عدم‌نمایش هر بخش برای کاربر نهایی تغییر می‌کند.، حذف پارامتر از فرم، مشاهده سابقه تغییرات فرم
- عناصر سفارشی: `my-toggle-switch`

### `projects/automation/modal-project-automation-item`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationManager / cancel / modal/panel`
- متن‌ها: (اختیاری)، : 'اینجا تعیین می‌کنید وقتی این قانون فعال شد چه کاری به‌صورت خودکار انجام شود.'، : 'در این بخش مشخص می‌کنی چه شرایطی باید برقرار باشه تا این قانون خودکار اجرا بشه.')، : 'عنوان قانون'، : 'قانون'، : '🎯 شرط‌های وظیفه'}}، ? 'اینجا تعیین می‌کنید وقتی کاربر روی این دکمه کلیک کرد چه کاری به‌صورت خودکار انجام شود.'، ? 'در این بخش شرایطی که لازمه برقرار باشه رو مشخص کن.'، ? 'در این بخش مشخص می‌کنی چه شرایطی باید برقرار باشه تا این دکمه نمایش داده بشه.'، ? 'در این بخش مشخص کن وقتی این حالت اتفاق افتاد، چه کاری باید انجام بشه.'، ? '🎯 شرایط نمایش دکمه'، ? (automateItem.workflow_type === 'condition' ? 'حالت' : 'اتفاق')، ? (automateItem.workflow_type === 'condition' ? 'عنوان شرط' : 'عنوان اتفاق که قراره اتفاق بیفته')، این توضیح فقط برای مستندسازی است و به کاربر نمایش داده نمی‌شود.، این فقط پیش‌نمایش دکمه است و فقط وقتی در پنجره وظیفه دیده می‌شود، قابل اجرا می‌باشد.، این متن بعد از اجرای دکمه، به صورت اعلان کوتاه به کاربر نمایش داده می‌شود.، بستن، توضیحات، در حال بارگذاری اطلاعات...، در حالت ساده، دکمه همیشه به کاربر نشان داده می‌شود.، در حالت پیشرفته می‌توانید برای این دکمه شرط تعریف کنید؛، رنگ دکمه، شرط، شرط جدید، عملیات، … (+7)
- عمل‌ها: `addConditionItem` `automateItem.button_color=color` `cancel` `err.index` `newAction` `setActiveEditing`
- فیلدها: `automateItem.description` `automateItem.is_advanced` `automateItem.is_enabled` `automateItem.title`
- راهنماها: این فقط پیش‌نمایش دکمه است و فقط وقتی در پنجره وظیفه دیده می‌شود، قابل اجرا می‌باشد.، بستن
- عناصر سفارشی: `my-automate-button`
- زیرقالب: `projects/automation/partial/partial-automation-actions` `projects/automation/partial/partial-automation-conditions` `projects/automation/partial/partial-automation-item-buttons` `projects/automation/partial/partial-automation-side-summary-panel`

### `projects/automation/modal-project-automation-item-details`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationManager / close / modal/panel`
- متن‌ها: بستن، جزئیات، سابقه تغییرات
- عمل‌ها: `close` `showAutomationHistory`
- راهنماها: بستن

### `projects/automation/modal-project-automation-item-history`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationManager / close / directive/other`
- متن‌ها: بستن، در حال بارگذاری سابقه تغییرات...، سابقه تغییرات
- عمل‌ها: `close`
- راهنماها: بستن

### `projects/automation/modal-project-automation-items`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationManager / toggleShowDeletedParams / modal/panel`
- متن‌ها: بستن، خودکارسازی پروژه، دکمه‌های خودکار، طراحی جریان کار، فرم‌های درخواست، قوانین خودکار، مدیریت ماژول، پارامترهای سفارشی، گزارش عملکرد
- عمل‌ها: `close` `selectedTab`
- زیرقالب: `projects/automation/partial/automate-items-tabs/partial-modal-project-automation-items-tab-buttons` `projects/automation/partial/automate-items-tabs/partial-modal-project-automation-items-tab-forms` `projects/automation/partial/automate-items-tabs/partial-modal-project-automation-items-tab-params` `projects/automation/partial/automate-items-tabs/partial-modal-project-automation-items-tab-report` `projects/automation/partial/automate-items-tabs/partial-modal-project-automation-items-tab-rules` `projects/automation/partial/automate-items-tabs/partial-modal-project-automation-items-tab-workflow`

### `projects/automation/modal/modal-automation-role-selector`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationWorkflowRoleManager / cancelEdit / modal/panel`
- متن‌ها: از پارامتر، اعضای این نقش، افراد این لیست می‌توانند برای مراحلی که این نقش دارند، به‌عنوان انجام‌دهنده در نظر گرفته شوند.، افزودن عضو، انتخاب شد:، انتخاب نقش انجام‌دهنده، انتخاب و مدیریت نقش‌ها، انتخاب پارامتر، انصراف، این نقش انجام‌دهنده را از مقدار یک پارامتر (از نوع کاربر) موجود در فرم می‌گیرد.، بدون عضو، ثابت (انتخاب اعضا)، در حال بارگذاری...، ذخیره نقش، روش تعیین انجام‌دهنده، عضو، عنوان پارامتر انجام‌دهنده مشخص نیست.، می‌تونی اعضا را دستی تعیین کنی یا انجام‌دهنده را از روی یک پارامتر از فرمی که پر شده است بگیری.، نام نقش، نام نقش و روش تعیین انجام‌دهنده را مشخص کن.، نقش جدید، نقش سیستمی، هنوز عضوی برای این نقش انتخاب نشده است.، هنوز هیچ نقشی تعریف نشده است.، هیچ عضوی برای این نقش انتخاب نشده است.، … (+5)
- عمل‌ها: `addMember` `cancelEdit` `close` `createNewActorParam` `deleteRole` `refreshActorParams` `removeMember` `saveRole` `selectRole` `startAddRole` `startEditRole`
- فیلدها: `currentRole.selection_mode` `currentRole.selection_param_id` `currentRole.title` `rolesSearch`
- راهنماها: انتخاب پارامتر...، جستجو در نام نقش‌ها...

### `projects/automation/modal/modal-automation-text-compose-config`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationTextComposeManager / cancel / modal/panel`
- متن‌ها: «مدیریت ماژول خودکارسازی پروژه»، «پارامترهای سفارشی»، انصراف، برای درج هر پارامتر در متن، روی آن کلیک کنید:، بستن، تأیید، تنظیم متن پیشرفته، در بخش، متن پیام:، می‌توانید از داخل پنجره، پارامتر سفارشی فعالی وجود ندارد.، پارامترهای موردنظر خود را اضافه کنید.، پیش‌نمایش متن:
- عمل‌ها: `addVariableToTemplate` `cancel` `save`
- راهنماها: بستن

### `projects/automation/modal/modal-automation-workflow-editor`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationWorkflowManager / close / modal/panel`
- متن‌ها: : 'انتخاب نقش' }}، ارسال، ارسال برای مدیر پروژه، از این مراحل هیچ مسیری به مراحل پایانی وجود ندارد. برای رفع، مسیر(ها) را طوری وصل کنید که به یکی از مراحل پایانی برسد.، از پارامتر:، اطلاعات مرحله، افزودن دکمه، افزودن دکمه جدید برای این مرحله، افزودن مرحله جدید، انتخاب توسط کاربر، انتخاب فرمِ مربوط به این جریان کار، انتشار، انتقال‌های قابل اجرا، انجام دوباره (Redo)، انجام‌دهندهٔ فعلی از بین اعضای نقش، نفر بعدی را انتخاب می‌کند.، ایجاد مرحله جدید، این دکمه‌ها مرحله مقصد ندارند و انتقال انجام نمی‌شود. برای رفع، برای هر دکمه یک «مرحله مقصد» انتخاب کنید.، این مراحل هیچ دکمه‌ای ندارند و جریان در آن‌ها گیر می‌کند. برای رفع، دکمه اضافه کنید یا مرحله را «پایانی» کنید.، بازگشت (Undo)، بازگشت برای اصلاح توسط درخواست‌دهنده، برای این مراحل نقش انجام‌دهنده تعیین نشده است. برای رفع، از پنل سمت چپ یک نقش برای مرحله انتخاب کنید.، بررسی، بستن، به کدام مرحله یا نقش، تأیید، … (+78)
- عمل‌ها: `!saving` `$event.stopPropagation` `addButton` `addState` `autoLayout` `close` `delete` `deleteState` `editAutomationItem` `editButtonInline` `editEntryCondition` `editStateBasic` `editWorkflowTitle` `enterSimulationMode` `exitSimulationMode` `onButtonActionsBadgeClick` `onButtonColorChanged` `onNodeButtonClick` `onStateClick` `openFormGateSelector` `redo` `removeButton` `saveWorkflow` `scrollToStateInGraph` `selectActorRole` `showTitleHint` `simulationExecuteButton` `simulationJumpToHistory` `simulationReset` `simulationStepBack` `summaryPanelVisible` `toggleFocusMode` `toggleIssuesPanel` `undo`
- فیلدها: `currentButtonWrapper.to_state_id` `selectedAutomationItem.title` `selectedState.actor.assignment_type` `selectedState.is_end` `selectedState.is_start` `selectedState.title`
- راهنماها: انتخاب مرحله مقصد، عنوان دکمه، {{ getStateIssuesText(state) }}، {{ workflow.is_enabled ? 'غیرفعال‌سازی جریان (قابل بازگشت)' : 'فعال‌سازی جریان' }}، افزودن دکمه، افزودن مرحله جدید، انتخاب فرمِ مربوط به این جریان کار، انجام دوباره (Redo)، بازگشت (Undo)، بستن، حالت فوکوس، خروج از شبیه‌سازی، شبیه‌سازی، شروع مجدد، مشکلات جریان کار، … (+2)

### `projects/automation/modal/modal-automation-workflow-select-branch-type`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: انتخاب توسط کاربر، بررسی شرایط وظیفه، تعریف حالت جدید، تو این مرحله از فرآیند، نوع حالت جدیدت رو مشخص کن، مسیر بعدی به صورت خودکار، با توجه به شرایطی که تو تعیین می‌کنی انتخاب میشه.، کاربر خودش با زدن دکمه‌ای که تو براش تعریف می‌کنی، مسیر بعدی رو انتخاب می‌کنه.
- عمل‌ها: `close` `selectType`

### `projects/automation/modal/modal-automation-workflow-wizard`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationWorkflowWizardManager / showWizard / modal/panel`
- متن‌ها: : 'چه انتقال‌هایی به مراحل دیگر می‌تواند وجود داشته باشند؟'، ? 'فقط یک انتقال به مرحله بعد باید تعریف شود.'، \|\| 'مشخص نشده'، از مرحله، اطلاعات کلی، اطلاعات کلی جریان کار، افزودن عضو، افزودن مرحله جدید، افزودن نقش جدید، الگو، الگوهای پیشنهادی، انتقال‌ها، انتقال‌ها (دکمه‌ها)، انتقال‌ها/دکمه‌ها را بساز، انصراف، اگر چند مرحله پایانی داشته باشی، جریان می‌تواند از مسیرهای مختلف به پایان برسد.، ایجاد جریان و ورود به ویرایش پیشرفته، ایجاد جریان کار جدید، این مرحله پایانی است و انتقالی به مرحله بعد ندارد.، برای هر مرحله اجرایی، انتقال‌های ممکن به مراحل دیگر را مشخص کن.، برای هر مرحله مشخص کن چه نقشی مسئول انجام آن است.، برای هر نقش، افراد مرتبط با آن نقش را مشخص کن.، بستن، تعریف انتقال جدید، تعریف نقش‌ها، … (+62)
- عمل‌ها: `` `addNewRoleInline` `addNewTransition` `addRoleMemberInline` `addStateRow` `applyTemplateBasic` `cancelRoleTitle` `clearTemplateSelection` `close` `closeWf5AddRow` `commitRoleTitle` `finishWizard` `goToStateIndex` `nextState` `openParamsManager` `openRoleSelectorForSingleStep` `openWf5AddRow` `prevState` `prevStep` `removeRoleInline` `removeRoleMemberInline` `removeStateRow` `removeTransition` `setTemplateCategory` `startEditRoleTitle` `tempNewAction.color` `toggleFormErrorDetails` `tr.color` `tryNextStep`
- فیلدها: `role._titleDraft` `st._is_end` `st.role_id` `st.title` `tempNewAction.title` `tempNewAction.to` `tplUi.q` `tr.title` `tr.to_state_temp_id` `wizard.data.basic.description` `wizard.data.basic.title`
- راهنماها: جستجو در عنوان/توضیح الگو...، عنوان مرحله، عنوان نقش، مثلاً: فرآیند خرید تجهیزات، یک توضیح کوتاه برای فهم بهتر اعضا، بستن

### `projects/automation/modal/modal-project-automation-custom-param-history`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationCustomParamsManager / close / modal/panel`
- متن‌ها: بستن، در حال بارگذاری سابقه تغییرات...، سابقه تغییرات پارامتر، هیچ سابقه‌ای برای این پارامتر یافت نشد.
- عمل‌ها: `close`
- راهنماها: بستن

### `projects/automation/modal/modal-project-automation-form-request-history`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationFormRequestsManager / None / modal/panel`
- متن‌ها: بستن، در حال بارگذاری سابقه تغییرات...، سابقه تغییرات فرم، هیچ سابقه‌ای برای این فرم یافت نشد.
- عمل‌ها: `close`
- راهنماها: بستن

### `projects/automation/modal/modal-project-automation-param-input`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationCustomParamsManager / cancel / modal/panel`
- متن‌ها: : 'لطفاً مقادیر پارامترهای مورد نیاز در فرم زیر را وارد کنید:' }}، ? 'لطفاً اطلاعات زیر را با دقت وارد کنید تا درخواست شما ثبت شود.'، ارسال درخواست، انصراف، فرم درخواست:، هیچ پارامتری برای این فرم تعریف نشده است.، ورود اطلاعات مورد نیاز
- عمل‌ها: `cancel` `save`
- عناصر سفارشی: `my-project-automation-param-field-input`

### `projects/automation/modal/modal-project-automation-param-selector`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationCustomParamsManager / cancel / modal/panel`
- متن‌ها: ( فیلد)، «مدیریت ماژول خودکارسازی پروژه»، «پارامترهای سفارشی»، از همین‌جا می‌توانید با «افزودن پارامتر جدید» پارامتر بسازید، استفاده از الگو، افزودن پارامتر جدید، انتخاب الگو، انتخاب فیلدهای الگو، انتخاب و اعمال الگو، انتخاب پارامترهای سفارشی، انصراف، اگر دوست دارید، می‌توانید از الگو برای انتخاب/ساخت سریع فیلدها استفاده کنید.، با «ساخت و انتخاب»، فیلدهای موجود انتخاب می‌شوند و مورد جدید ساخته می‌شود.، بخش، برای ادامه، یک الگو انتخاب کنید تا پیش‌نمایش و گزینه‌های اعمال فعال شوند.، برای مدیریت کامل (ویرایش، مرتب‌سازی، فعال/غیرفعال‌کردن و حذف)، برخی فیلدهای هم‌نام با الگو یکسان نیستند و قبل از اعمال الگو باید بررسی شوند.، بررسی اختلاف‌ها، به پنجره، تأیید، تنظیمات متفاوت است، در حالت «بدون الگو»، این بخش غیرفعال است و شما می‌توانید پارامترها را دستی انتخاب کنید.، ساخت و انتخاب فیلدهای الگو، عبارت جستجو را تغییر دهید یا پاک کنید.، غیرفعال، … (+18)
- عمل‌ها: `addNewParam` `applyTemplateEnsureAndSelect` `cancel` `clearTemplateSearch` `confirm` `editParam` `pickTemplate` `selectTemplateCategory` `selectTemplateOnly` `toggleConflictPanel` `toggleSelect` `toggleTemplatePicker` `toggleUserTemplate`
- فیلدها: `templateSearch.filter`
- راهنماها: جستجو در الگوها…

### `projects/automation/modal/modal-project-automation-task-param-values-history`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationCustomParamsManager / close / modal/panel`
- متن‌ها: بستن، در حال بارگذاری سابقه تغییرات...، سابقه تغییرات پارامترها، هیچ سابقه‌ای برای پارامترهای این وظیفه یافت نشد.
- عمل‌ها: `close`
- راهنماها: بستن

### `projects/automation/modal/modal-task-workflow-viewer`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAutomationWorkflowManager / close / modal/panel`
- متن‌ها: افراد، ‌ها، انتخاب‌شده، انتقالی تعریف نشده است.، انتقال‌ها، انجام‌دهنده، این مرحله پایانی است.، بستن، جریان کاری برای این وظیفه تعریف نشده است.، حالت تمرکز، در صورت نیاز، از تنظیمات پروژه یک جریان کار برای وظیفه انتخاب کنید.، شروع، فرد، فعلی، مجاز این مرحله:، مرحله فعلی، مرحله فعلی:، پایان
- عمل‌ها: `close` `onStateClick` `toggleFocusMode`
- راهنماها: بستن، حالت تمرکز

### `projects/automation/partial/automate-items-tabs/partial-modal-project-automation-items-tab-buttons`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/automation/modal-project-automation-items`
- متن‌ها: (تیک نزده باشند)، (در پنجره مشاهده وظیفه برای، (که نیاز به دسترسی ویرایش ندارند) برای، - دکمه‌های حاوی عملیاتی مانند، - دکمه‌های حاوی عملیاتی که منجر به، «ارسال برای بررسی موجودی انبار»، «بررسی موجودی انبار»، «در انتظار بررسی»، ارسال برای بررسی موجودی انبار، این دکمه فقط زمانی نمایش داده می‌شود که وظیفه در لیست، این کار باعث تسریع در گردش وظایف بین واحدها و جلوگیری از توقف فرآیند می‌شود.، باشد، باشد.، برای این منظور، می‌توانید دکمه‌ای با عنوان، تعریف کنید تا با یک کلیک، ثبت گزارش، دکمه جدید، دکمه‌ها را جابجا کنید و سپس ذخیره کنید.، دکمه‌هایی که کاربران در صفحه وظیفه می‌بینند و با کلیک روی آنها، عملیات سریع انجام می‌شود.، ذخیره تغییرات، سیستم به‌صورت خودکار انجام‌دهنده را تغییر می‌دهد و درخواست‌کننده را از طریق دستیار مطلع می‌سازد.، غیرفعال، فرض کنید در فرآیند درخواست خرید، فقط برای کاربرانی نمایش داده می‌شوند که:، قوانین نمایش دکمه‌ها:، … (+34)
- عمل‌ها: `cancelEditOrder` `editItem` `newButton` `saveOrder` `showItemDetails` `startEditOrder`
- راهنماها: مشاهده جزئیات، ویرایش

### `projects/automation/partial/automate-items-tabs/partial-modal-project-automation-items-tab-forms`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/automation/modal-project-automation-items`
- متن‌ها: «درخواست خرید تجهیزات»، آخرین استفاده:، اجرا می‌شود و می‌تواند شامل چندین، الگوی وظیفه، با ارسال این فرم، وظیفه‌ای جدید در لیست، باشد.، برای این کار، فرمی با عنوان، تعداد، تعداد استفاده:، توضیح مختصر درباره‌ی هدف خرید، در این بخش می‌توانید فرم‌هایی طراحی کنید که کاربران از طریق آن‌ها درخواست جدید در پروژه ثبت می‌کنند.، درخواست‌های خرید، دلیل خرید، راهنمای فرم‌های درخواست:، ساخته می‌شود و مسئول تدارکات فوراً مطلع می‌شود.، سیستم تمام پارامترهای فرم را ذخیره می‌کند تا روند خرید و پیگیری آن به‌صورت خودکار انجام شود.، طراحی می‌کنید تا کاربران با پرکردن آن، عدد (number)، غیرفعال، فرض کنید در پروژه‌ی تأمین، کاربران نیاز دارند درخواست خرید تجهیزات ثبت کنند.، فرم جدید، فرم‌ها برای ثبت درخواست ساختارمند عالی‌اند؛ مثل درخواست خرید، مرخصی، خدمات، یا پشتیبانی.، قابل تنظیم است.، متن (text)، متن چندخطی (textarea)، … (+17)
- عمل‌ها: `editFormRequestTemplate` `newFormRequestTemplate`
- راهنماها: ویرایش فرم

### `projects/automation/partial/automate-items-tabs/partial-modal-project-automation-items-tab-params`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/automation/modal-project-automation-items`
- متن‌ها: ( گزینه)، (در پنجره مشاهده وظیفه برای، «ثبت تأیید قرارداد»، «در انتظار تأیید»، انتخاب کاربر (user)، این دکمه فقط زمانی باید به کاربر نمایش داده شود که وظیفه در لیست، بازیابی، باشد.، برای ثبت زمان تأیید و امضای قرارداد، برای ثبت شناسهٔ رسمی قرارداد، برای مشخص کردن شخص نهایی تأییدکننده قرارداد، تاریخ (date)، تاریخ امضا، ثبت تأیید قرارداد، در، در انتظار تأیید، در این حالت، مسئول قراردادها با کلیک روی این دکمه، فرم زیر را مشاهده کرده و اطلاعات مربوط به قرارداد را وارد می‌کند:، در لیست، در هر مرحله از گردش‌کار، چه پارامترهایی باید توسط کاربران تکمیل شوند، دکمه‌های خودکار، ذخیره تغییرات، را تعریف کنید.، راهنمای پارامترهای سفارشی:، شماره قرارداد، صفحهٔ جزئیات وظیفه، … (+34)
- عمل‌ها: `cancelEditOrder` `newCustomParam` `restoreParam` `saveOrder` `showCustomParamModal` `startEditOrder` `toggleShowDeletedParams`
- راهنماها: نمایش فقط در صورت داشتن مقدار، ویرایش

### `projects/automation/partial/automate-items-tabs/partial-modal-project-automation-items-tab-report`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/automation/modal-project-automation-items`
- متن‌ها: آخرین اجرا:، آخرین استفاده:، آخرین ویرایش، استفاده:، برای شروع، چند دکمه خودکار تعریف کنید.، برای شروع، یک جریان‌کار جدید بسازید.، بهتر است هر مرحله‌ی فرآیند مشخص کند کدام پارامتر باید تکمیل شود.، تحلیل دکمه‌ها، تحلیل قوانین، تعداد استفاده:، تعداد جریان‌کارها، جریان‌کارها، جریان‌کارهای ثبت‌شده برای این پروژه، جریان‌کارهای در حال طراحی، جریان‌کارهای فعال، جزئیات، حالت جریان‌کار، حالت کلاسیک، دکمه‌ها، راهنما:، رنگ:، زمان آخرین ویرایش جریان کار، غیرفعال، فرم درخواستی وجود ندارد، فرم‌ها برای ثبت درخواست‌های سازمانی و یا شروع فرآیند بسیار مفیدند.، … (+25)
- عمل‌ها: `editFormRequestTemplate` `editItem` `editWorkflow` `showItemDetails`
- راهنماها: جزئیات، ویرایش، ویرایش جریان‌کار، ویرایش فرم

### `projects/automation/partial/automate-items-tabs/partial-modal-project-automation-items-tab-rules`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/automation/modal-project-automation-items`
- متن‌ها: «بررسی موجودی انبار»، «بررسی موجودی انبار» 📦، است.، اگر وظیفه به لیست، این قانون به‌صورت خودکار اجرا می‌شود و نیازی به دخالت کاربر ندارد.، این کار باعث می‌شود هماهنگی بین واحدها سریع‌تر انجام شود و هیچ وظیفه‌ای بدون پیگیری باقی نماند.، با فعال‌شدن آن، تغییر انجام‌دهنده و ارسال پیام هر دو به‌صورت هم‌زمان انجام می‌شوند.، به محض انتقال وظیفه به لیست «بررسی موجودی انبار»، انجام‌دهنده به مدیر انبارداری تغییر می‌کند، در نتیجه فرآیند خرید بدون توقف و با هماهنگی کامل بین واحدها پیش می‌رود.، ذخیره تغییرات، شرط‌ها، عملیات، غیرفعال، فرض کنید در فرآیند خرید، زمانی که وظیفه به لیست، قانون جدید، قوانین برای اجرای خودکار بدون دخالت کاربر مناسب‌اند؛ مثل تغییر وضعیت، برچسب‌گذاری، یا ارسال اعلان بر اساس شرط‌ها.، قوانین را جابجا کنید و سپس دکمه ذخیره را بزنید.، قوانینی که در صورت تحقق شرایط مشخص، سیستم به طور خودکار عملیات را اجرا می‌کند.، لغو، مثال کاربردی: تعیین خودکار انجام‌دهنده هنگام ورود به مرحله بررسی موجودی انبار، مدیر انبارداری، مشاهده جزئیات، منتقل شود، منتقل می‌شود، می‌خواهید سیستم به‌صورت خودکار انجام‌دهنده را تغییر دهد و پیام اطلاع‌رسانی برای درخواست‌کننده ارسال کند.، … (+16)
- عمل‌ها: `cancelEditOrder` `editItem` `newRule` `saveOrder` `showItemDetails` `startEditOrder`
- راهنماها: مشاهده جزئیات، ویرایش

### `projects/automation/partial/automate-items-tabs/partial-modal-project-automation-items-tab-workflow`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/automation/modal-project-automation-items`
- متن‌ها: «ارسال برای تایید مدیر پروژه»، «برگشت برای اصلاح»، «تایید بودجه و ارسال به تدارکات»، «تایید و ارسال به مالی»، آخرین استفاده:، آخرین ویرایش:، این یعنی پیگیری سریع‌تر، خطای کمتر و هماهنگی بهتر بین واحدها.، با جریان کار، مراحل انجام یک وظیفه را مرحله‌به‌مرحله تعریف می‌کنید تا مسئولیت‌ها و انتقال‌ها شفاف و قابل پیگیری شوند.، با جریان کار، وظیفه از ابتدا تا پایان مسیر مشخصی دارد و هر مرحله مسئول خودش را دارد.، بررسی بودجه و تایید پرداخت / رد، بررسی نیاز و تایید یا برگشت برای اصلاح، بستن درخواست و آرشیو، تأیید مالی، تأیید مدیر، تدارکات، تعداد استفاده:، تعداد مراحل:، ثبت اطلاعات اولیه و ارسال برای تایید مدیر پروژه، ثبت درخواست، جریان کار برای فرآیندهای چندمرحله‌ای عالی است؛ مثل تأیید، بررسی، اجرا و بستن.، جریان کار به چه درد می‌خورد؟، جریان‌کار جدید، خرید و تحویل، خرید کالا، ثبت فاکتور و تحویل، درخواست‌کننده، … (+32)
- عمل‌ها: `editWorkflow` `newWorkflow`
- راهنماها: ویرایش جریان‌کار

### `projects/automation/partial/partial-automation-actions`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/automation/modal-project-automation-item`
- متن‌ها: (لیست یافت نشد)، ... روز بعد، افزودن عمل، افزودن کاربر، انتخاب برچسب، انتخاب کاربران، انتقال به لیست مشخص، انجام‌دهنده‌های وظیفه، انصراف، اگر این گزینه روشن باشد، هنگام اجرای دکمه، مقادیر قبلی فیلدها به‌صورت خودکار در فرم قرار می‌گیرند.، ایجادکننده وظیفه / درخواست دهنده اولیه، بازگشت، بازگشت به لیست قبلی، بالای لیست، تاریخ معین، تعداد روز، تعیین پارامترها، توضیح:، حذف عمل، حذف پارامتر، روز جاری، فردا، متن، مدیران پروژه، مقدار عددی، … (+12)
- عمل‌ها: `!actionType.disabled` `addActionItem` `addActionMember` `cancelEditAction` `cancelEditActionItem` `editAction` `openCustomParamSelector` `removeActionItem` `removeActionMember` `removeCustomParam` `selectBoardForAction` `selectLabels` `setActiveEditing`
- فیلدها: `action.value` `action.value.load_previous_values` `action.value.mode` `action.value.operator` `action.value.receiver_type` `action.value.value` `param.required`
- راهنماها: تاریخ انتخاب کنید، حذف پارامتر، ویرایش عمل
- زیرقالب: `projects/automation/partial/partial-automation-textcompose`

### `projects/automation/partial/partial-automation-conditions`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/automation/modal-project-automation-item`
- متن‌ها: آخرین روز در ماه باشد، اضافه یا حذف شود، افزودن شرط، انتخاب برچسب، انتخاب فرد، انتخاب لیست، انصراف، اولین روز در ماه باشد، ایجادکنندهٔ وظیفه باشد، این شرط زمانی فعال می‌شود که یک فیلد تغییر کند.، این شرط زمانی فعال می‌شود که یک فیلد مشخص به مقدار مورد نظر شما تغییر کند.، بازگشت، بازگشت به انتخاب دسته، بعد از تاریخ ...، بیشتر از ... روز گذشته باشد، بیشتر یا مساوی، تعداد روز، تغییر کند، توضیح:، جمعه، حداقل .... روز تاخیر دارد، حداقل یکی از این برچسب‌ها باشد، حداکثر .... روز تاخیر دارد، حذف شرط، دارد، … (+55)
- عمل‌ها: `!conditionType.disabled` `addConditionItem` `addConditionMember` `cancelEditCondition` `cancelEditConditionItem` `conditionState.selectedCategory` `editCondition` `removeConditionItem` `removeConditionMember` `selectBoardsForCondition` `selectLabels` `setActiveEditing`
- فیلدها: `condition.value.days` `condition.value.operator` `condition.value.value`
- راهنماها: انتخاب الگو، تاریخ انتخاب کنید، مثال‌ها: • اگر درصد پیشرفت ۵۰٪ باشد . • اگر تاریخ انجام قبل از فردا باشد . • اگر مسؤول انجام وظیفه علی رضایی باشد .، مثال‌ها: • وقتی درصد پیشرفت تغییر کند . • وقتی تاریخ انجام عوض شود . • وقتی کاربری اضافه یا حذف شود .، ویرایش شرط

### `projects/automation/partial/partial-automation-item-buttons`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/automation/modal-project-automation-item`
- متن‌ها: انتشار، انصراف، ایجاد و انتشار، این تغییرات به‌صورت پیش‌نویس ذخیره می‌شود و هنوز فعال نخواهد شد، این عمل‌خودکار بلافاصله منتشر و قابل استفاده می‌شود، به‌روزرسانی، به‌روزرسانی پیش‌نویس، حذف، ذخیره، ذخیره به‌عنوان پیش‌نویس، مشاهده سابقه تغییرات
- عمل‌ها: `$mdMenu.open` `cancel` `delete` `publish` `saveAsDraft` `showAutomationHistory` `update`
- راهنماها: این تغییرات به‌صورت پیش‌نویس ذخیره می‌شود و هنوز فعال نخواهد شد، این عمل‌خودکار بلافاصله منتشر و قابل استفاده می‌شود، مشاهده سابقه تغییرات

### `projects/automation/partial/partial-automation-side-summary-panel`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / sendAudio / directive/other`؛ داخل قالب `projects/automation/modal-project-automation-item`
- متن‌ها: آخرین استفاده:، آخرین ویرایش:، تاریخ انتشار:، تعداد استفاده:، توسط:، خلاصه، شرط \| عمل، شرط شماره، شرط‌ها فقط در حالت پیشرفته قابل تعریف هستند.، عملیات شماره، مشخصات بلوک جریان کار، هیچ شرطی تعریف نشده است.، هیچ عملیاتی تعریف نشده است.، و سپس، و همچنین، وضعیت:، پیش‌نویس، ⚡ عملیات خودکار:، 🎯 شرط‌ها:، 🧩 عنوان بلوک جریان کار
- عمل‌ها: `scrollToActionFromSummary` `scrollToConditionFromSummary`
- راهنماها: شرط شماره {{ $index + 1 \| persian_digits_with_zero }}، عملیات شماره {{ $index + 1 \| persian_digits_with_zero }}

### `projects/automation/partial/partial-automation-textcompose`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/automation/partial/partial-automation-actions`
- متن‌ها: * در حالت پیشرفته می‌توانید قالب متن را با متغیرها و فیلدهای اختیاری بسازید.، «تنظیم متن پیشرفته»، استفاده کنید.، با متغیرها و قالب‌ها، تنظیم متن پیشرفته، در این حالت می‌توانید قالب پویا بسازید و از متغیرها و فیلدهای اختیاری استفاده کنید.، لطفا از دکمه، متن انتخاب شده (پیشرفته):، متن ساده، متن پیشرفته، هنوز متنی را مشخص نکرده‌اید.
- عمل‌ها: `openTextComposeConfig`
- فیلدها: `action.value.simpleText` `action.value.useAdvanced`
- راهنماها: متن را وارد کنید…

### `projects/calendar/calendar-viewer`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.tasks.calendar`؛ `service:IdleManager / start / state`؛ داخل قالب `projects/monitoring_calendar`؛ داخل قالب `projects/projects`
- متن‌ها: تعداد وظایف بیشتر از ۱۰۰ مورد ...، امروز، امروز:، ایجاد وظیفه جدید، تعداد وظایف این روز، جمعه، دوشنبه، زمان یادآوری، سه‌شنبه، شنبه، فیلتر نمایش، مهلت انجام، نحوه نمایش وظایف، نمایش بر اساس:، نمایش وظایف بدون زمان، نمایش وظایف بدون مهلت، نمایش کامل عناوین، وظایف همه کاربران، وظیفه، پنجشنبه، چهارشنبه، یکشنبه
- عمل‌ها: `$mdMenu.open` `addTask` `goToday` `nextMonth` `prevMonth` `setVisibilityType` `showMobileDayTasks` `toggleFilterOptions`
- فیلدها: `show_all_users` `show_complete_task_title_tmp` `show_no_time_tasks`
- راهنماها: نحوه نمایش وظایف، ایجاد وظیفه جدید، تعداد وظایف این روز
- کنترلر: `AppCalendarViewerController`
- زیرقالب: `projects/calendar/partial-calendar-view-task` `projects/calendar/partial-task-filter`

### `projects/calendar/partial-calendar-view-task`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/calendar/calendar-viewer`
- متن‌ها: —
- عمل‌ها: `showTask`
- راهنماها: {{task.title}}

### `projects/calendar/partial-task-filter`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/calendar/calendar-viewer`
- متن‌ها: انتخاب، ایجاد کننده، برچسب‌ها، مسؤول انجام، نامشخص، پروژه \| دسته‌بندی
- عمل‌ها: `filterClearAssignee` `filterClearOwner` `filterClearProject` `filterSelectAssignee` `filterSelectLabels` `filterSelectLabelsClear` `filterSelectOwner` `filterSelectProject`

### `projects/gantt/gantt-task-selector`

- منبع: views/ + embedded
- استفاده: `service:AppGanttManager / cancel / modal/panel`
- متن‌ها: تعریف وظیفه جدید، انصراف
- عمل‌ها: `cancel` `createNewTask` `ok`
- فیلدها: `filter.title` `taskselector_selection[task._id]`
- راهنماها: انتخاب از وظایف موجود جهت افزوده شدن به گانت

### `projects/gantt/gantt-viewer`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/projects`
- متن‌ها: افزودن وظیفه، امروز، توقف حذف وظایف، حذف وظایف از گانت (با انتخاب)، روز، زمان شروع، زمان پایان، عنوان وظیفه، فاز جدید، ویرایش فاز
- عمل‌ها: `$mdMenu.open` `addPhase` `toggleMultipleRemove`
- راهنماها: افزودن وظیفه، ویرایش فاز
- کنترلر: `AppGanttViewerController`

### `projects/gantt/modal-new-gantt-phase`

- منبع: views/ + embedded
- استفاده: `service:AppGanttManager / cancel / modal/panel`
- متن‌ها: انصراف، این فیلد الزامی است.، تعریف فاز، حذف فاز، عنوان فاز، نمایش این فاز بعد از
- عمل‌ها: `cancel` `create` `delete`
- فیلدها: `phase.prevPhase` `phase.title`
- راهنماها: حذف فاز

### `projects/gantt/partial-gantt-scale-selection`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/partial/chat-header-project`
- متن‌ها: انتخاب مقیاس بزرگنمایی نمایش گانت، بزرگنمایی:، روزانه، فصلی، ماهانه
- عمل‌ها: `$mdMenu.open` `setGanttViewZoomScale`
- راهنماها: انتخاب مقیاس بزرگنمایی نمایش گانت

### `projects/import_project`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.import_project`؛ `service:IdleManager / None / state`
- متن‌ها: انتخاب، انتخاب فایل، انتخاب لیست وظایف انجام شده، انتقال اطلاعات، انتقال اطلاعات (Import) وظایف به میزیتو، انتقال اطلاعات از ترلو، انتقال اطلاعات از فایل CSV، انتقال اطلاعات از فایل اکسل، تعداد خطا:، تعیین اعضا:، تعیین برچسب‌ها:، توجه! در حالت دمو، فقط تعداد، دانلود فایل نمونه csv، دانلود فایل نمونه excel، راهنما، راهنمای انتقال اطلاعات از ترلو، ردیف، عنوان پروژه، قابل انتقال می‌باشد.، مرحله قبل، مرحله ۱: انتخاب فایل، مرحله ۲: نمایش، مرحله ۳: تبدیل، مشاهده پروژه، هیچکدام، … (+2)
- عمل‌ها: `cancel` `downloadSampleFile` `importTasks` `selectLabel` `selectMember` `showFinalProject` `showImportHelp` `uploadFile`
- فیلدها: `fieldIndexes[$index]` `kanbanDoneListTitle` `projectTitle`
- کنترلر: `AppImportProjectController`

### `projects/kanban-viewer`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/projects`
- متن‌ها: + افزودن لیست جدید، تنظیمات لیست، حذف، زمان آخرین تغییرات ← جدیدتر اول، زمان آخرین تغییرات ← قدیمی‌تر اول، زمان ایجاد ← جدیدتر اول، زمان ایجاد ← قدیمی‌تر اول، زمان وظیفه ← جدیدتر اول، زمان وظیفه ← قدیمی‌تر اول، مرتب‌سازی ...، وظیفه جدید، ویرایش لیست، پیش فرض
- عمل‌ها: `$mdMenu.open` `addKanbanBoard` `addTask` `editBoard` `removeBoard` `sortTasks`
- راهنماها: تنظیمات لیست
- کنترلر: `AppKanbanViewerController`

### `projects/modal-duplicate-project`

- منبع: views/ + embedded
- استفاده: `service:AppProjectDuplicateManager / duplicateProject / modal/panel`
- متن‌ها: انصراف، مرحله قبل
- عمل‌ها: `close` `nextStep` `prevStep`
- زیرقالب: `projects/partial/duplicate-project/partial-duplicate-project-confirm` `projects/partial/duplicate-project/partial-duplicate-project-info` `projects/partial/duplicate-project/partial-duplicate-project-steps` `projects/partial/duplicate-project/partial-duplicate-tasks`

### `projects/modal-new-kanban-board`

- منبع: views/ + embedded
- استفاده: `service:AppKanbanManager / update / modal/panel`
- متن‌ها: انتخاب رنگ، انصراف، ایجاد، ایجاد لیست‌ها بر اساس الگو، این فیلد الزامی است.، مشخصات لیست، نام لیست
- عمل‌ها: `cancel` `kanbanBoard.color=color` `selectTemplate` `update`
- فیلدها: `kanbanBoard.title`

### `projects/modal-project-advanced-features`

- منبع: views/ + embedded
- استفاده: `service:AppProjectsManager / update / modal/panel`
- متن‌ها: (مانند: برآورد زمان، میزان سختی، هزینه صرف شده یا امتیاز وظیفه)، افراد دارای دسترسی:، افزودن، انصراف، ایجاد و ویرایش وظایف، با توجه به قابل ویرایش بودن وظایف توسط همه اعضا، زمان یادآوری نیز قابل ویرایش می‌باشد.، بورد پروژه، تنظیمات پروژه پیشرفته، در این بخش می‌توانید دسترسی اعضا به مانیتورینگ پروژه را اضافه کنید.، در صورت فعال بودن، امکان تعریف زمان مهلت انجام برای هر وظیفه فعال می‌شود.، در صورت فعال بودن، فقط مدیران پروژه پیشرفته می‌توانند وظایف را ویرایش کنند.، در صورت فعال بودن، فقط مدیران پروژه پیشرفته می‌توانند وظیفه جدید ثبت کنند.، در صورت فعال بودن، می‌توانید برای وظایف وزن تعیین کنید.، در صورت فعال بودن، نمودارهای پیشرفت پروژه بر اساس مجموع وزن وظایف نمایش داده می‌شوند.، در صورت فعال بودن، وظایف انجام شده در بورد باقی می‌مانند و فقط با تایید مدیر پروژه پیشرفته از بورد حذف می‌شوند.، در صورت فعال بودن، کاربران غیرمدیر نمی‌توانند زمان یادآوری وظایف را در دستیار میزیتو تغییر دهند.، ذخیره، زمان یادآوری وظایف توسط کاربران قابل تمدید نباشد.، زمان‌بندی و وزن، سابقه تغییرات تنظیمات پروژه پیشرفته، فقط مدیران می‌توانند وظایف را ویرایش کنند.، فقط مدیران می‌توانند وظیفه ایجاد کنند.، مانیتورینگ پروژه، مدیران پروژه پیشرفته، نمودار پیشرفت پروژه بر اساس وزن باشد.، … (+3)
- عمل‌ها: `addPermissionMonitoringViewer` `cancel` `removePermissionMonitoringViewer` `showChangesHistory` `update`
- فیلدها: `advanced.advanced_duplicate_confirm` `advanced.advanced_has_deadline` `advanced.advanced_project_summary_with_weight` `advanced.advanced_public_create_task_reverse` `advanced.advanced_tasks_edit_only_admins` `advanced.advanced_tasks_has_weight` `advanced.advanced_tasks_prevent_snooze_by_users` `advanced.members_admin`
- راهنماها: افزودن مدیر...، سابقه تغییرات تنظیمات پروژه پیشرفته
- زیرقالب: `partial/partial-chip-user-selector` `partial/partial-chip-user-template` `projects/partial/partial-modal-project-advanced-features-modules` `projects/partial/partial-modal-project-advanced-features-task-templates`

### `projects/modal-project-advanced-features-history`

- منبع: views/ + embedded
- استفاده: `service:AppProjectAdvancedHistoryManager / close / modal/panel`
- متن‌ها: بستن، در حال بارگذاری سابقه تغییرات...، سابقه تغییرات تنظیمات پروژه پیشرفته، هیچ سابقه‌ای برای این تنظیمات یافت نشد.
- عمل‌ها: `close`
- راهنماها: بستن

### `projects/monitoring_calendar`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.projects_monitoring_calendar`؛ `service:IdleManager / start / state`
- متن‌ها: مانیتورینگ پروژه‌های زیر:
- عمل‌ها: `showMonitorPage` `toggleSelectProject`
- کنترلر: `AppMonitoringProjectsForUserCalendarController`
- زیرقالب: `projects/calendar/calendar-viewer`

### `projects/partial/chat-header-project`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/projects`
- متن‌ها: بورد پروژه، تقویم پروژه، جلسه آنلاین، فیلتر وظایف، نمایش فایل‌ها، نمایش میزان پیشرفت وظایف در بورد پروژه، نمایش وظایف به صورت خلاصه، وظایف پروژه، پرینت، گانت پروژه، گروه پروژه
- عمل‌ها: `callDialog` `mobileShowProjectsList` `printGantt` `returnToChat` `showProjectBoard` `showProjectCalendar` `showProjectFilesFromBoard` `showProjectGantt` `showProjectTasks` `showTasksFilterFromBoard` `toggleShowBoardCompress` `toggleShowBoardStatistics`
- راهنماها: نمایش میزان پیشرفت وظایف در بورد پروژه، نمایش وظایف به صورت خلاصه، پرینت
- زیرقالب: `chat/partial-chat-dialog-header-filter-buttons` `chat/partial-chat-dialog-header-menu` `chat/partial-chat-header-back-callout` `projects/gantt/partial-gantt-scale-selection`

### `projects/partial/duplicate-project/partial-duplicate-project-confirm`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/modal-duplicate-project`
- متن‌ها: آیا پروژه با وظیفه ایجاد شود؟

### `projects/partial/duplicate-project/partial-duplicate-project-info`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/modal-duplicate-project`
- متن‌ها: انتخاب نام برای پروژه جدید:، عنوان پروژه
- فیلدها: `projectTitle.title`

### `projects/partial/duplicate-project/partial-duplicate-project-steps`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/modal-duplicate-project`
- متن‌ها: —

### `projects/partial/duplicate-project/partial-duplicate-tasks`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/modal-duplicate-project`
- متن‌ها: لیست وظایف موجود در پروژه (انتخاب شده: )، وظیفه‌ای در این پروژه وجود ندارد.
- عمل‌ها: `toggleSelect`

### `projects/partial/kanban-board-selector`

- منبع: views/ + embedded
- استفاده: `service:AppKanbanManager / selectList / modal/panel`
- متن‌ها: (پیش‌فرض)، انصراف، تایید ( )
- عمل‌ها: `$event.stopPropagation` `cancel` `confirmSelection` `multiSelect`
- فیلدها: `filter`
- راهنماها: فیلتر لیست بورد

### `projects/partial/pane/project-statistics`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/partial/project-pane`
- متن‌ها: وضعیت پیشرفت بورد پروژه
- کنترلر: `ChatProjectStatisticsCtrl`
- زیرقالب: `projects/partial/pane/project-statistics-normal` `projects/partial/pane/project-statistics-weight`

### `projects/partial/pane/project-statistics-normal`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/partial/pane/project-statistics`
- متن‌ها: انجام شده، بدون زمان، دارای تاخیر، دارای زمان، وضعیت کلی پروژه: «تعداد کار باقیمانده:، کارهای انجام شده: مورد، کارهای بدون زمان: مورد، کارهای دارای تاخیر: مورد، کارهای دارای زمان: مورد، کارهای دیگران، کارهای من
- عمل‌ها: `showTasks`
- راهنماها: کارهای انجام شده: {{status_done \| persian_digits_with_zero}} مورد، کارهای بدون زمان: {{status_no_time \| persian_digits_with_zero}} مورد، کارهای دارای تاخیر: {{status_overdue \| persian_digits_with_zero}} مورد، کارهای دارای زمان: {{status_with_time \| persian_digits_with_zero}} مورد

### `projects/partial/pane/project-statistics-weight`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/partial/pane/project-statistics`
- متن‌ها: (بر اساس وزن وظایف)، انجام شده، انجام شده: % درصد، باقیمانده، باقیمانده: % درصد، دارای تاخیر، دارای تاخیر: % درصد، دارای پیشرفت، دارای پیشرفت: % درصد، وضعیت کلی پروژه، کارهای دیگران، کارهای من
- عمل‌ها: `showTasks`
- راهنماها: انجام شده: %{{status_done_percent \| persian_digits_with_zero}} درصد، باقیمانده: %{{status_remain_percent \| persian_digits_with_zero}} درصد، دارای تاخیر: %{{status_overdue_percent \| persian_digits_with_zero}} درصد، دارای پیشرفت: %{{status_partial_completed_percent \| persian_digits_with_zero}} درصد

### `projects/partial/partial-dialog`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/projects-list`
- متن‌ها: آخرین وظیفه انجام شده:، انتخاب گروه، وضعیت کل پروژه:، وظایف انجام شده:، وظایف من:، کارهای من
- عمل‌ها: `dialogSelect` `setProjectLabel`
- راهنماها: کارهای من

### `projects/partial/partial-modal-project-advanced-features-modules`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/modal-project-advanced-features`
- متن‌ها: افراد با دسترسی فقط مشاهده:، افزودن کاربر، انتخاب مناسب‌تری است.، اگر دنبال مدیریت سریع و ساده هستید، فعال‌سازی این بخش ضرورتی ندارد.، اگر پروژهٔ شما به گردش کار چندمرحله‌ای نیاز ندارد، با فعال‌سازی این ماژول، امکانات خودکارسازی در پروژه فعال می‌شود.، برای تیم‌های اداری و سازمانی، جریان کار چندمرحله‌ای در حالت Workflow، حالت جریان کار (Workflow)، حالت کلاسیک، حالت کلاسیک (Classic)، در صورت نیاز می‌توانید تعیین کنید چه افرادی دسترسی، دکمه‌های خودکار برای انجام سریع عملیات روی وظایف، سریع، کاربردی و بدون پیچیدگی، شامل دکمه‌ها، قوانین و فرم‌ها.، صورتجلسه ساده:، صورتجلسه سازمانی مناسب تیم‌ها و سازمان‌هایی است که به مدیریت کامل مراحل جلسات و رأی‌گیری اعضا نیاز دارند.، صورتجلسه سازمانی:، فرآیندمحور و اداری، شامل دستور جلسه، حضور و غیاب، امضا و ...، فرم‌های درخواست قابل‌سفارشی‌سازی برای ثبت درخواست‌های سازمانی/اداری، فقط مدیران پروژه پیشرفته امکان، فقط مشاهده، قوانین خودکار که در شرایط مشخص، عملیات لازم را انجام می‌دهند، ماژول خودکارسازی پروژه، ماژول صورتجلسه سازمانی، … (+18)
- عمل‌ها: `addPermissionGanttViewer` `removePermissionGanttViewer` `setAutomationMode` `showProjectAutomationsModal` `toggleViewAutomationExamples`
- فیلدها: `advanced.advanced_minutes` `advanced.advanced_support_automation` `advanced.advanced_support_gantt`

### `projects/partial/partial-modal-project-advanced-features-task-templates`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/modal-project-advanced-features`؛ داخل قالب `tasks/modal-new-project`
- متن‌ها: (آخرین: )، استفاده:، افزودن الگو، انجام‌دهنده:، بدون مهلت، برای شروع، روی دکمه، حذف الگو، روز بعد، فهرست الگوهای وظیفه، مهلت:، نامشخص، هیچ الگویی برای وظایف تعریف نشده است، ویرایش الگو، پیوست‌ها:، چک‌لیست:، کلیک کنید تا اولین الگوی خود را بسازید.
- عمل‌ها: `addNewTaskTemplate` `editTaskTemplate` `removeTaskTemplate`
- راهنماها: حذف الگو، ویرایش الگو

### `projects/partial/project-pane`

- منبع: views/ + embedded
- استفاده: `service:AppProjectsManager / close / modal/panel`؛ داخل قالب `projects/projects`
- متن‌ها: اعضا:، تنظیمات پروژه، جلسه آنلاین
- عمل‌ها: `callDialog` `editProject` `showProjectsList` `startChat`
- راهنماها: تنظیمات پروژه
- کنترلر: `AppProjectPaneController`
- زیرقالب: `projects/partial/pane/project-statistics`

### `projects/partial/project_dialog_summary_details`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / link / directive/other`
- متن‌ها: انجام شده: % درصد، باقیمانده: % درصد، دارای تاخیر: % درصد، دارای پیشرفت: % درصد، کارهای انجام شده: مورد، کارهای بدون زمان: مورد، کارهای دارای تاخیر: مورد، کارهای دارای زمان: مورد
- عمل‌ها: `showTasks`
- راهنماها: انجام شده: %{{status_done_percent \| persian_digits_with_zero}} درصد، باقیمانده: %{{status_remain_percent \| persian_digits_with_zero}} درصد، دارای تاخیر: %{{status_overdue_percent \| persian_digits_with_zero}} درصد، دارای پیشرفت: %{{status_partial_completed_percent \| persian_digits_with_zero}} درصد، کارهای انجام شده: {{status_done \| persian_digits_with_zero}} مورد، کارهای بدون زمان: {{status_no_time \| persian_digits_with_zero}} مورد، کارهای دارای تاخیر: {{status_overdue \| persian_digits_with_zero}} مورد، کارهای دارای زمان: {{status_with_time \| persian_digits_with_zero}} مورد

### `projects/partial/project_dialog_summary_details_modal`

- منبع: views/ + embedded
- استفاده: `service:AppTasksManager / cancel / modal/panel`
- متن‌ها: بازگشت، وضعیت پیشرفت پروژه، وظایف لیست:
- عمل‌ها: `cancel`
- کنترلر: `AppTasksController`
- زیرقالب: `tasks/project-viewer-statistics`

### `projects/projects`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.projects`؛ `service:IdleManager / start / state`
- متن‌ها: در حال بارگذاری، هنوز پیغامی وجود ندارد ...
- عمل‌ها: `gotoRepliedBaseMessage`
- کنترلر: `AppImController` `AppTasksController` `ChatViewCtrl`
- زیرقالب: `chat/chat-input` `chat/chat-pinned-message-viewer` `chat/chat-viewer` `projects/calendar/calendar-viewer` `projects/gantt/gantt-viewer` `projects/kanban-viewer` `projects/partial/chat-header-project` `projects/partial/project-pane` `projects/projects-list` `tasks/project-viewer`

### `projects/projects-list`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/projects`
- متن‌ها: اتمام گروه‌بندی، انتقال اطلاعات (Import) وظایف به میزیتو، ایجاد پروژه، ایجاد پروژه جدید، تبدیل وضعیت پروژه‌ها به خوانده شده، تعداد پروژه‌ها:، مانیتورینگ، مانیتورینگ پروژه‌ها، مدیریت گروه‌بندی پروژه‌ها، همه پروژه‌ها، پروژه جدید، پروژه‌ها
- عمل‌ها: `$mdMenu.open` `dialog_filter='';` `importProjectFromFile` `markAllAsSeen` `null` `showMonitoringProjectsPage` `showSelectUsersForNewGroupChat` `toggleEditProjectGroups` `toggleProjectLabelSelect` `toggleProjectLabelSelectOff`
- فیلدها: `dialog_filter`
- راهنماها: فیلتر عنوان پروژه ...، تبدیل وضعیت پروژه‌ها به خوانده شده
- کنترلر: `AppImDialogsController`
- زیرقالب: `projects/partial/partial-dialog`

### `projects/task_template/modal-task-template-editor`

- منبع: views/ + embedded
- استفاده: `service:AppTaskTemplatesManager / cancel / modal/panel`
- متن‌ها: : خودم، : نامشخص، افراد مجاز جهت تأیید نهایی وظیفه:، افزودن توضیحات، افزودن مسؤول انجام، انتخاب، انصراف، این فیلد الزامی است.، بدون یادآور پیش‌فرض، برچسب، برچسب‌ها: +، برچسب‌های مرتبط، تعیین فرد مجاز جهت تأیید نهایی وظیفه، توضیحات، خودم، روز بعد از ایجاد وظیفه، زمان یادآور پیش‌فرض (بر حسب روز بعد از ایجاد)، عنوان الگو، فقط افراد مجاز می‌توانند وظیفه را تأیید کنند، لیست بورد:، مسؤول انجام، مهلت پیش‌فرض، نامشخص، وزن پیش‌فرض:، پیوست فایل، … (+1)
- عمل‌ها: `addAssignee` `addAttachment` `addChecklistItem` `cancel` `clearDefaultDue` `removeAssignee` `removeAttachment` `removeChecklistItem` `saveTemplate` `showDescriptionField` `showKanbanBoardSelector` `showLabelSelector` `showUserSelector` `toggleDefaultDueEdit` `toggleResponsibleEnable` `toggleResponsibleUser` `toggleShowChecklist`
- فیلدها: `item.title` `new_checklist.title` `template.is_active` `template.notes` `template.title` `template.weight_default`
- راهنماها: توضیحات مربوط به الگو...، عنوان چک لیست، چک لیست: عنوان جدید...، تعیین فرد مجاز جهت تأیید نهایی وظیفه فقط افراد مجاز می‌توانند وظیفه را تأیید کنند، مسؤول انجام، افزودن مسؤول انجام، برچسب‌های مرتبط، زمان یادآور پیش‌فرض (بر حسب روز بعد از ایجاد)، پیوست فایل، چک لیست

## `sales/` (13)

### `sales/customer-pane-sales`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `crm/customer-pane`
- متن‌ها: (هنوز فرصتی برای این مشتری ثبت نشده است.)، سند مالی جدید، فرصت باز، فرصت فروش جدید، فرصت ناموفق، فروش موفق
- عمل‌ها: `newDeal` `newPayment` `toggleShowDeals` `toggleShowPayments`

### `sales/deals-inbox-viewer`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `sales/monitoring-deals`
- متن‌ها: احتمال فروش، ارزش فروش:، ارزش وزنی فروش:، تومان

### `sales/modal-new-deal`

- منبع: views/ + embedded
- استفاده: `service:AppDealsManager / cancel / modal/panel`
- متن‌ها: ( ) توسط:، احتمال موفقیت، ارزش با ضریب احتمال، ارزش فرصت (تومان)، اطلاعات فرصت، انصراف، این فیلد الزامی است.، برچسب‌ها، تاریخ فاکتور/قرارداد، تغییر، توضیحات، ثبت اطلاعات مشتری جدید، سابقه تغییرات فرصت، عدم موفقیت، عنوان فرصت، مسؤول پیگیری، موفقیت کامل، پیوست، ۱۰ درصد، ۲۰ درصد، ۴۰ درصد، ۶۰ درصد، ۷۵ درصد، ۹۰ درصد
- عمل‌ها: `addFile` `addNewCustomer` `cancel` `changeTrackingUser` `createDeal` `removeAttachment` `selectHistory` `setProbability` `showChangesHistory` `showLabelSelector`
- فیلدها: `deal.comments` `deal.customer_user` `deal.invoice_date` `deal.price` `deal.probability` `deal.title`
- راهنماها: مشتری
- عناصر سفارشی: `md-persian-datepicker`

### `sales/modal-new-payment`

- منبع: views/ + embedded
- استفاده: `service:AppPaymentsManager / cancel / modal/panel`
- متن‌ها: ( ) توسط:، ابطال پرداخت، احتمالی، انصراف، ایجاد، بازیابی از سابقه، برچسب‌ها، تاریخ، دریافت، سابقه تغییرات سند مالی، سند پرداختی / دریافتی، شرح سند، مبلغ (تومان)، نقدی، نوع، پرداخت، پیوست، چک
- عمل‌ها: `addFile` `cancel` `createPayment` `removeAttachment` `selectHistory` `showChangesHistory` `showLabelSelector`
- فیلدها: `payment.comments` `payment.date` `payment.is_cashed` `payment.price` `payment.type` `payment.type2`
- راهنماها: —
- عناصر سفارشی: `md-persian-datepicker`

### `sales/monitoring-deals`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `crm/crm`
- متن‌ها: احتمال مبلغ فروش:، فیلتر، فیلتر نمایش فرصت‌های فروش، مشاهده، هنوز فرصت فروشی ثبت نکرده‌اید. در پرونده مشتریان می‌توانید، فرصت‌های فروش متناسب را ثبت نمایید.
- عمل‌ها: `showDeals` `toggleFilterOptions`
- کنترلر: `AppDealsMonitoringController`
- زیرقالب: `sales/deals-inbox-viewer` `sales/partial-monitoring-deals-filter`

### `sales/monitoring-payments`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `crm/crm`
- متن‌ها: درآمد احتمالی، درآمد قطعی، درآمد معوقه، فیلتر نمایش اسناد مالی، مشاهده، نمایش همزمان در جدول، نمودار مالی، پرداختی احتمالی، پرداختی قطعی
- عمل‌ها: `getReportDetails` `showAll` `showAllCharts` `toggleFilterOptions`
- کنترلر: `AppPaymentsMonitoringController`
- زیرقالب: `sales/partial-monitoring-payments-all-chart` `sales/partial-monitoring-payments-all-table` `sales/partial-monitoring-payments-details` `sales/partial-monitoring-payments-filter`

### `sales/partial-deal-card`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / link / directive/other`
- متن‌ها: مالی، ویرایش، ویرایش شد
- عمل‌ها: `showCustomer` `showDeal` `showDealPayments`
- راهنماها: --> {{deal.status_title}} --> <!--

### `sales/partial-monitoring-deals-filter`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `sales/monitoring-deals`
- متن‌ها: انتخاب، انصراف، داشتن برچسب، فیلتر، فیلتر نمایش فرصت‌های فروش، مسؤول پیگیری، نامشخص، نداشتن برچسب
- عمل‌ها: `doFilter` `filter.labels=[]` `filter.labels_not=[]` `filterSelectLabels` `filterSelectLabelsNot` `filterSelectTrackingUser` `filterSelectTrackingUserRemove` `toggleFilterOptions`

### `sales/partial-monitoring-payments-all-chart`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `sales/monitoring-payments`
- متن‌ها: نمایش در یک نمودار، نمودارهای مالی
- فیلدها: `all_in_one_chart`
- کنترلر: `AppPaymentsMonitoringAllController` `AppPaymentsMonitoringChartsController`

### `sales/partial-monitoring-payments-all-table`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `sales/monitoring-payments`
- متن‌ها: درآمد قطعی (تومان)، درآمد معوقه / احتمالی (تومان)، سال، سند مالی برای این گزارش موجود نمی‌باشد. «اسناد مالی در پرونده مشتری ثبت می‌شوند»، ماه، پرداختی احتمالی (تومان)، پرداختی قطعی (تومان)، گزارش مالی
- کنترلر: `AppPaymentsMonitoringAllController`

### `sales/partial-monitoring-payments-details`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `sales/monitoring-payments`
- متن‌ها: سند مالی برای این گزارش موجود نمی‌باشد. «اسناد مالی در پرونده مشتری ثبت می‌شوند»، مشاهده جزئیات
- عمل‌ها: `showDetails` `toggleShowYearInfo`
- کنترلر: `AppPaymentsMonitoringDetailsController`

### `sales/partial-monitoring-payments-filter`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `sales/monitoring-payments`
- متن‌ها: انتخاب، انصراف، داشتن برچسب، فیلتر، فیلتر نمایش اسناد مالی، نداشتن برچسب
- عمل‌ها: `doFilter` `filter.labels=[]` `filter.labels_not=[]` `filterSelectLabels` `filterSelectLabelsNot` `toggleFilterOptions`

### `sales/partial-payment-card`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / showCustomer / directive/other`
- متن‌ها: ویرایش، ویرایش شد
- عمل‌ها: `showCustomer` `showPayment`
- راهنماها: —

## `search/` (1)

### `search/search`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.search`؛ صفحه‌ی `ws.bookmarks`؛ `service:IdleManager / None / state`
- متن‌ها: در، نامه‌ها، نمایش نتایج بیشتر، وظایف، وظایف تکمیل شده، پرونده مشتریان، گفتگوها
- عمل‌ها: `chatShowMore` `customersShowMore` `inboxShowMore` `tasksCompletedShowMore` `tasksShowMore`
- کنترلر: `AppSearchController`

## `support/` (8)

### `support/admin/support-chat-input`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `support/admin/support_admin`
- متن‌ها: این گفتگو توسط خاتمه داده شده است؛ نیازی به ارسال پیام برای خاتمه گفتگو نیست.، این گفتگو در اختیار است.، در حال ویرایش پیام، زمان خاتمه:، پاسخ به پیام
- عمل‌ها: `addFile` `cancelEditMessage` `cancelReply` `sendDraftMessage` `showSupportEmojiPicker`
- فیلدها: `draftMessage.message`
- راهنماها: {{editingMessage ? 'ویرایش پیام...' : 'متن خود را بنویسید...'}}

### `support/admin/support-chat-viewer`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `support/admin/support_admin`
- متن‌ها: بازخورد مثبت مشتری، در حال حذف...، در حال ویرایش...، مشاهده و پیگیری بازخورد منفی
- عمل‌ها: `deleteMessage` `openMessageFeedback` `scrollToReply` `setReplyMessage` `startEditMessage`
- راهنماها: بازخورد مثبت مشتری، مشاهده و پیگیری بازخورد منفی

### `support/admin/support-dialog-list`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `support/admin/support_admin`
- متن‌ها: بازخورد منفی نیازمند بررسی، بازخوردها، بیشتر...، جستجوی پیام‌ها، پیام‌های بدون پاسخ
- عمل‌ها: `dialog_filter='';` `loadMore` `null` `selectDialog` `toggleFeedbackMonitorPane` `toggleFilterUnResponseDialogs` `toggleShowSearchPane`
- فیلدها: `dialog_filter`
- راهنماها: نام \| میزکار \| شماره همراه، {{isDialogSupportLockMine(dialog) ? 'قفل شده توسط شما' : 'قفل شده توسط همکار دیگر'}}، بازخورد منفی نیازمند بررسی، بازخوردها، جستجوی پیام‌ها، پیام‌های بدون پاسخ

### `support/admin/support-feedback-monitor`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `support/admin/support_admin`
- متن‌ها: آمار پشتیبان‌ها، ارزیابی عملکرد، ارزیابی عملکرد پشتیبانی، از صف نیازمند بررسی خارج شد، انتخاب، انصراف، بازخورد ثبت‌شده، بازخوردها، بازه دلخواه، بازه زمانی، بازه گزارش، بازگشایی، بازگشایی شد، برای این انتخاب، یادداشت داخلی الزامی است.، بررسی را شروع کرد، بررسی را نهایی کرد، بررسی‌شده، بررسی‌شده توسط، بیشتر، تعداد رأی‌های مثبت فعلی برای پاسخ‌های ارسال‌شده در دوره، تعداد مواردی که مدیر «عملکرد نیازمند اصلاح است» تأیید کرده است، ثبت، ثبت نتیجه، در آمار منفی پشتیبان، در حال بررسی، … (+45)
- عمل‌ها: `clearFeedbackMonitorDateRange` `clearFeedbackMonitorFilters` `clearFeedbackMonitorSupportUser` `closeFeedbackMonitorFilters` `closeFeedbackMonitorPane` `gotoFeedbackMessage` `item.show_activities=!item.show_activities` `item.show_review_form=false` `loadFeedbackMonitor` `reopenFeedbackReview` `resolveFeedbackReview` `selectFeedbackMonitorDateRange` `selectFeedbackMonitorSupportUser` `setFeedbackMonitorMode` `setFeedbackMonitorStatus` `setFeedbackReportPeriod` `showResolveFeedbackReview` `show_feedback_supporter_stats=!show_feedback_supporter_stats` `startFeedbackReview` `toggleFeedbackMonitorFilters`
- فیلدها: `feedback_monitor_filter.dissatisfaction_reason` `feedback_monitor_filter.reason` `feedback_monitor_filter.review_result` `item.dissatisfaction_reason_draft` `item.review_note_draft` `item.review_result_draft`
- راهنماها: فیلترها

### `support/admin/support-search-content`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `support/admin/support_admin`
- متن‌ها: انتخاب، بازه زمانی، بستن، بیشتر...، جستجو، فیلترها، نتیجه‌ای پیدا نشد.، نوع پیام، همه، پاک کردن فیلترها، پشتیبان، پشتیبان‌ها، کاربران
- عمل‌ها: `clearContentSearchDateRange` `clearContentSearchFilters` `clearContentSearchSupportUser` `content_search_string=''` `gotoSearchMessage` `loadMoreSearchContent` `searchContents` `selectContentSearchDateRange` `selectContentSearchSupportUser` `toggleContentSearchFilters` `toggleShowSearchPane`
- فیلدها: `content_search_filter.message_type` `content_search_string`
- راهنماها: {{'search' \| translate}}، بستن، فیلترها

### `support/admin/support_admin`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.support`؛ `service:IdleManager / None / state`
- متن‌ها: «دمو»، آخرین بازخورد، آزاد کردن قفل، این گفتگو بدون ارسال پاسخ خاتمه می‌یابد، برای شروع مکالمه یک مخاطب را انتخاب کنید، تمدید قفل برای ۳ دقیقه، حس اخیر مشتری:، خاتمه گفتگو، در اختیار شما، در حال بارگذاری، سابقه بازخورد مشتری، طرح، طرح رایگان، علت‌های اخیر نارضایتی، قفل گفتگو، مالک میزکار، مثبت، مدیر میزکار، مشاهده میزکار، مشاهده کاربر، منفی، منقضی شده ·، مهمان، نرخ رضایت، نیازمند اصلاح، … (+4)
- عمل‌ها: `closeSupportDialogResponse` `copySupportUserName` `extendSupportDialogLock` `lockSupportDialog` `showMonitorPage` `showMonitorUserPage` `showUserPhone` `show_mobile_support_details=!show_mobile_support_details` `show_support_feedback_context=!show_support_feedback_context` `unlockSupportDialog` `unselectDialog`
- راهنماها: آزاد کردن قفل، این گفتگو بدون ارسال پاسخ خاتمه می‌یابد، تمدید قفل برای ۳ دقیقه، حس اخیر مشتری: {{getCustomerSentimentTitle()}}، مشاهده میزکار، مشاهده کاربر، کپی نام کاربر
- کنترلر: `AppAdminSupportChatController`
- زیرقالب: `support/admin/support-chat-input` `support/admin/support-chat-viewer` `support/admin/support-dialog-list` `support/admin/support-feedback-monitor` `support/admin/support-search-content`

### `support/new_suggestion`

- منبع: views/ + embedded
- استفاده: `service:AppSupportManager / close / modal/panel`
- متن‌ها: ارسال درخواست مشاوره، انصراف، این فیلد الزامی است.، درخواست مشاوره، لطفاً موضوع مشاوره خود را اعلام بفرمایید تا در اسرع وقت یکی از کارشناسان میزیتو با شما تماس بگیرند.، متن درخواست، موضوع مشاوره
- عمل‌ها: `close` `send`
- فیلدها: `suggestion.content` `suggestion.subject`

### `support/support_user`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: (اختیاری)، انصراف، اگر مایلید، دلیل این بازخورد را هم بگویید.، بازخورد شما ثبت شده است، بازخورد منفی، حذف رأی، در حال بارگذاری، در حال حذف...، در حال ویرایش پیام، در حال ویرایش...، راهنمای میزیتو، سلام، لطفاً منتظر بمانید. کاربران پشتیبانی در اسرع وقت پاسخ شما را خواهند داد.، هر سوالی داری بپرس، یا نظرت رو با ما در میون بذار، ویدیوهای آموزشی، پاسخ به پیام
- عمل‌ها: `addFile` `cancelEditMessage` `cancelReply` `cancelSupportFeedbackDetails` `close` `deleteMessage` `removeSupportFeedback` `scrollToReply` `sendDraftMessage` `setReplyMessage` `setSupportFeedback` `setSupportFeedbackReason` `showHelp` `showHelpVideos` `showSupportEmojiPicker` `startEditMessage` `submitSupportFeedback`
- فیلدها: `draftMessage.message` `historyMessage.feedback_comment_draft`
- راهنماها: {{editingMessage ? 'ویرایش پیام...' : 'متن خود را بنویسید...'}}، توضیح کوتاه (اختیاری)، {{historyMessage.feedback && historyMessage.feedback.value == 1 ? 'برداشتن بازخورد مثبت' : 'مفید بود'}}
- کنترلر: `AppSupportChatController`

## `tasks/` (27)

### `tasks/color-selector`

- منبع: views/ + embedded
- استفاده: `service:AppLabelManager / setColor / modal/panel`
- متن‌ها: انتخاب رنگ
- عمل‌ها: `setColor`

### `tasks/done-viewer`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.tasks.done`؛ `service:IdleManager / start / state`
- متن‌ها: انتخاب، انصراف، ایجاد کننده، بیشتر...، در حال بارگذاری، فیلتر، فیلتر نمایش، فیلتر نمایش وظایف، مسؤول انجام، نامشخص، وظیفه‌ای در این بخش وجود ندارد، پروژه (دسته‌بندی)، چاپ نتایج، کارهای انجام شده بر اساس زمان
- عمل‌ها: `doFilter` `filterDoneClearAssignee` `filterDoneClearOwner` `filterDoneClearProject` `filterDoneSelectAssignee` `filterDoneSelectOwner` `filterDoneSelectProject` `loadMore` `printDoneResult` `showTask` `toggleFilterDoneOptions`
- راهنماها: —
- کنترلر: `AppTasksDoneController`

### `tasks/inbox-viewer`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.tasks.inbox`؛ `service:IdleManager / start / state`؛ داخل قالب `monitoring/monitoring_user_tasks`
- متن‌ها: —
- کنترلر: `AppTasksInboxController`
- زیرقالب: `tasks/partial-tasks-viewer` `tasks/partial_inbox_viewer_header`

### `tasks/label-viewer`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.tasks.label`؛ `service:IdleManager / start / state`
- متن‌ها: مشاهده مشخصات
- عمل‌ها: `$mdMenu.open` `editLabelInfo`
- کنترلر: `AppTasksInboxController`
- زیرقالب: `tasks/partial-tasks-viewer` `tasks/partial_inbox_viewer_header`

### `tasks/modal-form-request-view`

- منبع: views/ + embedded
- استفاده: `service:AppTasksManager / showSeenDetails / modal/panel`
- متن‌ها: آخرین تغییر:، ارسال پیام جدید و یا ارسال فایل و مستندات، افزودن پیوست فایل، انجام‌شده، این درخواست تکمیل شده اما در مرحله پایانی جریان کار نیست.، برچسب‌ها:، بستن، بسته شده خارج از جریان، تأیید نهایی:، تاریخ ثبت:، تاریخچه وضعیت، ثبت و ارسال پیام، ثبت پیام جدید، ثبت‌کننده:، در انتظار بررسی، در حال پاسخ به پیام:، درج گزارش و یا نظر شما ...، زمان رسیدگی بعدی:، شماره پیگیری:، شکلک، فرم درخواست، متن گزارش، مراحل بررسی درخواست، مرحله فعلی:، مسؤول فعلی:، … (+15)
- عمل‌ها: `addCommentFile` `cancel` `clearReply` `closeNewCommentUI` `copyTrackingCode` `gotoComment` `openNewCommentUI` `removeCommentAttachment` `removeMention` `replyComment` `sendNewComment` `showEmojiPicker` `showMentionSelector` `showWorkflowDiagram`
- فیلدها: `task.newComment`
- راهنماها: {{'set_task_progress_comment_placeholder' \| translate}}، ارسال پیام جدید و یا ارسال فایل و مستندات، افزودن پیوست فایل، این درخواست تکمیل شده اما در مرحله پایانی جریان کار نیست.، شکلک، منشن، نمایش نمودار جریان کار درخواست، کپی شماره پیگیری
- عناصر سفارشی: `my-automate-button` `my-task-custom-params-viewer`

### `tasks/modal-new-project`

- منبع: views/ + embedded
- استفاده: `service:AppProjectsManager / selectHistory / modal/panel`
- متن‌ها: آرشیو دسته‌بندی، انصراف، ایجاد، بازیابی از سابقه، بستن، سابقه تغییرات دسته‌بندی، مشخصات دسته‌بندی
- عمل‌ها: `archiveProject` `cancel` `createProject` `showChangesHistory`
- راهنماها: —
- زیرقالب: `projects/partial/partial-modal-project-advanced-features-task-templates` `tasks/partial/partial-modal-new-project-main`

### `tasks/modal-new-task`

- منبع: views/ + embedded
- استفاده: `service:AppTasksManager / showSeenDetails / modal/panel`
- متن‌ها: * این وظیفه توسط یکی از اعضا، انجام شده است و منتظر تایید نهایی مجاز می‌باشد.، : خودم، : نامشخص، ? 'فرم درخواست'، «ایجاد شده به صورت خودکار»، «منتظر تأیید»، آخرین بروزرسانی:، استفاده از الگوی وظیفه، استفاده شده در گانت، افزودن توضیحات، افزودن مسؤول انجام، افزودن پیوست فایل، انتخاب، انتخاب کاربر، انجام شده توسط، انصراف، ایجاد، ایجاد وظیفه، این فیلد الزامی است.، این وظیفه، به وظایف دیگری در گانت وابسته می‌باشد، بازگشت، بازیابی وظیفه، بدون زمان یادآوری، برچسب، برچسب‌ها: +، … (+63)
- عمل‌ها: `$mdMenu.open` `addAssignee` `addCommentFile` `addFile` `cancel` `cancelTaskRepeat` `clearReply` `cloneTask` `convertToDuplicate` `copyTaskLink` `copyTrackingCode` `createTask` `deleteComment` `editComment` `editDeadline` `editDeadlineStart` `gotoComment` `gotoCustomerMessage` `gotoMinuteMessage` `gotoProjectPage` `openFormRequestView` `printTask` `removeAlarmDate` `removeAssignee` `removeAttachment` `removeCommentAttachment` `removeCopyUser` `removeDeadline` `removeDeadlineStart` `removeFromGantt` `removeMention` `removeTask` `removeTaskUndo` `replyComment` `sendNewComment` `setEditMode` `setTaskDone` `setTaskUnDone` `showCalendar` `showCustomParamValuesHistory` `showDescriptionField` `showEmojiPicker` `showHistory` `showKanbanBoardSelector` `showLabelSelector` `showMentionSelector` `showMultipleCopyUserSelector` `showProjectSelector` `showSeenDetails` `showTask` … (+8)
- فیلدها: `task.deadline` `task.deadline_start` `task.insertToChatGroup` `task.newComment` `task.notes` `task.title` `task.weight`
- راهنماها: {{'add_task_description_here' \| translate}}، {{'set_task_progress_comment_placeholder' \| translate}}، تعیین فرد مجاز جهت تأیید نهایی وظیفه فقط افراد مجاز می‌توانند وظیفه را تأیید کنند، تنظیمات وظیفه، افزودن مسؤول انجام، افزودن پیوست فایل، برچسب‌های مرتبط، تعداد مشاهده وظیفه، حذف گزارش، شکلک، مشاهده گروه پروژه، منشن، نمودار گردش جریان کار، ویرایش گزارش، پاسخ به گزارش، … (+3)
- عناصر سفارشی: `md-persian-datepicker` `my-automate-button` `my-automation-badge` `my-task-custom-params-viewer`
- زیرقالب: `tasks/partial/partial-model-new-task-checklist`

### `tasks/modal-task-history`

- منبع: views/ + embedded
- استفاده: `service:AppTasksManager / close / modal/panel`
- متن‌ها: بستن، در حال بارگذاری سابقه تغییرات...، سابقه تغییرات وظیفه، فقط سابقه گردش‌کار خودکار، مرتب‌سازی:، هیچ سابقه‌ای برای این وظیفه یافت نشد.
- عمل‌ها: `close` `toggleSortOrder`
- فیلدها: `showOnlyAutomated`
- راهنماها: بستن، مرتب‌سازی: {{ sortOrder === 'asc' ? 'قدیمی‌تر اول' : 'جدیدتر اول' }}

### `tasks/modal-task-link-share-dialog`

- منبع: views/ + embedded
- استفاده: `service:AppTasksManager / copy / modal/panel`
- متن‌ها: از لینک زیر جهت اشتراک‌گذاری این وظیفه می‌توانید استفاده نمایید:، کپی
- عمل‌ها: `copy` `ok`

### `tasks/modal-update-comment-text`

- منبع: views/ + embedded
- استفاده: `service:AppMinutesAdvancedManager / update / modal/panel`؛ `service:AppTasksManager / update / modal/panel`
- متن‌ها: انصراف، ویرایش متن گزارش
- عمل‌ها: `cancel` `update`
- فیلدها: `newMessage`

### `tasks/outbox-viewer`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.tasks.outbox`؛ `service:IdleManager / start / state`
- متن‌ها: —
- کنترلر: `AppTasksInboxController`
- زیرقالب: `tasks/partial-tasks-viewer` `tasks/partial_inbox_viewer_header`

### `tasks/partial-inbox-sort-selection`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `monitoring/monitoring_tasks`؛ داخل قالب `tasks/partial_inbox_viewer_header`؛ داخل قالب `tasks/project-viewer`
- متن‌ها: آخرین تغییرات، زمان ایجاد، مرتب‌سازی نمایش وظایف، مرتب‌سازی:، مهلت انجام / زمان یادآوری، پیش‌فرض
- عمل‌ها: `$mdMenu.open` `setSortType`
- راهنماها: مرتب‌سازی نمایش وظایف

### `tasks/partial-task-filter`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `tasks/partial-tasks-viewer`
- متن‌ها: انتخاب، انجام شده، انجام نشده، انصراف، ایجاد کننده، بازه زمانی، برچسب‌ها، شماره پیگیری فرم، فیلتر، فیلتر نمایش وظایف، لیست بورد، متن، مسؤول انجام، نامشخص، وضعیت انجام، پرونده مشتری
- عمل‌ها: `doFilter` `filter.date_range` `filter.dialog` `filter.labels=[]` `filterClearAssignee` `filterClearOwner` `filterClearProjectList` `filterSelectAssignee` `filterSelectDateRange` `filterSelectDialog` `filterSelectLabels` `filterSelectOwner` `filterSelectProjectList` `toggleFilterOptions`
- فیلدها: `filter.done_status` `filter.form_request_tracking_code` `filter.title`

### `tasks/partial-task-repeat-display`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / link / directive/other`
- متن‌ها: وظیفه تکرارشونده
- راهنماها: وظیفه تکرارشونده

### `tasks/partial-task-row`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / toggleViewCommentsLayout / directive/other`
- متن‌ها: «منتظر تأیید»، تغییر کرد، جدید، حذف از لیست پیگیری، شما مسؤول تایید نهایی این وظیفه هستید، فرم، مهلت:
- عمل‌ها: `removeTaskFromTracking` `setTaskDone` `setTaskUnDone` `showTask` `toggleViewCommentsLayout`
- راهنماها: حذف از لیست پیگیری، شما مسؤول تایید نهایی این وظیفه هستید

### `tasks/partial-tasks-viewer`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `tasks/inbox-viewer`؛ داخل قالب `tasks/label-viewer`؛ داخل قالب `tasks/outbox-viewer`؛ داخل قالب `tasks/project-viewer`؛ داخل قالب `tasks/project-viewer-statistics`
- متن‌ها: ( مورد)، بر اساس آخرین تغییر وظایف، بر اساس آخرین زمان ایجاد، بر اساس زمان وظیفه (فقط وظایف دارای زمان)، بیشتر...، در حال بارگذاری، وظایف آینده، وظایف امروز، وظایف انجام شده، وظایف بدون زمان، وظایف جاری، وظایف جدید، وظایف دارای تاخیر، وظایف منتظر تأیید دیگران، وظایف منتظر تأیید من، وظایفی که برای انجام آن‌ها یک بازه زمانی و مهلت انجام تعیین شده است، وظیفه‌ای برای این کاربر وجود ندارد، وظیفه‌ای در این بخش وجود ندارد
- عمل‌ها: `loadMore`
- راهنماها: —
- زیرقالب: `tasks/partial-task-filter`

### `tasks/partial/partial-modal-new-project-main`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `tasks/modal-new-project`
- متن‌ها: ( ) توسط:، افزودن عضو...، انتخاب رنگ، ایجاد شده است و فقط از طریق همان پروژه امکان ویرایش را خواهید داشت.، ایجاد پروژه، این دسته‌بندی از طریق، این فیلد الزامی است.، برای مثال: امور فروش، سابقه تغییرات دسته‌بندی، عنوان دسته‌بندی، قابل مشاهده برای
- عمل‌ها: `!project.dialog` `selectHistory`
- فیلدها: `project.members` `project.title`
- راهنماها: {{'add_member_dot' \| translate}}، {{'new_project_sample' \| translate}}
- زیرقالب: `partial/partial-chip-user-selector` `partial/partial-chip-user-template`

### `tasks/partial/partial-model-new-task-checklist`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `tasks/modal-new-task`
- متن‌ها: —
- عمل‌ها: `addChecklistItem` `checklistCheckedChanged` `removeChecklistItem`
- فیلدها: `item.checked` `item.title` `new_checklist.title`
- راهنماها: عنوان چک لیست، چک لیست: عنوان جدید...

### `tasks/partial_inbox_viewer_header`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `tasks/inbox-viewer`؛ داخل قالب `tasks/label-viewer`؛ داخل قالب `tasks/outbox-viewer`؛ داخل قالب `tasks/project-viewer`
- متن‌ها: ایجاد وظیفه، برای ایجاد فرم جدید به مسیر زیر بروید:، تنظیمات پروژه پیشرفته ← ماژول خودکارسازی ← فرم‌های درخواست، در حال بارگذاری فرم‌ها...، فیلتر نمایش وظایف، هیچ فرم درخواستی تعریف نشده است، چاپ نتایج، کارتابل وظایف
- عمل‌ها: `newTask` `openFormRequest` `printResult` `toggleFilterOptions` `toggleFormMenu`
- راهنماها: —
- زیرقالب: `tasks/partial-inbox-sort-selection`

### `tasks/project-files-viewer`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `tasks/project-viewer`
- متن‌ها: بارگزاری مجدد، بازگشت به وظایف، بیشتر...، تصاویر، جستجو عنوان فایل، در حال بارگذاری، فایلی بر اساس فیلتر انتخاب شده برای این پروژه وجود ندارد، فایلی برای وظایف این پروژه وجود ندارد، فایل‌ها، فایل‌های صوتی، فایل‌های پیوست شده به وظایف پروژه، فیلتر:، فیلم‌ها، مشاهده وظیفه
- عمل‌ها: `loadMore` `refresh` `setFilter` `showTask` `show_project_files.active`
- راهنماها: بارگزاری مجدد، تصاویر، جستجو عنوان فایل، فایل‌ها، فایل‌های صوتی، فیلم‌ها
- کنترلر: `AppProjectFilesController`

### `tasks/project-viewer`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.tasks.project`؛ `service:IdleManager / start / state`؛ داخل قالب `projects/projects`
- متن‌ها: ایجاد وظیفه، بدون انجام دهنده، فیلتر، مشاهده فایل‌ها، مشاهده مشخصات، نمایش:، چاپ نتایج، کارهای انجام شده، کارهای انجام نشده، کارهای بدون زمان، کارهای دارای تاخیر، کارهای دارای زمان، کارهای دارای پیشرفت، کارهای دیگران، کارهای من
- عمل‌ها: `$mdMenu.open` `addTaskFromTasksView` `editProjectInfo` `printResult` `show_project_files.active` `toggleFilterOptions`
- فیلدها: `only_project_filter.type`
- راهنماها: —
- کنترلر: `AppTasksInboxController`
- زیرقالب: `tasks/partial-inbox-sort-selection` `tasks/partial-tasks-viewer` `tasks/partial_inbox_viewer_header` `tasks/project-files-viewer`

### `tasks/project-viewer-statistics`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `projects/partial/project_dialog_summary_details_modal`
- متن‌ها: —
- کنترلر: `AppTasksInboxController`
- زیرقالب: `tasks/partial-tasks-viewer`

### `tasks/seen/modal-task-seen-details`

- منبع: views/ + embedded
- استفاده: `service:AppTasksManager / close / modal/panel`
- متن‌ها: «برای وظایف قدیمی این امکان غیرفعال است»، آخرین زمانی که هر کاربر این وظیفه را دیده است:، آخرین مشاهده وظیفه، اولین زمانی که هر کاربر این وظیفه را دیده است:، اولین مشاهده وظیفه، ایجاد شده توسط:، بازگشت، زمان ایجاد وظیفه، وضعیت مشاهده وظیفه
- عمل‌ها: `close`
- زیرقالب: `tasks/seen/partial-task-seen-row-details`

### `tasks/seen/partial-task-seen-row-details`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `tasks/seen/modal-task-seen-details`
- متن‌ها: در تاریخ، مشاهده از طریق اشتراک‌گذاری توسط، مشاهده شده از طریق لینک اشتراک‌گذاری
- عمل‌ها: `row.share_link_object_visible`
- راهنماها: مشاهده شده از طریق لینک اشتراک‌گذاری

### `tasks/tasks`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.tasks`؛ `service:IdleManager / start / state`
- متن‌ها: —
- عمل‌ها: `newTask`
- کنترلر: `AppTasksController`
- عناصر سفارشی: `ui-view`

### `tasks/template-selector`

- منبع: views/ + embedded
- استفاده: `service:AppTasksManager / selectTemplate / modal/panel`
- متن‌ها: فیلتر الگوی وظیفه، پروژه:
- عمل‌ها: `selectTemplate` `toggleTemplateInfo`
- فیلدها: `filter`
- راهنماها: {{'search_for_task_templates' \| translate}}

### `tasks/workspace-submenu`

- منبع: views/ + embedded
- استفاده: —
- متن‌ها: انجام شده روزانه، برچسب‌ها، تقویم، دسته‌بندی کارها، وظایف، پیگیری از دیگران، کارهای من
- عمل‌ها: `selectLabelToRoute` `selectProjectToRoute`

## `user/` (5)

### `user/delete_account`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: —
- کنترلر: `AppDeleteAccountController`

### `user/delete_account_request`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: درخواست حذف حساب کاربری، درخواست کد حذف حساب، شماره همراه خود را وارد نمایید، شماره همراه خود را وارد کنید، تا کد تایید حذف حساب کاربری برای شما ارسال شود.
- عمل‌ها: `sendDeleteAccountCodeRequest`
- فیلدها: `username`
- راهنماها: {{'enter_your_phone_number' \| translate}}
- کنترلر: `AppDeleteAccountRequestController`

### `user/delete_account_validation`

- منبع: embedded only (my-include)
- استفاده: —
- متن‌ها: حذف حساب کاربری، در پنل کاربری خود را وارد کنید، درخواست حذف حساب کاربری، دستیار میزیتو، کد ارسال شده توسط، کد تایید
- عمل‌ها: `deleteAccount`
- فیلدها: `validation_code`
- کنترلر: `AppDeleteAccountController`

### `user/user-status-color-selector`

- منبع: views/ + embedded
- استفاده: `service:AppUsersManager / setMode / modal/panel`
- متن‌ها: —
- عمل‌ها: `setMode`

### `user/user-status-selector`

- منبع: views/ + embedded
- استفاده: `service:AppUsersManager / update / modal/panel`
- متن‌ها: انصراف، وضعیت شما:
- عمل‌ها: `cancel` `setStatus` `showModeSelector` `update`
- فیلدها: `status.text`
- راهنماها: آنلاین

## `voice/` (1)

### `voice/voice-recorder`

- منبع: views/ + embedded
- استفاده: `directive:myPeerOnlineStatusLink / showTasks / directive/other`
- متن‌ها: ادامه ضبط پیام، توقف، توقف ضبط، در این نسخه مرورگر شما، قابلیت ضبط پیام صوتی وجود ندارد.، پخش پیام صوتی
- عمل‌ها: `recorder.playbackPause` `recorder.playbackResume` `recorder.startRecord` `recorder.stopRecord` `sendAudio`
- راهنماها: ادامه ضبط پیام، توقف، توقف ضبط، پخش پیام صوتی
- عناصر سفارشی: `ng-audio-recorder` `ng-audio-recorder-analyzer` `ng-audio-recorder-wave-view`

## `workspace/` (34)

### `workspace/change_password`

- منبع: views/ + embedded
- استفاده: `service:AppProfileManager / changePassword / modal/panel`
- متن‌ها: انصراف، تغییر کلمه عبور، تکرار کلمه عبور، کلمه عبور، کلمه عبور فعلی
- عمل‌ها: `changePassword` `close`
- فیلدها: `user.current` `user.password` `user.repassword`
- زیرقالب: `login/partial/partial-password-complexity-hint`

### `workspace/change_phone-number`

- منبع: views/ + embedded
- استفاده: `service:AppProfileManager / update / modal/panel`
- متن‌ها: » را وارد نمایید:، ارسال کد اعتبارسنجی، انصراف، تأیید، تغییر شماره تلفن، جهت تغییر شماره تلفن، لطفاً کلمه عبور حساب کاربری فعلی خود با شماره «، شماره جدید، لطفاً شماره تلفن جدید را وارد نمایید:، کلمه عبور فعلی
- عمل‌ها: `close` `update`
- فیلدها: `user.password` `user.phone_to`

### `workspace/feedback/modal-feedback-a`

- منبع: views/ + embedded
- استفاده: `service:AppProfileManager / snooze / modal/panel`
- متن‌ها: * نظر شما پس از بررسی، با نام شما در سایت رسمی میزیتو (mizito.ir) منتشر خواهد شد.، نظری ندارم، آیا تمایل دارید تیم رسانه‌ای میزیتو جهت معرفی کسب و کار شما در سایت رسمی میزیتو (mizito.ir) با شما مصاحبه داشته باشند؟، ایمیل، این فیلد الزامی است.، اینستاگرام و شبکه‌های اجتماعی، اینفلونسرها، بعداً نظر می‌دهم، بله، بنر تبلیغاتی، ثبت بازخورد، جستجو در اینترنت، خیر، سایر، لطفا طریقه آشنایی با میزیتو را انتخاب بفرمایید، معرفی دیگران، میزیتو در کنار شما هر روز پیشرفت میکنه، یه جمله‌ی خوب برامون بنویسید:، نظرسنجی میزیتو، همایش یا رویداد، پیامک
- عمل‌ها: `close` `noAnswer` `snooze`
- فیلدها: `feedback.acquisition_source` `feedback.answerAdmin[$index]` `feedback.answerUser[$index]` `feedback.myNote` `feedback.wantToIntroduce`

### `workspace/feedback/modal-feedback-intro`

- منبع: views/ + embedded
- استفاده: `service:AppProfileManager / snooze / modal/panel`
- متن‌ها: از همراهی شما سپاسگزاریم.، مشاهده فرم نظرسنجی، نظرسنجی میزیتو
- عمل‌ها: `close`

### `workspace/fix/fix_chat_groups`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.fix_chat_groups`؛ `service:IdleManager / start / state`
- متن‌ها: (انتخاب شده: )، «آرشیو شده»، «ایجادکننده:، «کانال»، آرشیو شده، آرشیو نشده، اصلاح دسترسی گروه‌های گفتگو، افزودن، انتخاب همه، بازیابی از آرشیو، تعداد کل:، جستجو، حذف، دسترسی از فرد، دسترسی به فرد، عدم مشاهده، فیلتر، قابل مشاهده برای، مشاهده اعضا، نامشخص، وضعیت
- عمل‌ها: `filterSelectHasAccess` `filterSelectHasAccessNot` `filterSelectHasAccessNotRemove` `filterSelectHasAccessRemove` `grantAccessToUser` `load` `markAll` `null` `showMembers` `toggleSelect`
- فیلدها: `dialog_filter` `filter.archive_status`
- کنترلر: `AppFixChatGroupsController`

### `workspace/fix/fix_customers`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.fix_customers`؛ `service:IdleManager / start / state`
- متن‌ها: (انتخاب شده: )، «آرشیو شده»، «ایجادکننده:، آرشیو شده، آرشیو نشده، اصلاح دسترسی پرونده مشتریان، افزودن، انتخاب، انتخاب همه، بازیابی از آرشیو، تعداد کل:، جستجو، حذف، داشتن برچسب، دسترسی از فرد، دسترسی به فرد، عدم مشاهده، فیلتر، قابل مشاهده برای، مشاهده اعضا، نامشخص، نداشتن برچسب، وضعیت
- عمل‌ها: `filter.labels=[]` `filter.labels_not=[]` `filterSelectHasAccess` `filterSelectHasAccessNot` `filterSelectHasAccessNotRemove` `filterSelectHasAccessRemove` `filterSelectLabels` `filterSelectLabelsNot` `grantAccessToUser` `load` `markAll` `null` `showMembers` `toggleSelect`
- فیلدها: `dialog_filter` `filter.archive_status`
- کنترلر: `AppFixCustomersController`

### `workspace/fix/fix_group_members`

- منبع: views/ + embedded
- استفاده: `controller:AppFixChatGroupsController / cancel / modal/panel`؛ `controller:AppFixCustomersController / cancel / modal/panel`؛ `controller:AppFixProjectsController / cancel / modal/panel`
- متن‌ها: آرشیو پروژه، افزودن عضو جدید، بازگشت، بازیابی ( ) وظایف آرشیو شده
- عمل‌ها: `addMember` `archiveProject` `cancel` `removeMember` `restoreArchivedTasks`

### `workspace/fix/fix_projects`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.fix_projects`؛ `service:IdleManager / start / state`
- متن‌ها: (انتخاب شده: )، «آرشیو شده»، «ایجادکننده:، آرشیو شده، آرشیو نشده، اصلاح دسترسی پروژه‌ها، افزودن، انتخاب، انتخاب همه، بازیابی ( ) وظایف آرشیو شده، بازیابی از آرشیو، تعداد کل:، جستجو، حذف، دسترسی از فرد، دسترسی به فرد، عدم مشاهده، فیلتر، قابل مشاهده برای، مشاهده اعضا، نامشخص، وضعیت، گروه‌بندی پروژه‌ها
- عمل‌ها: `filter.project_labels=[]` `filterSelectHasAccess` `filterSelectHasAccessNot` `filterSelectHasAccessNotRemove` `filterSelectHasAccessRemove` `filterSelectProjectLabels` `grantAccessToUser` `load` `markAll` `null` `restoreArchiveTasks` `showMembers` `toggleSelect`
- فیلدها: `dialog_filter` `filter.archive_status`
- کنترلر: `AppFixProjectsController`

### `workspace/fix/modal_fix_change_owner`

- منبع: views/ + embedded
- استفاده: `service:AppWorkspaceManager / cancel / modal/panel`
- متن‌ها: * انتقال فقط به فردی مجاز می‌باشد که در حال حاضر در این میزکار مدیر باشد.، * توجه نمایید که بعد از انتقال دیگر شما مالک این میزکار نخواهید بود.، انتخاب کاربر، انتقال مالکیت به کاربر:، انتقال مالکیت میزکار، انصراف، در حال حاضر شما مالک این میزکار با عنوان «
- عمل‌ها: `cancel` `selectUser` `update`

### `workspace/fix/modal_fix_change_user`

- منبع: views/ + embedded
- استفاده: `service:AppFixChangeUserManager / cancel / modal/panel`
- متن‌ها: از کاربر:، انتخاب کاربر، انصراف، به کاربر:، جابجایی کاربر، دسترسی پرونده مشتریان کاربر قدیمی به کاربر جدید منتقل می‌شود، سابقه عملیات، عضویت در گروه‌ها، می‌توانید وضعیت جاری یک کاربر را در بخش های مورد نظر به کاربر جدید منتقل کنید:، وظایف انجام نشده کاربر قدیمی و دسترسی پروژه‌ها و دسته‌بندی‌ها به کاربر جدید منتقل می‌شود، وظایف و پروژه‌ها، پرونده مشتریان، کاربر جدید جایگزین کاربر قدیمی در کلیه گروه‌های گفتگو می‌شود
- عمل‌ها: `cancel` `selectFromUser` `selectToUser` `showHistory` `update`
- فیلدها: `items.customers` `items.groups` `items.tasks`
- راهنماها: سابقه عملیات

### `workspace/fix/modal_fix_change_user_history`

- منبع: views/ + embedded
- استفاده: `service:AppFixChangeUserManager / cancel / modal/panel`
- متن‌ها: از کاربر، بازگشت، به کاربر، زمان، سابقه جابجایی کاربر، عملیات، کاربر مدیر
- عمل‌ها: `cancel`

### `workspace/modal-new-workspace`

- منبع: views/ + embedded
- استفاده: `service:AppWorkspaceManager / create / modal/panel`
- متن‌ها: انتخاب از دفترچه تلفن، انصراف، ایجاد میزِکار جدید، این فیلد الزامی است.، این میزکار یک محیط مستقل از میزکار فعلی شما خواهد بود و، تحت مالکیت و مدیریت شما، جهت دسترسی به امکانات میزیتو، یک میزِکار جدید برای خود ایجاد کنید:، شما در حال ایجاد یک میزکار جدید هستید.، شماره همراه، قرار خواهد گرفت.، میزِکار جدید ایجاد کنید:، نام شرکت و یا تیم، نام همکار، همکاران خود را به میزکار جدید دعوت نمایید:
- عمل‌ها: `addTeammate` `close` `create` `removeTeammate` `showContactSelector`
- فیلدها: `user.email_phone` `user.name` `workspace_name`
- راهنماها: {{'mobile' \| translate}}، {{'teammate_name' \| translate}}

### `workspace/modal-workspace-invoice-dialog`

- منبع: views/ + embedded
- استفاده: `service:AppWorkspaceManager / cancel / modal/panel`
- متن‌ها: انصراف، واریز وجه از طریق کارت به کارت، پرداخت آنلاین
- عمل‌ها: `cancel` `manualPayment` `onlinePayment`

### `workspace/modal_get_workspace_business_type`

- منبع: views/ + embedded
- استفاده: `service:AppWorkspaceManager / close / modal/panel`
- متن‌ها: تمایلی ندارم، حوزه فعالیت، خواهشمند است به منظور دریافت مشاوره و پشتیبانی بهتر، حوزه فعالیت خود را مشخص فرمایید و، دریافت نمایید:، ۱۵ روز اعتبار رایگان
- عمل‌ها: `close` `ok` `selectItem`

### `workspace/modal_invite_new_user`

- منبع: views/ + embedded
- استفاده: `service:AppUsersManager / cancel / modal/panel`
- متن‌ها: \u062F\u0639\u0648\u062A \xAB\u06A9\u0627\u0631\u0628\u0631 \u0645\u0647\u0645\u0627\u0646\xBB، آدرس ایمیل و یا شماره همراه، ارسال دعوتنامه، انتخاب از دفترچه تلفن، انصراف، دعوت عضو جدید، شماره همراه، شناسه کاربر، نام عضو مهمان، نام همکار
- عمل‌ها: `cancel` `sendInvite` `showContactSelector`
- فیلدها: `emailphone` `username`

### `workspace/modal_profile_settings`

- منبع: views/ + embedded
- استفاده: `service:AppProfileManager / emailSendNotificationSwitchChanged / modal/panel`
- متن‌ها: امنیت، انصراف، تغییر کلمه عبور، تنظیمات حساب کاربری، عمومی، نوتیفیکیشن با ایمیل
- عمل‌ها: `cancel` `changePassword` `update`
- زیرقالب: `workspace/profile_tabs/profile_tab_email` `workspace/profile_tabs/profile_tab_info` `workspace/profile_tabs/profile_tab_security`

### `workspace/profile_tabs/profile_tab_email`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `workspace/modal_profile_settings`
- متن‌ها: آدرس ایمیل شما:، ارسال کد اعتبارسنجی به ایمیل، بررسی کد اعتبارسنجی، به ایمیل من ارسال شوند، تغییر آدرس ایمیل، تغییر آدرس ایمیل \| ارسال مجدد کد، نوتیفیکیشن‌های میزیتو
- عمل‌ها: `changeEmail` `checkEmailVerificationCode` `setEmail`
- فیلدها: `profile.email` `profile.email_send_notifications` `profile.email_verification_code`
- راهنماها: آدرس ایمیل شما، کد اعتبارسنجی

### `workspace/profile_tabs/profile_tab_info`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `workspace/modal_profile_settings`
- متن‌ها: * در همه میزکارهایی که عضو هستید، همکارانتان در روز تولد شما باخبر می‌شوند.، آدرس ایمیل:، انتخاب تصویر پروفایل، این فیلد الزامی است.، تاریخ تولد، تغییر شماره تلفن، حذف، حذف تصویر، شماره موبایل:، شناسه کاربر:
- عمل‌ها: `changePhoneNumber` `removePhoto` `setPhoto`
- فیلدها: `profile.birthdate` `profile.firstname` `profile.lastname`
- راهنماها: نام، نام خانوادگی، تغییر شماره تلفن

### `workspace/profile_tabs/profile_tab_security`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `workspace/modal_profile_settings`
- متن‌ها: (ورود )، ارسال پیامک کد امنیتی، استفاده همزمان از، تلاش‌های ورود موفق، تلاش‌های ورود ناموفق، خروج از این نشست، خروج از سایر نشست‌های خودم، در حال بستن سایر نشست‌های شما...، رمز، زمان، زمان ورود، سیستم عامل، فعال‌سازی ورود دو مرحله‌ای به میزیتو، مرورگر، نشست‌های فعال شما در میزیتو:
- عمل‌ها: `terminateOtherSessions` `terminateSession`
- فیلدها: `login_history_view_success` `two_step_login`
- راهنماها: خروج از این نشست

### `workspace/setting_tabs/partial_roles_info`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `workspace/setting_tabs/settings_tab_invite`؛ داخل قالب `workspace/setting_tabs/settings_tab_members`
- متن‌ها: (ظرفیت کاربر باقیمانده: نفر)، (ظرفیت کاربر مهمان باقیمانده: نفر)، » عضو داشته باشید.، » کاربر مهمان داشته باشید.، ارتقاء طرح، با توجه به طرحی که انتخاب کرده‌اید، می‌توانید حداکثر «، تعریف انواع کاربر:، مالک میزکار:، مدیر میزکار:، کاربر عادی:، کاربر مهمان:
- عمل‌ها: `showPlansTab`

### `workspace/setting_tabs/partials/partial_settings_filter_members`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `workspace/setting_tabs/settings_tab_invite`؛ داخل قالب `workspace/setting_tabs/settings_tab_members`؛ داخل قالب `workspace/setting_tabs/settings_tab_removed`
- متن‌ها: —
- عمل‌ها: `members_filter.filter=''`
- فیلدها: `members_filter.filter`
- راهنماها: فیلتر ... (نام کاربر، شماره همراه کاربر، سِمت کاربر)

### `workspace/setting_tabs/partials/partial_settings_workspace_role_name`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `workspace/setting_tabs/settings_tab_invite`؛ داخل قالب `workspace/setting_tabs/settings_tab_members`؛ داخل قالب `workspace/setting_tabs/settings_tab_removed`
- متن‌ها: انتخاب عنوان سمت، انصراف، تایید، ویرایش
- عمل‌ها: `!not_editable_role` `workspaceRoleNameEditableCancel` `workspaceRoleNameEditableOk`
- فیلدها: `user.workspace_role_name_tmp`
- راهنماها: انصراف، تایید

### `workspace/setting_tabs/settings_tab_info`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `workspace/settings`؛ داخل قالب `workspace/settings_mobile_pages`
- متن‌ها: خواهشمند است به منظور دریافت مشاوره و پشتیبانی بهتر، حوزه فعالیت خود را مشخص فرمایید و، «دمو»، آپلود تصویر، ارتقاء فضای ذخیره سازی، اعمال تغییر نام، انتخاب طرح جهت خرید، انتخاب لوگو صفحه لاگین، انتقال مالکیت میزکار، این فیلد الزامی است.، برای فعال شدن کامل این میزِکار هنوز هیچ طرحی را انتخاب نکرده‌اید:، به منظور دریافت مشاوره و پشتیبانی بهتر از طرف میزیتو، لطفاً حوزه فعالیت خود را مشخص نمایید:، تغییر مالک میزکار، توجه نمایید که پس از انتقال، شما دیگر مالک این میزکار نخواهید بود.، ثبت حوزه فعالیت، حداکثر تعداد عضو:، حذف میزِکار، حوزه فعالیت، حوزه فعالیت شرکت یا تیم، در صورتیکه می‌خواهید میزِکار خود را حذف کنید، ابتدا تمامی اعضا را حذف کرده سپس دکمه زیر را انتخاب کنید:، دریافت نمایید:، روز باقیمانده از طرح:، طرح فعلی میزِکار شما، فضای میزِکار، فضای کاربری:، فضای کل، … (+7)
- عمل‌ها: `changeWorkspaceOwner` `deleteWorkspace` `showPlansTab` `updateWorkspaceBusinessType` `updateWorkspaceTitle` `uploadDedicatedLoginPhoto`
- فیلدها: `workspace.name` `workspace.selected_business`

### `workspace/setting_tabs/settings_tab_invite`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `workspace/settings`؛ داخل قالب `workspace/settings_mobile_pages`
- متن‌ها: «مهمان»، ارسال مجدد، دعوت کاربر (به عنوان مهمان)، دعوت کاربر جدید، عضو، لغو درخواست، مدیر
- عمل‌ها: `cancelInvite` `reInvite` `sendInvitation`
- فیلدها: `user.role`
- زیرقالب: `workspace/setting_tabs/partial_roles_info` `workspace/setting_tabs/partials/partial_settings_filter_members` `workspace/setting_tabs/partials/partial_settings_workspace_role_name`

### `workspace/setting_tabs/settings_tab_members`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `workspace/settings`؛ داخل قالب `workspace/settings_mobile_pages`
- متن‌ها: (مالک میزکار)، «مهمان»، تعداد اعضا: نفر، حذف، سِمت فرد، شما می‌توانید به ازای هر عضو میزکار، عضو، غیرفعال شدن سمت‌های سازمانی، فعال شدن سمت‌های سازمانی، مدیر
- عمل‌ها: `removeMember` `toggleWorkspaceRolesActive`
- فیلدها: `user.role`
- زیرقالب: `workspace/setting_tabs/partial_roles_info` `workspace/setting_tabs/partials/partial_settings_filter_members` `workspace/setting_tabs/partials/partial_settings_workspace_role_name`

### `workspace/setting_tabs/settings_tab_permissions`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `workspace/settings`؛ داخل قالب `workspace/settings_mobile_pages`
- متن‌ها: (تنظیمات اختصاصی مالک میزِکار)، (ثبت نامه وارده / نامه صادره) دسترسی دارند:، اصلاح دسترسی پرونده مشتریان، اصلاح دسترسی پروژه‌ها، اصلاح دسترسی گروه‌های گفتگو، اعضای مجاز:، اعضایی که به، اعضایی که به امکانات، اعضایی که به منوی، اعضایی که در بخش، اعضایی که در قسمت پرونده مشتریان به، اعضایی که در لیست همکارانم عنوان فعالیتشان، اعضایی که می‌توانند، اعضایی که می‌توانند از لیست پرونده مشتریان، اعضایی که کاربران مهمان می‌توانند آن‌ها را ببینند و با آنها ارتباط برقرار کنند:، افراد فوق می‌توانند به ازای هر پرونده مشتری، سند مالی ثبت کنند.، افراد فوق می‌توانند به ازای هر پرونده مشتری، فرصت‌های فروش متفاوت ثبت و آن‌ها را پیگیری نمایند.، افزودن کاربر، ایجاد پرونده مشتری، ایجاد پروژه، ایجاد کنند:، ایجاد گروه گفتگو/کانال، باشد:، به، به اعضای خارج از این لیست ندارند.، … (+42)
- عمل‌ها: `setUserPermission` `showFixChangeUser` `showFixChatGroups` `showFixCustomers` `showFixProjects`
- فیلدها: `perms_settings.custom_chat_group_creators` `perms_settings.custom_crm_creators` `perms_settings.custom_project_creators`

### `workspace/setting_tabs/settings_tab_plans`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `workspace/settings`؛ داخل قالب `workspace/settings_mobile_pages`
- متن‌ها: (+ کاربر مهمان)، (+ کاربر هدیه)، (پلن حمایتی)، «زمان باقیمانده روز دیگر»، «پلن پیشرفته میزیتو»، آپلود سند پرداختی، انتخاب نوع پلن، بررسی، تومان، دارای تخفیف می‌باشد، دارای امکاناتی بیشتر شامل پشتیبانی از، درخواست دمو، زمان طرح تمام شده است، سالانه، سند پرداختی شما توسط کارشناسان فروش در حال بررسی می‌باشد.، شامل (تعیین وضعیت -status- هر کاربر و ...) می‌باشد. در صورت نیاز به دریافت مشاوره خرید با شرکت تماس حاصل فرمایید.، طرح فعلی شما، عزیز، فضای ذخیره‌سازی بیشتر، فضای طرح تمام شده است، فضای کاربری، مانیتورینگ اعضا، مانیتورینگ درآمدهای احتمالی، مانیتورینگ فرصت‌های فروش، مانیتورینگ وضعیت مالی، … (+13)
- عمل‌ها: `checkCouponCode` `getCoupon` `requestTrial` `setEnterprisePlan` `showInvoiceForm` `showLastWaitingInvoice` `showLastWaitingInvoicePayment` `showSitePricingPage` `uploadLastWaitingInvoicePayment`
- فیلدها: `plan.discount_code`
- راهنماها: کد تخفیف

### `workspace/setting_tabs/settings_tab_removed`

- منبع: embedded only (my-include)
- استفاده: داخل قالب `workspace/settings`؛ داخل قالب `workspace/settings_mobile_pages`
- متن‌ها: (مالک میزکار)، «مهمان»، بازگشت مجدد، در این قسمت کاربرانی که از میزکار خود حذف کرده‌اید نمایش داده می‌شود، عضو، مدیر
- عمل‌ها: `reJoinMember`
- فیلدها: `user.role`
- زیرقالب: `workspace/setting_tabs/partials/partial_settings_filter_members` `workspace/setting_tabs/partials/partial_settings_workspace_role_name`

### `workspace/settings`

- منبع: views/ + embedded
- استفاده: `service:IdleManager / None / state`
- متن‌ها: اعضا، اعضای حذف شده، تنظیمات میزِکار «، دعوت عضو جدید، عمومی، مالی، مجوزها
- کنترلر: `AppWorkspaceSettingsController`
- زیرقالب: `workspace/setting_tabs/settings_tab_info` `workspace/setting_tabs/settings_tab_invite` `workspace/setting_tabs/settings_tab_members` `workspace/setting_tabs/settings_tab_permissions` `workspace/setting_tabs/settings_tab_plans` `workspace/setting_tabs/settings_tab_removed`

### `workspace/settings_mobile`

- منبع: views/ + embedded
- استفاده: `service:IdleManager / None / state`
- متن‌ها: اعضا، اعضا میزِکار، اعضای حذف شده، تنظیمات میزِکار «، تنظیمات پروفایل، دعوت عضو جدید، عمومی، مالی، مجوزها، مجوزهای میزِکار
- عمل‌ها: `profileSettings` `showMobilePage`
- کنترلر: `AppWorkspaceSettingsController`

### `workspace/settings_mobile_pages`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `ws.settings_mobile`؛ `service:IdleManager / None / state`
- متن‌ها: صفحه تنظیمات
- عمل‌ها: `backToSettingsMobile`
- کنترلر: `AppWorkspaceSettingsController`
- زیرقالب: `workspace/setting_tabs/settings_tab_info` `workspace/setting_tabs/settings_tab_invite` `workspace/setting_tabs/settings_tab_members` `workspace/setting_tabs/settings_tab_permissions` `workspace/setting_tabs/settings_tab_plans` `workspace/setting_tabs/settings_tab_removed`

### `workspace/switching`

- منبع: views/ + embedded
- استفاده: صفحه‌ی `workspace_switching`؛ `service:IdleManager / None / state`
- متن‌ها: لطفاً منتظر بمانید...
- کنترلر: `AppWorkspaceSwitchingController`

### `workspace/toast_new_user`

- منبع: views/ + embedded
- استفاده: `service:AppProfileManager / closeToast / modal/panel`
- متن‌ها: هم اکنون به جمع شما پیوست
- عناصر سفارشی: `md-toast`

### `workspace/upgrade_plan_valid_users_dialog`

- منبع: views/ + embedded
- استفاده: `service:AppWorkspaceManager / close / modal/panel`
- متن‌ها: افراد زیر می‌توانند اقدام به تمدید و یا ارتقاء طرح نمایند:، افراد مجاز
- عمل‌ها: `close`

