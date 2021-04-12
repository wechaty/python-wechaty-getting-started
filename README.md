# python-wechaty-getting-started ![PyPI Version](https://img.shields.io/pypi/v/wechaty?color=blue) [![Python 3.7](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)

![Python Wechaty](https://wechaty.github.io/python-wechaty/images/python-wechaty.png)

[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/wechaty/python-wechaty-getting-started)
[![Wechaty in Python](https://img.shields.io/badge/Wechaty-Python-blue)](https://github.com/wechaty/python-wechaty)

Python Wechaty Starter Project Template that Works Out-of-the-Box

## Connecting Chatbots

[![Powered by Wechaty](https://img.shields.io/badge/Powered%20By-Wechaty-brightgreen.svg)](https://github.com/Wechaty/wechaty)

Wechaty is a RPA SDK for Wechat **Individual** Account that can help you create a chatbot in 9 lines of Python.

## Requirements

1. python3.7+

## Live Coding Video Tutorial

Here's a great live coding video tutorial from our Python Wechaty creator @wj-Mcat: <https://wechaty.js.org/2020/10/26/python-wechaty-live-coding/>

## Quick Start

1. Clone python-wechaty-getting-started repository

   ```shell
   git clone https://github.com/wechaty/python-wechaty-getting-started
   cd python-wechaty-getting-started
   ```

2. Install Dependencies

   ```shell
   make install
   # or
   pip install -r requirements.txt
   ```

3. Set token for your bot

    ```sh
    # examples/ding-dong-bot.py : func-> main()
    # it must be donut token
    export WECHATY_PUPPET=wechaty-puppet-service
    export WECHATY_PUPPET_SERVICE_TOKEN=your_token_at_here
    ```
   
    or you can use `TOKEN` or `token` environment variable alias name to set **token**, for example:

    ```shell
    export TOKEN=your_token_at_here
    # or
    export token=your_token_at_here
    ```

4. Run the bot

   ```shell
   make bot
   # or
   python examples/ding-dong-bot.py
   ```

## The World's Shortest Python ChatBot: 9 lines of Code

```python
from wechaty import Wechaty

import asyncio
async def main():
    bot = Wechaty()
    bot.on('scan', lambda status, qrcode, data: print('Scan QR Code to login: {}\nhttps://wechaty.wechaty.js/qrcode/{}'.format(status, qrcode)))
    bot.on('login', lambda user: print('User {} logged in'.format(user)))
    bot.on('message', lambda message: print('Message: {}'.format(message)))
    await bot.start()
asyncio.run(main())
```

## Wechaty Getting Started in Multiple Languages

- [TypeScript Wechaty Getting Started](https://github.com/wechaty/wechaty-getting-started)
- [Python Wechaty Getting Started](https://github.com/wechaty/python-wechaty-getting-started)
- [Java Wechaty Getting Started](https://github.com/wechaty/java-wechaty-getting-started)
- [Go Wechaty Getting Started](https://github.com/wechaty/go-wechaty-getting-started)

## Badge

[![Wechaty in Python](https://img.shields.io/badge/Wechaty-Python-blue)](https://github.com/wechaty/python-wechaty)

```md
[![Wechaty in Python](https://img.shields.io/badge/Wechaty-Python-blue)](https://github.com/wechaty/python-wechaty)
```

## Maintainers

[@wechaty/python](https://github.com/orgs/wechaty/teams/python/members)

## Copyright & License

- Code & Docs © 2020 Wechaty Contributors <https://github.com/wechaty>
- Code released under the Apache-2.0 License
- Docs released under Creative Commons
