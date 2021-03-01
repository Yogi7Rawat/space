# Pygame template - skeleton for a new pygame project
import pygame
import random
import os
WIDTH = 600
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
POWERUP_TIME = 5000
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yogendra Space Game")
clock = pygame.time.Clock()


game_folder = os.path.dirname(__file__)
snd_folder = os.path.join(game_folder,'snd')
img_folder = os.path.join(game_folder,'img')

player_lives = pygame.transform.scale(pygame.image.load(os.path.join(img_folder,'playerShip1_orange.png')),(25,25)).convert()

powerup_images = {}
powerup_images['shield'] = pygame.image.load(os.path.join(img_folder, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(os.path.join(img_folder, 'bolt_gold.png')).convert()

meteor_img = []
meteor_list = ['meteorBrown_big1.png','meteorBrown_med1.png','meteorBrown_med3.png','meteorBrown_small1.png','meteorBrown_tiny1.png']
	   
for img in meteor_list:
	meteor_img.append(pygame.image.load(os.path.join(img_folder,img)).convert())


explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in range(9):
	filename = f'regularExplosion0{i}.png'
	img = pygame.image.load(os.path.join(img_folder,filename))
	img.set_colorkey(BLACK)
	img_lg = pygame.transform.scale(img,(75,75))
	explosion_anim['lg'].append(img_lg)
	img_sm = pygame.transform.scale(img,(32,32))
	explosion_anim['sm'].append(img_sm)
	filename = f'sonicExplosion0{i}.png'
	img = pygame.image.load(os.path.join(img_folder,filename)).convert()
	img.set_colorkey(BLACK)
	explosion_anim['player'].append(img)
	
shield_sound = pygame.mixer.Sound(os.path.join(snd_folder, 'pow4.wav'))
power_sound = pygame.mixer.Sound(os.path.join(snd_folder, 'pow5.wav'))
shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder,'pew.wav'))
expl_sounds = []
for snd in ['expl3.wav','expl6.wav']:
	expl_sounds.append(pygame.mixer.Sound(os.path.join(snd_folder,snd)))


pygame.mixer.music.load(os.path.join(snd_folder,'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

background = pygame.transform.scale(pygame.image.load(os.path.join(img_folder,"background-black.png")),(WIDTH,HEIGHT)).convert()
background_rect = background.get_rect()


font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
	font = pygame.font.Font(font_name,size)
	text_surface = font.render(text,False,WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surf.blit(text_surface,text_rect)
	





def draw_shield(x,y,pct):
	if pct<0:
		pct=0
	
	BAR_LENGTH = 100
	BAR_HEIGHT = 10
	
	fill = (pct/100) * BAR_LENGTH
	
	outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
	fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
	
	pygame.draw.rect(screen,GREEN,fill_rect)
	pygame.draw.rect(screen,WHITE,outline_rect,2)
	
def draw_lives(surf,x,y,lives,img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 30 * i
		img_rect.y = y
		surf.blit(player_lives,img_rect)


class Explosion(pygame.sprite.Sprite):
	def __init__(self,center,size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_anim[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50
	
	def update(self):
		now = pygame.time.get_ticks()
		if now-self.last_update>self.frame_rate:
			self.last_update = now
			self.frame+=1
			if self.frame == len(explosion_anim[self.size]):
				self.kill()
				
			else:
				center = self.rect.center
				self.image = explosion_anim[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center



class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(pygame.image.load(os.path.join(img_folder,'playerShip1_orange.png')),(70,70)).convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT-10
		self.radius = 20
		#pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
		self.x_speed = 0
		self.y_speed = 0
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.shield = 100
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()
		self.power = 1
		self.power_time = pygame.time.get_ticks()
	
		
		
	def update(self):
		# timeout for powerups
		if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
			self.power -= 1
			self.power_time = pygame.time.get_ticks()
			
			# unhide if hidden
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
			self.hidden = False
			self.rect.centerx = WIDTH / 2
			self.rect.bottom = HEIGHT - 10
			
		
		self.speedx = 0
		
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w] and self.rect.top>0:
			self.rect.y -= 4
			
		if keys[pygame.K_s] and self.rect.bottom+20<HEIGHT:
			self.rect.y += 4
			
		if keys[pygame.K_a] and self.rect.left>0:
			self.rect.x -= 5
			
		if keys[pygame.K_d] and self.rect.right<WIDTH:
			self.rect.x += 5
	
		self.rect.x +=self.x_speed
		self.rect.y+=self.y_speed
		
		
	def shoot(self):
		bullet = Bullet(self.rect.centerx,self.rect.top)
		all_sprites.add(bullet)
		bullets_sprites.add(bullet)
		shoot_sound.play()
		
	def powerup(self):
		self.power += 1
		self.power_time = pygame.time.get_ticks()
		
	def hide(self):
		# hide the player temporarily
		self.hidden = True
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (WIDTH / 2, HEIGHT + 200)
		
		
	
		
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_orig = random.choice(meteor_img)
		self.image = self.image_orig.copy()
		self.image_orig.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH-self.image.get_width())
		self.rect.y = random.randrange(-150,-100)
		self.y_speed = random.randrange(1,8)
		self.x_speed = random.randrange(-3,3)
		self.rot = 0
		self.rot_speed = random.randrange(-8,8)
		self.last_update = pygame.time.get_ticks()
		self.radius = int(self.rect.width*(0.85)/2)
		
		
	
	def rotate(self):
		now = pygame.time.get_ticks()
		if now-self.last_update>50:
			self.last_update = now
			self.rot = (self.rot+self.rot_speed)%360
			new_image = pygame.transform.rotate(self.image_orig,self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center
	
	
	def update(self):
		self.rotate()
		self.rect.y+=self.y_speed
		self.rect.x+=self.x_speed
		if self.rect.top>HEIGHT+10:
			self.rect.x = random.randrange(WIDTH-self.image.get_width())
			self.rect.y = random.randrange(-100,-40)
			self.y_speed = random.randrange(2,12)
			self.x_speed = random.randrange(-3,3)
		



class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join(img_folder,"laserRed16.png"))
		self.rect = self.image.get_rect()
		self.y_speed = -10
		self.rect.bottom = y
		self.rect.centerx = x
		
	def update(self):
		self.rect.y +=self.y_speed
		
		if self.rect.bottom<0:
			self.kill()
			
			
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

def newenemy():
	e = Enemy()
	all_sprites.add(e)
	enemy_sprites.add(e)
	
def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Lost in Space!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
	

# Game loop
running = True
game_over = True
score =0
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bullets_sprites = pygame.sprite.Group()
powerups = pygame.sprite.Group()
pygame.mixer.music.play(loops=-1)

for i in range(8):
	newenemy()
	
while running:
	# keep loop running at the right speed
	if game_over:
		show_go_screen()
		game_over = False
		all_sprites = pygame.sprite.Group()
		enemy_sprites = pygame.sprite.Group()
		bullets_sprites = pygame.sprite.Group()
		powerups = pygame.sprite.Group()
		player = Player()
		all_sprites.add(player)
		for i in range(8):
			newenemy()
			score = 0
			
	screen.fill(BLACK)
	screen.blit(background,(0,0))
	clock.tick(FPS)
		# Process input (events)
	
	for event in pygame.event.get():
			# check for closing windo
			
		if event.type ==pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()
		
		if event.type == pygame.QUIT:
			running = False
	
	
	
	hits = pygame.sprite.groupcollide(enemy_sprites,bullets_sprites,True,True)
	for hit in hits:
		score+=1
		random.choice(expl_sounds).play()
		exp = Explosion(hit.rect.center,'lg')
		all_sprites.add(exp)
		if random.random() > 0.9:
			pow = Pow(hit.rect.center)
			all_sprites.add(pow)
			powerups.add(pow)
		newenemy()
	
	hits = pygame.sprite.spritecollide(player,enemy_sprites,True,pygame.sprite.collide_circle)
	
	for hit in hits:
		player.shield -= hit.radius * 2
		exp = Explosion(hit.rect.center,'sm')
		all_sprites.add(exp)
		newenemy()
		
		if player.shield<=0:
			death_explosion = Explosion(player.rect.center,'player')
			all_sprites.add(death_explosion)
			random.choice(expl_sounds).play()
			player.hide()
			player.lives-=1
			player.shield = 100
	
	hits = pygame.sprite.spritecollide(player, powerups, True)
	for hit in hits:
		if hit.type == 'shield':
			player.shield += random.randrange(10, 30)
			shield_sound.play()
			if player.shield >= 100:
				player.shield = 100
		if hit.type == 'gun':
			player.powerup()
			power_sound.play()
			
	
	if player.lives ==0:
		game_over=True
	
	
	draw_text(screen,"Score: "+str(score),18,WIDTH/2+220,10)
	draw_shield(player.image.get_width()+player.rect.x-85,player.image.get_height()+player.rect.y,player.shield)
	draw_lives(screen,WIDTH/2-290,5,player.lives,player_lives)
	all_sprites.draw(screen)
	
	all_sprites.update() 
	
	
	pygame.display.update()

pygame.quit()

