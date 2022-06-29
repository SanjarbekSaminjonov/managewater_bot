from typing import Union


def makeup_user_info(data: Union[dict]) -> Union[str]:
    text = f"Telefon: {data.get('username')}\n"
    text += f"Ism: {data.get('first_name')}\n"
    text += f"Familiya: {data.get('last_name')}\n"
    text += f"Viloyat/Sh.: {data.get('region')}\n"
    text += f"Tuman/Sh.: {data.get('city')}\n"
    text += f"Tashkilot: {data.get('org_name')}"
    return text


def hash_password(password: Union[str], show_password: Union[bool]) -> Union[str]:
    return f'<b>{password if show_password else "*" * len(password)}</b>'
