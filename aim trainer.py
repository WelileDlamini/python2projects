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

LIVES = 3 

TOP_BAR_HEIGHT = 50

LABEL_FONT =pygame.font.SysFont("comicsans", 24)


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

    def collide(self, x, y):
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.size
    



def draw(win,targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)

    

def format_time(secs):
    milli = math.floor(int(secs*1000%1000)/100)
    seconds = int(round(secs%60,1))
    miniets = int(secs//60)

    return f"{miniets:02d}:{seconds:02d}:{milli}"

def draw_to_bar(win,elapsed_time,targets_pressed,misses):
    pygame.draw.rect(win,"grey",(0,0,WIDTH,TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time:{format_time(elapsed_time)}",1,"black")
    
    speed = round(targets_pressed/elapsed_time,1)
    speed_lebel = LABEL_FONT.render (f"Speed:{speed}/t/s", 1, "black")
    hits_lebel = LABEL_FONT.render (f"Hits:{targets_pressed}", 1, "black")
    lives_lebel = LABEL_FONT.render (f"Lives:{LIVES-misses}", 1, "black")



    
    
    win.blit(time_label, (5,5))
    win.blit(speed_lebel, (200,5))
    win.blit(hits_lebel,(450,5))
    win.blit(lives_lebel,(650,5))


def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time:{format_time(elapsed_time)}",1,"black")
    
    speed = round(targets_pressed/elapsed_time,1)
    speed_lebel = LABEL_FONT.render (f"Speed:{speed}/t/s", 1, "black")
    hits_lebel = LABEL_FONT.render (f"Hits:{targets_pressed}", 1, "black")

    accuracy = round(targets_pressed / clicks * 100, 1)

    accuracy_label = LABEL_FONT.render (f"Accuracy:{accuracy} %", 1, "black")


    win.blit(time_label, (get_middle(time_label),5))
    win.blit(speed_lebel, (get_middle(speed_lebel),5))
    win.blit(hits_lebel,(get_middle(hits_lebel),5))
    win.blit(accuracy_label,(get_middle(accuracy_label),5))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                run = False
                break



def get_middle(surface):
    return WIDTH/2 - surface.get_width()/2












def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()




    pygame.time.set_timer(target_event, target_increment)



    while run:
        clock.tick(60)
        click = False
        mouse_position = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == target_event:
                x = random.randint(target_padding, WIDTH -target_padding)
                y = random.randint(target_padding + TOP_BAR_HEIGHT, HEIGHT - target_padding)
                target = Target(x,y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        
        
        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_position):
                targets.remove(target)
                targets_pressed += 1
        
        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, clicks) 

        
        draw(WIN,targets)
        draw_to_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()






    pygame.quit()


if __name__ == '__main__':
    main()







