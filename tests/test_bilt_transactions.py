from bilt_transactions.parser import extract_paragraphs, parse_file
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

def test_parser():
    lst = parse_file('tests/feb.mhtml')
    assert len(lst) == 3
    assert [isinstance(x, dict) for x in lst]
    assert lst[0]['date'].month == 2
    assert lst[0]['date'].day == 9
    assert lst[0]['date'].year == 2026
    assert lst[0]['description'] == 'Best Buy'
    assert lst[-1]['date'].month == 2
    assert lst[-1]['date'].day == 8
    assert lst[-1]['date'].year == 2026
    assert lst[-1]['description'] == 'Art House'
    assert round(sum(x['amount'] for x in lst),2) == 81.45 
