def make_up_channel_device_info(data) -> str:
    text = str()
    text += f"🔵 Qurilma nomi: <b>{data[1]}</b>\n\n"
    text += f"🟢 Qurilma id si: <b>{data[0]}</b>\n\n"
    text += f"🟡 Telefon raqami: <b>{data[2]}</b>\n\n"
    text += f"🔴 Balandlik: <b>{data[3]} sm</b>\n\n"
    text += f"⚪ Balandlik sozlamasi: <b>{data[4]} sm</b>\n"
    return text
