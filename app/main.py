# Добавить системную папку для импорта модулей
import sys
sys.path.insert(0, r'\config')
sys.path.insert(0, r'C:\Users\user\Desktop\3d_arrays_map\3d_arrays_map\config\map')
sys.path.insert(0, r'C:\Users\user\Desktop\3d_arrays_map\3d_arrays_map\db')

# Импорт модулей приложения
import pygame as pg
from copy import deepcopy
from map import field
from query import DB
from shortest_way import bfs
from interface import InputBox, Button


# Основная программа
class Program:
    def __init__(self)->None:
        pass
    def print_field(self,field:list[list[str]], path:list,start:list,goal:list) ->list[list[str]]: # Функция, создающая новый массив, в котором отображается путь.
        if path:
            new_map:list[list] = deepcopy(field) # копирование основной карты в новый массив
            s = new_map[start[0]][start[1]] # Координата начальной точки
            new_map[start[0]][start[1]] = s[:start[2]]+"D"+ s[start[2]+1:] # Добавление точки старта на карту
            g = new_map[goal[0]][goal[1]] # Координата точки
            new_map[goal[0]][goal[1]] = g[:goal[2]]+"D"+ g[goal[2]+1:] #Добавление точки конца на карту
            for i in path:
                s = new_map[i[0]][i[1]] # Координата точки 
                new_map[i[0]][i[1]] = s[:i[2]]+ "0"+s[i[2]+ 1: ] # Добавление пути на карту
            return new_map
        else: return field # Если не передан путь, то возвращаем пустую карту


    def main(self,field:list[list[str]])->None:

        input_boxes:list = [ # Список со всеми полями ввода
            InputBox(900, 52, 280, 32),
            InputBox(900, 130, 280, 32)
        ]

        buttons:list[Button] = [ # Список со всеми кнопками
            Button(900, 270, 50, 50, (120, 240, 220), '/\\'),
            Button(900, 340, 50, 50, (120, 240, 220), '\\/'),
            Button(900,200,120,50,(120, 240, 220),"Подтвердить"),
            Button(1060,200,120,50,(120, 240, 220),"Отменить")
        ]

        start_name:str = '' # Стартовое имя
        goal_name:str = '' # Стартовое имя
        start:list = [] # Координата старта
        goal:list = [] # Координата Конечной точки
        path:list = [] # Сюда складываем путь
        get_start:bool = False # Проверяет еслть ли стартовая точка в БД
        get_goal:bool = False # Проверяет еслть ли стартовая точка в БД

        db:DB = DB() # Объект класса DB
        cols:int = len(field[0]) # количество колонн 
        rows:int = len(field[0][0]) # Количество строк
        floor:int = 1 # Номер этажа ( Служит для конкретизации отрисованного этажа )
        weight_tile:int =4 # Длина плитки ( служит для рисования каждой плитки )
        height_tile:int = 15 # Ширина плитки ( служит для рисования каждой плитки )


        entered_text:dict[str:str] = {'input1': '', "input2": ''} # Текст, который введён в поле ввода

        sc = pg.display.set_mode([rows *weight_tile+400, cols * height_tile+100]) # Создание экрана
        clock = pg.time.Clock() 
        font = pg.font.SysFont('arial', 32) # Инициализация шрифта

        

        while True:
            sc.fill(pg.Color((10,3,16))) # Красит экран в темный
            sc.blit(font.render(f"Этаж № {buttons[0].value}",True, (255,207,223)), (370, 480)) # \
            sc.blit(font.render("Начало пути",True ,(255,207,223)),(900,12)) # -                    Расположить текст на экране
            sc.blit(font.render("Конец пути",True ,(255,207,223)),(900,90)) # /

            [box.draw(sc) for box in input_boxes] # Располагает поля для текста
            [button.draw(sc) for button in buttons] # Располагает кнопки

            map:list[list[str]] = self.print_field(field, path,start,goal) # Обновление карты
            floor:int = buttons[0].value * 2 -1 # Получение текущей карты
            for y,row in enumerate(map[floor]):
                for x,col in enumerate(row):
                    # рисует плитку
                    if col == '0': pg.draw.rect(sc,(191,109,103),(x*weight_tile+weight_tile*0.5-2, y*height_tile+height_tile*0.5-3,3,3)) 
                    if col == '#': pg.draw.rect(sc,(84, 30, 120),(x*weight_tile, y*height_tile, 6, 13)) 
                    if col == 'D': pg.draw.rect(sc,(153,73,221),(x*weight_tile, y*height_tile, 6, 13))
                    if col == 'C':
                        sc.blit(pg.font.SysFont('arial',13).render(
                            db.select_name_for_text_pos((floor,x,y)),True,(255,207,223)),
                            (x*weight_tile,y*height_tile))
                    


            for event in pg.event.get(): 
                if event.type == pg.QUIT: exit() # Выход
                for i, box in enumerate(input_boxes):
                    # Обработчик вводимого текста
                    result = box.handle_event(event)
                    if result is not None:
                        entered_text[f'input{i+1}'] = result
                # Обработка нажатых кнопок
                if buttons[0].is_clicked(event) and buttons[0].value <len(field)//2:
                    buttons[0].value +=1
                elif buttons[1].is_clicked(event) and buttons[0].value >1:
                    buttons[0].value -=1
                if buttons[2].is_clicked(event):
                    for i,box in enumerate(input_boxes):
                        entered_text[f'input{i+1}'] = box.get_text()
                if buttons[3].is_clicked(event):
                    for i,box in enumerate(input_boxes):
                        box.delete_text()
                        entered_text[f'input{i+1}'] = ""
                        

            # Обработка введённого текста            
            if entered_text["input1"].strip(): # Проверяет если введён текст
                start_name = (entered_text["input1"]).upper()
                get_start = db.check_exists(start_name) # проверяет есть ли введённый текст 
            else: start_name = ''
            if entered_text["input2"].strip(): # Проверяет если введён текст
                goal_name = (entered_text["input2"]).upper()
                get_goal = db.check_exists(goal_name) # проверяет есть ли введённый текст 
            else: goal_name = ''
            start = db.select_coordinate_from_name(start_name) if get_start else [] # Получение координаты старта
            goal = db.select_coordinate_from_name(goal_name) if get_goal else [] # Получение координаты конечной точки
            path = bfs(field,start,goal) # Получение пути
            pg.display.flip()
            clock.tick(10)

programm = Program()
programm.main(field)