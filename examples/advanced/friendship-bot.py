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
from typing import Optional

from wechaty import (
    Wechaty, Contact, Friendship, FriendshipType
)


class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """
    def __init__(self):
        super().__init__()
        self.busy = False
        self.auto_reply_comment = "Automatic Reply: I cannot read your message because I'm busy now, will talk to you when I get back."

    async def on_friendship(self, friendship: Friendship):
        administrator = bot.Contact.load('admin-id')
        await administrator.ready()

        contact = friendship.contact()
        await contact.ready()

        log_msg = f'receive "friendship" message from {contact.name}'
        await administrator.say(log_msg)

        if friendship.type() == FriendshipType.FRIENDSHIP_TYPE_RECEIVE:
            if friendship.hello() == 'ding':
                log_msg = 'accepted automatically because verify messsage is "ding"'
                print('before accept ...')
                await friendship.accept()
                # if want to send msg, you need to delay sometimes

                print('waiting to send message ...')
                await asyncio.sleep(3)
                await contact.say('hello from wechaty ...')
                print('after accept ...')
            else:
                log_msg = 'not auto accepted, because verify message is: ' + friendship.hello()

        elif friendship.type() == FriendshipType.FRIENDSHIP_TYPE_CONFIRM:
            log_msg = 'friend ship confirmed with ' + contact.name

        print(log_msg)
        await administrator.say(log_msg)

    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')


bot: Optional[MyBot] = None


async def main():
    """Async Main Entry"""
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Java Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    global bot
    bot = MyBot()
    await bot.start()


asyncio.run(main())

