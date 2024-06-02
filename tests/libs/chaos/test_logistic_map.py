# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from functools import partial

import numpy as np
import pytest

from libs.chaos.logistic_map import cobweb, curve, logistic_map, sequence


def _linear_map(x: float) -> float:
    """A simple map function for testing other function such as cobweb"""
    return 2 * x


@pytest.mark.parametrize(
    "r, x, expected",
    [
        (2.5, 0.5, 0.625),  # Single float test case
        (2.5, np.array([0.1, 0.5, 0.9]), np.array([0.225, 0.625, 0.225])),  # Numpy array test case
        (3.7, 0.0, 0.0),  # Edge case where x is 0
        (3.7, 1.0, 0.0),  # Edge case where x is 1
        (4.0, 0.5, 1.0),  # Edge case where x is 0.5
    ],
)
def test_logistic_map(r, x, expected):
    result = logistic_map(r, x)
    if isinstance(expected, np.ndarray):
        np.testing.assert_allclose(
            result, expected, rtol=1e-5, err_msg=f"Expected {expected}, got {result}"
        )
    else:
        assert result == pytest.approx(expected), f"Expected {expected}, got {result}"


@pytest.mark.parametrize(
    "map_function, x0, length, expected",
    [
        (_linear_map, 1.0, 5, np.array([[1.0, 0], [1.0, 2.0], [2.0, 2.0], [2.0, 4.0], [4.0, 4.0]])),
        (_linear_map, 0.5, 3, np.array([[0.5, 0], [0.5, 1.0], [1.0, 1.0]])),
        (_linear_map, 0.0, 5, np.array([[0.0, 0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])),
    ],
)
def test_cobweb_with_linear_map(map_function, x0, length, expected):
    result = cobweb(map_function, x0, length)
    np.testing.assert_allclose(
        result, expected, rtol=1e-5, err_msg=f"Expected {expected}, got {result}"
    )


@pytest.mark.parametrize(
    "map_function, x0, length, expected",
    [
        (
            partial(logistic_map, r=0.2),
            0.9274860037134183,
            4,
            np.array(
                [[0.927486, 0.0], [0.927486, 0.01345114], [0.01345114, 0.01345114], [0.0, 0.0]]
            ),
        ),
        (
            partial(logistic_map, r=3.6),
            0.7703202667912032,
            4,
            np.array(
                [[0.77032027, 0.0], [0.77032027, 0.63693703], [0.63693703, 0.63693703], [0.0, 0.0]]
            ),
        ),
    ],
)
def test_cobweb_with_logistic_map(map_function, x0, length, expected):
    result = cobweb(map_function, x0, length)
    np.testing.assert_allclose(
        result, expected, rtol=1e-5, err_msg=f"Expected {expected}, got {result}"
    )


@pytest.mark.parametrize(
    "map_function, x0, length, expected",
    [
        (_linear_map, 1.0, 5, np.array([1.0, 2.0, 4.0, 8.0, 16.0])),
        (_linear_map, 0.5, 3, np.array([0.5, 1.0, 2.0])),
        (_linear_map, 0.0, 4, np.array([0.0, 0.0, 0.0, 0.0])),
    ],
)
def test_sequence_with_linear_map(map_function, x0, length, expected):
    result = sequence(map_function, x0, length)
    np.testing.assert_allclose(
        result, expected, rtol=1e-5, err_msg=f"Expected {expected}, got {result}"
    )


@pytest.mark.parametrize(
    "map_function, x0, length, expected",
    [
        (
            partial(logistic_map, r=0.2),
            0.04895206890209158,
            4,
            np.array(
                [
                    0.04895206890209158,
                    0.009311152770459293,
                    0.0018448910409088924,
                    0.0003682974835912133,
                ]
            ),
        ),
        (
            partial(logistic_map, r=3.2),
            0.30698286022955557,
            4,
            np.array(
                [
                    0.30698286022955557,
                    0.6807820280154776,
                    0.6954171467091554,
                    0.6777988440705678,
                ]
            ),
        ),
    ],
)
def test_sequence_with_logistic_map(map_function, x0, length, expected):
    result = sequence(map_function, x0, length)
    np.testing.assert_allclose(
        result, expected, rtol=1e-5, err_msg=f"Expected {expected}, got {result}"
    )


@pytest.mark.parametrize(
    "map_function, x, expected",
    [
        (_linear_map, np.array([0.0, 0.5, 1.0]), np.array([[0.0, 0.0], [0.5, 1.0], [1.0, 2.0]])),
        (_linear_map, np.array([-1.0, 0.0, 1.0]), np.array([[-1.0, -2.0], [0.0, 0.0], [1.0, 2.0]])),
    ],
)
def test_curve_linear_map(map_function, x, expected):
    result = curve(map_function, x)
    np.testing.assert_allclose(
        result, expected, rtol=1e-5, err_msg=f"Expected {expected}, got {result}"
    )


@pytest.mark.parametrize(
    "map_function, x, expected",
    [
        (
            partial(logistic_map, r=2.5),
            np.array([0.0, 0.5, 1.0]),
            np.array([[0.0, 0.0], [0.5, 0.625], [1.0, 0.0]]),
        ),
        (
            partial(logistic_map, r=3.7),
            np.array([0.0, 0.1, 0.5]),
            np.array([[0.0, 0.0], [0.1, 0.333], [0.5, 0.925]]),
        ),
    ],
)
def test_curve_logistic_map(map_function, x, expected):
    result = curve(map_function, x)
    np.testing.assert_allclose(
        result, expected, rtol=1e-5, err_msg=f"Expected {expected}, got {result}"
    )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
