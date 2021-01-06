import pygame
import neat
import time
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25  # max rotation of the bird
    ROT_VEL = 20  # velocity of the rotation
    ANIMATION_TIME = 5  # how fast the bird img is updated (flapping speed)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0  # how much the bird is currently tilted as it rotates
        self.tick_count = 0  # used for physics of jump and fall
        self.vel = 0
        self.height = self.y  # needed during tilt
        self.img_count = 0  # keep track of which img of our animation we are currently on
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y  # where the bird began

    # called every frame
    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2  # based on curr vel, calc arc of jump then fall
        if d >= 16:  # terminal velocity
            d = 16
        if d < 0:  # accelerate the jump
            d -= 2
        self.y = self.y + d

        # tilt
        if d < 0 or self.y < self.height + 50:  # keep upwards tilt if moving up or are above the pre-jump height
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:  # slowly tilt more downwards until 90 degree nose dive
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        # flap animation based on counter
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # nose dive means no flap animation
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2  # keep displaying correct image when method is called again

        # tilt image by rotating around its center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)  # rotate around center
        win.blit(rotated_image, new_rect.topleft)

    # used when we get collisions
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.move()
        draw_window(win, bird)
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()



