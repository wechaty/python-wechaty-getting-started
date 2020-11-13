"""send contact card to specific contact"""
# pylint: disable=R0801
import asyncio
import logging
from typing import Optional, Union

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
        room = msg.room()
        if room:
            await room.ready()

        # send contact-card
        if msg.type() == MessageType.MESSAGE_TYPE_CONTACT:
            # we can receive the contact-card event, and get the contact from message
            contact = await msg.to_contact()

        if text == 'send card':
            # find one of my friend to send to `from_contact`
            contacts = await bot.Contact.find_all()
            if contacts:
                # send one of my friend to the talker
                # !! this interface is not supported now
                await from_contact.say(contacts[0])
                print('have sended')
        elif msg.type() == MessageType.MESSAGE_TYPE_IMAGE:
            img = await msg.to_file_box()
            # save the image as local file
            await img.to_file(f'./{img.name}')
            # send image file to the room
            if room:
                await room.say(img)

        elif msg.type() == MessageType.MESSAGE_TYPE_VIDEO:
            video = await msg.to_file_box()
            # save the video as local file
            await video.to_file(f'./{video.name}')

            # send video file to the room
            if room:
                await room.say(video)

        elif msg.type() == MessageType.MESSAGE_TYPE_AUDIO:
            audio = await msg.to_file_box()
            # save the audio file as local file
            await audio.to_file(f'./{audio.name}')
            # !! we can't send audio to room/contact

        print('done')

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
