"""
Smoke Testing
"""

# from typing import (
#     # Any,
#     Iterable,
# )
import os

from wechaty import (
    Wechaty
)


def test_smoke_testing() -> None:
    """ wechaty """
    # os.environ['WECHATY_PUPPET_HOSTIE_TOKEN'] = 'test'
    # bot = Wechaty()
    assert Wechaty, 'should be imported successfully'
