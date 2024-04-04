from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery

from channels_db.subscribers_dao import save_chan_subs, delete_chan_subs, select_channel_subs
from code_bot.keyboards.with_channels import kbd_with_channels, btn_gift


private_router = Router()


CHAT_ID = [] # Список из id каналов, на которые необходимо подписаться


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
