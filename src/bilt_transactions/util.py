#
# helper functions for bilt_transactions
#

import logging

from rich.console import Console
from rich.logging import RichHandler

console = Console(emoji=None)

def setup_logging(arg):
    """
    Configure the logging modile.
    """
    match arg:
        case 'info':
            level = logging.INFO
        case 'debug':
            level = logging.DEBUG
        case _:
            level = logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(message)s',
        handlers = [RichHandler(markup=True, rich_tracebacks=True, show_time=False, show_path=(arg=='debug'))],
    )
