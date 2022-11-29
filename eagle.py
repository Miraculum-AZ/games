# cmd /K python "$(FULL_CURRENT_PATH)"

# pip install pygame

import pygame
import sys
import random
 
# size of any object in this game (tank or block)
TILE = 32

#--Creating eagle:
class Eagle(pygame.sprite.Sprite):

	def __init__(self, field_size):
		super().__init__()
		
		self.health = 1
		self.max_health = 999
		self.init_health = 1
#--Creating a two-image sequence:		
		self.eagle_complete = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Eagle/eagle_complete.png').convert_alpha()
		self.eagle_destroyed = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Eagle/eagle_destroyed.png').convert_alpha()
		self.eagle_silver = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Eagle/eagle_silver.png').convert_alpha()
		self.eagle_frames = [self.eagle_complete, self.eagle_destroyed, self.eagle_silver]
		self.eagle_frame_index = 0
		self.image = self.eagle_frames[self.eagle_frame_index]
#--Form to put an image above:
		self.width, self.height = field_size
		self.rect = self.image.get_rect(bottomleft=(self.width // 2, self.height))
		
	def update(self):
		pass
		
		
		