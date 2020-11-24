"""doc"""
# pylint: disable=R0801
import asyncio
import logging
from typing import Optional, Union

from wechaty_puppet import FileBox, ScanStatus  # type: ignore

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def create_gif():
    """
    refer to : https://note.nkmk.me/en/python-pillow-gif/

    you can create gif file with your own code.
    """
    from PIL import Image, ImageDraw

    images = []

    width = 200
    center = width // 2
    color_1 = (0, 0, 0)
    color_2 = (255, 255, 255)
    max_radius = int(center * 1.5)
    step = 8

    for i in range(0, max_radius, step):
        im = Image.new('RGB', (width, width), color_1)
        draw = ImageDraw.Draw(im)
        draw.ellipse((center - i, center - i, center + i, center + i), fill=color_2)
        images.append(im)

    for i in range(0, max_radius, step):
        im = Image.new('RGB', (width, width), color_2)
        draw = ImageDraw.Draw(im)
        draw.ellipse((center - i, center - i, center + i, center + i), fill=color_1)
        images.append(im)

    images[0].save('./bot.gif',
                   save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)


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
        if text == 'gif':
            conversation: Union[
                Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            await conversation.say('dong')
            file_box = FileBox.from_file('./bot.gif')
            await conversation.say(file_box)

    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')

    async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
                      data: Optional[str] = None):
        contact = self.Contact.load(self.contact_id)
        print(f'user <{contact}> scan status: {status.name} , '
              f'qr_code: {qr_code}')


async def main():
    """doc"""
    create_gif()
    bot = MyBot()
    await bot.start()


asyncio.run(main())
