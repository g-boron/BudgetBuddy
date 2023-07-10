from modules.functions.summaries import sum_lists


def test_sum_two_lists():
    l1 = [1, 2, 3]
    l2 = [2, 2, 2]

    result = sum_lists(l1, l2)
    assert result == [3, 4, 5]


def test_sum_three_lists():
    l1 = [1, 1, 1]
    l2 = [2, 2, 2]
    l3 = [3, 3, 3]

    result = sum_lists(l1, l2, l3)
    assert result == [6, 6, 6]