from typing import Any, Generator

from codeanim.parser import CodeAnimBlock, CodeAnimBlocks

PRELUDE = 'print("prelude")'
HEADER = 'print("header")'
COMMAND_1_1 = 'print("command-1")'
COMMAND_1_2 = 'print("command-1-line-2")'
COMMAND_2 = 'print("command-2")'
FOOTER = 'print("footer")'


def to_exprs(blocks: Generator[CodeAnimBlock, Any, None]) -> list[str]:
    return [expression for block in blocks for expression in block.expressions()]


def test_parse_md_default():
    blocks = CodeAnimBlocks.parse_file("tests/parse.md")
    exprs = to_exprs(blocks.filter())
    assert exprs == [PRELUDE, HEADER, COMMAND_1_1, COMMAND_1_2, COMMAND_2, FOOTER]


def test_parse_md_labels_is_header():
    blocks = CodeAnimBlocks.parse_file("tests/parse.md")
    exprs = to_exprs(blocks.filter(labels={"header"}))
    assert exprs == [PRELUDE, HEADER]


def test_parse_md_labels_is_command_1_and_2():
    blocks = CodeAnimBlocks.parse_file("tests/parse.md")
    exprs = to_exprs(blocks.filter(labels={"command-1", "command-2"}))
    assert exprs == [PRELUDE, COMMAND_1_1, COMMAND_1_2, COMMAND_2]


def test_parse_md_start_label_is_command_1():
    blocks = CodeAnimBlocks.parse_file("tests/parse.md")
    exprs = to_exprs(blocks.filter(start_label="command-1"))
    assert exprs == [PRELUDE, COMMAND_1_1, COMMAND_1_2, COMMAND_2, FOOTER]


def test_parse_md_labels_is_header_and_start_label_is_command_2():
    blocks = CodeAnimBlocks.parse_file("tests/parse.md")
    exprs = to_exprs(blocks.filter(labels={"header"}, start_label="command-2"))
    assert exprs == [PRELUDE, HEADER, COMMAND_2, FOOTER]


def test_parse_py_default():
    blocks = CodeAnimBlocks.parse_file("tests/parse.py")
    exprs = to_exprs(blocks.filter())
    assert exprs == [PRELUDE, HEADER, COMMAND_1_1, COMMAND_1_2, COMMAND_2, FOOTER]


def test_parse_py_labels_is_header():
    blocks = CodeAnimBlocks.parse_file("tests/parse.py")
    exprs = to_exprs(blocks.filter(labels={"header"}))
    assert exprs == [PRELUDE, HEADER]


def test_parse_py_labels_is_command_1_and_2():
    blocks = CodeAnimBlocks.parse_file("tests/parse.py")
    exprs = to_exprs(blocks.filter(labels={"command-1", "command-2"}))
    assert exprs == [PRELUDE, COMMAND_1_1, COMMAND_1_2, COMMAND_2]


def test_parse_py_start_label_is_command_1():
    blocks = CodeAnimBlocks.parse_file("tests/parse.py")
    exprs = to_exprs(blocks.filter(start_label="command-1"))
    assert exprs == [PRELUDE, COMMAND_1_1, COMMAND_1_2, COMMAND_2, FOOTER]


def test_parse_py_labels_is_header_and_start_label_is_command_2():
    blocks = CodeAnimBlocks.parse_file("tests/parse.py")
    exprs = to_exprs(blocks.filter(labels={"header"}, start_label="command-2"))
    assert exprs == [PRELUDE, HEADER, COMMAND_2, FOOTER]
