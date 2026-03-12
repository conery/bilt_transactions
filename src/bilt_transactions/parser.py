#
# Parse an MHTML file containing Bilt card transactions, print the
# transactions in CSV format
#

import logging
import re
from typing import NamedTuple
from types import FunctionType

from unmhtml import MHTMLConverter

from bilt_transactions.token import Token

class Edge(NamedTuple):
    '''
    A single edge ("arrow") in the state machine, defined by the name
    at the tail of the edge, the kind of input token that triggers the
    transistiom, the action to take, and the name of the state at the
    head of the edge.
    '''
    current: str
    input: str
    action: FunctionType
    next: str
    
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
    removes a paragraph from the list, creates a token, updates the current
    transaction using the value from the token, and then moves
    to the state defined by token type.

    Arguments:
        fn:  the name of the file to parse
    '''
    
    def consume(token, msg):
        '''
        Helper function, update the current transaction with the value of the token
        '''
        transaction[token.kind] = token.value
        logging.debug(f'{msg}: {token.kind} = {token.value}')

    def missing_edge(token, state):
        '''
        Helper function, called if there is an internal error in the parser
        '''
        logging.error(f'state {state} has no action for {token.kind} {token.value}')
    
    def clear_transaction():
        '''
        Action called by the state machine, clears all the fields of the current transaction
        '''
        for k in transaction.keys():
            transaction[k] = None

    def save_transaction():
        '''
        Action called by the state machine when a transaction is complete and ready to be written
        '''
        output.append(dict(transaction))
    
    def nop():
        '''
        Action called by the state machine when there is nothing to do
        '''
        pass

    def build_machine(edges):
        '''
        Traverse the list of edges, compile them into dicionary form so the main loop can
        efficiently look up the edge to traverse given the current state and input token type
        '''
        machine = {}
        for e in edge_list:
            dct = machine.setdefault(e.current, {})
            dct[e.input] = e
        return machine
    
    # Table defining the state machine.  There is one entry in this list for each
    # edge in the graph.

    edge_list = [
        Edge('A', 'date', clear_transaction, 'D'),
        Edge('D', 'description', nop, 'X'),
        Edge('X', 'amount', nop, 'N'),
        Edge('X', 'description', nop, 'X'),
        Edge('N', 'date', save_transaction, 'D'),
        Edge('N', 'description', save_transaction, 'X'),
    ]

    # This dictionary holds the fields of the transaction that is being parsed.  Fields
    # are updated by the "consume" method; the name of the field is defined by the name
    # of the edge in the edge list

    transaction = {
        'date': None,
        'description': None,
        'amount': None
    }

    states = build_machine(edge_list)
    paragraphs = extract_paragraphs(fn)
    state = 'A'
    output = []

    while paragraphs:
        p = paragraphs.pop(0)
        if t := Token(p):
            logging.debug(f'kind {t.kind} value {t.value}')
            node = states[state]
            if edge := node.get(t.kind):
                edge.action()
                consume(t, f'{state} -> {edge.next}')
                state = edge.next
            else:
                missing_edge(t, state)
                state = 'A'
        else:
            logging.error(f'error making token for {p}')

    save_transaction()
    return output

