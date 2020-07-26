import pygame

class Actor(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, events, dt):
        pass

class Player(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)

    def update(self, events, dt):
        pressed = pygame.key.get_pressed()
        move = pygame.Vector2((0, 0))
        if pressed[pygame.K_w]: move += (0, -1)
        if pressed[pygame.K_a]: move += (-1, 0)
        if pressed[pygame.K_s]: move += (0, 1)
        if pressed[pygame.K_d]: move += (1, 0)
        if move.length() > 0: move.normalize_ip()
        self.pos += move*(dt/5)
        self.rect.center = self.pos

class YAwareGroup(pygame.sprite.Group):
    def by_y(self, spr):
        return spr.pos.y

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=self.by_y):
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []

def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    dt = 0

    sprites = YAwareGroup(Player(pygame.image.load('Assets/garlic.png').convert_alpha(), (100, 200)),
                          Actor(pygame.image.load('Assets/vampire.png').convert_alpha(), (200, 200)))

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

        sprites.update(events, dt)
        screen.fill((30, 30, 30))
        sprites.draw(screen)

        pygame.display.update()
        dt = clock.tick(60)

if __name__ == '__main__':
    main()
