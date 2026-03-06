#
# Parse an MHTML file containing Bilt card transactions, print the
# transactions in CSV format
#

import logging
import re
from unmhtml import MHTMLConverter

from bilt_transactions.token import Token

def extract_paragraphs(fn: str):
    '''
    Return the contents of all the <P> elements in an MHTML file.

    Arguments:
        fn:  the name of the file
    '''
    converter = MHTMLConverter()
    html = converter.convert_file(fn)
    return re.findall(r'<p class.*?</p>', html)


def parse_file(fn: str):
    '''
    Parse an MHTML file, returning a list of dicts, where each dict
    describes a single transaction.  Attributes are date, description,
    and amount.

    The parser calls "extract_paragraphs" to get a list of text elements
    in the file.  It then uses a finite state machine (see "states.dot" 
    in the documentation) to create output records.  The main loop 
    removes a paragraph from the list, creates a token, and then moves
    to the state defined by token type. 

    Arguments:
        fn:  the name of the file to parse
    '''

    def step(token, state):
        match state:
            case 'A':
                clear_transaction()
                if token.kind == 'date':
                    consume(token, 'A -> D')
                    next = 'D'
                else:
                    missing_edge(token, 'A')
                    next = 'A'
            case 'D':
                if token.kind == 'description':
                    consume(token, 'D -> X')
                    next = 'X'
                else:
                    missing_edge(token, 'D')
                    next = 'A'
            case 'X':
                if token.kind == 'amount':
                    consume(token, 'X -> N')
                    next = 'N'
                elif token.kind == 'description':
                    consume(token, 'X -> X')
                    next = 'X'
                else:
                    missing_edge(token, 'X')
                    next = 'A'
            case 'N':
                save_transaction()
                if token.kind == 'date':
                    consume(token, 'N -> D')
                    next = 'D'
                elif token.kind == 'description':
                    consume(token, 'N -> X')
                    next = 'X'
                else:
                    missing_edge(token, 'N')
                    next = 'A'
            case _:
                logging.error(f'internal error: undefined state: {state}')
                exit(1)
        return next
    
    def consume(token, msg):
        transaction[token.kind] = token.value
        logging.debug(f'{msg}: {token.kind} = {token.value}')

    def missing_edge(token, state):
        logging.error(f'state {state} has no action for {token.kind} {token.value}')
    
    def clear_transaction():
        for k in transaction.keys():
            transaction[k] = None

    def save_transaction():
        output.append(dict(transaction))

    paragraphs = extract_paragraphs(fn)
    state = 'A'
    output = []

    transaction = {
        'date': None,
        'description': None,
        'amount': None
    }

    while paragraphs:
        p = paragraphs.pop(0)
        if t := Token(p):
            logging.debug(f'kind {t.kind} value {t.value}')
            state = step(t, state)
        else:
            logging.error(f'error making token for {p}')
    
    save_transaction()
    return output

