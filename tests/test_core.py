"""Unit tests for core.py module - mocking pynput dependencies."""

from unittest.mock import MagicMock, call

import pytest
from pynput.keyboard import Key
from pynput.mouse import Button
from pytest_mock import MockerFixture

from codeanim.core import CodeAnim
from codeanim.interpolators import Sigmoid


@pytest.fixture
def sleep(mocker: MockerFixture) -> MagicMock:
    sleep = mocker.patch("time.sleep")
    return sleep


@pytest.fixture
def pyperclip(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("codeanim.core.pyperclip")


@pytest.fixture
def listener(mocker: MockerFixture) -> MagicMock:
    mock = mocker.patch("codeanim.keyboard.Listener")
    listener = MagicMock()
    mock.return_value = listener
    return listener


@pytest.fixture
def keyboard() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mouse() -> MagicMock:
    mouse = MagicMock()
    mouse.position = (0, 0)
    return mouse


@pytest.fixture
def ca(
    keyboard: MagicMock,
    mouse: MagicMock,
    listener: MagicMock,
    sleep: MagicMock,
    pyperclip: MagicMock,
) -> CodeAnim:
    ca = CodeAnim()
    ca.keyboard.controller = keyboard
    ca.mouse = mouse
    return ca


def test_context_manager_calls_start_stop(ca: CodeAnim, listener: MagicMock):
    with ca:
        pass
    listener.start.assert_called_once()
    listener.stop.assert_called_once()


def test_registered_command_pauses_once(ca: CodeAnim, sleep: MagicMock):
    @ca.register
    def registered_command():
        pass

    registered_command()
    sleep.assert_called_once()


def test_multiple_registered_commands_pause_once(ca: CodeAnim, sleep: MagicMock):
    @ca.register
    def registered_subcommand():
        pass

    @ca.register
    def registered_command():
        registered_subcommand()

    registered_command()
    sleep.assert_called_once()


def test_registered_command_checks_abort(ca: CodeAnim):
    @ca.register
    def registered_command():
        pass

    ca.keyboard.aborted = True

    with pytest.raises(Exception, match="aborted"):
        registered_command()


def test_tap_single_key(ca: CodeAnim, sleep: MagicMock):
    ca.tap("a")
    sleep.assert_called()


def test_tap_with_modifiers(ca: CodeAnim, keyboard: MagicMock):
    ca.tap("c", modifiers=[Key.cmd])

    keyboard.press.assert_called_with(Key.cmd)
    keyboard.tap.assert_called_with("c")
    keyboard.release.assert_called_with(Key.cmd)


def test_tap_multiple_modifiers(ca: CodeAnim, keyboard: MagicMock):
    ca.tap("v", modifiers=[Key.cmd, Key.shift])

    press_calls = keyboard.press.call_args_list
    release_calls = keyboard.release.call_args_list

    assert call(Key.cmd) in press_calls
    assert call(Key.shift) in press_calls
    assert call(Key.cmd) in release_calls
    assert call(Key.shift) in release_calls


def test_tap_with_repeat(ca: CodeAnim, keyboard: MagicMock):
    ca.tap("x", repeat=3)
    assert keyboard.tap.call_count == 3


def test_tap_uses_custom_key_delay(ca: CodeAnim, sleep: MagicMock):
    with ca.delay(tap=0.02, keys={Key.enter: 0.5}):
        ca.tap(Key.enter)
    sleep.assert_has_calls([call(0.5), call(1)])


def test_click_at_current_position(ca: CodeAnim, mouse: MagicMock):
    ca.click()
    mouse.click.assert_called_once_with(Button.left, 1)


def test_click_with_position(ca: CodeAnim, mouse: MagicMock):
    ca.mouse.position = (0, 0)
    ca.click(pos=(100, 100))

    assert ca.mouse.position == (100, 100)
    mouse.click.assert_called_once()


def test_click_with_button(ca: CodeAnim, mouse: MagicMock):
    ca.click(button=Button.right)
    mouse.click.assert_called_once_with(Button.right, 1)


def test_click_with_count(ca: CodeAnim, mouse: MagicMock):
    ca.click(count=2)
    mouse.click.assert_called_once_with(Button.left, 2)


def test_move_to_position(ca: CodeAnim):
    ca.mouse.position = (0, 0)
    ca.move((100, 100))
    assert ca.mouse.position == (100, 100)


def test_move_uses_interpolator(ca: CodeAnim, sleep: MagicMock):
    ca.mouse.position = (0, 0)
    sigmoid = Sigmoid(speed=4, offset=8)

    ca.move((100, 100), interpolator=sigmoid, steps=10)

    # Should have set position multiple times (interpolated)
    assert sleep.call_count > 0


def test_drag_presses_and_releases(ca: CodeAnim, mouse: MagicMock):
    ca.mouse.position = (0, 0)
    ca.drag(start=(0, 0), end=(100, 100))

    mouse.press.assert_called_once_with(Button.left)
    mouse.release.assert_called_once_with(Button.left)
    assert ca.mouse.position == (100, 100)


def test_drag_with_button(ca: CodeAnim, mouse: MagicMock):
    ca.mouse.position = (0, 0)
    ca.drag(start=(0, 0), end=(50, 50), button=Button.right)

    mouse.press.assert_called_once_with(Button.right)
    mouse.release.assert_called_once_with(Button.right)


def test_write_simple_text(ca: CodeAnim, keyboard: MagicMock):
    ca.write("abc")
    keyboard.tap.assert_has_calls([call("a"), call("b"), call("c")])


def test_write_newline(ca: CodeAnim, keyboard: MagicMock):
    ca.write("a\nb")
    keyboard.tap.assert_has_calls([call("a"), call(Key.enter), call("b")])


def test_write_tab(ca: CodeAnim, keyboard: MagicMock):
    ca.write("\t")
    keyboard.tap.assert_called_with(Key.tab)


def test_write_backspace(ca: CodeAnim, keyboard: MagicMock):
    ca.write("\b")
    keyboard.tap.assert_called_with(Key.backspace)


def test_write_multibyte_character(ca: CodeAnim, pyperclip: MagicMock):
    ca.write("😀")
    pyperclip.copy.assert_called_with("😀")


def test_write_delays(ca: CodeAnim, sleep: MagicMock):
    with ca.delay(end=1.0, tap=0.02, keys={" ": 0.5}):
        ca.write("hello world")
    sleep.assert_has_calls(
        [
            call(0.02),
            call(0.02),
            call(0.02),
            call(0.02),
            call(0.02),
            call(0.5),
            call(0.02),
            call(0.02),
            call(0.02),
            call(0.02),
            call(0.02),
            call(1.0),
        ]
    )


def test_paste_copies_and_taps(ca: CodeAnim, keyboard: MagicMock, pyperclip: MagicMock):
    ca.paste("hello world")

    pyperclip.copy.assert_called_once_with("hello world")
    keyboard.press.assert_called_once_with(Key.cmd)
    keyboard.tap.assert_called_once_with("v")
    keyboard.release.assert_called_once_with(Key.cmd)


def test_backspace_single(ca: CodeAnim, keyboard: MagicMock):
    ca.backspace()
    keyboard.tap.assert_called_once_with(Key.backspace)


def test_backspace_multiple(ca: CodeAnim, keyboard: MagicMock):
    ca.backspace(num=3)
    assert keyboard.tap.call_count == 3


def test_scroll(ca: CodeAnim, mouse: MagicMock):
    ca.scroll(0, -5)
    mouse.scroll.assert_called_once_with(0, -5)


def test_pause_default(ca: CodeAnim, sleep: MagicMock):
    ca.pause()
    sleep.assert_called_once_with(1)


def test_pause_delay_set(ca: CodeAnim, sleep: MagicMock):
    ca.delay.set(end=2)
    ca.pause()
    sleep.assert_called_once_with(2)


def test_pause_custom_duration(ca: CodeAnim, sleep: MagicMock):
    ca.pause(2.5)
    sleep.assert_called_once_with(2.5)


def test_pause_zero_duration(ca: CodeAnim, sleep: MagicMock):
    ca.pause(0)
    sleep.assert_called_once_with(0)


def test_pause_context_manager(ca: CodeAnim, sleep: MagicMock):
    with ca.delay(end=2):
        ca.pause()
    sleep.assert_called_once_with(2)
