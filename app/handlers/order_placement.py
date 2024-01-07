import datetime
import config
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from app.keyboards.inline_kb import generate_calendar_markup, payment_kb, ordering_solution
from app.FSM.fsm import OrderPlacement
from app.database.requests import (
    adding_order_information,
    payment_cart,
    product_name_desc_price,
    retrieve_data,
    id_order_user,
    clear_cart_pr,
    payment_confirmation
)
from app.keyboards.reply_rb import user_menu_kb

payment = Router()

@payment.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Вы не заполняете форму, поэтому невозможно воспользоваться данной командой!'
    )

@payment.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Отмена заполнения формы\n\nПри необходимости заполните форму заново'
    )
    await state.clear()

@payment.message(F.text.endswith('Оформить заказ'), StateFilter(default_state))
async def process_payment(message: Message, state: FSMContext):
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    current_date = now.date()
    await message.answer('🗓 Укажите дату торжества, к которой необходим торт', reply_markup=await generate_calendar_markup(current_year, current_month, current_date))
    await state.set_state(OrderPlacement.data)

@payment.callback_query(F.data.startswith('calendar'))
async def process_calendar_callback(callback: CallbackQuery):
    _, year, month = callback.data.split("_")
    if 0 < int(month) < 13:
        current_date = datetime.datetime.now().date()
        markup = await generate_calendar_markup(int(year), int(month), current_date)

        await callback.bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=markup)
    else:
        await callback.answer('Вы пытаетесь выйти за пределы текущего года!')

@payment.callback_query(F.data.startswith('day🔒'))
@payment.callback_query(F.data.startswith('day'), StateFilter(OrderPlacement.data))
async def process_day_callback(callback: CallbackQuery, state: FSMContext):
    day = callback.data.split('_')[0][-1] 
    day_day = callback.data.split('_')[-1] 
    print(day_day[-1])
    if day != '🔒' and day_day != ' ':
        _, year, month, day = callback.data.split("_")
        selected_date = f"{day}.{month}.{year}"
        await state.update_data({'data':selected_date})
        await callback.answer(f'Дата доставки установлена на {selected_date}. Спасибо!')
        await callback.message.delete()
        await callback.message.answer('🚩Укажите адрес\n\nФормат: г.Москва, ул.Московская, д.1, кв.100')
        await state.set_state(OrderPlacement.address)
    else:
        await callback.answer('Данную дату нельзя выбрать')

@payment.message(StateFilter(OrderPlacement.address))
async def process_address(message: Message, state: FSMContext):
    await state.update_data({'address':message.text})
    result = await state.get_data()
    order = await payment_cart(message.from_user.id)
    content = [await product_name_desc_price(item[0]) for item in order]
    killo = [item[1] for item in order]
    _price = [item[0][1] for item in content]
    name_prod = [item[0][0] for item in content]
    desc_name_killo = dict(zip(name_prod, killo))
    total_cost = sum([float(i * killo[idx])  for idx, i in enumerate(_price)])
    address_d = result['address']

    if await adding_order_information(message.from_user.id, address_d, desc_name_killo, result['data'], total_cost):
        await message.answer('Заказ оформлен!', reply_markup=await payment_kb(message.from_user.id))
        await state.clear()
    else:
        await message.answer('Произошла ошибка обратитесь к администратору')
        await state.clear()

@payment.callback_query(F.data.startswith('order1'))
@payment.callback_query(F.data.startswith('order2'))
async def process_order1(callback: CallbackQuery):
    await callback.message.delete()
    id_order = await id_order_user(callback.from_user.id)
    index = id_order.all()[-1][0]
    content = await retrieve_data(index)
    if callback.data.split("_")[0] == 'order1':
        await callback.message.answer('Тестовая карта\n\nНомер карты: 1111 1111 1111 1026\nММ/ГГ: 12/22\nCVC: 000\n\nДанная карта предназначена только для тестирования платежной системы!')
        await callback.bot.send_invoice(
            chat_id=callback.from_user.id,
            title='Оплата корзины',
            description='; '.join([f'{k}: {v} шт.' for k, v in content[0][3].items()]),
            provider_token=config.TOKEN_YOUCASSA,
            payload=f'month_sub_{index}',
            currency='rub',
            prices=[{'label': 'Руб', 'amount': f"{content[0][4] * 100:.2f}"}],
            start_parameter='new_BOT',
        )
    elif callback.data.split("_")[0] == 'order2':
        await clear_cart_pr(callback.from_user.id)
        content = content[0]
        pos = '; '.join([f'{k}: {v} шт.' for k, v in content[3].items()])
        await callback.message.answer('✅ Товар оформлен и оплачен!\n\nОжидайте... Адинистратор с Вами свяжеться', reply_markup=await user_menu_kb())
        await callback.message.bot.send_message(chat_id=config.ADMIN_ID, text=f'Новый заказ № {index} от {callback.from_user.first_name}\n\nДата готовности: {content[1]}\n\nПозиции: {pos}\n\n💸 ОБЩАЯ СТОИМОСТЬ: {content[4]} RUB\n\n♻️ СТАТУС ОПЛАТЫ: {"✅" if content[5]else "❌"}', reply_markup=await ordering_solution(index, callback.from_user.id))
        
    
    await callback.answer()

@payment.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout: types.PreCheckoutQuery):
    await pre_checkout.answer(ok=True)

@payment.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: Message):
    index = message.successful_payment.invoice_payload.split('_')[-1]
    await payment_confirmation(message.from_user.id, int(index))
    await clear_cart_pr(message.from_user.id)
    content = await retrieve_data(index)
    content = content[0]
    pos = '\n'.join([f'{k}: {v} шт.' for k, v in content[3].items()])
    await message.answer('✅ Товар оформлен и оплачен!\n\nОжидайте... Адинистратор с Вами свяжеться', reply_markup=await user_menu_kb())
    await message.bot.send_message(chat_id=config.ADMIN_ID, text=f'Новый заказ № {index} от {message.from_user.first_name}\n\nДата готовности: {content[1]}\n\nПозиции: {pos}\n\n💸 ОБЩАЯ СТОИМОСТЬ: {content[4]} RUB\n\n♻️ СТАТУС ОПЛАТЫ: {"✅" if content[5]else "❌"}', reply_markup=await ordering_solution(index, message.from_user.id))
    
