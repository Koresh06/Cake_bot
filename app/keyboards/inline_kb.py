from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.database.requests import *


async def new_user(tg_id, first_name):
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text=f'{first_name}',url=f'tg://user?id={tg_id}'))
    return builder.as_markup()

async def categories():
    cat = await output_categories()
    builder = InlineKeyboardBuilder()
    for i in cat:
        builder.row(InlineKeyboardButton(text=i[0], callback_data=f'categ_{str(i[1])}'))
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text='Добавить категорию', callback_data='add_categor'))
    return builder.as_markup()

non_categor = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Добавить категорию', callback_data='add_categor')]
    ]
)

async def user_categories():
    cat = await output_categories()
    builder = InlineKeyboardBuilder()
    for i in cat:
        builder.row(InlineKeyboardButton(text=i[0], callback_data=f'user.categ_{i[1]}'))
    builder.adjust(1)
    return builder.as_markup()

async def cake_weight(categ):
    builder = InlineKeyboardBuilder()

    for i in range(1, 6):
        builder.row(InlineKeyboardButton(text=f'{i} кг (от {100 * i} RUB)', callback_data=f'weight_{categ}_{i}'))

    builder.adjust(1)
    return builder.as_markup()

async def add_cart(id_categ, id_product, index=0):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🛒 Добавить в корзину', callback_data=f'{id_categ}_{id_product}_{index}_add_cart'))
    count_quant = await count_quantuty(id_categ)
    builder.row(InlineKeyboardButton(text='« Назад', callback_data=f'back_{id_categ}_{index}'),
                InlineKeyboardButton(text=f'{index + 1}/{count_quant}', callback_data=f'count.value_{id_categ}_{index + 1}_{count_quant}'),
                InlineKeyboardButton(text='Вперед »', callback_data=f'forward_{id_categ}_{index}'))
    builder.row(InlineKeyboardButton(text='⬅️ Каталог', callback_data='bat_categ'))
    return builder.as_markup()

async def user_cart_product(id_categ, id_product, index=0):
    builder = InlineKeyboardBuilder()

    count_product = await check_quantuty(id_product)
    count_quant = await count_quantuty(id_categ)
    builder.row(
        InlineKeyboardButton(text='🔽', callback_data=f'{id_categ}_{id_product}_{index}_minus'),
        InlineKeyboardButton(text=f'🛒 {count_product} шт.', callback_data=f'{id_product} count'),
        InlineKeyboardButton(text='🔼', callback_data=f'{id_categ}_{id_product}_{index}_plus'),
        )
    builder.row(InlineKeyboardButton(text='« Назад', callback_data=f'back_{id_categ}_{index}'),
                InlineKeyboardButton(text=f'{index + 1}/{count_quant}', callback_data=f'count.value_{id_categ}_{index + 1}_{count_quant}'),
                InlineKeyboardButton(text='Вперед »', callback_data=f'forward_{id_categ}_{index}'))
    builder.row(InlineKeyboardButton(text='⬅️ Каталог', callback_data='bat_categ'))
        
    return builder.as_markup()

kb_help = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Администратор', url='https://t.me/korets_24')]
    ]
)

async def menu_catalog(categ, index):
    builder = InlineKeyboardBuilder()
    categ_d = await check_name_cake(categ)

    for count, elen in enumerate(categ_d):
        if count == index:
            builder.row(
                InlineKeyboardButton(text=f'👁 🍽 {elen[0]}', callback_data=f'men.cat_{categ}_{count}')
            )
        else:
            builder.row(
                InlineKeyboardButton(text=f'🍽 {elen[0]}', callback_data=f'men.cat_{categ}_{count}')
            )

    return builder.as_markup()

