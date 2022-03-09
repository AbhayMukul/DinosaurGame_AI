import pygame
import os
import time
import neat
import random

WIN_WIDTH = 450
WIN_HEIGHT = 500

pygame.init()

IMG_DINO_JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

IMG_DINO_RUNNING = [
    (pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png"))),
    (pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png")))]

IMG_TRACK = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

IMG_CACTUS = [(pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png"))),
              (pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png"))),
              (pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))), ]

IMG_CACTUS_SMALL = [(pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png"))),
                    (pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png"))),
                    (pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png")))]

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


class Cactus:
    IMG = IMG_CACTUS
    Y_POS = 375

    def __init__(self, x, game_speed):
        self.X_POS = x
        self.game_speed = game_speed
        self.index = random.randrange(0, 2)

    def draw(self):
        screen.blit(self.IMG[self.index], (self.X_POS, self.Y_POS))

    def move(self):
        self.X_POS -= self.game_speed

    def collide(self, dinosaur):
        b_point = False
        dinosaur_mask = dinosaur.get_mask()
        cactus_mask = pygame.mask.from_surface(self.IMG[self.index])

        offset = (self.X_POS - dinosaur.X_POS, self.Y_POS - round(dinosaur.Y_POS))

        b_point = dinosaur_mask.overlap(cactus_mask, offset)

        return b_point


class Background:
    X_POS = 0
    Y_POS = 450
    IMG = IMG_TRACK

    def __init__(self, game_speed):
        self.game_speed = game_speed

    def animate(self):
        image_width = self.IMG.get_width()
        screen.blit(self.IMG, (self.X_POS, self.Y_POS))
        screen.blit(self.IMG, (self.X_POS + image_width, self.Y_POS))

        self.X_POS -= self.game_speed

        if self.X_POS <= -image_width:
            self.X_POS = 0


class Dinosaur:
    VEL = 5
    X_POS = 20
    Y_POS = 375
    JUMP_VEL = 5
    IMGS_RUNNNING = IMG_DINO_RUNNING
    IMG_JUMPING = IMG_DINO_JUMPING

    def __init__(self):
        self.jump_count = 0
        self.dino_jump = False
        self.dino_run = True
        self.jump_vel = self.JUMP_VEL
        self.step_index = 0
        self.img = self.IMGS_RUNNNING[0]
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, self.img.get_width(), self.img.get_height())

    def check(self):
        if self.dino_run:
            self.run()

        elif self.dino_jump:
            self.jump()

    def run(self):
        if self.step_index > 9:
            self.step_index = 0

        self.img = IMG_DINO_RUNNING[self.step_index // 5]
        self.step_index += 1

    def jump(self):
        # called once per frame
        if self.dino_jump:
            if self.jump_count < 20:
                self.Y_POS -= 10
                self.jump_count += 1

            elif self.jump_count < 40:
                self.jump_count += 1
                self.Y_POS += 10

            else:
                self.dino_jump = False
                self.dino_run = True
                self.jump_count = 0

    def draw(self):
        screen.blit(self.img, (self.X_POS, self.Y_POS))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class main():
    dinosaurs = [Dinosaur()]
    background = Background(10)
    cactuses = [Cactus(500, 5)]

    clock = pygame.time.Clock()
    run = True

    add_cactus = False

    while run:
        clock.tick(30)

        if len(dinosaurs) <= 0:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass

        screen.fill((255, 255, 255))

        for cactus in cactuses:
            cactus.draw()
            cactus.move()

            if cactus.X_POS < -50:
                add_cactus = True
                cactuses.remove(cactus)

            for dinosaur in dinosaurs:
                if cactus.collide(dinosaur):
                    dinosaur.dino_jump = True
                    dinosaur.dino_run = False

        if add_cactus:
            add_cactus = False
            cactuses.append(Cactus(500, 5))

        for dinosaur in dinosaurs:
            dinosaur.check()
            dinosaur.draw()

        background.animate()

        pygame.display.update()

main()
