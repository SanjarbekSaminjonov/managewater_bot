import datetime


def make_up_channel_device_info_pre_save(data):
    text = str()
    text += f"🔵 Qurilma nomi: <b>{data.get('name')}</b>\n\n"
    text += f"🟢 Qurilma id si: <b>{data.get('device_id')}</b>\n\n"
    text += f"🟡 Telefon raqami: <b>{data.get('phone')}</b>\n\n"
    text += f"🔴 Balandlik: <b>{data.get('height')} sm</b>\n\n"
    return text


def make_up_channel_device_info(data) -> str:
    text = str()
    text += f'🔵 Qurilma nomi: <b>{data[1]}</b>\n\n'
    text += f'🟢 Qurilma id si: <b>{data[0]}</b>\n\n'
    text += f'🟡 Telefon raqami: <b>{data[2]}</b>\n\n'
    text += f'🔴 Balandlik: <b>{data[3]} sm</b>\n\n'
    text += f'⚪ Balandlik sozlamasi: <b>{data[4]} sm</b>\n'
    return text


def makeup_channel_device_message_info(device_name, channel_device_message) -> str:
    text = str()

    def bat_power():
        bat = float(channel_device_message[6])
        if bat > 4.12:
            bat = 4.12
        if bat < 3.7:
            bat = 3.7
        return round((bat - 3.70) / 0.42 * 100)
    
    def dtime():
        dt = channel_device_message[7] + datetime.timedelta(hours=5)
        return dt.strftime('%H:%M | %d.%m.%Y')

    text += f'🔵 Qurilma nomi: <b>{device_name}</b>\n'
    text += f'📆  So\'ngi o\'lchangan vaqti <b>{dtime()}</b>\n\n'
    text += f'📏  Suvdan qurilma balandligi: <b>{channel_device_message[1]} sm</b>\n'
    text += f'📏  Suv sathidan balandligi: <b>{channel_device_message[2]} sm</b>\n'
    text += f'🌊  O\'tayotgan suv miqdori: <b>{channel_device_message[3]} litr/sekund</b>\n'
    text += f'🌊  O\'tayotgan suv miqdori: <b>{channel_device_message[4]} m³/soat</b>\n'
    text += f'📈  Jami o\'tayotgan suv miqdori: <b>{int(channel_device_message[5])} m³</b>\n'
    text += f'🔋  Batareya quvvati: <b>{bat_power()} %</b>\n'
    text += f'📡  GPRS Antena kuchi: <b>{channel_device_message[6]} net</b>\n'
    return text
