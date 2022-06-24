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
                         '<i>Parol uzunligi 4 - 6 xonali bo\'lishi lozim</i>\n\nParol:\0'
    }
}


def get_word(key: Union[str], lang: Union[str] = 'uz') -> Union[str]:
    return words[lang].get(key)


def get_words(keys: Union[list[str]], lang: Union[str] = 'uz') -> Union[list]:
    res = list()
    for key in keys:
        word = words[lang].get(key)
        if word is not None:
            res.append(word)
    return res


if __name__ == '__main__':
    uz_words = get_words(['yes', 'no'])
    en_words = get_words(['yes', 'no', 'cancel'])
    print(uz_words)
    print(en_words)
