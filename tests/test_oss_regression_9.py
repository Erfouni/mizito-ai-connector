"""Regression coverage for sparse XLSX cell references."""
import io
import zipfile

import pytest

from mizito.files import extract_text


@pytest.mark.parametrize(
    ("rows", "expected"),
    [
        (
            '<row r="1"><c r="A1" t="inlineStr"><is><t>Product</t></is></c>'
            '<c r="B1" t="inlineStr"><is><t>Note</t></is></c>'
            '<c r="C1" t="inlineStr"><is><t>Quantity</t></is></c></row>'
            '<row r="2"><c r="A2" t="s"><v>0</v></c><c r="C2"><v>4</v></c></row>',
            "Product\tNote\tQuantity\nDesk\t\t4",
        ),
        (
            '<row r="3"><c r="C3" t="inlineStr"><is><r><t>Desk</t></r>'
            '<r><t> &amp; chair</t></r></is></c><c r="E3"><v>7</v></c></row>',
            "\t\tDesk & chair\t\t7",
        ),
        (
            '<row r="1"><c r="Z1" t="s"><v>0</v></c><c r="AB1"><v>4</v></c></row>'
            '<row r="2"><c r="AA2" t="inlineStr"><is><t>AA</t></is></c></row>',
            "\t" * 25 + "Desk\t\t4\n" + "\t" * 26 + "AA",
        ),
        (
            '<row><c t="s"><v>0</v></c><c/><c><v>4</v></c></row>',
            "Desk\t\t4",
        ),
    ],
    ids=["middle-gap", "leading-gap", "beyond-z", "unreferenced-cells"],
)
def test_xlsx_preserves_omitted_columns(rows: str, expected: str) -> None:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr(
            "xl/workbook.xml",
            '<workbook><sheets><sheet name="Data" sheetId="1"/></sheets></workbook>',
        )
        archive.writestr("xl/sharedStrings.xml", "<sst><si><t>Desk</t></si></sst>")
        archive.writestr(
            "xl/worksheets/sheet1.xml",
            f"<worksheet><sheetData>{rows}</sheetData></worksheet>",
        )

    assert extract_text("sparse.xlsx", None, buffer.getvalue()) == (
        "xlsx", f"[Data]\n{expected}"
    )
