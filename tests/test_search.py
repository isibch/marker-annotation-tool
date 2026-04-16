from marker_tool.search import find_best_ensg


def test_cd20_lookup():
    ensg = find_best_ensg("CD20")

    assert ensg == "ENSG00000156738"