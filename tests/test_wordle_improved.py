import pytest

from wordle.wordle_improved import Wordle


@pytest.fixture()
def wordle_fixture() -> Wordle:
    # Create an instance of a Wordle
    print("Generating a Wordle")
    return Wordle(compute_table=False)


def test_compute_score_once(wordle_fixture: Wordle):
    """Test that compute_score scores words correctly."""
    assert wordle_fixture.compute_score(guess="TARES", answer="STEAM") == "11011"


@pytest.mark.parametrize(
    "guess, answer, score",
    [
        ("TARES", "STEAM", "11011"),
        ("CHILD", "STEAM", "00000"),
        ("HELLO", "HELLO", "22222"),
    ],
)
def test_compute_score_parametrized(wordle_fixture: Wordle, guess: str, answer: str, score: str):
    """Test that compute_score scores words correctly.
    Parametrized over multiple test cases"""
    assert wordle_fixture.compute_score(guess=guess, answer=answer) == score
