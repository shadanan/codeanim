"""Unit tests for delayer module - timing configuration and context manager."""

from unittest.mock import MagicMock, call, patch

import pytest
from pynput.keyboard import Key, KeyCode

from codeanim import CodeAnim


@pytest.fixture
def ca() -> CodeAnim:
    ca = CodeAnim()
    ca.keyboard.controller = MagicMock()
    return ca


def test_set_updates_values(ca: CodeAnim):
    new_keys: dict[str | Key | KeyCode, float] = {Key.space: 0.3}
    prev = ca.delay.set(end=2.0, tap=0.05, keys=new_keys)

    assert ca.delay.end == 2.0
    assert ca.delay.tap == 0.05
    assert ca.delay.keys == new_keys
    assert prev == (1.0, 0.02, {})


def test_set_partial_update(ca: CodeAnim):
    prev = ca.delay.set(end=2.0)

    assert ca.delay.end == 2.0
    assert ca.delay.tap == 0.02
    assert ca.delay.keys == {}
    assert prev == (1.0, 0.02, {})


@patch("time.sleep")
def test_pause_default(mock_sleep: MagicMock, ca: CodeAnim):
    ca.pause()
    mock_sleep.assert_called_once_with(1)


@patch("time.sleep")
def test_pause_delay_set(mock_sleep: MagicMock, ca: CodeAnim):
    ca.delay.set(end=2)
    ca.pause()
    mock_sleep.assert_called_once_with(2)


@patch("time.sleep")
def test_pause_custom_duration(mock_sleep: MagicMock, ca: CodeAnim):
    ca.pause(2.5)
    mock_sleep.assert_called_once_with(2.5)


@patch("time.sleep")
def test_pause_zero_duration(mock_sleep: MagicMock, ca: CodeAnim):
    ca.pause(0)
    mock_sleep.assert_called_once_with(0)


@patch("time.sleep")
def test_pause_context_manager(mock_sleep: MagicMock, ca: CodeAnim):
    with ca.delay(end=2):
        ca.pause()
    mock_sleep.assert_called_once_with(2)


def test_context_manager_restores_values(ca: CodeAnim):
    ca.delay.set(end=1.0, tap=0.02, keys={Key.enter: 0.5})

    with ca.delay(end=2.0, tap=0.05, keys={Key.space: 0.3}):
        assert ca.delay.end == 2.0
        assert ca.delay.tap == 0.05
        assert ca.delay.keys == {Key.space: 0.3}

    # Values restored after context
    assert ca.delay.end == 1.0
    assert ca.delay.tap == 0.02
    assert ca.delay.keys == {Key.enter: 0.5}


def test_context_manager_partial_update(ca: CodeAnim):
    ca.delay.set(end=1.0, tap=0.02, keys={Key.enter: 0.5})

    with ca.delay(end=3.0):  # Only change end
        assert ca.delay.tap == 0.02  # Unchanged
        assert ca.delay.end == 3.0  # Changed
        assert ca.delay.keys == {Key.enter: 0.5}  # Unchanged

    # All values restored
    assert ca.delay.tap == 0.02
    assert ca.delay.end == 1.0
    assert ca.delay.keys == {Key.enter: 0.5}


def test_nested_context_managers(ca: CodeAnim):
    ca.delay.set(end=1.0, tap=0.02, keys={Key.enter: 0.5})

    with ca.delay(end=2.0):
        assert ca.delay.end == 2.0

        with ca.delay(end=3.0):
            assert ca.delay.end == 3.0

        assert ca.delay.end == 2.0  # Restored to outer context

    assert ca.delay.end == 1.0  # Restored to original


@patch("time.sleep")
def test_write_delays(mock_sleep: MagicMock, ca: CodeAnim):
    with ca.delay(end=1.0, tap=0.02, keys={" ": 0.5}):
        ca.write("hello world")
    mock_sleep.assert_has_calls(
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
