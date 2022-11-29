# cmd /K python "$(FULL_CURRENT_PATH)"

# pip install pygame

import pygame
import sys
import random
from bullet_2 import Bullet

#--Creating a tank:
class Tank_2(pygame.sprite.Sprite):

	def __init__(self, field_size):
		super().__init__()
#--Level of the tank:		
		self.level = 2
#--Lives of the tank. If health == 0, deduct 1 life:
		self.lives = 2
#--Maximum health for bonus_helmet
		self.max_health = 999
#--self.image and self.rect are mandatory and will not work if misspelled (named differently)
		self.list_of_tank_images = [
			'tank1',
			'tank2',
			'tank3',
			'tank4'
			]
			
		self.image = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Player2/' + self.list_of_tank_images[self.level - 1] + '.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, (23, 23))
#--self.position_list contains following directions: right, left, up, down
#--Why use it? It creates a structure from __init__, which cannot be later overwritten in def navigation().
#--If we add pygame.transform.rotate directly in def navigation(), our picture would rotated constantly
		self.position_list = [
			pygame.transform.rotate(self.image, -90),
			pygame.transform.rotate(self.image, 90),
			pygame.transform.rotate(self.image, 0),
			pygame.transform.rotate(self.image, 180)
			]
#--View from which we start:
		self.image = self.position_list[2]
#--So that the tank does not run away
		self.width, self.height = field_size
#--Set level.Changing level will change some variables: speed, number of bullets, etc.
#--self.health = how many damage the tank can take before being destroyed
#--self.damage = how many damage it deals
#--self.tank_addition_to_bullet_speed = how fast a bullet flies
		
		self.level_speed = 2
		self.health = 3
		self.damage = 0
		self.tank_addition_to_bullet_speed = 0
		
#--SHOOTING--------------------------------------
		self.bullet_fire_time = 0
		self.charged = True
	#--Shooting frequency:
		self.gun_barrel_cooldown_time = 900
	#--Group or lasers together
		self.bullet_group = pygame.sprite.Group()
		

###------------>We can update the initial position of our tank. Maybe make it random?
		self.rect = self.image.get_rect(bottomleft=(365,field_size[1]))
###------------> Speed attribute may depend on the level of your tank
		self.speed_mode = [0, 2, 4, 5]
		self.speed = self.speed_mode[1]
		
#--Checking for a current level:	
		self.player_tank_level_check()

#--Creating shield:
		self.shield_frame1_org = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Shield/shield1.png').convert_alpha()
		self.shield_frame2_org = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Shield/shield2.png').convert_alpha()
		
		self.shield_frame1 = pygame.transform.scale(self.shield_frame1_org, (23, 23))
		self.shield_frame2 = pygame.transform.scale(self.shield_frame2_org, (23, 23))
		
		self.shield_frames = [self.shield_frame1, self.shield_frame2]
		self.shield_index = 0
		self.shield_image = self.shield_frames[self.shield_index]
		self.shield_rect = self.shield_image.get_rect(topleft=(self.rect.x, self.rect.y))
		
	def navigation(self):
	#---------->Maybe later I can pass a list of keys (if a second player is to be added)
#--Main objectives: change image position with self.position_list and move the rect with self.speed
		keys = pygame.key.get_pressed()
		self.current_x, self.current_y = self.rect.topleft
		#match self.level:
			#case 1: 
				#self.image = pygame.transform.scale(pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/' + self.list_of_tank_images[self.level - 1] + '.png').convert_alpha(), (23, 23))

		#print("Your level is one")
		if keys[pygame.K_d]:
			self.image = self.position_list[0]
			self.rect.x += self.speed
			self.shield_rect = self.shield_image.get_rect(topleft=(self.rect.x, self.rect.y))
		elif keys[pygame.K_a]:
			self.image = self.position_list[1]
			self.rect.x -= self.speed
			self.shield_rect = self.shield_image.get_rect(topleft=(self.rect.x, self.rect.y))
		elif keys[pygame.K_w]:
			self.image = self.position_list[2]
			self.rect.y -= self.speed
			self.shield_rect = self.shield_image.get_rect(topleft=(self.rect.x, self.rect.y))
		elif keys[pygame.K_s]:
			self.image = self.position_list[3]
			self.rect.y += self.speed
			self.shield_rect = self.shield_image.get_rect(topleft=(self.rect.x, self.rect.y))
		elif keys[pygame.K_x] and self.charged:
			self.shooting()
			self.bullet_fire_time = pygame.time.get_ticks()
			self.charged = False
			
	def bullet_recharge(self):
		self.current_time = pygame.time.get_ticks()
		if self.current_time - self.bullet_fire_time >= self.gun_barrel_cooldown_time:
			self.charged = True
			
	def shooting(self):
		self.bullet_sprite = Bullet(self.rect.center)
		self.bullet_group.add(self.bullet_sprite)
#--Our bullets should always point to the same direction as the gun barrel and depending on its position, fly in appropriate direction
		if self.image == self.position_list[0]:
			self.bullet_sprite.image = self.bullet_sprite.position_list[0]
		elif self.image == self.position_list[1]:
			self.bullet_sprite.image = self.bullet_sprite.position_list[1]
		elif self.image == self.position_list[2]:
			self.bullet_sprite.image = self.bullet_sprite.position_list[2]
		elif self.image == self.position_list[3]:
			self.bullet_sprite.image = self.bullet_sprite.position_list[3]
			
		self.bullet_sprite.speed += self.tank_addition_to_bullet_speed
			

	def border_control(self):
#--The goal is to check whether our tank is trying to leave the boarders of the screen and if so prohibit it
		if self.rect.left < 0: self.rect.left = 0
		elif self.rect.right > self.width: self.rect.right = self.width
		elif self.rect.bottom > self.height: self.rect.bottom = self.height
		elif self.rect.top < 0: self.rect.top = 0
		
#--What is our tank's level? Depending on the level, some parameters might be changed		
	def player_tank_level_check(self):
		match self.level:
			case 1: 
				self.health = 1
				self.damage = 0
				self.level_speed = 2
				self.tank_addition_to_bullet_speed = 0
				self.gun_barrel_cooldown_time = 900
				self.image = pygame.transform.scale(pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Player2/' + self.list_of_tank_images[self.level - 1] + '.png').convert_alpha(), (23, 23))
#--How the image should change
				self.position_list = [
					pygame.transform.rotate(self.image, -90),
					pygame.transform.rotate(self.image, 90),
					pygame.transform.rotate(self.image, 0),
					pygame.transform.rotate(self.image, 180)
							]
			case 2:
				self.health = 2
				self.damage = 1
				self.tank_addition_to_bullet_speed = 1
				self.gun_barrel_cooldown_time = 700
				self.image = pygame.transform.scale(pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Player2/' + self.list_of_tank_images[self.level - 1] + '.png').convert_alpha(), (23, 23))
#--How the image should change
				self.position_list = [
					pygame.transform.rotate(self.image, -90),
					pygame.transform.rotate(self.image, 90),
					pygame.transform.rotate(self.image, 0),
					pygame.transform.rotate(self.image, 180)
					]
			case 3:
				self.health = 3
				self.damage = 2
				self.tank_addition_to_bullet_speed = 3
				self.level_speed = self.speed_mode[2]
				self.gun_barrel_cooldown_time = 600
				self.image = pygame.transform.scale(pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Player2/' + self.list_of_tank_images[self.level - 1] + '.png').convert_alpha(), (23, 23))
#--How the image should change
				self.position_list = [
					pygame.transform.rotate(self.image, -90),
					pygame.transform.rotate(self.image, 90),
					pygame.transform.rotate(self.image, 0),
					pygame.transform.rotate(self.image, 180)
							]
			case 4:
				self.health = 4
				self.damage = 99
				self.tank_addition_to_bullet_speed = 4
				self.level_speed = self.speed_mode[3]
				self.gun_barrel_cooldown_time = 500
				self.image = pygame.transform.scale(pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Player2/' + self.list_of_tank_images[self.level - 1] + '.png').convert_alpha(), (23, 23))
#--How the image should change
				self.position_list = [
					pygame.transform.rotate(self.image, -90),
					pygame.transform.rotate(self.image, 90),
					pygame.transform.rotate(self.image, 0),
					pygame.transform.rotate(self.image, 180)
							]
			
			case _:
				self.health = 5
				self.gun_barrel_cooldown_time = 400
				self.tank_addition_to_bullet_speed = 5
				self.level_speed = self.speed_mode[3]
				self.damage = 99
				# self.tank_addition_to_bullet_speed += 1
				# if self.gun_barrel_cooldown_time == 0:
					# self.gun_barrel_cooldown_time = 0
				# else:
					# self.gun_barrel_cooldown_time -= 50
				
		
	def update(self):
		
		self.navigation()
		self.border_control()
		
		
		self.bullet_recharge()
		self.bullet_group.update()

		
		
