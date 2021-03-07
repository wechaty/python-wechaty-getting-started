"""
Python Wechaty - https://github.com/wechaty/python-wechaty
Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>
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
import os
import asyncio
from typing import Optional, Union

from wechaty import Wechaty, Contact, Room
from wechaty.user import Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """
    def __init__(self):
        super().__init__()
        self.busy = False
        self.auto_reply_comment = "Automatic Reply: I cannot read your message because I'm busy now, will talk to you when I get back."

    async def message(self, msg: Message):
        """back on message"""
        from_contact = msg.talker()
        text = msg.text()
        room = msg.room()
        if text == '#ding':
            conversation: Union[
                Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            await conversation.say('dong')

    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')


bot: Optional[MyBot] = None


async def tick(bot: Wechaty):
    """
    find a specific room, and say something to it.
    """
    room = bot.Room.load('room-id')
    await room.ready()
    from datetime import datetime
    await room.say(f'it"s a new day, let"s welcome, now it"s {datetime.now()}')
    await room.say('hello world !')


async def main():
    """Async Main Entry"""
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    global bot
    bot = MyBot()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick, 'interval', seconds=10, args=[bot])

    scheduler.start()
    await bot.start()


asyncio.run(main())
