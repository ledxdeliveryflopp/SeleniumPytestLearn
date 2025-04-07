from dataclasses import dataclass


class PAGENAMECONST:
    names: dict = {"login_page": "Вход - Battlestate Games", "confirm_page": "Завершите вход - Battlestate Games"}


class FORMERORSCONST:
    texts: list = ["Поле Пароль не может быть пустым.", "Поле E-mail не может быть пустым."]


@dataclass
class ProfileCenterConst:
    pages: PAGENAMECONST
    forms_texts: FORMERORSCONST


profile_center_const = ProfileCenterConst(PAGENAMECONST(), FORMERORSCONST())
