from codeanim import markdown

WAIT = "wait()"
HEADER = 'print("header")'
COMMAND_1 = 'print("command-1")'
COMMAND_2 = 'print("command-2")'
FOOTER = 'print("footer")'


def test_parse_default():
    commands = markdown.parse("tests/parse.md")
    assert commands[0] == HEADER
    assert commands[1] == COMMAND_1
    assert commands[2] == COMMAND_2
    assert commands[3] == FOOTER


def test_parse_labels_is_header():
    commands = markdown.parse("tests/parse.md", labels=["header"])
    assert len(commands) == 1
    assert commands[0] == HEADER


def test_parse_labels_is_command_1_and_2():
    commands = markdown.parse("tests/parse.md", labels=["command-1", "command-2"])
    assert len(commands) == 2
    assert commands[0] == COMMAND_1
    assert commands[1] == COMMAND_2


def test_parse_start_label_is_command_1():
    commands = markdown.parse("tests/parse.md", start_label="command-1")
    assert len(commands) == 3
    assert commands[0] == COMMAND_1
    assert commands[1] == COMMAND_2
    assert commands[2] == FOOTER


def test_parse_labels_is_header_and_start_label_is_command_2():
    commands = markdown.parse(
        "tests/parse.md", labels=["header"], start_label="command-2"
    )
    assert len(commands) == 3
    assert commands[0] == HEADER
    assert commands[1] == COMMAND_2
    assert commands[2] == FOOTER


def test_parse_live_injects_wait():
    commands = markdown.parse("tests/parse.md", live=True)
    assert len(commands) == 8
    assert commands[0] == WAIT
    assert commands[1] == HEADER
    assert commands[2] == WAIT
    assert commands[3] == COMMAND_1
    assert commands[4] == WAIT
    assert commands[5] == COMMAND_2
    assert commands[6] == WAIT
    assert commands[7] == FOOTER
