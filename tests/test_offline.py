"""Offline checks for the helpers (no Mizito account needed): uv run python tests/test_offline.py"""
import io
import sys
import zipfile
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mizito.app import (  # noqa: E402
    ToolError, alarm_options, gregorian_to_jalali, iso, jalali, jalali_to_gregorian, parse_when,
)
from mizito.files import extract_text  # noqa: E402


def test_calendar_round_trip() -> None:
    day = date(1990, 1, 1)
    while day < date(2060, 1, 1):
        jy, jm, jd = gregorian_to_jalali(day.year, day.month, day.day)
        assert jalali_to_gregorian(jy, jm, jd) == (day.year, day.month, day.day), day
        day += timedelta(days=1)
    assert gregorian_to_jalali(2026, 3, 21) == (1405, 1, 1)  # Nowruz 1405
    assert gregorian_to_jalali(2026, 10, 1) == (1405, 7, 9)


def test_parse_when() -> None:
    assert iso("2026-10-01T14:30") == "2026-10-01T11:00:00.000Z"  # Tehran is UTC+03:30
    assert iso("1405/07/09 14:30") == "2026-10-01T11:00:00.000Z"
    assert iso("۱۴۰۵/۰۷/۰۹ ۱۴:۳۰") == "2026-10-01T11:00:00.000Z"  # Persian digits
    assert iso("2026-10-01T14:30:00+03:30") == "2026-10-01T11:00:00.000Z"
    assert iso("2026-10-01T11:00:00Z") == "2026-10-01T11:00:00.000Z"
    assert iso("1405-07-09") == "2026-10-01T05:30:00.000Z"  # date only = 09:00 Tehran
    assert iso(None) is None and iso("") is None
    for bad in ("tomorrow", "1405/13/01", "2026-02-30"):
        try:
            parse_when(bad)
        except ToolError:
            continue
        raise AssertionError(f"accepted {bad!r}")
    assert jalali("2026-10-01T11:00:00.000Z") == "1405/07/09 14:30"
    assert jalali(1790621492000) is not None and jalali("garbage") is None


def test_alarm_options() -> None:
    once = alarm_options("1405/07/09 08:00")
    assert once == {"date": "2026-10-01T04:30:00.000Z", "time": "08:00", "repeat_type": "none",
                    "has_custom_repeat": False, "repeat_options": {}}
    weekly = alarm_options("1405/07/09 08:00", "weekly", ["sat", "mon"], until="1405/12/29")
    assert weekly["repeat_type"] == "weekly" and weekly["has_custom_repeat"]
    assert weekly["repeat_options"]["week_days"] == {"0": True, "1": False, "2": True, "3": False,
                                                    "4": False, "5": False, "6": False}
    assert weekly["repeat_options"]["repeat_until_type"] == "limit_date"
    monthly = alarm_options("1405/07/01 10:00", "monthly", day_of_month="last", times=6)
    assert monthly["repeat_options"] == {"monthly_interval": 1, "special_day_in_month": "lastDay",
                                         "repeat_until_type": "limit_days", "repeat_until_days": 6}
    first_sat = alarm_options("1405/07/01 10:00", "monthly_first_weekday", ["sat"])
    assert first_sat["repeat_type"] == "firstMonthly" and first_sat["repeat_options"]["day_of_week"] == 0
    assert alarm_options("1405/07/01", "daily")["repeat_type"] == "daily"
    for kwargs in ({"repeat": "hourly"}, {"repeat": "monthly_first_weekday"}, {"repeat": "weekly", "weekdays": ["xyz"]}):
        try:
            alarm_options("1405/07/01", **kwargs)
        except ToolError:
            continue
        raise AssertionError(kwargs)


def _zip(files: dict[str, str]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, body in files.items():
            z.writestr(name, body)
    return buf.getvalue()


def test_extract_text() -> None:
    docx = _zip({"word/document.xml": '<w:document><w:body><w:p><w:r><w:t>سلام</w:t></w:r></w:p>'
                                      '<w:p><w:r><w:t>دنیا &amp; ما</w:t></w:r></w:p></w:body></w:document>'})
    assert extract_text("a.docx", None, docx) == ("docx", "سلام\nدنیا & ما\n")
    xlsx = _zip({
        "xl/workbook.xml": '<workbook><sheets><sheet name="فروش" sheetId="1"/></sheets></workbook>',
        "xl/sharedStrings.xml": "<sst><si><t>کالا</t></si><si><t>تعداد</t></si></sst>",
        "xl/worksheets/sheet1.xml": '<worksheet><sheetData><row r="1"><c r="A1" t="s"><v>0</v></c>'
                                    '<c r="B1" t="s"><v>1</v></c></row><row r="2"><c r="A2" t="inlineStr"><is><t>میز</t></is></c>'
                                    '<c r="B2"><v>4</v></c></row></sheetData></worksheet>'})
    assert extract_text("b.xlsx", None, xlsx) == ("xlsx", "[فروش]\nکالا\tتعداد\nمیز\t4")
    pptx = _zip({"ppt/slides/slide2.xml": "<p:sld><a:p><a:r><a:t>دوم</a:t></a:r></a:p></p:sld>",
                 "ppt/slides/slide1.xml": "<p:sld><a:p><a:r><a:t>اول</a:t></a:r></a:p></p:sld>"})
    assert extract_text("c.pptx", None, pptx) == ("pptx", "[slide 1]\nاول\n\n\n[slide 2]\nدوم\n")
    assert extract_text("d.txt", None, "متن".encode("cp1256")) == ("text", "متن")
    assert extract_text("e.csv", None, "a,b\n1,2".encode("utf-8-sig")) == ("text", "a,b\n1,2")
    assert extract_text("f.html", "text/html", "<p>سلام</p><br>دنیا".encode()) == ("text", "سلام\n\nدنیا")
    assert extract_text("g.jpg", "image/jpeg", b"\xff\xd8")[0] == "image"
    assert extract_text("h.bin", None, b"\x00\x01")[0] == "binary"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok", name)
