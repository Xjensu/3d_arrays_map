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
    def print_field(self,field:list[list[str]], path:list,start:list,goal:list) ->list[list[str]]:
        if path:
            new_map:list[list] = deepcopy(field)
            s = new_map[start[0]][start[1]]
            new_map[start[0]][start[1]] = s[:start[2]]+"1"+ s[start[2]+1:]
            g = new_map[goal[0]][goal[1]]
            new_map[goal[0]][goal[1]] = g[:goal[2]]+"1"+ g[goal[2]+1:]
            for i in path:
                s = new_map[i[0]][i[1]]
                new_map[i[0]][i[1]] = s[:i[2]]+ "0"+s[i[2]+ 1: ]
            return new_map
        else: return field


    def main(self,field):

        input_boxes:list = [InputBox(900, 20, 280, 32), InputBox(900, 70, 280, 32)]
        buttons = [
            Button(900, 130, 50, 50, (120, 240, 220), '/\\'),
            Button(900, 200, 50, 50, (120, 240, 220), '\\/'),
        ]

        start_name:str = ''
        goal_name:str = ''
        start:list = []
        goal:list = []
        path:list = []
        get_start:bool = False
        get_goal:bool = False

        db:DB = DB()
        cols:int = len(field[0])
        rows:int = len(field[0][0])
        floor:int = 1


        entered_text:dict[str:str] = {'input1': '', "input2": ''}

        sc = pg.display.set_mode([rows * 4+400, cols * 15+100])
        clock = pg.time.Clock()
        font = pg.font.SysFont('arial', 32)

        

        while True:
            sc.fill(pg.Color((10,3,16)))
            sc.blit(font.render(f"Этаж № {buttons[0].value}",True, (255, 0, 0)), (370, 480))
            
            map = self.print_field(field, path,start,goal)
            floor = buttons[0].value * 2 -1
            for y,row in enumerate(map[floor]):
                for x,col in enumerate(row):
                    if col == '0': pg.draw.circle(sc,(191,109,103),(x*4, y*15), 5) 
                    if col == '#': pg.draw.rect(sc,(84, 30, 120),(x*4, y*15, 6, 13))
                    if col == '1': pg.draw.rect(sc,(153,73,221),(x*4, y*15, 6, 13))


            for event in pg.event.get(): 
                if event.type == pg.QUIT: exit()
                for i, box in enumerate(input_boxes):
                    result = box.handle_event(event)
                    if result is not None:
                        entered_text[f'input{i+1}'] = result
                if buttons[0].is_clicked(event) and buttons[0].value <2:
                    buttons[0].value +=1
                elif buttons[1].is_clicked(event) and buttons[0].value >1:
                    buttons[0].value -=1
                        

            [box.draw(sc) for box in input_boxes]
            [button.draw(sc) for button in buttons]


            if entered_text["input1"].strip():
                start_name = (entered_text["input1"]).upper()
                get_start = db.check_exists(start_name)
            else: start_name = ''
            if entered_text["input2"].strip():
                goal_name = (entered_text["input2"]).upper()
                get_goal = db.check_exists(goal_name)
            else: goal_name = ''
            start = db.select_coordinate_from_name(start_name) if get_start else []
            goal = db.select_coordinate_from_name(goal_name) if get_goal else []


            path = bfs(field,start,goal)
            
            pg.display.flip()
            clock.tick(10)

programm = Program()
print(programm.main(field))