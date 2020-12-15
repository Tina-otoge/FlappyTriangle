import logging
import os

if os.environ.get('DEBUG'):
    logging.basicConfig(
        format='{levelname}: {message}',
        style='{',
        level=logging.DEBUG,
    )
