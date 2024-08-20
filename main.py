#aiogram
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

#project-files
from config import j, current_note
from db_controller import DataBase
import keyboards

#modules
from datetime import datetime
import asyncio

class TGBOT_ToDoList:
    def __init__(self, TOKEN: str, ADMIN: str = None) -> None:
        self.bot = Bot(TOKEN)
        self.dp = Dispatcher()
        self.db = DataBase(db_path = 'data\\data.db', table_name = 'notes')
        self.ADMIN = ADMIN
        
    async def listen(self) -> None:
        # -- start --
        @self.dp.message(Command('start'))
        async def start(message: Message) -> None:
            await message.answer(
                text = """
                <b>Привет</b>🖐!
                Добро пожаловать в TodoList бот!
                Чтобы узнать, как пользоватся ботом - используйте комманду /commands
                """, 
                parse_mode = 'html'
                )
            
        # -- commands --
        @self.dp.message(Command(commands = ('commands', 'help')))
        async def show_list_commands(message: Message) -> None:
            with open('data\\list_commands.txt', 'r') as file:
                await message.answer(text = file.read(), parse_mode = 'html')
              
        # -- create_note --  
        @self.dp.message(Command('create'))
        async def create_note(message: Message) -> None:
            await message.answer("Опишите цель заметки📝...")
            
        # -- notes --
        @self.dp.message(Command('notes'))
        async def show_notes(message: Message) -> None:
            try:
                notes = self.db.notes()  # Получаем список заметок
                print(f"Notes fetched: {notes}")  # Логируем полученные заметки
                
                if not notes:
                    await message.answer("У вас нет заметок.")
                    return
                else:
                    text: str = ""
                    for index in notes:
                        text += f"-- {index[0]}\n<b>Дата создания:{index[1]}</b>\n\n"
                        
                    await message.answer(text = text, parse_mode = 'html')
                    
                keyboard = keyboards.make_button_list(notes)  # Создаем новую клавиатуру
                
                await message.answer(
                    text="<b>Список ваших заметок</b>🔥",
                    parse_mode='html',
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error in show_notes: {e}")

        # -- echo --
        @self.dp.message()
        async def echo(message: Message) -> None:
            """
            -- add data in database
            -- update keyboard 
            -- delete note

            Проверяем есть ли заметка в БД или нет.
            Если заметка есть в БД, то удаляем её, а если нету, то добавляем в БД
            """
            
            status_delete: bool = False
            
            for index in self.db.notes():
                if message.text == index[0]:
                    current_note = message.text
                    
                    self.db.delete_note(description_note = current_note) #delete note
                    status_delete = True
                    current_note = None
                    
                    await message.answer(text = 'Заметка удалена! 🗑')
                    break
                
            if status_delete is False:
                #Add note to DB
                self.db.add_note(
                    description = message.text,
                    date = datetime.now().strftime("%H:%M:%S")
                )
            
                #answer message
                await message.answer(
                    text = "<b>Заметка создана</b>✅\nиспользуйте /notes чтобы посмотреть все ваши заметки",
                    parse_mode = 'html'
                )
            
            #build keyboard notes
            notes = self.db.notes()  # Получаем список заметок
            print(f"Notes fetched: {notes}")  # Логируем полученные заметки
            
            if not notes:
                await message.answer("У вас нет заметок! ❌")
                return
                
            keyboard = keyboards.make_button_list(notes)  # Создаем новую клавиатуру
            
            await message.answer(
                text="<b>Список ваших заметок</b>🔥",
                parse_mode='html',
                reply_markup=keyboard
            )
                
    async def main(self) -> None:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"{self.ADMIN} is started bot! [{current_time}]")
        
        await self.bot.delete_webhook(drop_pending_updates = True)
        await self.dp.start_polling(self.bot)
        
if __name__ == '__main__':
    tg_bot = TGBOT_ToDoList(TOKEN = j["TOKEN"], ADMIN = j["ADMIN"])    
    asyncio.run(tg_bot.listen())
    asyncio.run(tg_bot.main())
    
