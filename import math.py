import math
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Aim Trainer")

target_increment = 400
target_event = pygame.USEREVENT
target_padding = 30

BG_COLOR = (0,25,40)



class Target:
    max_size = 30
    gowth_rate = 0.2
    color = 'red'
    second_color = 'white'

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.gowth_rate >= self.max_size:
            self.grow = False

        if self.grow:
            self.size += self.gowth_rate
        else:
            self.size -= self.gowth_rate

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y), self.size)
        pygame.draw.circle( win, self.second_color, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle( win, self.color, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle( win, self.second_color, (self.x, self.y), self.size * 0.4)


def draw(win,targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)

    pygame.display.update()






def main():
    run = True
    targets = []

    pygame.time.set_timer(target_event, target_increment)



    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == target_event:
                x = random.randint(target_padding, WIDTH -target_padding)
                y = random.randint(target_padding, HEIGHT - target_padding)
                target = target(x,y)
                targets.append(target)
        for target in targets:
            target.update()
        draw(WIN,targets)





    pygame.quit()


if __name__ == '__main__':
    main()