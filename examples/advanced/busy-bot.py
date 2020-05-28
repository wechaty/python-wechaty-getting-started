"""doc"""
# pylint: disable=R0801
import asyncio
import logging
from typing import Optional

from wechaty_puppet import ScanStatus  # type: ignore

from wechaty import Wechaty, Contact
from wechaty.user import Message

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

    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        from_contact = msg.talker()
        text = msg.text()
        room = msg.room()
        to = msg.to()
        if room is None and to.contact_id == self.contact_id:
            # say msg to the bot
            if text == '#status':
                msg = 'busy' if self.busy else 'free'
                await from_contact.say(
                    f'My status: {msg}')
                await from_contact.say(self.auto_reply_comment)
            elif text == '#free':
                await from_contact.say('auto reply stopped.')
            elif text == '#busy':
                self.busy= True
                await from_contact.say('auto reply enabled')
            else:
                await from_contact.say(self.auto_reply_comment)


    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')

    async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
                      data: Optional[str] = None):
        contact = self.Contact.load(self.contact_id)
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
