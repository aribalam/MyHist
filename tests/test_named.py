from hist import axis, NamedHist, Hist
from boost_histogram import loc, sum

import pytest


def test_basic_usage():

    # Check if axis without name raises an error
    with pytest.raises(KeyError):
        h_named = NamedHist(
            axis.Regular(10, 0, 1, name="x"),
            axis.Regular(10, 0, 1)
        )

    h_named = NamedHist(
        axis.Regular(10, 0, 1, name="x"),
        axis.Regular(10, 0, 1, name="y")
    )  # NamedHist should require axis.Regular to have a name set

    # Check if filling without keyword raises error
    with pytest.raises(ValueError):
        h_named.fill([0.35, 0.35, 0.45], y=[0.65, 0.75, 0.85])

    h_named.fill(x=[0.35, 0.35, 0.45], y=[5, 10, 14])  # Fill should be keyword only, with the names

    h_normal = Hist(
        axis.Regular(10, 0, 1, name="x"),
        axis.Regular(10, 5, 15, name="y")
    )
    h_normal.fill([0.35, 0.35, 0.45], [0.65, 0.75, 0.85])

    assert (h_named.view() == h_normal.view()).all()

    h = NamedHist(
        axis.Regular(10, 0, 1, name='x')
    )

    h.fill(x=[0.35, 0.35, 0.45])

    # Example of a test that should be made to pass:
    assert h[{'x': 2}] == 0  # Should work
    assert h[{'x': 3}] == 2  # Should work
    assert h[{'x': 4}] == 1  # Should work
    assert h[{'x': 5}] == 0  # Should work

    # Additional Test cases on indexing

    h2 = h_normal[{0: slice(1, 5, None), 1: slice(None, 5, None)}]
    h3 = h_named[{'y': slice(None, 5, None), 'x': slice(1, 5, None)}]

    # Check if indexing by axis name works correctly
    assert (h2.view() == h3.view()).all()

    h2 = h_normal[{0: 3}]
    h3 = h_named[{'x': 3}]

    # Check if indexing works correctly
    assert (h2.view() == h3.view()).all()

    h2 = h_normal[{0: loc(0.35)}]
    h3 = h_normal[loc(0.35), :]
    h4 = h_named[{'x': loc(0.35)}]

    # Checking if indexing with loc() works correctly
    assert (h2.view() == h3.view()).all()
    assert (h3.view() == h4.view()).all()

    h2 = h_normal[{1: slice(None, None, sum)}]
    h3 = h_named[{'y': slice(None, None, sum)}]

    # Check if indexing with sum works correctly
    assert (h2.view() == h3.view()).all()
