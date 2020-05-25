"""doc"""
# pylint: disable=R0801
import asyncio
import logging
import os
from typing import Optional, Union

from wechaty_puppet import ScanStatus  # type: ignore

from wechaty import Wechaty, Contact, Room
from wechaty.user import Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """
    def __init__(self):
        super().__init__()
        self.busy = False
        self.auto_reply_comment = "Automatic Reply: I cannot read your message because I'm busy now, will talk to you when I get back."

    async def message(msg: Message):
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

    async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
                      data: Optional[str] = None):
        contact = self.Contact.load(self.contact_id)
        print(f'user <{contact}> scan status: {status.name} , '
              f'qr_code: {qr_code}')


bot: Optional[MyBot] = None


async def tick(bot: Wechaty):
    room = bot.Room.load('room-id')
    await room.ready()
    from datetime import datetime
    await room.say(f'say ding automatically, {datetime.now()}')
    await room.say('ding')


async def main():
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = MyBot()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick, 'interval', seconds=10, args=[bot])

    scheduler.start()
    await bot.start()


asyncio.run(main())
