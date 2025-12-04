from src.main import origins


def test_origins_ok():
    assert "http://localhost:5500" in origins


def test_origins_not_ok():
    assert not "http://localhost:8000" in origins
