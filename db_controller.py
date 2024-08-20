from datetime import date
from typing import List, Any

import sqlite3 as sql

class DataBase:
    def __init__(self, db_path: str, table_name: str) -> None:
        self.table_name = table_name
        
        self.db = sql.connect(db_path)
        self.cursor = self.db.cursor()
        
    def add_note(self, description: str, date: date | str) -> None:
        self.cursor.execute(
            f"INSERT INTO {self.table_name} VALUES (?,?)", 
            (description, str(date))
        )
        self.db.commit()
        
    def edit_note(self, now_description: str, new_description: str) -> None:
        self.cursor.execute(
            f"UPDATE {self.table_name} SET description = ? WHERE description = ?",
            (new_description, now_description)
        )
        self.db.commit()
        
    def delete_note(self, description_note: str) -> None:
        self.cursor.execute(
            f"DELETE FROM {self.table_name} WHERE description = ?",
            (description_note,)
            )
        self.db.commit()
        
    def notes(self) -> List[tuple[Any]]:
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        return self.cursor.fetchall()
    
if __name__ == '__main__':
    db = DataBase(db_path = 'data\\data.db', table_name = 'notes')
    
    # db.add_note(description = 'Заметка 1', date = '20.08.2024')
    # print(db.notes()) #[('Заметка 1', '20.08.2024'), ('Заметка 1', '20.08.2024')]
    
    db.delete_note('Заметка 1')
    print(db.notes())
        
    
        