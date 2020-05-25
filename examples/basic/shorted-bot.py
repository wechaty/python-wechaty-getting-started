import asyncio, os
from wechaty import Wechaty, WechatyOptions
os.environ['WECHATY_PUPPET_HOSTIE_TOKEN'] = 'your-token-here'

async def run():
    Wechaty.on('')