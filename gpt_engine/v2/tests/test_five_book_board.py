"""Five-book as-of board: no fake quotes, exact contract identity, best price."""
import pytest
from gpt_engine.v2.five_book_board import build_board, to_markdown, BOOKS

def quote(book,odds,line=230.5,market="game:total:230.5",side="over"):
    return {
       "game_id":"game:nba:example",
       "market_id":market,"market_type":"total","selection":side,
       "line":line,"player_id":None,"book":book,"decimal_odds":odds,
       "model_probability":.55,"no_vig_market_probability":.5,
       "expected_roi":.55*odds-1,"decision":"RESEARCH_ONLY",
       "observed_at_utc":"2026-11-21T12:00:00Z"
    }

def test_best_quote_and_missing_book_are_explicit():
    board=build_board({"markets":[
        quote("FanDuel",1.91),quote("Stake",2.05),
        quote("1xbet",1.98),quote("Bet365",2.05)
    ]})
    assert board["books"]==list(BOOKS)
    assert board["market_count"]==1
    row=board["markets"][0]
    assert row["best_decimal_odds"]==pytest.approx(2.05)
    assert row["books_tied_for_best_price"]==["Stake","Bet365"]
    assert row["books"]["MelBet"] is None
    assert row["available_book_count"]==4
    md=to_markdown(board)
    assert all(book in md for book in BOOKS)
    assert "2.05" in md and "—" in md
    assert "uncalibrated" in md.lower()

def test_different_point_lines_never_merged():
    board=build_board({"markets":[
        quote("FanDuel",1.91,line=230.5),
        quote("Stake",2.10,line=231.5,market="game:total:231.5")
    ]})
    assert board["market_count"]==2
    assert all(row["available_book_count"]==1 for row in board["markets"])

def test_inconsistent_model_predictions_raise():
    a=quote("FanDuel",1.91)
    b=quote("Stake",2.00)
    b["model_probability"]=.63
    with pytest.raises(ValueError,match="Inconsistent"):
        build_board({"markets":[a,b]})
    with pytest.raises(ValueError,match="Duplicate"):
        build_board({"markets":[a,a]})


def test_zero_cost_bookset_preserves_all_five_even_if_some_are_missing():
    from gpt_engine.v2.hoopsapi_free import FREE_BOOKS
    a=quote("FanDuel",1.95)
    b=quote("1xbet",2.05)
    board=build_board({"markets":[a,b]},books=FREE_BOOKS)
    assert board["books"]==list(FREE_BOOKS)
    assert board["market_count"]==1
    market=board["markets"][0]
    assert market["books"]["Unibet"] is None
    assert market["books"]["Betway"] is None
    assert market["books"]["Pinnacle"] is None
    assert market["books_tied_for_best_price"]==["1xbet"]
    assert market["available_book_count"]==2
    markdown=to_markdown(board)
    assert "Unibet" in markdown
    assert "Stake" not in markdown


def test_public_board_can_have_zero_named_books_without_fake_columns():
    board=build_board({"markets":[]},books=())
    assert board["books"]==[]
    assert board["market_count"]==0
    md=to_markdown(board)
    assert "No independently verified bookmaker prices" in md
    assert "FanDuel" not in md
    assert "Bet365" not in md


def test_public_board_with_only_actual_provider():
    price=quote("Draft Kings",2.1)
    board=build_board({"markets":[price]},books=("Draft Kings",))
    assert board["books"]==["Draft Kings"]
    assert board["market_count"]==1
    assert board["markets"][0]["available_book_count"]==1
    assert "Draft Kings" in to_markdown(board)
    assert "Stake" not in to_markdown(board)
