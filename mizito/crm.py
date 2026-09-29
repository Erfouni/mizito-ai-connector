"""CRM (مشتریان، فروش، مالی): customer files, deals, payments and call logs.
Registered only with MIZITO_ENABLE_CRM=1; the workspace plan must include CRM / sales."""
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field

from mizito.app import (
    TEHRAN, WHEN_HELP, AttachmentIds, ToolError, call, chat_full, check, client, compact, html_to_text, iso, jalali,
    media_attachments, names, parse_when, send_chat, simplify_message, tool,
)
from mizito_client import MizitoError

HINT = "CRM/sales must be part of the workspace plan, and you need access to that customer file"
CustomerChat = Annotated[str, Field(description="Customer file conversation id: mizito_list_customers or mizito_list_conversations(kind='customer').")]


def _customer(conversation_id: str) -> dict:
    customer = chat_full(conversation_id).get("customer")
    if not isinstance(customer, dict) or not customer.get("_id"):
        raise ToolError("That conversation is not a customer file")
    return customer


def _customer_row(customer: dict, conversation_id: str | None = None) -> dict:
    return compact({
        "conversation_id": conversation_id or customer.get("dialog"),
        "customer_id": customer.get("_id"),
        "name": customer.get("name"), "short_name": customer.get("short_name"),
        "mobile": [m.get("phone_number") for m in customer.get("mobile") or [] if isinstance(m, dict)],
        "phone": [m.get("phone_number") for m in customer.get("phone") or [] if isinstance(m, dict)],
        "email": customer.get("email"), "website": customer.get("website"), "address": customer.get("address"),
        "postal_code": customer.get("postal_code"), "national_code": customer.get("national_code"),
        "economic_code": customer.get("economic_code"), "notes": html_to_text(customer.get("notes")),
        "labels": customer.get("labels"), "members": names(customer.get("members")),
        "representatives": compact(customer.get("representatives") or []),
    })


@tool("فهرست پرونده‌های مشتریان", feature="crm")
def mizito_list_customers(
    search: Annotated[str | None, Field(description="Only customers whose name contains this text.")] = None,
    limit: Annotated[int, Field(description="Maximum customers to return.", ge=1, le=300)] = 100,
) -> dict:
    """CRM customer files (پرونده مشتری) you can access, with contact details, labels and responsible
    colleagues. Each customer file is also a conversation (conversation_id) for notes, call logs and tasks."""
    rows = []
    for d in (client.call("chat.getDialogs", {}) or {}).get("dialogs", []):
        if not d.get("is_customer_entity"):
            continue
        try:
            customer = chat_full(d["_id"]).get("customer") or {}
        except ToolError:
            continue
        row = _customer_row(customer, d["_id"]) if customer else {"conversation_id": d["_id"], "name": client.dialog_title(d)}
        if search and search not in (row.get("name") or "") and search not in (row.get("short_name") or ""):
            continue
        rows.append(row)
        if len(rows) >= limit:
            break
    return {"count": len(rows), "customers": rows}


@tool("پرونده‌ی کامل یک مشتری", feature="crm")
def mizito_get_customer(
    conversation_id: CustomerChat,
    with_history: Annotated[bool, Field(description="Also return the change history of the customer record.")] = False,
) -> dict:
    """One customer file: contact details, representatives, labels, responsible colleagues, deals (open / won /
    lost with totals) and payments (received, paid, cheques, probable), plus optionally its change history."""
    customer = _customer(conversation_id)
    out = {"customer": _customer_row(customer, conversation_id)}
    for key, endpoint in (("deals", "deal.getCustomerDeals"), ("payments", "payment.getCustomerPayments")):
        try:
            out[key] = compact(client.call(endpoint, {"customer": customer["_id"]}) or [])
        except MizitoError:
            out[key] = "not available in this plan"
    if with_history:
        out["history"] = compact(call("customer.history", {"customer_id": customer["_id"]}, HINT) or [])
    return out


def _phones(numbers: list[str] | None) -> list[dict]:
    return [{"phone_number": n} for n in numbers or []]


@tool("ساخت پرونده‌ی مشتری", kind="create", feature="crm")
def mizito_create_customer(
    name: Annotated[str, Field(description="Customer (person or company) name.")],
    mobile: Annotated[str | None, Field(description="Mobile number.")] = None,
    email: Annotated[str, Field(description="Email.")] = "",
    address: Annotated[str, Field(description="Address.")] = "",
    notes: Annotated[str, Field(description="Notes about the customer.")] = "",
    member_ids: Annotated[list[str] | None, Field(description="Colleagues who can see the file (default: you).")] = None,
) -> dict:
    """Create a CRM customer file (پرونده مشتری). It gets its own customer conversation; member_ids are the
    colleagues who can see it. Only on the user's explicit request."""
    payload = {
        "name": name, "phone": [], "mobile": _phones([mobile] if mobile else []),
        "address": address, "notes": notes, "members": member_ids or [client.my_user_id()],
        "website": "", "email": email, "postal_code": "", "fax": "", "national_code": "",
        "economic_code": "", "representatives": [], "photo": None,
    }
    result = call("customer.add", payload, HINT) or {}
    if isinstance(result, dict) and result.get("customers_exceeded"):
        raise ToolError("The workspace plan's customer limit is reached")
    if not isinstance(result, dict):
        raise ToolError(f"Mizito did not create the customer: {result!r}")
    return {"created": True, "customer": compact(result.get("apiCustomer") or result),
            "conversation_id": (result.get("apiDialog") or {}).get("_id")}


@tool("ویرایش پرونده‌ی مشتری", kind="update", feature="crm")
def mizito_update_customer(
    conversation_id: CustomerChat,
    name: Annotated[str | None, Field(description="New name.")] = None,
    mobiles: Annotated[list[str] | None, Field(description="Mobile numbers (replaces the list).")] = None,
    phones: Annotated[list[str] | None, Field(description="Landline numbers (replaces the list).")] = None,
    email: Annotated[str | None, Field(description="Email.")] = None,
    website: Annotated[str | None, Field(description="Website.")] = None,
    address: Annotated[str | None, Field(description="Address.")] = None,
    postal_code: Annotated[str | None, Field(description="Postal code.")] = None,
    national_code: Annotated[str | None, Field(description="National id (شناسه/کد ملی).")] = None,
    economic_code: Annotated[str | None, Field(description="Economic code (کد اقتصادی).")] = None,
    notes: Annotated[str | None, Field(description="Notes.")] = None,
    member_ids: Annotated[list[str] | None, Field(description="Colleagues with access (replaces the list).")] = None,
    add_label_ids: Annotated[list[str] | None, Field(description="Customer labels to add (mizito_list_labels kind='customer').")] = None,
    remove_label_ids: Annotated[list[str] | None, Field(description="Customer labels to remove.")] = None,
) -> dict:
    """Edit a customer file's details, access or labels. Omitted fields stay as they are."""
    customer = dict(_customer(conversation_id))
    changes = {k: v for k, v in (("name", name), ("email", email), ("website", website), ("address", address),
                                 ("postal_code", postal_code), ("national_code", national_code),
                                 ("economic_code", economic_code), ("notes", notes), ("members", member_ids)) if v is not None}
    if mobiles is not None:
        changes["mobile"] = _phones(mobiles)
    if phones is not None:
        changes["phone"] = _phones(phones)
    if changes:
        payload = {**customer, **changes, "customer": customer["_id"]}
        payload.pop("_id", None)
        if isinstance(payload.get("photo"), dict):
            payload["photo"] = payload["photo"].get("_id")
        call("customer.update", payload, HINT)
    for label in add_label_ids or []:
        call("customer.updateLabel", {"customer_id": customer["_id"], "is_add": True, "label_id": label}, HINT)
    for label in remove_label_ids or []:
        call("customer.updateLabel", {"customer_id": customer["_id"], "is_add": False, "label_id": label}, HINT)
    return {"customer": _customer_row(_customer(conversation_id), conversation_id)}


STAGES = {"lost": 0, "10": 10, "20": 20, "40": 40, "60": 60, "75": 75, "90": 90, "won": 100}


@tool("فهرست و آمار فرصت‌های فروش", feature="crm")
def mizito_list_deals(
    stage: Annotated[Literal["all", "lost", "10", "20", "40", "60", "75", "90", "won"], Field(description="Pipeline column: probability percent, won (100) or lost (0); all = statistics per column.")] = "all",
    tracking_user_id: Annotated[str | None, Field(description="Only deals followed by this colleague.")] = None,
    label_ids: Annotated[list[str] | None, Field(description="Only deals with these labels (kind='deal').")] = None,
    from_date: Annotated[str | None, Field(description="Created from. " + WHEN_HELP)] = None,
    to_date: Annotated[str | None, Field(description="Created until. " + WHEN_HELP)] = None,
) -> dict:
    """Sales deals / opportunities (فرصت‌های فروش، سفارش‌ها) of the sales pipeline. stage=all returns the
    pipeline statistics; a stage returns the deals in that column."""
    flt = {"labels": label_ids or [], "labels_not": [], "tracking_user": tracking_user_id,
           "from_date": iso(from_date, default_time=(0, 0)), "to_date": iso(to_date, default_time=(23, 59))}
    if stage == "all":
        return {"statistics": compact(call("deal.getReportStatistics", {"filter": flt}, HINT))}
    deals = call("deal.getAll", {"filter": flt, "probability": STAGES[stage]}, HINT) or []
    return {"stage": stage, "count": len(deals), "deals": compact(deals)}


@tool("ثبت یا ویرایش فرصت فروش", kind="update", feature="crm")
def mizito_save_deal(
    title: Annotated[str, Field(description="Deal / order title.")],
    customer_conversation_id: Annotated[str | None, Field(description="Customer file (required for a new deal).")] = None,
    deal_id: Annotated[str | None, Field(description="Existing deal id to edit (from mizito_list_deals / mizito_get_customer).")] = None,
    price: Annotated[float | None, Field(description="Amount in Rials.", ge=0)] = None,
    stage: Annotated[Literal["lost", "10", "20", "40", "60", "75", "90", "won"], Field(description="Probability column, won or lost.")] = "10",
    comments: Annotated[str, Field(description="Description.")] = "",
    tracking_user_id: Annotated[str | None, Field(description="Colleague who follows the deal (default: you).")] = None,
    label_ids: Annotated[list[str] | None, Field(description="Deal labels.")] = None,
    attachment_ids: AttachmentIds = None,
) -> dict:
    """Create or update a sales deal (فرصت فروش) of a customer. Only on the user's explicit request."""
    if deal_id:
        deal = dict(call("deal.info", {"deal_id": deal_id}, HINT) or {})
        if not deal.get("_id"):
            raise ToolError("Deal not found")
    else:
        if not customer_conversation_id:
            raise ToolError("customer_conversation_id is required for a new deal")
        deal = {"customer": _customer(customer_conversation_id)["_id"], "attachments": []}
    deal.update({"title": title, "comments": comments, "probability": STAGES[stage],
                 "tracking_user": tracking_user_id or deal.get("tracking_user") or client.my_user_id(),
                 "labels": label_ids if label_ids is not None else deal.get("labels") or []})
    if price is not None:
        deal["price"] = price
    if attachment_ids:
        deal["attachments"] = list(deal.get("attachments") or []) + media_attachments(attachment_ids, wrap=True)
    result = call("deal.update" if deal_id else "deal.add", deal, HINT)
    return {"saved": True, "deal": compact(check(result, "save the deal"))}


PAYMENT_METHOD = {"cash": 0, "cheque": 1, "probable": 2, "canceled": 3}


@tool("ثبت یا ویرایش سند مالی (دریافت/پرداخت)", kind="update", feature="crm")
def mizito_save_payment(
    direction: Annotated[Literal["received", "paid"], Field(description="received = money from the customer (دریافت), paid = money to them (پرداخت).")],
    price: Annotated[float, Field(description="Amount in Rials.", ge=0)],
    date: Annotated[str, Field(description="Payment / due date. " + WHEN_HELP)],
    customer_conversation_id: Annotated[str | None, Field(description="Customer file (required for a new payment).")] = None,
    payment_id: Annotated[str | None, Field(description="Existing payment id to edit.")] = None,
    method: Annotated[Literal["cash", "cheque", "probable", "canceled"], Field(description="cash (نقدی), cheque (چک), probable (احتمالی), canceled (ابطال).")] = "cash",
    cashed: Annotated[bool, Field(description="For cheques: already cashed.")] = False,
    comments: Annotated[str, Field(description="Description.")] = "",
    label_ids: Annotated[list[str] | None, Field(description="Payment labels.")] = None,
    attachment_ids: AttachmentIds = None,
) -> dict:
    """Record or edit a financial document (سند مالی) of a customer in Mizito's sales module: a receipt or a
    payment, in cash, cheque or probable. This only records bookkeeping data in Mizito; it moves no money.
    Only on the user's explicit request."""
    if payment_id:
        payment = dict(call("payment.info", {"payment_id": payment_id}, HINT) or {})
        if not payment.get("_id"):
            raise ToolError("Payment not found")
    else:
        if not customer_conversation_id:
            raise ToolError("customer_conversation_id is required for a new payment")
        payment = {"customer": _customer(customer_conversation_id)["_id"], "attachments": []}
    payment.update({"type": 0 if direction == "received" else 1, "type2": PAYMENT_METHOD[method], "price": price,
                    "date": iso(date), "is_cashed": cashed, "comments": comments,
                    "labels": label_ids if label_ids is not None else payment.get("labels") or []})
    if attachment_ids:
        payment["attachments"] = list(payment.get("attachments") or []) + media_attachments(attachment_ids, wrap=True)
    result = call("payment.update", payment, HINT) if payment_id else call("payment.add", {"payment": payment}, HINT)
    return {"saved": True, "payment": compact(check(result, "save the payment"))}


@tool("گزارش مالی فروش", feature="crm")
def mizito_payment_report(
    from_date: Annotated[str | None, Field(description="From. " + WHEN_HELP)] = None,
    to_date: Annotated[str | None, Field(description="Until. " + WHEN_HELP)] = None,
    label_ids: Annotated[list[str] | None, Field(description="Only payments with these labels.")] = None,
) -> dict:
    """Totals of the sales module's financial documents: received, paid, probable and overdue income, by
    month."""
    flt = {"labels": label_ids or [], "labels_not": [], "from_date": iso(from_date, default_time=(0, 0)),
           "to_date": iso(to_date, default_time=(23, 59))}
    return {"statistics": compact(call("payment.getReportStatistics", {"filter": flt}, HINT))}


@tool("ثبت گزارش تماس با مشتری", kind="create", feature="crm")
def mizito_log_call(
    conversation_id: CustomerChat,
    notes: Annotated[str, Field(description="What was discussed.")],
    date: Annotated[str | None, Field(description="When the call happened (default: now). " + WHEN_HELP)] = None,
    outgoing: Annotated[bool, Field(description="true = you called them, false = they called.")] = True,
) -> dict:
    """Record a phone call (گزارش تماس) in a customer file, as the web app's «گزارش تماس» does."""
    when = parse_when(date) if date else datetime.now(TEHRAN)
    log = {"date": iso(when.isoformat()), "time": when.astimezone(TEHRAN).strftime("%H:%M"),
           "notes": notes, "is_out_call": outgoing, "owner": client.my_user_id()}
    message = send_chat(conversation_id, "", {"_": "messageMediaCallLog", "call_log": log})
    if not message:
        raise ToolError("Mizito did not record the call: " + HINT)
    return {"logged": True, "message": simplify_message(message), "date_jalali": jalali(log["date"])}
