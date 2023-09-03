from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import webbrowser
import subprocess
import sqlite3


bot = Bot('6642168984:AAFSfcVaenYSyLcBFFirIkOP5AuiBxCTHO0')
dp = Dispatcher(bot, storage=MemoryStorage())
user_id = 0
nick_name = ''
payment = 0
device = ''
reg_date = ''

callback_need_vpn_filter = ['need_vpn', 'cancel']
callback_device_filter = ['phone_user', 'pc_user']
callback_phone_type_filter = ['android', 'iphone']
callback_computer_type_filter = ['windows', 'macos']
callback_ask_install_filter = ['install_done', 'no_install']

command_first = "./wireguard-install.sh"
command_second = "1"
command_third = "\n\n"


@dp.message_handler(commands=['start'])
async def main(message: types.Message):
    global user_id, nick_name
    user_id = message.from_user.id
    nick_name = message.from_user.full_name

    conn = sqlite3.connect('vpn_nora_users.sql')
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INT auto_increment primary key, 
    nick_name varchar(100),
    payment INT,
    device varchar(100),
    reg_date varchar(50)
    )
    """)
    conn.commit()

    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    btn_need_vpn = types.InlineKeyboardButton(text='Нужен VPN', callback_data='need_vpn')
    btn_cancel = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
    markup.add(btn_need_vpn, btn_cancel)

    await bot.send_message(message.chat.id, 'Привет, <<инф...>>', reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data in callback_need_vpn_filter)
async def callback_need_vpn(callback: types.CallbackQuery):
    if callback.data == 'need_vpn':
        await callback.message.answer('Чтобы воспользоваться нашим сервисом нужно провести оплату')
        await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
        await making_payment(callback.message)
    elif callback.data == 'cancel':
        await callback.message.answer('Если надумаете воспользоваться нашим сервисом обязательно возвращайтесь!')
        await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
    else:
        await callback.message.answer('Пожалуйста, нажмите на кнопку')


async def making_payment(message: types.Message):
    await bot.send_message(message.chat.id, 'Оплата...')
    await bot.send_message(message.chat.id, 'Оплата проведена успешна!')
    await ask_device(message)


async def ask_device(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    btn_phone = types.InlineKeyboardButton(text='На телефон', callback_data='phone_user')
    btn_pc = types.InlineKeyboardButton(text='На ПК', callback_data='pc_user')
    markup.add(btn_phone, btn_pc)

    await bot.send_message(message.chat.id, 'Расскажи для какого устройства тебе нужен VPN', reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data in callback_device_filter)
async def callback_ask_device(callback: types.CallbackQuery):
    if callback.data == 'phone_user':
        await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
        await ask_phone_type(callback.message)
    elif callback.data == 'pc_user':
        await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
        await ask_pc_type(callback.message)
    else:
        await callback.message.answer('Пожалуйста, нажмите на кнопку')


async def ask_phone_type(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    btn_android = types.InlineKeyboardButton(text='Android', callback_data='android')
    btn_iphone = types.InlineKeyboardButton(text='Iphone', callback_data='iphone')
    markup.add(btn_android, btn_iphone)

    await bot.send_message(message.chat.id, 'Расскажи для какого конкретного телефона тебе нужен VPN',
                           reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data in callback_phone_type_filter)
async def callback_phone_type(callback: types.CallbackQuery):
    if callback.data == 'android':
        await callback.message.answer('Теперь чтобы все работало корректно - установи wireguard')
        webbrowser.open("https://play.google.com/store/apps/details?id=com.wireguard.android")
        await ask_install(callback.message)
    elif callback.data == 'iphone':
        await callback.message.answer('Теперь чтобы все работало корректно - установи wireguard')
        webbrowser.open("https://itunes.apple.com/us/app/wireguard/id1441195209?ls=1&mt=8")
        await ask_install(callback.message)
    else:
        await callback.message.answer('Пожалуйста, нажмите на кнопку')


async def ask_pc_type(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    btn_android = types.InlineKeyboardButton(text='Windows', callback_data='windows')
    btn_iphone = types.InlineKeyboardButton(text='macOS', callback_data='macos')
    markup.add(btn_android, btn_iphone)

    await bot.send_message(message.chat.id, 'Расскажи для какого конкретного ПК тебе нужен VPN', reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data in callback_computer_type_filter)
async def callback_computer_type(callback: types.CallbackQuery):
    if callback.data == 'windows':
        await callback.message.answer('Теперь чтобы все работало корректно - установи wireguard')
        webbrowser.open("https://download.wireguard.com/windows-client/wireguard-installer.exe")
        await ask_install(callback.message)
    elif callback.data == 'macos':
        await callback.message.answer('Теперь чтобы все работало корректно - установи wireguard')
        webbrowser.open("https://itunes.apple.com/us/app/wireguard/id1451685025?ls=1&mt=12")
        await ask_install(callback.message)
    else:
        await callback.message.answer('Пожалуйста, нажмите на кнопку')


async def ask_install(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    btn_done = types.InlineKeyboardButton(text='Получилось', callback_data='install_done')
    btn_no = types.InlineKeyboardButton(text='Не удалось', callback_data='no_install')
    markup.add(btn_done, btn_no)
    await bot.send_message(message.chat.id, 'Установили ?', reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data in callback_ask_install_filter)
async def callback_ask_install(callback: types.CallbackQuery):
    if callback.data == 'install_done':
        await callback.message.answer('Отлично, используйте этот QR код для подключения')
        await call_qr(callback.message)
    elif callback.data == 'no_install':
        await callback.message.answer("Жаль")
    else:
        await callback.message.answer('Пожалуйста, нажмите на кнопку')


async def call_qr(message: types.Message):
    subprocess.run(command_first, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    subprocess.run(command_second, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    subprocess.run(message.from_user.full_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = subprocess.run(command_third, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    stdout = result.stdout
    stderr = result.stderr
    await bot.send_message(message.chat.id, stdout)
    print(stdout)
    print(stderr)


executor.start_polling(dp, skip_updates=True)
