from bubop import format_dict


def test_format_dict():
    expected = "Header: \n========\n\n  - 1  : 2\n  - 123: kalimera\n\n"
    assert format_dict(header="Header", items={1: 2, 123: "kalimera"}) == expected
