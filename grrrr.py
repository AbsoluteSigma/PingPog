from pygame import *
font.init()
plr_lost = 0
enabled = True
game = True
clock = time.Clock()
window = display.set_mode((960,600))
display.set_caption("пинг понг")
background = transform.scale(image.load("clouds.jpg"), (960,600))
font1 = font.SysFont("verdana", 52)


class Plate(sprite.Sprite):
    def __init__(self, plr1):
        super().__init__()
        self.plr1 = plr1
        self.image = transform.scale(image.load("plate.png"), (28, 160))
        self.rect = self.image.get_rect()
        self.rect.y = 200
        if plr1: self.rect.x = 60
        else: self.rect.x = 840

class Ball(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = transform.scale(image.load("plate.png"), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.y = 200
        self.rect.x = 300
        self.speed_x = 5
        self.speed_y = 5
        self.bounces = 0
        self.last_plr_collision = 0


    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        global game, plr_lost
        if self.rect.y < 0 or self.rect.y > 540:
            self.speed_y *= -1

        if self.rect.x < 0:
            game = False
            plr_lost = 1
            plr1.kill()
            plr2.kill()
            ball.kill()

        if self.rect.x > 960:
            game = False
            plr_lost = 2
            plr1.kill()
            plr2.kill()
            ball.kill()

        if sprite.collide_rect(plr1, self):
            if self.last_plr_collision != 1:
                self.last_plr_collision = 1
                self.speed_x *= -1
                self.bounces += 1
                print(self.bounces)
                if self.bounces == 8:
                    self.bounces = 0
                    self.speed_x *= 1.05
                    self.speed_y *= 1.05

        if sprite.collide_rect(plr2, self):
            if self.last_plr_collision != 2:
                self.last_plr_collision = 2
                self.speed_x *= -1
                self.bounces += 1
                if self.bounces == 8:
                    self.bounces = 0
                    self.speed_x *= 1.05
                    self.speed_y *= 1.05


        window.blit(self.image, (self.rect.x, self.rect.y))


def update_players():
    keys_pressed = key.get_pressed()
    if keys_pressed[K_w] and plr1.rect.y > 30: plr1.rect.y -= 10
    elif keys_pressed[K_s] and plr1.rect.y < 410: plr1.rect.y += 10
    if keys_pressed[K_UP] and plr2.rect.y > 30: plr2.rect.y -= 10
    elif keys_pressed[K_DOWN] and plr2.rect.y < 410: plr2.rect.y += 10
    window.blit(plr1.image, (plr1.rect.x, plr1.rect.y))
    window.blit(plr2.image, (plr2.rect.x, plr2.rect.y))

plr1 = Plate(True)
plr2 = Plate(False)

plrs = sprite.Group()
plrs.add(plr1,plr2)

ball = Ball()


while enabled:
    if game:
        window.blit(background,(0,0))
        update_players()
        ball.update()

    else:
        a = font1.render("Игрок " + str(plr_lost) + " лох", True, (255, 5, 5))
        window.blit(a, (320, 250))

    for e in event.get():
        if e.type == QUIT: enabled = False
        if e.type == KEYDOWN and e.key == K_r and not game:
            plr1 = Plate(True)
            plr2 = Plate(False)
            plrs = sprite.Group()
            plrs.add(plr1,plr2)
            ball = Ball()
            game = True

    clock.tick(30)
    display.update()