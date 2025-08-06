from aiogram import Router, F, Bot
from aiogram.filters import  Command, CommandStart
from aiogram.types import Message, ContentType
import os
from service import r_from_user, r_to_user
router = Router()

@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    tg_id = message.from_user.id
    await message.answer(text=f"<b>Добро пожаловать!</b>\nПишите сообщения, отправляйте видео, фотографии или стикеры и мы обязательно ответим вам в ближайшее время 😁")
    
    check_exist_id = r_from_user.get(name=tg_id)

    if not check_exist_id:
        topic = await bot.create_forum_topic(os.getenv("GROUP_ID"),name=f"{tg_id}")
        r_from_user.set(name=tg_id,value=topic.message_thread_id)
        r_to_user.set(name=topic.message_thread_id,value=tg_id)
    

@router.message(Command("info"))
async def ping(message: Message):
    try:
        await message.answer(text=f"ID GROUP: {message.chat.id}\nID TOPIC: {message.message_thread_id}")
    except Exception as error:
        await message.answer(f"{error}")


@router.message(Command("test"))
async def ping(message: Message):
    try:
        if r_to_user.ping():
            await message.answer("Redis доступен")
        else:
            await message.answer("Redis не доступен")
    except Exception as error:
        await message.answer(f"{error}")


@router.message(F.chat.type == "private")
async def transfer_from_user(message: Message, bot: Bot) -> None:
    await message.answer("Ваше сообщение отправленно 👌")
    await bot.set_message_reaction(chat_id=message.from_user.id,message_id=message.message_id,reaction=[{"type": "emoji", "emoji": "🎉"}])
    await bot.forward_message(chat_id=os.getenv("GROUP_ID"),from_chat_id=message.chat.id,message_id=message.message_id,message_thread_id=r_from_user.get(message.from_user.id))
    

@router.message(F.content_type != ContentType.FORUM_TOPIC_CREATED)
async def forward_to_user(message: Message, bot: Bot):
    topic_id = message.message_thread_id
    user_id = int(r_to_user.get(name=topic_id)) 

    if message.text:
        await bot.send_message(chat_id=user_id, text=f"{message.text}")
        await message.reply(f"Отправлено")
    elif message.photo:
        await bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id, caption=message.caption)
        await message.reply(f"Отправлено")
    elif message.video:
        await bot.send_video(chat_id=user_id, video=message.video.file_id, caption=message.caption)
        await message.reply(f"Отправлено")
    elif message.document:
        await bot.send_document(chat_id=user_id, document=message.document.file_id, caption=message.caption)
        await message.reply(f"Отправлено")
    elif message.sticker:
        await bot.send_sticker(chat_id=user_id, sticker=message.sticker.file_id)
        await message.reply(f"Отправлено")
    else:
        await message.answer(f"⚠️ Этот тип контента пока не поддерживается. Type: {message.content_type}")
    
