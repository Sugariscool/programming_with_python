from easygraphics.turtle import *

def main():
    create_world(800, 600)

    set_speed(20)

    for i in range(8):
        for j in range(6):
            fd(100)
            rt(60)
        rt(45)

    pause()
    close_world()

easy_run(main)