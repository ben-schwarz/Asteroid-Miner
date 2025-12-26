import pygame
from AsteroidMainShip import MainShip, laser
from Asteroid import Asteroid, MoneyPickup


pygame.init()

screen_width = 1280
screen_height = 768
score = 0
aggregateScore = 0
playerHitsRemaining = 3
playerMaxHitsRemaining = 3
round = 1
hitable = False
hitTimer = 0
hitTimerDuration = 1500
speed = 1
shots = 1
furthest_wave = 0
shotsize = 1
shieldsOn = False
shieldsActive = False
shieldTimer = -60000
shieldCooldown = 60000
WHITE = (255, 255, 255)
DARKGREY = (153, 153, 155)
LIGHTGREY = (203, 203, 205)
BLACK = (0, 0, 0)

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = LIGHTGREY
        self.pressed = False
        self.pressedTimer = 0
        self.pressedDuration = 150

    def draw(self, surface):
        if self.pressed == True:
            self.color = DARKGREY
        else:
            self.color = LIGHTGREY
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.SysFont('timesnewroman',  30)
        txt = font.render(self.text, True, BLACK)
        surface.blit(txt, (self.rect.x + 15, self.rect.y + 15))
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.pressed = True
            self.pressedTimer = pygame.time.get_ticks()
            return True
    
    def update(self):
        if self.pressed and pygame.time.get_ticks() - self.pressedTimer > self.pressedDuration:
            self.pressed = False


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Asteroid Miner")
background = pygame.image.load("AsteroidMinerBackground.png").convert_alpha()
background = pygame.transform.scale(background, (screen_width, screen_height))
thumbnail = pygame.image.load("AsteroidMinerThumbnail.png").convert_alpha()
thumbnail = pygame.transform.scale(thumbnail, (screen_width, screen_height))

asteroids = pygame.sprite.Group()
lasers = pygame.sprite.Group()
money = pygame.sprite.Group()

#set up refresh rate
clock = pygame.time.Clock()

#character position
#player = MainShip((screen_width/2, screen_height/2))
#all_sprites.add(player)
def spawnAsteroids(speed=1):
    asteroid = Asteroid((0, 0), 1, speed)
    asteroids.add(asteroid)
    asteroid = Asteroid((1000, 666), 1, speed)
    asteroids.add(asteroid)
    asteroid = Asteroid((400, 366), 1, speed)
    asteroids.add(asteroid)
    asteroid = Asteroid((800, 366), 1, speed)
    asteroids.add(asteroid)
start_screen = True
run_over = False
play = Button(390, 500, 500, 50, f"Play")
while start_screen == True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                start_screen = False
                run_over = True
        if play.is_clicked(event):
            start_screen = False
    play = Button(599, 640, 82, 50, f"Play")
    play.update()
    #screen.fill((0, 0, 0))
    screen.blit(thumbnail, (0, 0))
    play.draw(screen)
    #font = pygame.font.SysFont('timesnewroman',  50)
    #text = font.render(f'Asteroid Miner', True, WHITE)
    #textRect = text.get_rect()
    #textRect.center = (screen_width/2, 50)
    #screen.blit(text, textRect)
    font = pygame.font.SysFont('timesnewroman',  25)
    text = font.render(f'Dodge Asteroids!', True, WHITE)
    textRect = text.get_rect()
    textRect.center = (screen_width/2, 150)
    screen.blit(text, textRect)
    text = font.render(f'Destroy Asteroids so   you can colllect gold!', True, WHITE)
    textRect = text.get_rect()
    textRect.center = (screen_width/2+15, 250)
    screen.blit(text, textRect)
    text = font.render(f'Use gold to   buy upgrades!', True, WHITE)
    textRect = text.get_rect()
    textRect.center = (screen_width/2+25, 350)
    screen.blit(text, textRect)
    text = font.render(f'Get as far   as you can!', True, WHITE)
    textRect = text.get_rect()
    textRect.center = (screen_width/2+20, 450)
    screen.blit(text, textRect)
    
    pygame.display.flip()


#game loop boolean
game_over = False
shop_open = False
while run_over == False:
    round = 1
    shieldTimer = 0
    playerHitsRemaining = playerMaxHitsRemaining
    spawnAsteroids()
    hitable = False
    player = MainShip((screen_width/2, screen_height/2), speed, shotsize)
    while game_over == False:
        if round > furthest_wave:
            furthest_wave = round
        current_time = pygame.time.get_ticks()

        if hitable == False and current_time - hitTimer >= hitTimerDuration:
            hitable = True
        if shieldsOn:
            if shieldsActive == False and current_time - shieldTimer >= shieldCooldown:
                shieldsActive = True
        if playerHitsRemaining == 0:
            player.kill()
            game_over = True
            shop_open = True
        if len(asteroids) == 0 & len(money):
            round += 1
            spawnAsteroids(2)
            hitable = False
            hitTimer = pygame.time.get_ticks()

        asteroids.update()
        lasers.update()
        money.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                shop_open = False
                run_over = True
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        shop_open = False
                        run_over = True
                        game_over = True
            laser = player.handle_event(event)
            if laser:
                laser = player.handle_event(event)
                lasers.add(laser)
        player.handle_event(event)
        #screen.fill(pygame.Color('black'))
        screen.blit(background, (0, 0))
        if hitable == True:
            player.setOpacity(255)
            #player.applyOpacity()
        else:
            player.setOpacity(150)
            #player.applyOpacity()
        player.update(shieldsActive)

        screen.blit(player.image, player.rect)
        asteroids.draw(screen)
        lasers.draw(screen)
        money.draw(screen)

        laserHit = pygame.sprite.groupcollide(lasers, asteroids, True, False)
        for hit, asteroid in laserHit.items():
            for aster in asteroid:
                drop = MoneyPickup((aster.get_position()))
                money.add(drop)
                #asteroids.add(asteroid)
                if aster.get_size() == 1:
                    if round > 1:
                        asteroid = Asteroid((aster.get_position()), 2, 2)
                        asteroids.add(asteroid)
                        asteroid = Asteroid((aster.get_position()), 2, 2)
                        asteroids.add(asteroid)
                    else:
                        asteroid = Asteroid((aster.get_position()), 2, 1)
                        asteroids.add(asteroid)
                        asteroid = Asteroid((aster.get_position()), 2, 1)
                        asteroids.add(asteroid)
                    aster.kill()
                if aster.get_size() == 2:
                    if round > 1:
                        asteroid = Asteroid((aster.get_position()), 4, 2)
                        asteroids.add(asteroid)
                        asteroid = Asteroid((aster.get_position()), 4, 2)
                        asteroids.add(asteroid)
                    else:
                        asteroid = Asteroid((aster.get_position()), 4, 1)
                        asteroids.add(asteroid)
                        asteroid = Asteroid((aster.get_position()), 4, 1)
                        asteroids.add(asteroid)
                    aster.kill()
                if aster.get_size() == 4:
                    aster.kill()

        asteroidHit = pygame.sprite.spritecollide(player, asteroids, False)
        for aster in asteroidHit:
            if hitable == True:
                drop = MoneyPickup((aster.get_position()))
                money.add(drop)
                if aster.get_size() == 1:
                    if round > 1:
                        asteroid = Asteroid((aster.get_position()), 2, 2)
                        asteroids.add(asteroid)
                        asteroid = Asteroid((aster.get_position()), 2, 2)
                        asteroids.add(asteroid)
                    else:
                        asteroid = Asteroid((aster.get_position()), 2, 1)
                        asteroids.add(asteroid)
                        asteroid = Asteroid((aster.get_position()), 2, 1)
                        asteroids.add(asteroid)
                    aster.kill()
                if aster.get_size() == 2:
                    if round > 1:
                        asteroid = Asteroid((aster.get_position()), 4, 2)
                        asteroids.add(asteroid)
                        asteroid = Asteroid((aster.get_position()), 4, 2)
                        asteroids.add(asteroid)
                    else:
                        asteroid = Asteroid((aster.get_position()), 4, 1)
                        asteroids.add(asteroid)
                        asteroid = Asteroid((aster.get_position()), 4, 1)
                        asteroids.add(asteroid)
                    aster.kill()
                if aster.get_size() == 4:
                    aster.kill()
                if shieldsActive:
                    shieldsActive = False
                    shieldTimer = pygame.time.get_ticks()
                else:
                    playerHitsRemaining -= 1
                hitable = False
                hitTimer = pygame.time.get_ticks()

        moneyGet = pygame.sprite.spritecollide(player, money, False)
        for m in moneyGet:
            score += 100
            aggregateScore += 100
            m.kill()
        font = pygame.font.SysFont('timesnewroman',  30)
        text = font.render(f'Hits Remaining: {playerHitsRemaining} | Cash: {score} | Wave {round}', True, WHITE)
        textRect = text.get_rect()
        textRect.center = (screen_width/2, 25)
        screen.blit(text, textRect)
        pygame.display.flip()

    for sprite in money:
        sprite.kill()
    for sprite in asteroids:
        sprite.kill()

    Continue = Button(560, 600, 160, 50, "Continue")
    shckabs = Button(240, 150, 800, 50, f"Upgrade Shock Absorbers: {hitTimerDuration} ms I-frames | Costs 1000")
    blasters = Button(390, 225, 500, 50, f"Upgrade Blasters: lvl {shotsize} | Costs 2000")
    bstrs = Button(390, 300, 500, 50, f"Upgrade Boosters: lvl {speed} | Costs 2500")
    shields = Button(340, 375, 600, 50, f"Shield Generators: Not Purchased | Costs 3000")
    armr = Button(390, 450, 500, 50, f"Upgrade Armor: lvl {playerMaxHitsRemaining} | Costs 2500")
    while shop_open == True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    shop_open = False
                    run_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        shop_open = False
                        run_over = True
                        game_over = True
                if Continue.is_clicked(event):
                    shop_open = False
                    game_over = False
                if shckabs.is_clicked(event) and score >= 1000:
                    score -= 1000
                    hitTimerDuration += 500
                if bstrs.is_clicked(event) and score >= 2500:
                    score -= 2500
                    speed = 2
                if armr.is_clicked(event) and score >= 2500:
                    score -= 2500
                    playerMaxHitsRemaining += 1
                if blasters.is_clicked(event) and score >= 2000:
                    score -= 2000
                    shotsize += 1
                if shields.is_clicked(event) and score >= 3000:
                    score -= 3000
                    shieldsOn = True
        Continue.update()
        shckabs.update()
        bstrs.update()
        armr.update()
        blasters.update()
        shields.update()
        #screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        if hitTimerDuration < 3500:
            shckabs.draw(screen)
        if speed < 2:
            bstrs.draw(screen)
        if playerMaxHitsRemaining < 5:
            armr.draw(screen)
        if shotsize < 2:
            blasters.draw(screen)
        if shieldsOn == False:
            shields.draw(screen)
        font = pygame.font.SysFont('timesnewroman',  30)
        text = font.render(f'Shop | Cash: {score} | Furthest Wave: {furthest_wave}', True, WHITE)
        textRect = text.get_rect()
        textRect.center = (screen_width/2, 25)
        screen.blit(text, textRect)
        Continue.draw(screen)
        pygame.display.flip()

pygame.quit ()
