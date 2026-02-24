from domain.services import normalize_text


def test_normalization():
    assert normalize_text("Blusa Manga 3/4 Feminina") == "blusa_manga_3-4_feminina"