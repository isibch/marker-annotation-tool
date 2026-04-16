from marker_tool.extract import extract_marker


def test_extract_simple():
    filename = "BCL2 (23) CB-T1.0 TMA AcpH9 07.07.2025.svs"
    marker = extract_marker(filename)

    assert marker == "BCL2"


def test_extract_ca9():
    filename = "CA 9 (307) CB-T1.0 TMA AcpH9 07.07.2025.svs"
    marker = extract_marker(filename)

    assert marker == "CA 9"


def test_extract_with_prefix():
    filename = "CB-T1.0 TMA ALK (179).svs"
    marker = extract_marker(filename)

    assert marker == "ALK"