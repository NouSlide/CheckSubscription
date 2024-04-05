from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from channels_db.users_dao import add_user, select_user
from channels_db.subscribers_dao import save_chan_subs, delete_chan_subs, select_channel_subs
from code_bot.keyboards.with_channels import kbd_with_channels, btn_gift


private_router = Router()


CHAT_ID = [] # Список из id каналов, на которые необходимо подписаться
ADMIN_ID = 1 # ID администратора бота


class MailingStatesGroup(StatesGroup):
    mailing_txt = State()


@private_router.chat_member()
async def chat_member_handler(update: ChatMemberUpdated):

    if update.chat.id in CHAT_ID:

        if update.new_chat_member.status == 'creator' or update.new_chat_member.status == 'member':
            await save_chan_subs(update.chat.id, update.from_user.id, update.from_user.username)

        elif update.new_chat_member.status == 'left':
            await delete_chan_subs(update.chat.id, update.from_user.id)


@private_router.message(Command('start'))
async def cmd_get(message: Message):
    await message.answer('Чтобы получить подарок, подпишитесь на два канала и жмите <b>ГОТОВО</b>',
                         reply_markup=await kbd_with_channels(), parse_mode='HTML')
    await add_user(message.from_user.full_name, message.from_user.id, message.from_user.username) # Сохранение пользователя в бд


@private_router.callback_query(F.data == 'done')
async def handler_btn_done(callback: CallbackQuery):
    subscribers_lis = []
    for one_channel_id in CHAT_ID:
        subscribers_lis.append(await select_channel_subs(one_channel_id, callback.from_user.id))
    if subscribers_lis.count(callback.from_user.id) == 2: # 2 - это количество каналов, на которые необходимо подписаться:
        # Здесь может быть любой бонус
        await callback.message.edit_text('Поздравляем! 🎉 Вы получаете закрытый доступ к вебинару', reply_markup=await btn_gift())
    else:
        await callback.message.answer('Чтобы продолжить, подпишитесь на два канала ☝️')


# Функция рассылки
@private_router.message(StateFilter(None), Command('send'))
async def cmd_sendall(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await state.set_state(MailingStatesGroup.mailing_txt)
        await message.answer('Введи текст рассылки')


@private_router.message(F.text, MailingStatesGroup.mailing_txt)
async def send_mailing_text(message: Message, state: FSMContext):
    for user_id in await select_user():
        await message.bot.send_message(user_id, message.text)
    await message.answer('Рассылка прошла успешно!')
    await state.clear()

