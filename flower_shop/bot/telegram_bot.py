from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

TELEGRAM_TOKEN = '7416609444:AAHlQ3ysCQfOqovyGkzrO9emlLgCGkdC9zc'
TELEGRAM_CHAT_ID = '1445610019'

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

async def send_order_notification(order_info):
    """
    Функция для отправки уведомления о новом заказе в Telegram.
    """
    message = (
        f"Новый заказ!\n"
        f"Имя: {order_info['name']}\n"
        f"Адрес: {order_info['address']}\n"
        f"Телефон: {order_info['phone']}\n"
        f"Общая сумма: {order_info['total_price']} руб.\n"
    )
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def send_status_change_notification(order_id, new_status):
    """
    Функция для отправки уведомления о смене статуса заказа.
    """
    message = (
        f"Статус заказа #{order_id} был изменен!\n"
        f"Новый статус: {new_status}"
    )
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

@dp.message(Command(commands=['start']))
async def start_command(message: types.Message):
    await message.answer("Привет! Этот бот будет уведомлять о новых заказах и изменениях статусов.")

async def main():
    """
    Основная функция для запуска бота.
    """
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
