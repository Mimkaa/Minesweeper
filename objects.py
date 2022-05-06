import pygame as pg
vec=pg.Vector2
from settings import *

class Cell:
    def __init__(self,index,game):
        self.index=vec(index)
        self.pos=(self.index.copy())*TILESIZE+vec(1,1)
        self.revieled=False
        self.mine=False
        self.count=0
        self.game=game

    def count_mines(self,field):
        possibilities_2d=[[(i,j) for i in range(GRIDWIDTH)] for j in range(GRIDHEIGHT)]
        possibilities_1d=[vec(j) for i in possibilities_2d for j in i]
        dirs=[(0,1),(1,0),(-1,0),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
        for d in dirs:
            dir_vec=self.index.copy()+vec(d)
            if dir_vec in possibilities_1d:
                if field[int(dir_vec.y)][int(dir_vec.x)].mine:
                    self.count+=1

        if self.mine:
            self.count=-1

    def open_empty(self,field,found):
        possibilities_2d=[[(i,j) for i in range(GRIDWIDTH)] for j in range(GRIDHEIGHT)]
        possibilities_1d=[vec(j) for i in possibilities_2d for j in i]
        dirs=[(0,1),(1,0),(-1,0),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
        # field_new_1d=[j for i in field for j in i if j.index!=self.index]
        for d in dirs:
            dir_vec=self.index.copy()+vec(d)
            if dir_vec not in found and dir_vec in possibilities_1d and field[int(dir_vec.y)][int(dir_vec.x)].count==0:
                found.append(dir_vec)
                field[int(dir_vec.y)][int(dir_vec.x)].revieled=True
                field[int(dir_vec.y)][int(dir_vec.x)].open_empty(field,found)


    def show(self,surf):
        pg.draw.rect(surf,WHITE,(self.pos.x,self.pos.y,TILESIZE,TILESIZE))
        pg.draw.rect(surf,BLACK,(self.pos.x,self.pos.y,TILESIZE,TILESIZE),1)
        if self.revieled:
            pg.draw.rect(surf,LIGHTGREY,(self.pos.x,self.pos.y,TILESIZE,TILESIZE))
            pg.draw.rect(surf,BLACK,(self.pos.x,self.pos.y,TILESIZE,TILESIZE),1)
            offset=vec(TILESIZE//2,TILESIZE//2)
            if self.mine:
                pg.draw.circle(surf,DARKGREY,self.pos+offset,TILESIZE//4)
            else:
                if self.count!=0:
                    pos=self.pos+offset
                    self.game.draw_text(surf,str(self.count),self.game.font,TILESIZE,BLACK,pos.x,pos.y,align="center")

