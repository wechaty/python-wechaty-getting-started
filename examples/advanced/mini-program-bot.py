"""send contact card to specific contact"""
# pylint: disable=R0801
import asyncio
import logging
from typing import Optional, Union
import json
from dataclasses import asdict

from wechaty_puppet import FileBox, ScanStatus  # type: ignore
from wechaty_puppet import MessageType

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """
    def __init__(self):
        super().__init__()

    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        from_contact = msg.talker()
        text = msg.text()

        room = self.Room.load('19961884194@chatroom')
        await room.ready()

        if msg.type() == MessageType.MESSAGE_TYPE_MINI_PROGRAM:
            mini_program = await msg.to_mini_program()

            # save the mini-program data as string
            mini_program_data = asdict(mini_program.payload)

            # load the min-program
            loaded_mini_program = self.MiniProgram.create_from_json(
                payload_data=mini_program_data
            )

            await room.say(loaded_mini_program)

    async def on_login(self, contact: Contact):
        """login event. It will be triggered every time you login"""
        log.info(f'user: {contact} has login')

    async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
                      data: Optional[str] = None):
        """scan event, It will be triggered when you scan the qrcode to login.
        And it will not be triggered when you have logined
        """
        contact = self.Contact.load(self.contact_id)
        await contact.ready()
        print(f'user <{contact}> scan status: {status.name} , '
              f'qr_code: {qr_code}')


bot: Optional[MyBot] = None


async def main():
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = MyBot()
    await bot.start()


asyncio.run(main())
