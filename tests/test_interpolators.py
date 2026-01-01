"""Unit tests for interpolators module - pure mathematical functions."""

from codeanim.interpolators import Sigmoid, Spring


def test_sigmoid_at_start():
    sigmoid = Sigmoid()
    position, velocity = sigmoid(0)
    assert 0 <= position < 0.01  # Nearly at start
    assert velocity > 0  # Moving forward


def test_sigmoid_at_end():
    sigmoid = Sigmoid()
    position, velocity = sigmoid(1)
    assert position > 0.99  # Nearly at end
    assert velocity >= 0


def test_sigmoid_bounded_position():
    sigmoid = Sigmoid()
    for t in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.5, 2.0]:
        position, _ = sigmoid(t)
        assert 0 <= position <= 1


def test_sigmoid_velocity_positive():
    sigmoid = Sigmoid()
    for t in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
        _, velocity = sigmoid(t)
        assert velocity >= 0


def test_sigmoid_custom_speed():
    slow = Sigmoid(speed=2)
    fast = Sigmoid(speed=8)

    # At midpoint, faster should be further along
    slow_pos, _ = slow(0.5)
    fast_pos, _ = fast(0.5)
    assert fast_pos > slow_pos


def test_sigmoid_custom_offset():
    low_offset = Sigmoid(offset=4)
    high_offset = Sigmoid(offset=12)

    # At t=0, lower offset starts further along
    low_pos, _ = low_offset(0)
    high_pos, _ = high_offset(0)
    assert low_pos > high_pos


def test_spring_at_start():
    spring = Spring(gamma=10, omega=0)
    position, velocity = spring(0)
    assert position == 0  # Exactly at start
    assert velocity > 0  # Moving forward


def test_spring_at_end():
    spring = Spring(gamma=10, omega=0)
    position, velocity = spring(5)
    assert position > 0.99  # Nearly at end
    assert velocity < 0.01  # Nearly stopped


def test_spring_bounded_position():
    spring = Spring(gamma=10, omega=0)
    for t in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
        position, _ = spring(t)
        assert -0.5 <= position <= 1.5  # Allow some overshoot


def test_spring_velocity_positive():
    spring = Spring(gamma=5, omega=10)
    for t in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
        _, velocity = spring(t)
        assert velocity >= 0


def test_spring_convergence():
    spring = Spring(gamma=10, omega=5)

    # Check convergence at increasing time values
    pos_1, _ = spring(1)
    pos_2, _ = spring(2)
    pos_5, _ = spring(5)

    # Should get progressively closer to 1
    assert abs(1 - pos_5) < abs(1 - pos_2) < abs(1 - pos_1)
