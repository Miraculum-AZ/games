# cmd /K python "$(FULL_CURRENT_PATH)"

# pip install pygame

import pygame
import sys
import random
from bullet_ally import Bullet

TILE = 32

#--Creating a tank:
class Ally(pygame.sprite.Sprite):

	def __init__(self, field_size, pos):
		super().__init__()
		
#--So that the tank does not run away
		self.width, self.height = field_size
#--self.image and self.rect are mandatory and will not work if misspelled (named differently)
#--Giving it appropriate image and rect:
		self.image = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Ally/ally1.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, (23, 23))
		#self.rect = self.image.get_rect(bottomleft=(self.width - TILE, 0))
		self.rect = self.image.get_rect(bottomleft=(pos))
		
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
#--Set level.Changing level will change some variables: speed, number of bullets, etc.
#--self.health = how many damage the tank can take before being destroyed
#--self.damage = how many damage it deals
#--self.tank_addition_to_bullet_speed = how fast a bullet flies


		self.speed_mode = [0, 2, 2, 4]
		

		self.health = 2
		self.damage = 1
		self.tank_addition_to_bullet_speed = 4
		self.level_speed = 3
		self.gun_barrel_cooldown_time = 800
			
		self.speed = self.level_speed
		
#--Basic navigation variables:
		self.list_of_directions = ['go_right', 'go_left', 'go_up', 'go_down']
		self.till_random_turn = 100
#--Setting initial direction:
		self.direction = random.choices(self.list_of_directions)
		
#--SHOOTING--------------------------------------
		self.bullet_fire_time = 0
		self.charged = True
	#--Group or lasers together
		self.bullet_group = pygame.sprite.Group()
		
		
	def navigation(self):
#--Main objectives: change image position with self.position_list and move the rect with self.speed

		match self.direction[0]:
			case 'go_right':
				self.image = self.position_list[0]
				self.rect.x += self.speed
			case 'go_left':
				self.image = self.position_list[1]
				self.rect.x -= self.speed
			case 'go_up':
				self.image = self.position_list[2]
				self.rect.y -= self.speed
			case 'go_down':
				self.image = self.position_list[3]
				self.rect.y += self.speed

			
		if self.charged:
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
		self.current_x, self.current_y = self.rect.topleft
		if self.rect.left < 0: 
			self.rect.left = 0
			self.direction = random.choices(['go_right', 'go_up', 'go_down'])
		elif self.rect.right > self.width: 
			self.rect.right = self.width
			self.direction = random.choices(['go_left', 'go_up', 'go_down'])
		elif self.rect.bottom > self.height: 
			self.rect.bottom = self.height
			self.direction = random.choices(['go_right', 'go_left', 'go_down'])
		elif self.rect.top < 0: 
			self.rect.top = 0
			self.direction = random.choices(['go_right', 'go_left', 'go_up'])
		elif self.till_random_turn == 0:
			self.direction = random.choices(['go_right', 'go_left', 'go_up', 'go_down'])
			self.till_random_turn = 100
		
		
	def update(self):
		self.navigation()
		self.border_control()
		self.till_random_turn -= 1
		
		
		self.bullet_recharge()
		self.bullet_group.update()

		
class Ally_Big(Ally):
	def __init__(self, field_size, pos):
		super().__init__(field_size, pos)
		#--So that the tank does not run away
		self.width, self.height = field_size
#--self.image and self.rect are mandatory and will not work if misspelled (named differently)
#--Giving it appropriate image and rect:
		self.image = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Ally/ally2.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, (23, 23))
		#self.rect = self.image.get_rect(bottomleft=(self.width - TILE, 0))
		self.rect = self.image.get_rect(bottomleft=(pos))
		
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
#--Set level.Changing level will change some variables: speed, number of bullets, etc.
#--self.health = how many damage the tank can take before being destroyed
#--self.damage = how many damage it deals
#--self.tank_addition_to_bullet_speed = how fast a bullet flies
		self.speed_mode = [0, 2, 2, 4]
		
		self.health = 4
		self.damage = 99
		self.tank_addition_to_bullet_speed = 2
		self.level_speed = 2
		self.gun_barrel_cooldown_time = 1000
			
		self.speed = self.level_speed
		
#--Basic navigation variables:
		self.list_of_directions = ['go_right', 'go_left', 'go_up', 'go_down']
		self.till_random_turn = 100
#--Setting initial direction:
		self.direction = random.choices(self.list_of_directions)
		
#--SHOOTING--------------------------------------
		self.bullet_fire_time = 0
		self.charged = True
	#--Group or lasers together
		self.bullet_group = pygame.sprite.Group()
