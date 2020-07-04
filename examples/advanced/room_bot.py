import asyncio
import re
import time
from datetime import datetime
from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from wechaty import Contact, Room, Wechaty, get_logger, Message

welcome = """=============== Powered by Python-Wechaty ===============
-------- https://github.com/Chatie/python-wechaty --------
Hello,
I'm a Wechaty Botie with the following super powers:
1. Find a room
2. Add people to room
3. Del people from room
4. Change room topic
5. Monitor room events
6. etc...
If you send a message of magic word 'ding',
you will get a invitation to join my own room!
__________________________________________________
Hope you like it, and you are very welcome to
upgrade me for more super powers!
Please wait... I'm trying to login in..."""
HELPER_CONTACT_NAME = '黄纯洪'

print(welcome)
log = get_logger('RoomBot')


async def check_room_join(bot, room, invitee_list, inviter):
    try:
        user_self = bot.user_self()
        if inviter.id != user_self.contact_id:
            await room.say('RULE1: Invitation is limited to me, the owner only. '
                           'Please do not invite people without notify me.' + inviter)
            await room.say('Please contact me: by send "ding" to me, I will re-send you a invitation. '
                           'Now I will remove you out, sorry.' + ''.join(invitee_list))
            await room.topic('ding - warn ' + inviter.name())
            scheduler = AsyncIOScheduler()
            for i in invitee_list:
                scheduler.add_job(room.delete, args=[i], seconds=10)
            scheduler.start()
        else:
            await room.say('Welcome to my room! :)')
            welcomeTopic = ', '.join(map(lambda c: c.name, invitee_list))
            await room.topic('ding - welcome ' + welcomeTopic)
    except Exception as e:
        log.exception(e)


async def manage_ding_room(bot):
    time.sleep(3)
    log.info('Bot' + 'manage_ding_room()')
    try:
        room = await bot.Room.find(topic='ding')
        if not room:
            log.warning('Bot ' + 'there is no room topic ding(yet)')
            return
        log.info('Bot' + 'start monitor "ding" room join/leave/topic event')

        def on_join(inviteeList, inviter):
            log.info('room.on(join) id:', room.room_id)
            check_room_join(bot, room, inviteeList, inviter)

        def on_leave(leaverList, remover):
            log.info('Bot' + 'Room EVENT: leave - "%s" leave(remover "%s"), bye bye' % (','.join(leaverList),
                                                                                        remover or 'unknown'))

        def on_topic(topic, oldTopic, changer):
            log.info('Bot' +
                     'Room EVENT: topic - changed from "%s" to "%s" by member "%s"' % (oldTopic, topic, changer.name()))

        room.on('join', on_join)
        room.on('leave', on_leave)
        room.on('topic', on_topic)
    except Exception as e:
        log.exception(e)


async def put_in_room(contact, room):
    log.info('Bot' + 'put_in_room("%s", "%s")' % (contact.name(), await room.topic()))
    try:
        await room.add(contact)
        scheduler = AsyncIOScheduler()
        scheduler.add_job(lambda x: room.say('Welcome ', contact))
        scheduler.start()
    except Exception as e:
        log.exception(e)


async def get_out_room(contact, room):
    log.info('Bot' + 'get_out_room("%s", "%s")' % (contact, room))
    try:
        await room.say('You said "ding" in my room, I will remove you out.')
        await room.delete(contact)
    except Exception as e:
        log.exception('get_out_room() exception: ', e)


def get_helper_contact(bot):
    log.info('Bot' + 'get_helper_contact()')
    return bot.Contact.find(HELPER_CONTACT_NAME)


async def create_ding_room(bot, contact):
    log.info('create_ding_room("%s")' % contact)
    try:
        helperContact = await get_helper_contact(bot)
        if not helperContact:
            log.warning('get_helper_contact() found nobody')
            await contact.say("""You don't have a friend called "%s", because create a new room at
            least need 3 contacts, please set [HELPER_CONTACT_NAME] in the code first!""" % HELPER_CONTACT_NAME)
            return
        log.info('get_helper_contact() ok. got: "%s"' % helperContact.name())
        contactList = [contact, helperContact]
        await contact.say(
            """There isn't ding room. I'm trying to create a room with "{0}" and you""" % helperContact.name())
        room = await bot.Room.create(contactList, 'ding')
        log.info('create_ding_room() new ding room created: "%s"' % room)
        await room.topic('ding - created')
        await room.say('ding - created')
        return room
    except Exception as e:
        log.exception('get_helper_contact() exception:', e)


class MyBot(Wechaty):

    # def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
    #             data: Optional[str] = None):
    #     qr_terminal(qr_code, 1)
    #     log.info("{0}\n[{1}] Scan QR Code in above url to login: ".format(qr_code, status))

    def on_error(self, payload):
        log.info(str(payload))

    def on_logout(self, contact: Contact):
        log.info('Bot %s logouted' % contact.name)

    async def on_login(self, contact: Contact):
        msg = contact.payload.name + ' logined'
        log.info('bot ' + msg)
        await contact.say(msg)

        msg = "setting to manage_ding_room() after 3 seconds..."
        log.info('Bot' + msg)
        print(self.user_self())
        await contact.say(msg)
        await manage_ding_room(self)

    async def on_room_join(self, room: Room, invitees: List[Contact],
                           inviter: Contact, date: datetime):
        log.info('Bot' + 'EVENT: room-join - Room "%s" got new member "%s", invited by "%s"' %
                 (await room.topic(), ','.join(map(lambda c: c.name, invitees)), inviter.name))
        print('bot room-join room id:', room.room_id)
        topic = await room.topic()
        await room.say('welcome to "{0}"!'.format(topic), [invitees[0].__str__()])

    async def on_room_leave(self, room: Room, leavers: List[Contact],
                            remover: Contact, date: datetime):
        log.info('Bot' + 'EVENT: room-leave - Room "%s" lost member "%s"' %
                 (await room.topic(), ','.join(map(lambda c: c.name(), leavers))))
        topic = await room.topic()
        name = leavers[0].name if leavers[0] else 'no contact!'
        await room.say('kick off "{0}" from "{1}"!'.format(name, topic))

    async def on_room_topic(self, room: Room, new_topic: str, old_topic: str,
                            changer: Contact, date: datetime):
        try:
            log.info('Bot' + 'EVENT: room-topic - Room "%s" change topic from "%s" to "%s" by member "%s"' %
                     (room, old_topic, new_topic, changer))
            await room.say('room-topic - change topic from "{0}" to "{1}" '
                           'by member "{2}"'.format(old_topic, new_topic, changer.name))
        except Exception as e:
            log.exception(e)

    async def on_message(self, msg: Message):
        if msg.age() > 3 * 60:
            log.info('Bot' + 'on(message) skip age("%d") > 3 * 60 seconds: "%s"', msg.age(), msg)
            return
        room = msg.room()
        talker = msg.talker()
        text = msg.text()
        if not talker:
            return
        if msg.is_self():
            return
        if re.search('^ding$', text):
            if room:
                if re.search('^ding', await room.topic()):
                    await get_out_room(talker, room)
            else:
                try:
                    dingRoom = await self.Room.find('^ding')
                    if dingRoom:
                        log.info('Bot' + 'onMessage: got dingRoom: "%s"' % await dingRoom.topic())
                        if await dingRoom.has(talker):
                            topic = await dingRoom.topic()
                            log.info('Bot' + 'onMessage: sender has already in dingRoom')
                            await dingRoom.say('I found you have joined in room "{0}"!'.format(topic), talker)
                            await talker.say(
                                'no need to ding again, because you are already in room: "{}"'.format(topic))
                        else:
                            log.info('Bot' + 'onMessage: add sender("%s") to dingRoom("%s")' % (
                                talker.name, dingRoom.topic()))
                            await talker.say('ok, I will put you in ding room!')
                            await put_in_room(talker, dingRoom)
                    else:
                        log.info('Bot' + 'onMessage: dingRoom not found, try to create one')
                        newRoom = await create_ding_room(self, talker)
                        print('create_ding_room id:', newRoom.id)
                        await manage_ding_room(self)
                except Exception as e:
                    log.exception(e)


async def main():
    bot = MyBot()
    await bot.start()


if __name__ == '__main__':
    asyncio.run(main())
