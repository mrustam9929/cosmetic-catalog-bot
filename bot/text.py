class MessageTextKey:
    START_CHAT = 'start_chat'
    SEARCH = 'search'


def get_text(key: str, lang: str = 'ru') -> str:
    return TRANSLATE[key][lang]


TRANSLATE = {
    MessageTextKey.START_CHAT: {
        'ru': 'Привет',
        'en': 'Привет',
        'uz': 'Привет',
    },
    MessageTextKey.SEARCH: {
        'ru': 'Поиск продуктов',
        'en': 'Поиск продуктов',
        'uz': 'Поиск продуктов',
    }

}
