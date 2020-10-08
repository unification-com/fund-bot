import logging
import os

log = logging.getLogger(__name__)


def get_secret(key):
    password_file = os.path.join(os.path.expanduser("~"), ".secrets")
    with open(password_file, 'r') as f:
        contents = f.read()
    data = contents.strip()
    rows = data.splitlines()
    for row in rows:
        splitted = row.split()
        if splitted[0].strip() == key:
            return splitted[1].strip()
    log.warning(f'Secret {key} not found')
