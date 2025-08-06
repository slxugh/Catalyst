import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router
from aiogram.client.default import DefaultBotProperties


async def main():

    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.include_routers(
        router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        
        print("stop")
