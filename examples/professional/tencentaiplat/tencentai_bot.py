import asyncio
import logging
from typing import Optional, Union

from wechaty_puppet import PuppetOptions, FileBox  # type: ignore

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room

from .tencentaiplat import TencentAI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(filename)s <%(funcName)s> %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger('DingDongBot')

chat_friend: list = []

async def message(msg: Message):
    """back on message"""
    from_contact = msg.talker()
    text = msg.text()
    room = msg.room()
    conversation: Union[
        Room, Contact] = from_contact if room is None else room

    global chat_friend

    if "#关闭闲聊" == text:
        try:
            chat_friend.remove(conversation)
        except Exception as e:
            return
        await conversation.ready()
        await conversation.say('好的，有需要随时叫我')
        return

    elif "#开启闲聊" == text:
        chat_friend.append(conversation)
        await conversation.ready()
        await conversation.say('闲聊功能开启成功！现在你可以和我聊天啦！')
        return

    if conversation in chat_friend:
        data = TencentAI(text)
        await conversation.ready()
        await conversation.say(data)
        return

    if text == '#ding':
        await conversation.ready()
        await conversation.say('dong')

        file_box = FileBox.from_url(
            'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
            'u=1116676390,2305043183&fm=26&gp=0.jpg',
            name='ding-dong.jpg')
        await conversation.say(file_box)


bot: Optional[Wechaty] = None


async def main():
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = Wechaty().on('message', message)
    await bot.start()


asyncio.run(main())
