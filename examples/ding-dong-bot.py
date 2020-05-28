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

from wechaty import (
    FileBox,
    Message,
    Wechaty,
)


async def onMessage(msg: Message):
    """
    Message Handler for Wechaty
    """
    from_contact = msg.talker()
    text = msg.text()
    room = msg.room()
    if text == '#ding':
        talker = from_contact if room is None else room
        await talker.ready()
        await talker.say('dong')

        file_box = FileBox.from_url(
            'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
            'u=1116676390,2305043183&fm=26&gp=0.jpg',
            name='ding-dong.jpg')
        await talker.say(file_box)


async def main():
    """
    Main Entry for the Async Wechaty
    """
    #
    # Make sure we have set WECHATY_PUPPET_HOSTIE_TOKEN in the environment variables.
    #
    WECHATY_PUPPET_HOSTIE_TOKEN = 'WECHATY_PUPPET_HOSTIE_TOKEN'
    if WECHATY_PUPPET_HOSTIE_TOKEN not in os.environ:
        print("""
            Error: WECHATY_PUPPET_HOSTIE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Java Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_hostie_token
        """)

    bot = Wechaty()
    bot.on('message', onMessage)
    await bot.start()

asyncio.run(main())
