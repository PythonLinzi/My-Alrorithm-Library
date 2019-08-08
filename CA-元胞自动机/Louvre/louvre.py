import pygame
import sys
import numpy as np


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


class Louvre:

    def __init__(self):
        pygame.init()
        self.width = 1000
        self.height = 700
        self.display_surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.cell_size = 5
        self.x_bound = int(self.width / self.cell_size)
        self.y_bound = int(self.height / self.cell_size)
        self.white = (255, 255, 255)
        self.display_surface.fill(self.white)
        self.population = 100
        self.tourists = []
        pygame.display.set_caption("The Louvre")
        self.exit_number = 4
        self.exit = []
        self.cnt = self.population
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self.check = np.zeros((self.x_bound, self.y_bound)).astype(np.bool)

    def draw_grid(self):
        gray = (210, 210, 210)
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.display_surface, gray, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.display_surface, gray, (0, y), (self.width, y))

    def set_population(self, number): self.population = self.cnt = number

    def set_exit_number(self, number): self.exit_number = number

    def create_tourists(self):
        for i in range(0, self.population):
            self.tourists.append({'x': np.random.randint(2, self.x_bound - 2),
                                  'y': np.random.randint(2, self.y_bound - 2),
                                  'in': True,
                                  'decision': 0,
                                  'distance': 0})

    def create_exit(self):
        for i in range(0, self.exit_number):
            self.exit.append({'x': np.random.randint(1, self.x_bound - 1),
                              'y': np.random.randint(0, self.y_bound - 1),
                              'is_floor': False})

    def draw_object(self, objects, color):
        if type(objects).__name__ == 'list':
            for item in objects:
                x = item['x'] * self.cell_size
                y = item['y'] * self.cell_size
                item_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.display_surface, color, item_rect)
        else:
            x = objects['x'] * self.cell_size
            y = objects['y'] * self.cell_size
            obj_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.display_surface, color, obj_rect)

    def draw_tourists(self):
        deep_sky_blue = (0, 191, 255)
        for peo in self.tourists:
            if peo['in']:
                x = peo['x'] * self.cell_size
                y = peo['y'] * self.cell_size
                peo_rect = pygame.Rect(x, y, self.cell_size - 0.5, self.cell_size - 0.5)
                pygame.draw.rect(self.display_surface, deep_sky_blue, peo_rect)

    def draw_exit(self):
        green = (0, 255, 0)
        self.draw_object(self.exit, green)

    def update_check_array(self):
        for peo in self.tourists:
            x = peo['x']
            y = peo['y']
            self.check[x][y] = peo['in']

    def choose_closest_exit(self):
        for i in range(0, self.population):
            distance = 1e9
            ans = 0
            for j in range(0, self.exit_number):
                temp = np.sqrt((self.tourists[i]['x'] - self.exit[j]['x']) ** 2 +
                               (self.tourists[i]['y'] - self.exit[j]['y']) ** 2)
                if temp < distance:
                    distance = temp
                    ans = j
            self.tourists[i]['distance'] = distance
            self.tourists[i]['decision'] = ans

    def update_distance(self):
        for i in range(0, self.population):
            idx = self.tourists[i]['decision']
            distance = dist(self.tourists[i]['x'], self.tourists[i]['y'], self.exit[idx]['x'], self.exit[idx]['y'])
            self.tourists[i]['distance'] = distance

    def choose_direction(self, person):
        d = []
        for i in range(0, 8):
            d.append(0)
        x1 = person['x']
        y1 = person['y']
        #  idx denote the index of the exit
        idx = person['decision']
        x2 = self.exit[idx]['x']
        y2 = self.exit[idx]['y']
        s = dist(x1, y1, x2, y2)
        #  exit1
        if dist(x1 - 1, y1 - 1, x2, y2) > s:
            d[0] = 1e3
        elif (x1 > 1 and y1 > 1) and (not self.check[x1 - 1][y1 - 1]):
            d[0] = angle(x1 - 1, y1 - 1, x2, y2)
        else:
            d[0] = 1e3
        #  exit2
        if dist(x1, y1 - 1, x2, y2) > s:
            d[1] = 1e3
        elif y1 > 1 and (not self.check[x1][y1 - 1]):
            d[1] = angle(x1, y1 - 1, x2, y2)
        else:
            d[1] = 1e3
        #  exit3
        if dist(x1 + 1, y1 - 1, x2, y2) > s:
            d[2] = 1e3
        elif x1 < self.x_bound - 1 and y1 > 1 and (not self.check[x1 + 1][y1 - 1]):
            d[2] = angle(x1 + 1, y1 - 1, x2, y2)
        else:
            d[2] = 1e3
        #  exit4
        if dist(x1 - 1, y1, x2, y2) > s:
            d[3] = 1e3
        elif x1 > 1 and (not self.check[x1 - 1][y1]):
            d[3] = angle(x1 - 1, y1, x2, y2)
        else:
            d[3] = 1e3
        #  exit5
        if dist(x1 + 1, y1, x2, y2) > s:
            d[4] = 1e3
        elif x1 < self.x_bound - 1 and (not self.check[x1 + 1][y1]):
            d[4] = angle(x1 + 1, y1, x2, y2)
        else:
            d[4] = 1e3
        #  exit6
        if dist(x1 - 1, y1 + 1, x2, y2) > s:
            d[5] = 1e3
        elif x1 > 1 and y1 < self.y_bound - 1 and (not self.check[x1 - 1][y1 + 1]):
            d[5] = angle(x1 - 1, y1 + 1, x2, y2)
        else:
            d[5] = 1e3
        #  exit7
        if dist(x1, y1 + 1, x2, y2) > s:
            d[6] = 1e3
        elif y1 < self.y_bound - 1 and (not self.check[x1][y1 + 1]):
            d[6] = angle(x1, y1 + 1, x2, y2)
        else:
            d[6] = 1e3
        #  exit8
        if dist(x1 + 1, y1 + 1, x2, y2) > s:
            d[7] = 1e3
        elif x1 < self.x_bound - 1 and y1 < self.y_bound - 1 and (not self.check[x1 + 1][y1 + 1]):
            d[7] = angle(x1 + 1, y1 + 1, x2, y2)
        else:
            d[7] = 1e3
        ans = np.argmin(d)
        canmove = True
        if d[int(ans)] == 1e3:
            canmove = False
        return ans, canmove

    def move(self):
        self.update_distance()
        for i in range(0, self.population):
            dis = self.tourists[i]['distance']
            self.draw_object(self.tourists[i], (255, 255, 255))
            bound = np.sqrt(2)
            if dis > bound:
                direction, canmove = self.choose_direction(self.tourists[i])
                if canmove:
                    self.check[self.tourists[i]['x']][self.tourists[i]['y']] = False
                    if direction == 0:
                        self.tourists[i]['x'] -= 1
                        self.tourists[i]['y'] -= 1
                    elif direction == 1:
                        self.tourists[i]['y'] -= 1
                    elif direction == 2:
                        self.tourists[i]['x'] += 1
                        self.tourists[i]['y'] -= 1
                    elif direction == 3:
                        self.tourists[i]['x'] -= 1
                    elif direction == 4:
                        self.tourists[i]['x'] += 1
                    elif direction == 5:
                        self.tourists[i]['x'] -= 1
                        self.tourists[i]['y'] += 1
                    elif direction == 6:
                        self.tourists[i]['y'] += 1
                    else:
                        self.tourists[i]['x'] += 1
                        self.tourists[i]['y'] += 1
            else:
                if self.tourists[i]['in']:
                    self.cnt -= 1
                self.tourists[i]['in'] = False

    def show_people_number(self):
        number_surface = self.font.render("count : "+str(self.cnt), True, (0, 0, 0))
        number_rect = number_surface.get_rect()
        number_rect.topleft = (self.width - 150, 10)
        self.display_surface.blit(number_surface, number_rect)

    def show_success(self):
        font = pygame.font.Font('freesansbold.ttf', 100)
        success_surface = font.render('Successfully', True, (0, 0, 0))
        escape_surface = font.render('Escaped', True, (0, 0, 0))
        success_rect = success_surface.get_rect()
        escape_rect = escape_surface.get_rect()
        success_rect.midtop = (self.width / 2, 200)
        escape_rect.midtop = (self.width / 2, success_rect.height + 200 + 25)

        self.display_surface.blit(success_surface, success_rect)
        self.display_surface.blit(escape_surface, escape_rect)

    def run(self):
        self.create_tourists()
        self.create_exit()
        self.choose_closest_exit()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if self.cnt > 0:
                self.display_surface.fill(self.white)
                self.update_check_array()
                self.move()
                self.draw_tourists()
                self.draw_exit()
                self.draw_grid()
            self.draw_grid()
            self.show_people_number()
            pygame.display.update()
            pygame.time.delay(200)
            if self.cnt == 0:
                self.show_success()

    def set_full_screen(self):
        self.display_surface = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)


if __name__ == '__main__':
    place = Louvre()
    place.set_population(1000)
    place.set_exit_number(10)
    place.run()
