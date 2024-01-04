from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types.input_media_photo import InputMediaPhoto

from app.database.requests import *
from app.keyboards.inline_kb import *
from app.keyboards.reply_rb import *
from app.FSM.fsm import Collecting_the_cake
from app.filters.filter import CheckImageFilter

import config


router = Router()

@router.message(F.text.endswith('Главное меню'))
@router.message(CommandStart())
async def cmd_start(message: Message):
    user = await chek_user(message.from_user.id, message.from_user.first_name)
    if not user:
        if await add_user(message.from_user.id, message.from_user.first_name):
            await message.answer('Вас приветсвует кондитерская <b>ВКУСНЫЕ ТОРТЫ</b>\n\n', reply_markup=await user_menu_kb())
            await message.bot.send_message(chat_id=config.ADMIN_ID, text=f'Новый пользователь - {message.from_user.first_name}', reply_markup=await new_user(message.from_user.id, message.from_user.first_name))
        else:
            await message.answer('Ошибка, обратитесь к администратору: https://t.me/korets_24')
    else:
        await message.answer('Доброго времени суток, мы рады вновь Вас приветствать в нашей кондитерской <b>ВКУСНЫЕ ТОРТЫ</b>\n\nДля работы с ботом выберите команду из меню ⬇️', reply_markup=await user_menu_kb())

@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Вы не заполняете форму, поэтому невозможно воспользоваться данной командой!'
    )

@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Отмена заполнения формы\n\nПри необходимости заполните форму заново'
    )
    await state.clear()

@router.message(F.text.endswith('Меню'))
async def cmd_categories_product(message: Message):
    await message.answer('Выбирете', reply_markup=await men_menu())

@router.message(F.text.endswith('Собрать свой торт'), StateFilter(default_state))
async def cmd_categories_product(message: Message, state: FSMContext):
    await message.answer('Магазин <b>"ВКУСНЫЕ ТОРТЫ"</b> предоставляет услугу по собору своего торта\n\nДля реализации задуманного укажите событие, на которое требуется прbготовить торт\n\n❌ Отмена - /cancel')
    await state.set_state(Collecting_the_cake.event)

@router.message(StateFilter(Collecting_the_cake.event))
async def process_event(message: Message, state: FSMContext):
    await state.update_data(event=message.text)
    await message.answer('Далее нам от Вас потребуется описание торта, по параметрам:\n\nВес (в кг.) -\nКоличество уровлней (1, 2 ...) -\nФормы каждого уровня (Прямоугольник, круг, сердце, <i>Ваш вариант</i>) -\nЦвет глазури -\nНачинка (бисквит и т.д.) -\nНадпись на торте (при необходимости)\nТакже можете указать любые Ваши пожелания\n\n❌ Отмена - /cancel')
    await state.set_state(Collecting_the_cake.description)

@router.message(StateFilter(Collecting_the_cake.description))
async def process_descriphion(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Загрузите 📷 фото примерного торта, который Вам необходим\n\n❌ Отмена - /cancel')
    await state.set_state(Collecting_the_cake.image)

@router.message(StateFilter(Collecting_the_cake.image), CheckImageFilter())
async def process_image(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    total = await state.get_data()
    if await collecting_cake(total, message.from_user.id):
        await message.answer_photo(total['image'], caption=f"<b><i>Событие:</i></b> {total['event']}\n\n<b><i>Описание:</i></b> {total['description']}")
        await message.answer('✅ Ваш заказ успешно отправлен администратору на рассмотрение', reply_markup=await user_menu_kb())
        await message.bot.send_photo(chat_id=config.ADMIN_ID, photo=total['image'], caption=f"<b><i>Событие:</i></b> {total['event']}\n\n<b><i>Описание:</i></b> {total['description']}", reply_markup=await new_user(message.from_user.id, message.from_user.first_name))
    else:
        await message.answer('Произошла ошибка')


@router.message(F.text.endswith('Каталог'))
async def cmd_categories_product(message: Message):
    name_categories = await output_categories()
    if name_categories:
        await message.answer('Категории', reply_markup=await user_categories())
    else:
        await message.answer('Каталог категорий пуст', reply_markup=await user_menu_kb())

@router.callback_query(F.data.startswith('user_categ '))
async def cmd_fast_food(callback: CallbackQuery):
    await callback.message.delete()
    item = await output_fast_food(int(callback.data.split()[-1]))
    if item:
        await callback.message.answer_photo(item[0][1], caption=f"🍰 <b><i>Наименование:</i></b> {item[0][0]}  \n\n🔖 <b><i>Состав/описание торта:</i></b> {item[0][2]}\n\n💵 <b><i>Прайс:</i></b> {item[0][3]} RUB", reply_markup=await add_cart(int(callback.data.split()[-1]), item[0][4]))
        await callback.answer()
    else:
        await callback.message.answer('На данный момент каталог продуктов пуст, загляните к нам чуть позже')
        await callback.answer()

@router.callback_query(F.data.startswith('forward'))
async def cmd_fast_food(callback: CallbackQuery):
    categ_id = int(callback.data.split('_')[-2])
    index = int(callback.data.split('_')[-1])
    item = await output_fast_food(categ_id)
    if item:
        if index < len(item) - 1:
            index += 1
            await callback.message.edit_media(media=InputMediaPhoto(media=item[index][1]))
            await callback.message.edit_caption(caption=f"🍰 <b><i>Наименование:</i></b> {item[index][0]}  \n\n🔖 <b><i>Состав/описание торта:</i></b> {item[index][2]}\n\n💵 <b><i>Прайс:</i></b> {item[index][3]} RUB", reply_markup=await add_cart(categ_id, item[index][4], index))
            await callback.answer()
        else:
            await callback.message.edit_media(media=InputMediaPhoto(media=item[0][1]))
            await callback.message.edit_caption(caption=f"🍰 <b><i>Наименование:</i></b> {item[0][0]}  \n\n🔖 <b><i>Состав/описание торта:</i></b>{item[0][2]}\n\n💵 <b><i>Прайс:</i></b> {item[0][3]} RUB", reply_markup=await add_cart(categ_id, item[0][4]))
            await callback.answer()
    else:
        await callback.message.answer('На данный момент каталог продуктов пуст, загляните к нам чуть позже')
        await callback.answer()

@router.callback_query(F.data.startswith('back'))
async def cmd_fast_food(callback: CallbackQuery):
    categ_id = int(callback.data.split('_')[-2])
    index = int(callback.data.split('_')[-1])
    item = await output_fast_food(categ_id)
    if item:
        if index > 0:
            index -= 1
            await callback.message.edit_media(media=InputMediaPhoto(media=item[index][1]))
            await callback.message.edit_caption(caption=f"🍰 <b><i>Наименование:</i></b>{item[index][0]}  \n\n🔖 <b><i>Состав/описание торта:</i></b> {item[index][2]}\n\n💵 <b><i>Прайс:</i></b>{item[index][3]} RUB", reply_markup=await add_cart(categ_id, item[index][4], index))
            await callback.answer()
        else:
            await callback.message.edit_media(media=InputMediaPhoto(media=item[-1][1]))
            await callback.message.edit_caption(caption=f"🍰 <b><i>Наименование:</i></b>{item[-1][0]}  \n\n<b><i>Состав/описание торта:</i></b> {item[-1][2]}   \n\n💵 <b><i>Прайс:</i></b>{item[-1][3]} RUB", reply_markup=await add_cart(categ_id, item[-1][4], len(item) - 1))
            await callback.answer()
    else:
        await callback.message.answer('На данный момент каталог продуктов пуст, загляните к нам чуть позже')
        await callback.answer()

#Уменьшение количества товара, при попытке уменьшить меньше еденицы товар удаляется из корзины и переход в исходную клаву
@router.callback_query(F.data.endswith('minus'))
async def cmd_minus(callback: CallbackQuery):
    id_categ = int(callback.data.split('_')[0])
    id_product = int(callback.data.split('_')[1])
    index = int(callback.data.split('_')[2])
    if await minus_count_product(id_product):
        await callback.message.edit_reply_markup(reply_markup=await user_cart_product(id_categ, id_product, index))
    else:
        await delete_cart(callback.from_user.id, id_product)
        await callback.message.edit_reply_markup(reply_markup=await add_cart(id_categ, id_product, index))

#Добавление количества товара, максимальное количество 10 шт.
@router.callback_query(F.data.endswith('plus'))
async def cmd_minus(callback: CallbackQuery):
    id_categ = int(callback.data.split('_')[0])
    id_product = int(callback.data.split('_')[1])
    index = int(callback.data.split('_')[2])
    if await plus_count_product(id_product):
        await callback.message.edit_reply_markup(reply_markup=await user_cart_product(id_categ, id_product, index))
    else:
        await callback.answer('Максимальное количество 10 шт.')

@router.callback_query(F.data.endswith('count'))
async def cmd_minus(callback: CallbackQuery):
    check_count = await check_quantuty(int(callback.data.split()[0]))
    await callback.answer(f'У вас в корзине 🛒 {check_count} шт.')
    await callback.answer()

@router.callback_query(F.data.startswith('count.value'))
async def count_quanty(callback: CallbackQuery):
    current_value = int(callback.data.split('_')[-2])
    categ = int(callback.data.split('_')[-1])
    await callback.answer(text=f'Товар №{current_value} из {categ}', show_alert=True)
    await callback.answer()

#Уменьшение количества товара, при попытке уменьшить меньше еденицы товар удаляется из корзины и переход в исходную клаву
@router.callback_query(F.data.endswith('minus'))
async def cmd_minus(callback: CallbackQuery):
    id_categ = int(callback.data.split('_')[0])
    id_product = int(callback.data.split('_')[1])
    index = int(callback.data.split('_')[2])
    if await minus_count_product(id_product):
        await callback.message.edit_reply_markup(reply_markup=await user_cart_product(id_categ, id_product, index))
    else:
        await delete_cart(callback.from_user.id, id_product)
        await callback.message.edit_reply_markup(reply_markup=await add_cart(id_categ, id_product, index))

#Добавление количества товара, максимальное количество 10 шт.
@router.callback_query(F.data.endswith('plus'))
async def cmd_minus(callback: CallbackQuery):
    id_categ = int(callback.data.split('_')[0])
    id_product = int(callback.data.split('_')[1])
    index = int(callback.data.split('_')[2])
    if await plus_count_product(id_product):
        await callback.message.edit_reply_markup(reply_markup=await user_cart_product(id_categ, id_product, index))
    else:
        await callback.answer('Максимальное количество 10 шт.')

@router.callback_query(F.data.endswith('count'))
async def cmd_minus(callback: CallbackQuery):
    check_count = await check_quantuty(int(callback.data.split()[0]))
    await callback.answer(f'У вас в корзине 🛒 {check_count} шт.')
    await callback.answer()


#При изменении количества изменяется клава
@router.callback_query(F.data.endswith('add_cart'))
async def cmd_add_cart(callback: CallbackQuery):
    id_categ = int(callback.data.split('_')[0])
    id_product = int(callback.data.split('_')[1])
    index = int(callback.data.split('_')[2])
    if await add_cart_product(callback.from_user.id, id_product):
        await callback.message.edit_reply_markup(reply_markup=await user_cart_product(id_categ, id_product, index))
        await callback.answer(text='Товар добавлен в корзину')
    else:
        await callback.answer('Товар уже был добавлен в корзину', show_alert=True)

@router.callback_query(F.data == 'bat_categ')
async def cmd_categ_back(callback: CallbackQuery):
    if await output_categories():
        await callback.message.delete()
        await callback.message.answer('Категории', reply_markup=await user_categories())
        await callback.answer()
    else:
        await callback.message.answer('Каталог пуст, для добавления нажмите ⬇️')

@router.message(F.text.endswith('Корзина'))
async def cmd_cart(message: Message):

    items = await check_user_cart(message.from_user.id)
    if items:
        lst_menu = []
        for item in items:
            parser_product_attr = await pars_product(item[0])
            lst_menu.append(parser_product_attr)

        content = '\n➖➖➖➖➖➖➖➖➖➖➖\n'.join([f"|-🍽 {lst_menu.index(item) + 1}. {item[0][0]}\n|-{item[1]} шт. х {item[0][1]} = {item [1] * item[0][1]} BYN" for item in lst_menu])
        total_cost = sum([i[1] * i[0][1] for i in lst_menu])
        name_count_product = [(item[0][0], item[1]) for item in lst_menu]

        await message.answer(text=f'🛒 Ваша корзина:\n\n{content}\n\n💸 ИТОГО: {total_cost} RUB', reply_markup=await kb_menu_cart(name_count_product))
        
    else:
        await message.answer('Корзина пуста, перейдите в котолог [📋 Меню] и сделайте свой выбор', reply_markup=await user_menu_kb())

#Удаление позиций из корзины
@router.message(F.text.startswith('❌'))
async def cmd_delete_product(message: Message):
    name = message.text.split('.')[1]
    if await count_minus(name):
        items = await check_user_cart(message.from_user.id)
        if items:
            lst_menu = []
            for item in items:
                parser_product_attr = await pars_product(item[0])
                lst_menu.append(parser_product_attr)

            content = '\n➖➖➖➖➖➖➖➖➖➖➖\n'.join([f"|-🍽 {lst_menu.index(item) + 1}. {item[0][0]}\n|-{item[1]} шт. х {item[0][1]} = {item [1] * item[0][1]} BYN" for item in lst_menu])
            total_cost = sum([i[1] * i[0][1] for i in lst_menu])
            name_count_product = [(item[0][0], item[1]) for item in lst_menu]

            await message.answer(text=f'🛒 Ваша корзина:\n\n{content}\n\n💸 ИТОГО: {total_cost} RUB', reply_markup=await kb_menu_cart(name_count_product))
        else:
            await message.answer('Корзина пуста, перейдите в котолог [📋 Меню] и сделайте свой выбор')
    else:
        if await delete_menu_product(name):
            items = await check_user_cart(message.from_user.id)
            if items:
                lst_menu = []
                for item in items:
                    parser_product_attr = await pars_product(item[0])
                    lst_menu.append(parser_product_attr)

                content = '\n➖➖➖➖➖➖➖➖➖➖➖\n'.join([f"|-🍽 {lst_menu.index(item) + 1}. {item[0][0]}\n|-{item[1]} шт. х {item[0][1]} = {item[1] * item[0][1]} BYN" for item in lst_menu])
                total_cost = sum([i[1] * i[0][1] for i in lst_menu])
                name_count_product = [(item[0][0], item[1]) for item in lst_menu]

                await message.answer(text=f'🛒 Ваша корзина:\n\n{content}\n\n💸 ИТОГО: {total_cost} RUB', reply_markup=await  kb_menu_cart(name_count_product))
            else:
                await message.answer('Корзина пуста, перейдите в котолог [📋 Меню] и сделайте свой выбор', reply_markup=await user_menu_kb())

@router.message(F.text.endswith('Очистить корзину'))
async def clear_cart(message: Message):
    if await clear_cart_pr(message.from_user.id):
        await message.answer('Корзина очищена, для пополнения переёдите в 📋 Меню)', reply_markup=await user_menu_kb())
    else:
        await message.answer('Ошибка, обратитесь к администратору [🤝 Помощь]')

@router.message(F.text.endswith('Помощь'))
async def cmd_help(message: Message):
    await message.answer('🔸У вас возникли вопросы?\nМы с удовольствием ответим!\n', reply_markup=kb_help)

@router.message()
async def cmd_echo(message: Message):
    await message.answer('Данная команда/текст находится в разработке или вы пишите какую-то ерунду и бот Вас не понимает 🥴')