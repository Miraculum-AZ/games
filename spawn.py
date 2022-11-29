# cmd /K python "$(FULL_CURRENT_PATH)"

# pip install pygame

import pygame
import sys
import random
 
# size of any object in this game (tank or block)
TILE = 32

#--Creating eagle:
class Spawn(pygame.sprite.Sprite):

	def __init__(self, pos_x, pos_y):
		super().__init__()
		self.pos_x, self.pos_y = pos_x, pos_y
		
#--Creating a three-image sequence:		
		self.spawn1_org = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Spawn/spawn1.png').convert_alpha()
		self.spawn2_org = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Spawn/spawn2.png').convert_alpha()
		self.spawn3_org = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Spawn/spawn3.png').convert_alpha()
		self.spawn4_org = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Spawn/spawn4.png').convert_alpha()
		
		self.spawn1 = pygame.transform.scale(self.spawn1_org, (23,23))
		self.spawn2 = pygame.transform.scale(self.spawn2_org, (23,23))
		self.spawn3 = pygame.transform.scale(self.spawn3_org, (23,23))
		self.spawn4 = pygame.transform.scale(self.spawn4_org, (23,23))
		
		self.spawn_frames = [self.spawn1, self.spawn2, self.spawn3, self.spawn4, self.spawn1, self.spawn2, self.spawn3, self.spawn4]
		self.spawn_frame_index = 0
		self.image = self.spawn_frames[int(self.spawn_frame_index)]
#--Form to put an image above:
		self.rect = self.image.get_rect(bottomleft=(pos_x, pos_y))
		
		
	def update(self):
		self.spawn_frame_index += 0.09
		if self.spawn_frame_index >8: 
			self.kill()
			#self.spawn_frame_index = 0
		else: self.image = self.spawn_frames[int(self.spawn_frame_index)]
	
	def draw(self):
		return self.spawn_frames[int(self.spawn_frame_index)]
		
		
		