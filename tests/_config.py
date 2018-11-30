"""Config."""

import os

if os.environ.get('MURIA_SETUP') is None:
    os.environ['MURIA_SETUP'] = \
        os.path.join(
            os.path.dirname(__file__),
            'settings.ini'
    )
