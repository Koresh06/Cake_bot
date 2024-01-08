import calendar
import datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup 

from app.requests.keyboard_requests import (
    check_name_cake, 
    count_quantuty, 
)
from app.requests.admin_requests import output_categories, users
from app.requests.product_cards_requests import check_quantuty
from app.requests.order_user_requests import nomer_order, nomer_assembly_user

import tracemalloc
tracemalloc.start()


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
        InlineKeyboardButton(text=f'🛒 {count_product} кг.', callback_data=f'{id_product} count'),
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

    
async def generate_calendar(year, month, current_date):
    cal = calendar.monthcalendar(year, month)
    month_days = []

    for week in cal:
        week_days = []
        for day in week:
            if day == 0:
                week_days.append(" ")
            elif datetime.date(year, month, day) < current_date:
                week_days.append(f"🔒 {day}")
            else:
                week_days.append(str(day))
        month_days.append(week_days)

    return month_days

async def generate_calendar_markup(year, month, current_date):
    month_days = await generate_calendar(year, month, current_date)

    markup = InlineKeyboardBuilder()

    for week in month_days:
        for day in week:
            if day[0] == '🔒':
                markup.add(InlineKeyboardButton(text=day, callback_data=f"day🔒_{year}_{month}_{day}"))
            else: 
                markup.add(InlineKeyboardButton(text=day, callback_data=f"day_{year}_{month}_{day}"))
    markup.adjust(7)
    markup.row(InlineKeyboardButton(text='◀️', callback_data=f"calendar_{year}_{month-1}"),
               InlineKeyboardButton(text=f"{calendar.month_name[month]} {year}", callback_data="ignore"),
               InlineKeyboardButton(text='▶️', callback_data=f"calendar_{year}_{month+1}"))
    
    return markup.as_markup()


async def payment_kb(tg_id):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='💳 Оплатить сейчас', callback_data=f'order1_{tg_id}'),
        InlineKeyboardButton(text='🎁 Оплатить после получения заказа', callback_data=f'order2_{tg_id}')
    )
    builder.adjust(1)
    return builder.as_markup()

async def ordering_solution(index, tg_id):
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text='Принять заказ', callback_data=f'readiness_{index}_{tg_id}'))
    builder.add(InlineKeyboardButton(text='Отклонить', callback_data=f'del_{index}_{tg_id}'))

    return builder.as_markup()

async def users_inline_buttons():
    but = await users()
    
    builder = InlineKeyboardBuilder()
    for item in but:
        builder.add(InlineKeyboardButton(text=item[0], url=f'tg://user?id={item[1]}'))
    builder.adjust(1)
    return builder.as_markup()

async def admin_order():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Заказы из каталога', callback_data='order_catalog'),
        InlineKeyboardButton(text='Торты на заказ', callback_data='cake_collection')
    )
    builder.adjust(1)
    return builder.as_markup()

async def user_orders_list(tg_id):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='📊 Заказы в работе', callback_data=f'orders_progress'),
        InlineKeyboardButton(text='👷🎂 Сборки тортов', callback_data=f'cake_assembly_{tg_id}'),
        InlineKeyboardButton(text='📖 История', callback_data=f'user_history_{tg_id}')
    )
    builder.adjust(1)
    return builder.as_markup()

async def order_nomer_user(tg_id):
    builder = InlineKeyboardBuilder()

    nomer = await nomer_order(tg_id)

    for item in nomer:
        builder.add(InlineKeyboardButton(text=f'Заказ № {item[0]}', callback_data=f'nomer_zak_{item[0]}'))
    builder.adjust(1)
    return builder.as_markup()

async def nomer_assembly(tg_id):
    builder = InlineKeyboardBuilder()

    nomer = await nomer_assembly_user(tg_id)

    for item in nomer:
        builder.add(InlineKeyboardButton(text=f'Сборка № {item[0]}', callback_data=f'nomer_assem_{item[0]}'))
    builder.adjust(1)
    return builder.as_markup()

async def payment_cancellation(_id, payment):
    builder = InlineKeyboardBuilder()

    if not payment:
        builder.add(InlineKeyboardButton(text='💵 Оплатить', callback_data=f'pyment_order_{_id}'))
    builder.add(InlineKeyboardButton(text='🚫 Отменить заказ', callback_data=f'cancellation_order_{_id}'))
    builder.add(InlineKeyboardButton(text='⬅️ Назад', callback_data=f'backward_user'))
    builder.adjust(1)
    return builder.as_markup()

async def cancellation_sborka(_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🚫 Отменить заказ', callback_data=f'cancellation_sborka_{_id}'))
    builder.add(InlineKeyboardButton(text='⬅️ Назад', callback_data=f'backward_user'))
    builder.adjust(1)
    return builder.as_markup()
