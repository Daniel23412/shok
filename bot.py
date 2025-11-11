# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder

# === НАСТРОЙКИ ===
BOT_TOKEN = "8540670040:AAFyqoJNU2LVjbub-IJFQ9jqIbAiwIMNknE"  # ← твой токен
REF_LINK = "https://lkbz.pro/e1877d"

# ← ВСТАВЬ СВОИ file_id ↓
PHOTO_REG_1 = "AgACAgIAAxkBAAI..."
PHOTO_REG_2 = "AgACAgIAAxkBAAI..."
PHOTO_SIGNAL = "AgACAgIAAxkBAAI..."

logging.basicConfig(level=logging.INFO)

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# === СОСТОЯНИЯ (ВАЖНО: ДО ВСЕХ ХЕНДЛЕРОВ!) ===
class UserState(StatesGroup):
    registered = State()

# === Клавиатуры ===
def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="INSTRUCTION", callback_data="instruction")
    kb.button(text="Start", callback_data="start_game")
    kb.adjust(1)
    return kb.as_markup()

def instruction_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="Register", url=REF_LINK)
    kb.button(text="Restricted? Click here", callback_data="vpn")
    kb.button(text="Main", callback_data="main")
    kb.adjust(1)
    return kb.as_markup()

def after_restricted():
    kb = InlineKeyboardBuilder()
    kb.button(text="Registered", callback_data="registered")
    kb.button(text="Start", callback_data="start_game")
    kb.adjust(1)
    return kb.as_markup()

# === Хендлеры ===
@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    text = (
        "Welcome to <b>MINES Sora2</b>\n\n"
        "Mines is a gambling game at 1win bookmaker.\n"
        "Your goal is to open safe cells and avoid falling into traps.\n\n"
        "Our bot is based on a <b>neural network from SoraV2</b>\n"
        "It can predict the location of stars with a probability of <b>97%</b>"
    )
    await message.answer(text, reply_markup=main_menu())

@dp.callback_query(F.data == "main")
async def back_to_main(call: types.CallbackQuery):
    text = (
        "Welcome to <b>MINES Sora2</b>\n\n"
        "Mines is a gambling game at 1win bookmaker.\n"
        "Your goal is to open safe cells and avoid falling into traps.\n\n"
        "Our bot is based on a <b>neural network from SoraV2</b>\n"
        "It can predict the location of stars with a probability of <b>97%</b>"
    )
    await call.message.edit_text(text, reply_markup=main_menu())

@dp.callback_query(F.data == "instruction")
async def send_instruction(call: types.CallbackQuery):
    text = (
        "1. Register here 1WIN\n"
        "2. Enter promocode: <b>LDBONUS</b> (GET 500% BONUS)\n"
        "3. Make at least a 5-10$ Deposit (500|5|200)\n"
        "4. Write @ to get access"
    )
    await call.message.delete()
    await call.message.answer_photo(PHOTO_REG_1)
    await call.message.answer_photo(PHOTO_REG_2)
    await call.message.answer(text, reply_markup=instruction_menu())

@dp.callback_query(F.data == "vpn")
async def vpn_instruction(call: types.CallbackQuery):
    text = (
        "<b>First you download any VPN and (turn on Argentina)</b>\n"
        "Then find your country code at 1WIN!\n"
        "CHECK"
    )
    await call.message.edit_text(text, reply_markup=after_restricted())

@dp.callback_query(F.data == "registered")
async def mark_registered(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.registered)
    await call.message.edit_text("Registration confirmed! Now press Start.", reply_markup=after_restricted())

@dp.callback_query(F.data == "start_game")
async def start_game(call: types.CallbackQuery, state: FSMContext):
    if await state.get_state() != UserState.registered:
        kb = InlineKeyboardBuilder()
        kb.button(text="Register Now", url=REF_LINK)
        await call.message.edit_text(
            "First, register an account\n"
            "Make at least a 5-10$ Deposit (500|5|200)",
            reply_markup=kb.as_markup()
        )
        return

    msg = await call.message.edit_text("The game is found")
    await asyncio.sleep(1)
    await msg.edit_text("The hash has been confirmed .")
    await asyncio.sleep(1)
    await msg.edit_text("Mines: 3\nEffective: 4 min")
    await asyncio.sleep(1)

    kb = InlineKeyboardBuilder()
    kb.button(text="Take the signal", callback_data="get_signal")
    await msg.edit_text("Mines: 3\nEffective: 4 min", reply_markup=kb.as_markup())

@dp.callback_query(F.data == "get_signal")
async def send_signal(call: types.CallbackQuery):
    from datetime import datetime, timedelta
    time = (datetime.now() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M:%S")
    caption = (
        f"<b>GAME 1</b> 11.11.2025 01:00:41 (GMT+3)\n"
        f"<b>Win Probability 99.91 %</b>\n"
        "Signal unavailable"
    )
    await call.message.delete()
    await call.message.answer_photo(PHOTO_SIGNAL, caption=caption)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
