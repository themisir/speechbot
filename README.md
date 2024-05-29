# speechbot

Telegram bot to transcribe voice mails to text messages. Currently only available for Azerbaijani language.


## Installation

The project can be hosted as a docker container. You can use the docker-compose configuration below to host your own instance:

```yaml
services:
  bot:
    image: ghcr.io/themisir/speechbot:main
    environment:
      BOT_TOKEN: enter the token you got from @bothfather here
```

## Credits

- [BHOSAI/Pichilti-base-v1](https://huggingface.co/BHOSAI/Pichilti-base-v1)
- [python-telegram-bot](https://python-telegram-bot.org)
