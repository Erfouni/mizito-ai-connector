"""Regression coverage for sitemap text cleanup."""

import ast
import re
from pathlib import Path


def _clean_text():
    source = Path("tools/build_site_map.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    function = next(
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "clean_text"
    )
    namespace = {"re": re}
    exec(compile(ast.Module(body=[function], type_ignores=[]), "clean_text", "exec"), namespace)
    return namespace["clean_text"]


def test_clean_text_preserves_visible_quotes_and_handles_boundaries():
    clean_text = _clean_text()

    # A quote followed by > is visible prose, not an attribute fragment.
    assert clean_text('She said "> hello') == 'She said "> hello'
    # Attribute debris can still occur when markup was split before this helper.
    assert clean_text('href="/guide">Visible title') == "Visible title"
    assert clean_text("") == ""
    assert clean_text("سلام\u00a0دنیا") == "سلام دنیا"
