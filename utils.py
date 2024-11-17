from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


class ValidationError(Exception):
    pass


def _convert_buttons_to_reply_markup(buttons_groups):
    _buttons = []

    for buttons in buttons_groups:
        _buttons.append([
            InlineKeyboardButton(text=text, callback_data=callback)
            for text, callback in buttons
        ])

    return InlineKeyboardMarkup(_buttons)
