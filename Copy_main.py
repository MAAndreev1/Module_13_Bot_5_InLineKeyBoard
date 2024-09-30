from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Расчитать'), KeyboardButton(text='Информация')]
    ], resize_keyboard=True
)


kb_InL = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_InL.add(button1)
kb_InL.add(button2)

class UserState(StatesGroup):
    age = State()     # Возраст
    growth = State()  # Рост
    weight = State()  # Вес


@dp.message_handler(text = ['Расчитать'])
async def main_menu(message):
    await message.answer('Выберете опцию:', reply_markup = kb_InL)

@dp.callback_query_handler(text= ['formulas'])
async def text_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 х рост (см) - 5 х возраст (г) - 161')
    await call.answer()


@dp.callback_query_handler(text= ['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост.')
    await UserState.growth.set()

@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес.')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = (10 * int(data["weight"])) + (6.5 * int(data["growth"])) - (5 * int(data["age"])) + 5
    await message.answer(f'Ваша норма калорий {calories}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
