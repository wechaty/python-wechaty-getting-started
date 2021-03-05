"""
Smoke Testing
"""

# from typing import (
#     # Any,
#     Iterable,
# )
from wechaty import (
    Wechaty,
    Contact,
)


def test_smoke_testing() -> None:
    """ wechaty """
    # os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'test'
    # bot = Wechaty()
    assert Wechaty, 'should be imported successfully for Wechaty'
    assert Contact, 'should be imported successfully for Contact'
