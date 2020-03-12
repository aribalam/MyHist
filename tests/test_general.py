from hist import Hist, axis
from boost_histogram import loc

import pytest


def test_basic_usage():

    # Check hist with only one axis
    h = Hist(axis.Regular(10, 0, 1))

    h.fill([0.35, 0.35, 0.45])

    assert h[2] == 0
    assert h[3] == 2
    assert h[4] == 1
    assert h[5] == 0

    # Check hist with two axes
    h = Hist(
        axis.Regular(10, 0, 1),
        axis.Regular(10, 0, 1)
    )

    h.fill([0.35, 0.35, 0.45], [0.65, 0.65, 0.85])

    assert h[3, 6] == 2
    assert h[4, 8] == 1
    assert h[3, 5] == 0

    # Checking hist with axis type bool
    h = Hist(
        axis.bool()
    )

    h.fill([0, 1, 1])

    assert h[0] == 1
    assert h[1] == 2

    # check if there are exactly two bins (accessing h[2] raises IndexError)
    with pytest.raises(IndexError):
        assert h[2] == 0

    # check if flow is disabled (if view() with or without flow gives the same output)
    assert (h.view() == h.view(flow=True)).all()

    h = Hist(
        axis.Regular(10, 0, 1),
        axis.Regular(10, 0, 1)
    )

    h.fill([0.35, 0.35, 0.45], [0.65, 0.65, 0.85])

    # Check indexing using dict and bh.loc()
    h2 = h[loc(0.35), :]

    # Broken in 0.6.2, fixed now
    h3 = h[{0: loc(0.35)}]

    assert (h2.view() == h3.view()).all()