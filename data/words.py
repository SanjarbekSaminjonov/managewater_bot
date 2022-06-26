from typing import Union

words = {
    'uz': {
        'cancel': 'Bekor qilish',
        'yes': 'Ha',
        'no': 'Yo\'q',
        'add_device': 'Qurilma qo\'shish',
        'my_devices': 'Mening qurilmalarim',
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
        'saving_process': 'Ma\'lumotlar tizimga saqlanmoqda ...'
    }
}


def get_word(key: Union[str], lang: Union[str] = 'uz') -> Union[str]:
    return words[lang].get(key)
