from typing import List, Any

from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton
)

buttons_list: List[Any] = []

def make_button_list(notes: List[tuple[Any]]) -> ReplyKeyboardMarkup:
    buttons_list = []
    
    for note in notes:
        buttons_list.append(KeyboardButton(text=note[0]))  # Убедитесь, что вы обращаетесь к нужному элементу
    
    return ReplyKeyboardMarkup(
        keyboard=[buttons_list],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder='ЛКМ по кнопке - удаление заметки'
    )


keyboard_notes: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard = [
        buttons_list
    ],
    resize_keyboard = True,
    one_time_keyboard = False,
    input_field_placeholder = 'ЛКМ по кнопке - удаление заметки'
)

editor_note_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text = "Удалить заметку"),
            InlineKeyboardButton(text = "Изменить заметку")
        ]
    ]
)