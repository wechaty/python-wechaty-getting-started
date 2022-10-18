"""doc"""
# pylint: disable=R0801
import asyncio
import logging
from typing import Optional, Union

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room
from wechaty_puppet import FileBox, ScanStatus  # type: ignore

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
        room = msg.room()
        if text == '#ding':
            conversation: Union[
                Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            await conversation.say('dong')
            file_box = FileBox.from_url(
                'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
                'u=1116676390,2305043183&fm=26&gp=0.jpg',
                name='ding-dong.jpg')
            await conversation.say(file_box)

    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')

    async def on_scan(self,
                      qr_code: str,
                      status: ScanStatus,
                      data: Optional[str] = None):
        if status == ScanStatus.Waiting:
            print("qr_code: ", "https://wechaty.js.org/qrcode/" + qr_code)
        else:
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
