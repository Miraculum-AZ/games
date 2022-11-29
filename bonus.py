# cmd /K python "$(FULL_CURRENT_PATH)"

# pip install pygame

import pygame
import sys
import random
 
# size of any object in this game (tank or block)
TILE = 34

#--Creating eagle:
class Bonus(pygame.sprite.Sprite):

	def __init__(self, field_size):
		super().__init__()
		
		self.bonus_activation_time = 0
		
		self.list_of_bonuses = [
			'bonus_bomb',
			'bonus_helmet',
			'bonus_shovel',
			'bonus_star',
			'bonus_tank',
			'bonus_time',
			'bonus_ally'
			]
			
		self.random_bonus = random.choices(self.list_of_bonuses, weights=[1,1,2,1,1,1,1])
		self.selected_bonus = self.random_bonus[0]
		
		self.bonus_frame1 = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Bonus/' + self.selected_bonus + '.png').convert_alpha()
		self.bonus_frame2 = pygame.Surface((TILE,TILE), pygame.SRCALPHA)
		self.bonus_frames = [self.bonus_frame1, self.bonus_frame2]
		self.bonus_frame_index = 0
		self.destroy_frame_time_index = 0
		
		self.image = self.bonus_frames[self.bonus_frame_index]
		
#--Where the bonuses will be displayed:
		self.width, self.height = field_size
		
		self.rect = self.image.get_rect(topleft=(random.randint(0, self.width// TILE)*TILE, random.randint(0, self.height // TILE)*TILE))
		
		
		
	def update(self):
		self.destroy_frame_time_index += 0.02
		if self.destroy_frame_time_index >10: self.kill()
	
	def draw(self):
		return self.bonus_frames[int(self.bonus_frame_index)]
		
		
		
class Bonus_time(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		
		self.bonus_time_reference_time = 0
		self.bonus_type = ""