from aiogram import Router, F
from aiogram.types import Message
from config import get_settings
from keyboards.user_kb import main_menu_kb

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message) -> None:
    settings = get_settings()
    is_admin = message.from_user.id in settings.admin_ids
    await message.answer(
        "👋 Добро пожаловать!",
        reply_markup=main_menu_kb(is_admin),
    )
