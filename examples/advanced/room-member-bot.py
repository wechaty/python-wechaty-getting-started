"""
Python Wechaty - https://github.com/wechaty/python-wechaty
Authors:    Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020 @ Copyright Wechaty Contributors <https://github.com/wechaty>
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations
import os
import asyncio
from typing import List, Optional

from wechaty import Wechaty, Room, RoomQueryFilter
from wechaty.user.contact import Contact
from wechaty_puppet import get_logger

log = get_logger('RoomMemberBot')


class MyBot(Wechaty):
    """oop wechaty bot, all of your entrypoint should be done here.
    """
    async def on_ready(self, payload):
        """all of initialization jobs shoule be done here.
        """
        log.info('ready event<%s>', payload)
        # search contact and add them to the specific room
        room: Optional[Room] = await self.Room.find(query=RoomQueryFilter(topic='room-topic-name'))
        if not room:
            return
        contacts: List[Contact] = await self.Contact.find_all()

        for contact in contacts:
            await contact.ready()
            if contact.name == 'your-friend-name':
                await room.add(contact)


async def main():
    """Async Main Entry"""
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = MyBot()
    await bot.start()


asyncio.run(main())
