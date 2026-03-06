from bilt_transactions.parser import extract_paragraphs
from bilt_transactions.token import Token

def test_paragraphs():
    lst = extract_paragraphs('tests/feb.mhtml')
    assert len(lst) == 8

def test_date_token():
    lst = extract_paragraphs('tests/feb.mhtml')
    t = Token(lst[0])
    assert t.kind == 'date'
    assert t.value.month == 2
    assert t.value.day == 9
    assert t.value.year == 2026

def test_description_token():
    lst = extract_paragraphs('tests/feb.mhtml')
    t = Token(lst[-2])
    assert t.kind == 'description'
    assert t.value == 'Art House'

def test_amount_token():
    lst = extract_paragraphs('tests/feb.mhtml')
    t = Token(lst[-1])
    assert t.kind == 'amount'
    assert round(t.value, 2) == 13.20


