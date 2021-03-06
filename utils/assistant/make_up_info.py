import datetime


def make_up_channel_device_info_pre_save(data):
    text = str()
    text += f"ðµ Qurilma nomi: <b>{data.get('name')}</b>\n\n"
    text += f"ð¢ Qurilma id si: <b>{data.get('device_id')}</b>\n\n"
    text += f"ð¡ Telefon raqami: <b>{data.get('phone')}</b>\n\n"
    text += f"ð´ Balandlik: <b>{data.get('height')} sm</b>\n\n"
    return text


def make_up_channel_device_info(data) -> str:

    full_h = f'{data[4]} sm' if data[4] else 'sozlanmagan'

    text = str()
    text += f'ðµ Qurilma nomi: <b>{data[1]}</b>\n\n'
    text += f'ð¢ Qurilma id si: <b>{data[0]}</b>\n\n'
    text += f'ð¡ Telefon raqami: <b>{data[2]}</b>\n\n'
    text += f'ð´ Umumiy balandlik: <b>{full_h}</b>\n\n'
    text += f'âª Balandlik sozlamasi: <b>{data[5]} sm</b>\n'
    return text


def makeup_channel_device_message_info(device, channel_device_message) -> str:
    text = str()

    def bat_power(bat, is_charging):
        bat = float(bat)
        if bat > 4.12:
            bat = 4.12
        if bat < 3.7:
            bat = 3.7
        bat = round((bat - 3.70) / 0.42 * 100)
        return f'{bat} % (quvvatlanmoqda)' if is_charging else f'{bat} % (quvvat olmayapti)'

    def dtime(time):
        dt = time + datetime.timedelta(hours=5)
        return dt.strftime('%H:%M | %d.%m.%Y')

    text += f'ðµ Qurilma nomi: <b>{device[1]}</b>\n'
    text += f'ð  So\'ngi o\'lchangan vaqti <b>{dtime(channel_device_message[5])}</b>\n\n'
    text += f'ð  Suvdan qurilma balandligi: <b>{channel_device_message[0]} sm</b>\n'
    text += f'ð  O\'tayotgan suv miqdori: <b>{channel_device_message[1]} mÂ³/sekund</b>\n'
    text += f'ð  Batareya quvvati: <b>{bat_power(channel_device_message[2], channel_device_message[3])}</b>\n'
    text += f'ð¡  GPRS Antena kuchi: <b>{channel_device_message[4]} net</b>\n'
    return text
