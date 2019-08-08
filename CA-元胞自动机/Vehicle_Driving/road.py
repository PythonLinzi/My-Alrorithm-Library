import pygame
import sys
import numpy as np
from numpy import array, zeros, ones
from numpy.random import rand, randint


def angle(x1, y1, x2, y2):
    s1 = np.sqrt(x1 * x1 + y1 * y1)
    s2 = np.sqrt(x2 * x2 + y2 * y2)
    try:
        cos = (x1 * x2 + y1 * y2) / (s1 * s2)
        return np.arccos(cos)
    except ValueError:
        return 0


def dist(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Road:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 400
        self.surf = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.cell_size = 20
        self.x_bnd = int(self.width / self.cell_size)
        self.y_bnd = int(self.height / self.cell_size)
        self.white, self.black = (255, 255, 255), (0, 0, 0)
        self.surf.fill(self.white)
        self.N = 100
        self.car1 = []
        self.car2 = []
        pygame.display.set_caption("The Road")
        self.exit_num = 4
        self.exit = []
        self.cnt = 0
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self.road = zeros((self.x_bnd, self.y_bnd)).astype(np.bool)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.p1 = 0.4 # 变道概率
        self.p2 = 0.4 # 转弯概率
        self.X = self.x_bnd // 2
        self.Y = self.y_bnd // 2
        for j in range(self.x_bnd):
            self.road[j][self.Y - 2] = True
            self.road[j][self.Y - 1] = True
            self.road[j][self.Y] = True
            self.road[j][self.Y + 1] = True
        for i in range(self.y_bnd):
            self.road[self.Y - 1][i] = True
            self.road[self.Y][i] = True

    def __draw_grid(self):
        gray = (210, 210, 210)
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.surf, gray, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.surf, gray, (0, y), (self.width, y))


    class Car:
        def __init__(self, x=0, y=10):
            self.x, self.y = x, y
            self.v = 1
            self.exist = False


    def create_car1(self):
        x, y = 0, randint(self.Y, self.Y + 2, size=1)
        if self.road[x][y]:
            self.car1.append(self.Car(x, y))

    def create_car2(self):
        x, y = self.x_bnd - 1, randint(self.Y - 2, self.Y, size=1)
        if self.road[x][y]:
            self.car2.append(self.Car(x, y))


    def move1(self):
        n = len(self.car1)
        tmp = self.car1
        remove_idx = []
        for i in range(n):
            car = tmp[i]
            x, y = car.x, car.y
            if x == self.x_bnd - 1:
                remove_idx.append(i)
                continue
            '''
            if x == self.X - 1 and y == self.Y and rand() < self.p2:
            '''
            if self.road[x + 1][y]:
                self.car1[i].x = x + 1
            elif y == self.Y - 1 and self.road[x + 1][y + 1] and rand() < self.p1:
                self.car1[i].x = x + 1
                self.car1[i].y = y + 1
            elif y == self.Y and self.road[x + 1][y - 1] and rand() < self.p1:
                self.car1[i].x = x + 1
                self.car1[i].y = y - 1
        for idx in remove_idx:
            self.car1.pop(idx)

    def move2(self):
        n = len(self.car2)
        tmp = self.car2
        remove_idx = []
        for i in range(n):
            car = tmp[i]
            x, y = car.x, car.y
            if x == 0:
                remove_idx.append(i)
                continue
            if self.road[x - 1][y]:
                self.car2[i].x = x - 1
            elif y == self.Y - 1 and self.road[x - 1][y + 1] and rand() < self.p1:
                self.car2[i].x = x - 1
                self.car2[i].y = y + 1
            elif y == self.Y and self.road[x - 1][y - 1] and rand() < self.p1:
                self.car2[i].x = x - 1
                self.car2[i].y = y - 1
        for idx in remove_idx:
            self.car2.pop(idx)



    def draw_object(self, objects, color):
        if type(objects).__name__ == 'list':
            for item in objects:
                x = item.x * self.cell_size
                y = item.y * self.cell_size
                item_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.surf, color, item_rect)
        else:
            x = objects.x * self.cell_size
            y = objects.x * self.cell_size
            obj_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.surf, color, obj_rect)


    def time_count(self):
        ''' 计时器 '''
        time_surf = self.font.render("time : "+str(self.cnt), True, (0, 0, 0))
        time_rect = time_surf.get_rect()
        time_rect.topleft = (self.width - 150, 10)
        self.surf.blit(time_surf, time_rect)


    def set_full_screen(self):
        self.surf = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.create_car1()
            self.create_car2()
            self.move1()
            self.move2()
            self.surf.fill(self.white)
            self.draw_object(self.car1, self.blue)
            self.draw_object(self.car2, self.blue)
            self.__draw_grid()
            self.cnt += 1
            self.time_count()
            pygame.display.update()
            pygame.time.delay(10)




if __name__ == '__main__':
    road = Road()
    road.run()

