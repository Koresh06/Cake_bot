from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from app.middlewares.middleware import Is_Admin
from app.keyboards.inline_kb import *
from app.keyboards.reply_rb import *
from app.FSM.fsm import Add_categories ,Update_product
from app.filters.filter import IsDigitFilter, CheckImageFilter

admin = Router()

admin.message.middleware(Is_Admin())

@admin.message(Command('admin'), StateFilter(default_state))
async def cmd_admin(message: Message):
    await message.answer('Привет хозяин', reply_markup=await admin_menu_kb())

@admin.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='🚫 Отмена заполнения формы\n\nПри необходимости заполните форму заново'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()

@admin.message(F.text.endswith('Добавить товар'))
async def cmd_add_product(message: Message):
    if await output_categories():
        await message.answer('Категории', reply_markup=await categories())
    else:
        await message.answer('Каталог категорий пуст, для добавления нажмите ⬇️', reply_markup=non_categor)

@admin.callback_query(F.data == 'add_categor', StateFilter(default_state))
async def but_add_categ(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите название категории:\n\n❌ Отмена - /cancel')
    await state.set_state(Add_categories.name)
    await callback.answer()

@admin.message(StateFilter(Add_categories.name))
async def cmd_categ_name(message: Message, state: FSMContext):
    data = await state.update_data(name=message.text)
    if await add_categories(data['name']):
        await message.answer('✅ Категория добавлена успешно')
        await state.clear()
    else:
        await message.answer('🚫 Данная категория уже была добавлена', reply_markup=await admin_menu_kb())
        await state.clear()

@admin.callback_query(F.data.startswith('categ_'), StateFilter(default_state))
async def product_categ(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('🍰 Введите название товара:\n\n❌ Отмена - /cancel')
    await state.set_state(Update_product.name)
    await state.update_data(id_categ=int(callback.data[-1]))
    await callback.answer()

@admin.message(StateFilter(Update_product.name))
async def cmd_name_product(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('📷 Загрузите изображение товара:\n\n❌ Отмена - /cancel')
    await state.set_state(Update_product.image)

@admin.message(StateFilter(Update_product.image), CheckImageFilter())
async def cmd_image_product(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer('🔖 Введите описание товара:\n\n❌ Отмена - /cancel')
    await state.set_state(Update_product.description)

@admin.message(StateFilter(Update_product.description))
async def cmd_description_product(messsage: Message, state: FSMContext):
    await state.update_data(description=messsage.text)
    await messsage.answer('💵 Введите прайс/цену товара:\n\n❌ Отмена - /cancel')
    await state.set_state(Update_product.price)

#Вес торта!
#@admin.message(StateFilter(Update_product.weight))
#async def cmd_description_product(messsage: Message, state: FSMContext):
#    await state.update_data(description=messsage.text)
#    await messsage.answer('Введите вес торта:\n\n❌ Отмена - /cancel')
#    await state.set_state(Update_product.price)

@admin.message(StateFilter(Update_product.price), IsDigitFilter())
async def cmd_price_product(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    product = await state.get_data()
    await message.answer_photo(product['image'])
    await message.answer(f"🍰 <b><i>Наименование:</i></b> {product['name']}\n\n🔖 <b><i>Состав/описание торта:</i></b> {product['description']}\n\n💵 <b><i>Прайс:</i></b> {product['price']} RUB")
    if await add_product_db(message.from_user.id, product):
        await message.answer('✅ Товар успешно добавлен', reply_markup=await admin_menu_kb())
        await state.clear()
    else:
        await message.answer('❌ Произошла ошибка')
        await state.clear()
