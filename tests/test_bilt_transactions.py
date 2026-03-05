from bilt_transactions.parser import extract_paragraphs

def test_paragraphs():
    lst = extract_paragraphs('tests/feb.mhtml')
    assert len(lst) == 8
