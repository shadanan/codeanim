"""Unit tests for delayer module - timing configuration and context manager."""

from pynput.keyboard import Key

from codeanim.delayer import Delayer


def test_set_updates_values():
    delayer = Delayer(end=1.0, tap=0.02, keys={Key.enter: 0.5})
    prev = delayer.set(end=2.0, tap=0.05, keys={Key.space: 0.3})

    assert delayer.end == 2.0
    assert delayer.tap == 0.05
    assert delayer.keys == {Key.space: 0.3}
    assert prev == (1.0, 0.02, {Key.enter: 0.5})


def test_set_partial_update():
    delayer = Delayer(end=1.0, tap=0.02, keys={Key.enter: 0.5})
    prev = delayer.set(end=2.0)

    assert delayer.end == 2.0
    assert delayer.tap == 0.02
    assert delayer.keys == {Key.enter: 0.5}
    assert prev == (1.0, 0.02, {Key.enter: 0.5})


def test_context_manager_restores_values():
    delayer = Delayer(end=1.0, tap=0.02, keys={Key.enter: 0.5})

    with delayer(end=2.0, tap=0.05, keys={Key.space: 0.3}):
        assert delayer.end == 2.0
        assert delayer.tap == 0.05
        assert delayer.keys == {Key.space: 0.3}

    assert delayer.end == 1.0
    assert delayer.tap == 0.02
    assert delayer.keys == {Key.enter: 0.5}


def test_context_manager_partial_update():
    delayer = Delayer(end=1.0, tap=0.02, keys={Key.enter: 0.5})

    with delayer(end=3.0):
        assert delayer.tap == 0.02
        assert delayer.end == 3.0
        assert delayer.keys == {Key.enter: 0.5}

    assert delayer.tap == 0.02
    assert delayer.end == 1.0
    assert delayer.keys == {Key.enter: 0.5}


def test_nested_context_managers():
    delayer = Delayer(end=1.0, tap=0.02, keys={Key.enter: 0.5})

    with delayer(end=2.0):
        assert delayer.end == 2.0
        with delayer(end=3.0):
            assert delayer.end == 3.0
        assert delayer.end == 2.0
    assert delayer.end == 1.0
