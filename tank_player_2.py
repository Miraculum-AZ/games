# cmd /K python "$(FULL_CURRENT_PATH)"

# pip install pygame

import pygame
import sys
import random
from bullet import Bullet

#--Creating a tank:
class Enemy(pygame.sprite.Sprite):

	def __init__(self, field_size):
		super().__init__()
#--self.image and self.rect are mandatory and will not work if misspelled (named differently)
		self.list_of_tank_enemy_names = [
			'tank_basic',
			'tank_fast',
			'tank_power',
			'tank_armor'
			]
#--Creating a random tank out of the list:			
		random_tank_enemy = random.choices(self.list_of_tank_enemy_names, weights=[3,2,1,1])
#--Giving it appropriate image and rect:		
		self.image = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Enemies/' + random_tank_enemy[0] + '.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, (23, 23))
		self.rect = self.image.get_rect(center=(400,200))
		
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
		self.image = self.position_list[3]
#--So that the tank does not run away
		self.width, self.height = field_size
#--Set level.Changing level will change some variables: speed, number of bullets, etc.
#--self.health = how many damage the tank can take before being destroyed
#--self.damage = how many damage it deals
#--self.tank_addition_to_bullet_speed = how fast a bullet flies
		self.level = 1
		self.level_speed = 2
		self.health = 1
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
		self.rect = self.image.get_rect(center=(400,200))
###------------> Speed attribute may depend on the level of your tank
		self.speed_mode = [0, 2, 4, 6]
		self.speed = self.speed_mode[1]
		
	def navigation(self):
	#---------->Maybe later I can pass a list of keys (if a second player is to be added)
#--Main objectives: change image position with self.position_list and move the rect with self.speed
		keys = pygame.key.get_pressed()
		self.current_x, self.current_y = self.rect.topleft
		if keys[pygame.K_d]:
			self.image = self.position_list[0]
			self.rect.x += self.speed
		elif keys[pygame.K_a]:
			self.image = self.position_list[1]
			self.rect.x -= self.speed
		elif keys[pygame.K_w]:
			self.image = self.position_list[2]
			self.rect.y -= self.speed
		elif keys[pygame.K_s]:
			self.image = self.position_list[3]
			self.rect.y += self.speed
		elif keys[pygame.K_z] and self.charged:
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
			case 1: pass
			case 2:
				self.health = 2
				self.damage = 1
				self.tank_addition_to_bullet_speed = 1
			case 3:
				self.health = 3
				self.damage = 2
				self.tank_addition_to_bullet_speed = 3
				self.level_speed = self.speed_mode[2]
			case 4:
				self.health = 4
				self.damage = 99
				self.tank_addition_to_bullet_speed = 4
				self.level_speed = self.speed_mode[3]
				
		
	def update(self):
		self.navigation()
		self.border_control()
		self.player_tank_level_check()
		
		
		self.bullet_recharge()
		self.bullet_group.update()

		
		
