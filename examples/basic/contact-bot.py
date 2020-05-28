"""contact bot"""
import asyncio
import logging
from typing import Optional

from wechaty_puppet import ScanStatus, ContactType  # type: ignore

from wechaty import Wechaty, Contact

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """
    def __init__(self):
        super().__init__()

    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')
        contacts = await self.Contact.find_all()
        log.info('bot #######################')
        log.info('bot Contact number: %s', len(contacts))

        # official
        for i, contact in enumerate(contacts):
            if contact.type() == ContactType.CONTACT_TYPE_OFFICIAL:
                log.info('Bot Official %d :%s', i, contact)
            elif contact.type() == ContactType.CONTACT_TYPE_PERSONAL:
                log.info('Bot Personal :%d %s %s',
                         i, contact.name, contact.contact_id)

        # get contact avatar url
        max_num = 17
        for i, contact in enumerate(contacts[:max_num]):
            avatar_url = contact.payload.avatar
            log.info(f'Bot Contact: {contact.name} with avatar url'
                     f' {avatar_url}')

        # send msg to someone

        for i, contact in enumerate(contacts):
            if contact.payload.alias == 'lover':
                await contact.say('my love')

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
