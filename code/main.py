import pygame
from random import randint, uniform
from os.path import join

import pygame.sprite

class ship(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image =  pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (Width/2, Height/2))
        self.direction = pygame.math.Vector2()
        self.speed = 500
        

        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown = 400
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown:
                self.can_shoot = True
   


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
         Laser(laser_surface, self.rect.midtop, (all_sprites, laser_sprites))
         self.can_shoot = False
         self.laser_shoot_time = pygame.time.get_ticks()
        
        self.laser_timer()
         

class Star(pygame.sprite.Sprite):
    def __init__(self, group, star_surf):
        super().__init__(group)
        self.image = star_surf
        self.rect = self.image.get_frect(center = (randint(0,Width), randint(0, Height)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self ,dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.time = pygame.time.get_ticks() #everytime we call this class it captures a point in time
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(400, 500)
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
         #if the duration of the entire game minus that point in time
         #is greater than or equal to the meteor lifetime
         #lets say the game has been running for 5 secs (5000)
         #he meteor was made like around 2 seconds ago (2000) in the entire life time of the game
         #so 5000 - 2000 = 3000
         #which is 3000 >= 3000 (meteor lifetime)
         #we kill it 
         
        if pygame.time.get_ticks() - self.time >= self.lifetime:
            self.kill()

def Collissions():

    global running
    collide_sprites = pygame.sprite.spritecollide(Ship, meteor_sprites, True)
    font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
    font_text = font.render("YOU DIED", True, (255, 100, 100))
    font_text_rect = font_text.get_rect(midbottom=(Width / 2, Height / 2))
    
    
    if collide_sprites:
        # Show the "YOU DIED" text when the ship collides with a meteor
        font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
        font_text = font.render("YOU DIED", True, (255, 100, 100))
        font_text_rect = font_text.get_rect(midbottom=(Width / 2, Height / 2))

        # Blit the text onto the display
        display.blit(font_text, font_text_rect)
        
        # Update the display to show the text
        pygame.display.update()

        # Add a small delay to allow the player to see the "YOU DIED" message
        pygame.time.delay(3000)  # 3 seconds delay

        # Stop the game after displaying the message
        running = False
        
        
    
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            
def display_score():
    current_time = pygame.time.get_ticks()// 100
    font_text = font.render(str(current_time), True, (240,240,240))
    font_text_rect = font_text.get_rect(midbottom = (Width/2, Height -50))
    display.blit(font_text, font_text_rect)
    #the font_text_rect.inflate() gives another rectangle so we can use .move() on it but im still a bit confused why
    pygame.draw.rect(display, "white", font_text_rect.inflate(50,30).move(0, -10), 5, 10)


# General Setup
pygame.init()
Width, Height = 1280, 620
display = pygame.display.set_mode((Width, Height))
running = True
clock = pygame.time.Clock()

# plain surfaces
surf = pygame.Surface((50, 50))
surf.fill('purple')
x = 50

# importing image/ image surface
""" ship_surface = pygame.image.load(join('images', 'player.png')).convert_alpha()
ship_rect = ship_surface.get_frect(center = (Width/2, Height/2)) #f rectangles, acts like a surface but you can be quick with putting it on the display
ship_direction = pygame.math.Vector2()
ship_speed = 300 """

all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha() # we do this here so it only imports one time
for i in range(20):
    Star(all_sprites, star_surf)
Ship = ship(all_sprites)
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)




#meteor and laser
meteor_surface = pygame.image.load(join('images', 'meteor.png')).convert_alpha()


laser_surface = pygame.image.load(join('images', 'laser.png')).convert_alpha()


#event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick()/ 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        """ if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            print(1)
        if event.type == pygame.MOUSEMOTION:
            ship_rect.center = event.pos """

        if event.type == meteor_event:
            x, y = randint(0, Width) , randint(-200, -100)
            Meteor(meteor_surface, (x,y), (all_sprites, meteor_sprites))
           
            
    #player movement
    """ keys = pygame.key.get_pressed()
    ship_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])  """
    
    # what we are doing here is that we are putting a boolean value inside
    #so if we press right we are getting 1 and left is 0
    #but if we press left we are getting 0 - 1 which is negative 1
    # so our x for player direction is -1 which makes it go left

    """ ship_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])  """
    #same logic here
    

    """  ship_rect.center += ship_direction * ship_speed * dt """
    #we then need this to make it actually move in the screen.
    #if we dont add this what only happens is that the value changes but you are not really moving the 
     #center of the ship
    """ ship_direction = ship_direction.normalize() if ship_direction else ship_direction """
    #  normalize() turns a vector into a vector that has a magnitude or value of 1
    #  when we normalize a vector that has a value of (0,0) it causes an error cuz you cant do that
    # but any other value we can, so if ship_direction has any other value then yeah normalize it else
    # dont and just keep it at 0/ if ship is moving normalize it
    
    """ recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE]:
        print('fire') """

    #the collission Function
    Collissions()
    
    #calls alls the update method in the group
    all_sprites.update(dt)
    
    # Drawing the game
    pygame.display.set_caption('Space Shooter') # sets the display title
    display.fill('black') #fills the display with a color

    """ for pos in star_positions: #displays the stars after the display has been filled with gray
        display.blit(star_surface, pos)      """  

    
    
    # display.blit(ship_surface, ship_rect)

    all_sprites.draw(display)
    display_score()


    



    pygame.display.update()


pygame.quit()