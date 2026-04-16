from marker_tool.clean import normalize_marker


def test_clean_spaces():
    marker = "  CA   9 "
    result = normalize_marker(marker)

    assert result == "CA 9"


def test_clean_dash():
    marker = "CA-9"
    result = normalize_marker(marker)

    assert result == "CA 9"


def test_clean_underscore():
    marker = "CA_9"
    result = normalize_marker(marker)

    assert result == "CA 9"