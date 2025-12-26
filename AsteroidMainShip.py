import pygame
import math

screen_width = 1280
screen_height = 768

RED = (255, 0, 0)

class MainShip(pygame.sprite.Sprite):  # Define a class `Character` that inherits from pygame's `Sprite` class.
    def __init__(self, position, speed, shotsize=1):  # Initialize the character object with a starting position.
        super().__init__()
        # Load the image file (spritesheet) into the `sheet` attribute.
        self.sheet = pygame.image.load('MainShip/MainShip.png').convert_alpha()
        
        # Define the area of a single sprite within the sheet (first sprite clip).
        self.sheet.set_clip(pygame.Rect(9, 10, 30, 28))
        
        # Get the clipped image (current sprite frame) and set it as the current image of the sprite.
        self.imageOriginal = self.sheet.subsurface(self.sheet.get_clip())
        self.imageRotated = self.imageOriginal.copy()
        self.image = self.imageOriginal.copy()
        # Get the rectangle of the current sprite image for positioning on the screen.
        self.rect = self.image.get_rect()
        
        # Set the top-left position of the sprite on the screen using the position parameter.
        self.rect.topleft = position
        self.angle = 0
        self.speed = speed
        self.opacity = 255
        self.shotsize = shotsize
        #self.shield = pygame.image.load('')

        
        # Initialize a frame counter for cycling through the frames (animations).
        #self.frame = 0
        
        # Define the coordinates of each animation frame in the spritesheet for different directions.
        #self.left_states = {0: (0, 76, 52, 76), 1: (52, 76, 52, 76), 2: (156, 76, 52, 76)}
        #self.right_states = {0: (0, 152, 52, 76), 1: (52, 152, 52, 76), 2: (156, 152, 52, 76)}
        #self.up_states = {0: (0, 228, 52, 76), 1: (52, 228, 52, 76), 2: (156, 228, 52, 76)}
        #self.down_states = {0: (0, 0, 52, 76), 1: (52, 0, 52, 76), 2: (156, 0, 52, 76)}

        #self.animation_speed = 100
        #self.last_update = pygame.time.get_ticks()


    #def get_frame(self, frame_set):  # Get the next frame in the given frame set (animation loop).
        #current_time = pygame.time.get_ticks()
        #if current_time - self.last_update >= self.animation_speed:
            # Increment the frame counter.
            #self.frame += 1
        
            #self.last_update = current_time

            # Loop back to the first frame if the counter exceeds the number of frames.
            #if self.frame > (len(frame_set) - 1):
                #self.frame = 0
        
            #print(frame_set[self.frame])  # Debugging: print the current frame's rectangle.  

        #return frame_set[self.frame] # Return the rectangle of the current frame.

    def clip(self, clipped_rect):  # Set the clipping region (current frame) based on a provided rectangle.
        if type(clipped_rect) is dict:  # If the clipped rect is a dictionary (animation set), get the next frame.
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            # Set the clipping area directly if it's a specific rectangle.
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect  # Return the clipped rectangle.

    def move(self, direction):  # Update the character's position and animation based on the direction.
        if direction == 'left':  # Move left and play left walking animation.
            #self.clip(self.left_states)
            self.angle = 90
            self.imageRotated=pygame.transform.rotate(self.imageOriginal, self.angle)
            self.rect = self.imageRotated.get_rect(center=self.rect.center)
            self.rect.x -= self.speed
        if direction == 'right':  # Move right and play right walking animation.
            #self.clip(self.right_states)
            self.angle = 270
            self.imageRotated=pygame.transform.rotate(self.imageOriginal, self.angle)
            self.rect = self.imageRotated.get_rect(center=self.rect.center)
            self.rect.x += self.speed
            #self.rect.x += 1
        if direction == 'up':  # Move up and play up walking animation.
            #self.clip(self.up_states)
            self.angle = 0
            self.imageRotated=pygame.transform.rotate(self.imageOriginal, self.angle)
            self.rect = self.imageRotated.get_rect(center=self.rect.center)
            self.rect.y -= self.speed
        if direction == 'down':  # Move down and play down walking animation.
            #self.clip(self.down_states)
            self.angle = 180
            self.imageRotated=pygame.transform.rotate(self.imageOriginal, self.angle)
            self.rect = self.imageRotated.get_rect(center=self.rect.center)
            self.rect.y += self.speed
        #self.applyOpacity()

        # Standing still animations (no movement, just switching frames to standing).
        #if direction == 'stand_left':
            #self.clip(self.left_states[0])
        #if direction == 'stand_right':
            #self.clip(self.right_states[0])
        #if direction == 'stand_up':
            #self.clip(self.up_states[0])
        #if direction == 'stand_down':
            #self.clip(self.down_states[0])

        # Update the image with the current clipped frame.
        #self.image = self.sheet.subsurface(self.sheet.get_clip())

    def handle_event(self, event):  # Handle keyboard events to move the character or stop movement.
        if event.type == pygame.KEYDOWN:  # If a key is pressed down:
            if event.key == pygame.K_LEFT:  # Move left if the left arrow is pressed.
                self.move('left')
            if event.key == pygame.K_RIGHT:  # Move right if the right arrow is pressed.
                self.move('right')
            if event.key == pygame.K_UP:  # Move up if the up arrow is pressed.
                self.move('up')
            if event.key == pygame.K_DOWN:  # Move down if the down arrow is pressed.
                self.move('down')
            if event.key == pygame.K_SPACE:
                speedx = 0
                speedy = 0
                if self.angle == 0:
                    speedy = -2
                if self.angle == 90:
                    speedx = -2
                if self.angle == 180:
                    speedy = 2
                if self.angle == 270:
                    speedx = 2
                shoot = laser(self.rect.center, speedx, speedy, self.shotsize)
                return shoot
            if self.rect.right < 0:
                self.rect.left = screen_width
            elif self.rect.left > screen_width:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = screen_height
            elif self.rect.top > screen_height:
                self.rect.bottom = 0

                

        #if event.type == pygame.KEYUP:  # If a key is released (stop movement):
            #if event.key == pygame.K_LEFT:  # Stop and stand facing left.
                #self.update('stand_left')
            #if event.key == pygame.K_RIGHT:  # Stop and stand facing right.
                #self.update('stand_right')
            #if event.key == pygame.K_UP:  # Stop and stand facing up.
                #self.update('stand_up')
            #if event.key == pygame.K_DOWN:  # Stop and stand facing down.
                #self.update('stand_down')
    
    def update(self, shield=False):
        rotated = pygame.transform.rotate(self.imageOriginal, self.angle)

        self.image = rotated.copy()
        self.image.fill((255, 255, 255, self.opacity), special_flags=pygame.BLEND_RGBA_MULT)
        if shield:
            self.image = self.shield_glow()
        
        self.rect = self.image.get_rect(center=self.rect.center)

    def setOpacity(self, opacity):
        self.opacity = max(0, min(255, opacity))

    def shield_glow(self):
        glowing = self.image.copy()
        surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        surface.fill((0, 80, 255, 40))
        glowing.blit(surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return glowing


class laser(pygame.sprite.Sprite):
    def __init__(self, position, speedx, speedy, shotsize):
        super().__init__()
        self.image = pygame.Surface((8*shotsize, 8*shotsize), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (4*shotsize, 4*shotsize), 4*shotsize)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.vx = speedx
        self.vy = speedy
        self.life = 0
        if shotsize == 1:
            self.death = 300
        else:
            self.death = 400

    def update(self):
        self.rect.x += self.vx  # Move horizontally
        self.rect.y += self.vy  # Move vertically
        self.life += 1
        if self.life >= self.death:
            self.kill()
        if self.rect.right < 0:
            self.rect.left = screen_width
        elif self.rect.left > screen_width:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = screen_height
        elif self.rect.top > screen_height:
            self.rect.bottom = 0
