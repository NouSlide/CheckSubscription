from aiogram import types


async def kbd_with_channels():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text='1 КАНАЛ', url='https://www.youtube.com/'),
        types.InlineKeyboardButton(text='2 КАНАЛ', url='https://www.youtube.com/')
        # Можно добавить еще каналы
    ],
        [
            types.InlineKeyboardButton(text='ГОТОВО ✅', callback_data='done')
        ]
    ])
    return markup


async def btn_gift():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text='ПЕРЕЙТИ 🏃‍♂️', url='')
    ]])
    return markup
