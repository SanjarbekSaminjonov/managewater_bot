from typing import Union

words = {
    'uz': {
        'cancel': 'Bekor qilish',
        'yes': 'Ha',
        'no': 'Yo\'q',
        'back': 'Orqaga',
        'settings': 'Sozlamalar',
        'channel_devices': 'Suv nazorat postlari',
        'well_devices': 'Kuzatuv quduqlari',
        'pump_station': 'Nasos stansiya',
        'register': 'Ro\'yxatdan o\'tish',
        'cancelled': 'Bekor qilindi',
        'request_contact': '📱 Telefon raqamni yuborish',
        'request_phone_number': '📝 Ro\'yxatga olish boshlandi \n\nQuyidagi\0'
                                'tugma orqali telefon raqamingizni yuboring',
        'request_first_name': 'Ismingizni kiriting',
        'request_last_name': 'Familiyangizni kiriting',
        'request_region': 'Viloyat/Shaharingizni tanlang',
        'request_city': 'Tuman/Shaharingizni tanlang',
        'request_org_name': 'Tashkilot nomini kiriting',
        'password_text': 'Barcha ma\'lumotlaringiz xavfsizligi uchun parol kiriting.\n'
                         '<i>Parol uzunligi 4 - 6 xonali bo\'lishi lozim</i>\n\nParol:\0',
        'saving_process': 'Ma\'lumotlar tizimga saqlanmoqda ...',
        'channel_devices_list': 'Barcha qurilmalar ro\'yxati',
        'add_new_channel_device': 'Yangi qurilma qo\'shish',
        'channel_devices_all_statistics': 'Barcha qurilmalar ma\'lumoti',
        'edit_device_data': '✏ Ma\'lumotlarni o\'zgartirish',
        'see_last_message': '📊 Oxirgi kelgan xabar',
        'see_location': '📍 Joylashuvni ko\'rish',
        'back_to_devices_list': '🔙 Qurilmalar ro\'yxati',
        'send_location': '📍 Qurilma joylashuvini yuborish',
        'ingore_step': 'Tashlab ketish'
    }
}


def get_word(key: Union[str], lang: Union[str] = 'uz') -> Union[str]:
    return words[lang].get(key)
