# cmd /K python "$(FULL_CURRENT_PATH)"

# pip install pygame

import pygame
import sys
import random
 
# size of any object in this game (tank or block)
TILE = 32

#--Creating eagle:
class Bang(pygame.sprite.Sprite):

	def __init__(self, pos_x, pos_y):
		super().__init__()
		self.pos_x, self.pos_y = pos_x, pos_y
		
#--Creating a three-image sequence:		
		self.bang1 = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Bang/bang1.png').convert_alpha()
		self.bang2 = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Bang/bang2.png').convert_alpha()
		self.bang3 = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Bang/bang3.png').convert_alpha()
		self.bang_frames = [self.bang1, self.bang2, self.bang3]
		self.bang_frame_index = 0
		self.image = self.bang_frames[int(self.bang_frame_index)]
#--Form to put an image above:
		self.rect = self.image.get_rect(center=(pos_x, pos_y))
		
		
	def update(self):
		self.bang_frame_index += 0.3
		if self.bang_frame_index >3: self.kill()
	
	def draw(self):
		return self.bang_frames[int(self.bang_frame_index)]
		
		
		