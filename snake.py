from tkinter import *
import pygame
from pygame import mixer
import tkinter.font
from PIL import ImageTk, Image
from tkinter import colorchooser
import random
import os

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

root = Tk()
root.title("CHARM THE SNAKE")
w = 900
h = 600
root.geometry("900x600")
cv = Canvas(width=w, height=h)
snake_color = "yellow"
food_color = "red"


def snake():
    global snake_color
    snake_color = (colorchooser.askcolor(title="Choose snake color"))[0]


def food():
    global food_color
    food_color = (colorchooser.askcolor(title="Choose food color"))[0]


def start():
    global cv
    mixer.init()
    mixer.music.load("intro1.wav")
    mixer.music.play()
    cv = Canvas(width=w, height=h)
    bg_img = Image.open("snake.png")
    new_img = bg_img.resize((w, h), Image.ANTIALIAS)
    new = ImageTk.PhotoImage(new_img)
    cv.pack(side='top', fill='both', expand='yes')
    cv.create_image(0, 0, image=new, anchor='nw')
    cv.pack()
    u = tkinter.font.Font()
    v = tkinter.font.Font()
    u.config(family="calibri", size=20)
    v.config(family="Times New Roman", size=25)
    label1 = Label(cv, text="WELCOME", fg="red", bg="black")
    label1.config(font=v)
    label1.place(x=310, y=280)
    button3 = Button(cv, text="Choose snake color", fg="red", bg="green", command=snake, width=15, height=1)
    button3.config(font=u)
    button3.place(x=50, y=350)
    button1 = Button(cv, text="PLAY", fg="red", bg="green", command=hide, width=5, height=1)
    button1.config(font=v)
    button1.place(x=330, y=400)
    button2 = Button(cv, text="Choose food color", fg="red", bg="green", command=food, width=15, height=1)
    button2.config(font=u)
    button2.place(x=500, y=350)
    root.config()
    root.mainloop()


def hide():
    root.withdraw()
    mixer.music.pause()
    play()


def play():
    global root
    snake_x = 45
    snake_y = 60
    vel_x = 0
    vel_y = 0
    slist = []
    len1 = 1
    score = 0
    snake_size = 20
    food_size = 20
    clock = pygame.time.Clock()
    pygame.display.init()
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("EXAMPLE")
    exit_game = False
    food_x = random.randint(100, w-100)
    food_y = random.randint(100, h-100)
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 40)
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = int(f.read())

    def write1(text, color, x, y):
        screen_text = myfont.render(text, True, color)
        screen.blit(screen_text, [x, y])

    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                mixer.music.load("slither.mp3")
                mixer.music.play()
                if event.key == pygame.K_RIGHT:
                    vel_x = 5
                    vel_y = 0
                if event.key == pygame.K_LEFT:
                    vel_x = -5
                    vel_y = 0
                if event.key == pygame.K_UP:
                    vel_y = -5
                    vel_x = 0
                if event.key == pygame.K_DOWN:
                    vel_y = 5
                    vel_x = 0
        snake_x += vel_x
        snake_y += vel_y
        screen.fill("black")
        if abs(snake_x-food_x) <= 6 and abs(snake_y-food_y) <= 6:
            mixer.music.load("score.mp3")
            mixer.music.play()
            score += 10
            len1 += 5
            hiscore = max(hiscore, score)
            food_x = random.randint(100, w-100)
            food_y = random.randint(100, h-100)
        write1("SCORE: "+str(score)+"     HISCORE: "+str(hiscore), red, 5, 5)
        face = [snake_x, snake_y]
        slist.append(face)
        if len(slist) > len1:
            del slist[0]
        pygame.draw.rect(screen, food_color, [food_x, food_y, food_size, food_size])
        for [s, t] in slist:
            pygame.draw.rect(screen, snake_color, [s, t, snake_size, snake_size])
        if face in slist[:-2]:
            mixer.music.load("gameover1.wav")
            mixer.music.play()
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            while not exit_game:
                screen.fill("white")
                write1("Game-Over! Press ENTER to continue", red, 100, 250)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            exit_game = True
                pygame.display.update()
                clock.tick(60)
        if snake_x < 0 or snake_x > w or snake_y < 0 or snake_y > h:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            mixer.music.load("gameover1.wav")
            mixer.music.play()
            while not exit_game:
                screen.fill("white")
                write1("Game-Over! Press ENTER to continue", red, 100, 250)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            exit_game = True
                pygame.display.update()
                clock.tick(60)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    root.deiconify()
    start()


start()
