import psycopg2
from psycopg import Connection
from pathlib import Path

root_folder = Path(__file__).parents[1]
my_path = root_folder / "config/configuration.txt"


class DB():
    def __init__(self) -> None:
        f = open(my_path,'r').readline().split()
        self.connection:Connection = psycopg2.connect( # Подключение к базе данных
            host = str(f[0]),
            user = str(f[1]),
            password = str(f[2]),
            dbname = str(f[3]),
            port = str(f[4])
        )

    def select_coordinate_from_name(self, name:str)->list[int]:
        cur = self.connection.cursor()
        if name.strip():
            cur.execute("SELECT coordinate FROM auditors WHERE name = %s",(name,))
            return cur.fetchall()[0][0]
        else: return []
        

    def select_name_for_text_pos(self,coordinate:list)->str:
        cur = self.connection.cursor()
        cur.execute("SELECT name from auditors WHERE text_pos = %s",(list(coordinate),))
        return cur.fetchall()[0][0]

    def check_exists(self, data:str|list) -> bool:
        if type(data) is str:
            query = "SELECT EXISTS(SELECT * FROM auditors where name = '%s')"
        elif type(data) is list:
            query = "SELECT EXISTS(SELECT * FROM auditors where coordinate = ARRAY %s)"

        cur = self.connection.cursor()
        cur.execute(query % data)
        return cur.fetchall()[0][0]

