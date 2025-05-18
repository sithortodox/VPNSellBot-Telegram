# handlers/user/start.py
from db.dao import get_or_create_user
...
@router.message(F.text == "/start")
async def cmd_start(message: Message) -> None:
    # ← добавляем пользователя (если ещё не был)
    await get_or_create_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    is_admin = message.from_user.id in get_settings().admin_ids
    await message.answer(
        "👋 Добро пожаловать!",
        reply_markup=main_menu_kb(is_admin),
    )
