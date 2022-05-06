import random

import pygame as pg
import sys
from settings import *
from objects import *
from os import path


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        self.font = path.join("PixelatedRegular-aLKm.ttf")

    def draw_text(self,surf, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        surf.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        # create the field
        self.field = [[Cell((i, j),self) for i in range(GRIDWIDTH)] for j in range(GRIDHEIGHT)]
        # set bombs
        self.mines=[]
        possibilities_2d=[[(i,j) for i in range(GRIDWIDTH)] for j in range(GRIDHEIGHT)]
        possibilities_1d=[j for i in possibilities_2d for j in i]
        for i in range(BOMBS_NUM):
            pos=random.choice(possibilities_1d)
            self.field[pos[1]][pos[0]].mine=True
            self.mines.append(pos)

            possibilities_1d.pop(possibilities_1d.index(pos))
        # calculate mines
        for i in range(GRIDWIDTH):
            for j in range(GRIDHEIGHT):
                self.field[i][j].count_mines(self.field)

        self.guesses=[]

        self.lost=0

        self.game_surf=pg.Surface((GRIDWIDTH*TILESIZE,GRIDHEIGHT*TILESIZE))
        self.game_surf_rect=self.game_surf.get_rect()
        self.game_surf_rect.center=(WIDTH//2,HEIGHT//2)


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def game_over(self):
        for i in range(GRIDWIDTH):
            for j in range(GRIDHEIGHT):
                self.field[i][j].revieled=True

    def open_cell(self):
        try:
            mx, my = pg.mouse.get_pos()
            mx=mx-self.game_surf_rect.left
            my=my-self.game_surf_rect.top
            self.field[my // TILESIZE][mx// TILESIZE].revieled = True
            self.field[my// TILESIZE][mx// TILESIZE].open_empty(self.field,[])
            if self.field[my // TILESIZE][mx // TILESIZE].mine:
                self.game_over()
                self.lost=1
        except:
            pass

    def guess(self):
        try:
            mx, my = pg.mouse.get_pos()
            mx=mx-self.game_surf_rect.left
            my=my-self.game_surf_rect.top
            if (mx // TILESIZE,my // TILESIZE) not in self.guesses:
                self.guesses.append((mx // TILESIZE,my // TILESIZE))
            else:
                self.guesses.remove((mx // TILESIZE,my // TILESIZE))

            result=all(elem in self.guesses  for elem in self.mines)
            if  result:
                self.game_over()
                self.lost=2
        except:
            pass


    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        # self.all_sprites.draw(self.screen)

        for i in range(GRIDWIDTH):
            for j in range(GRIDHEIGHT):
                self.field[i][j].show(self.game_surf)

        # guesses
        for c in self.guesses:
            dir=vec(c)*TILESIZE+vec(TILESIZE//2,TILESIZE//2)
            pg.draw.rect(self.game_surf,DARKGREY,(dir.x-TILESIZE//4,dir.y-TILESIZE//4,TILESIZE//2,TILESIZE//2))

        self.screen.blit(self.game_surf,(WIDTH//2-self.game_surf.get_width()/2,HEIGHT//2-self.game_surf.get_height()/2))
        self.draw_text(self.screen,f"mines :{BOMBS_NUM-len(self.guesses)}", self.font, 40, WHITE, WIDTH-50, 50, align="center")

        # game_over
        if self.lost==1:
            self.draw_text(self.screen,f"YOU HAVE LOST", self.font, 140, RED, WIDTH//2, HEIGHT//2, align="center")
            self.draw_text(self.screen,f"press SPACE to play again", self.font, 50, YELLOW, WIDTH//2, HEIGHT//2+50, align="center")
        elif self.lost==2:
            self.draw_text(self.screen,f"YOU WON", self.font, 140, GREEN, WIDTH//2, HEIGHT//2, align="center")
            self.draw_text(self.screen,f"press SPACE to play again", self.font, 50, YELLOW, WIDTH//2, HEIGHT//2+50, align="center")

        # fps
        self.draw_text(self.screen,str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here

        # if pg.mouse.get_pressed()[0]:
        #     self.open_cell()
        # if pg.mouse.get_pressed()[2]:
        #     self.guess()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.MOUSEBUTTONDOWN and event.button==1:
                self.open_cell()
            if event.type == pg.MOUSEBUTTONDOWN and event.button==3:
                self.guess()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key==pg.K_SPACE:
                    self.new()


# create the game object
g = Game()
g.new()
g.run()
