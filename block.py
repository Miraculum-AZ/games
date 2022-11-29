# cmd /K python "$(FULL_CURRENT_PATH)"

# pip install pygame

import pygame
import sys
import random
 
# size of any object in this game (tank or block)
TILE = 32
#--Creating a tank:
class Block(pygame.sprite.Sprite):

	def __init__(self, field_size):
		super().__init__()

		block_types = [
			'block_bushes',
			'block_armor',
			'block_brick',
			'block_ice',
			'block_water',
			'block_sand'
			]
#--Using above list of options and random.choices I generate different blocks randomly
#--On weights: Probability = element_weight/ sum of all weights
		random_block = random.choices(block_types, weights=[1,2,3,1,1,1])
		
		self.width, self.height = field_size
#--self.image and self.rect are mandatory and will not work if misspelled (named differently)
		if random_block[0] == 'block_water':
			self.water_frame1 = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Blocks/block_water.png').convert_alpha()
			self.water_frame2 = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Blocks/block_water2.png').convert_alpha()
			self.water_frames = [self.water_frame1, self.water_frame2]
			self.frame_index = 0
			self.image = self.water_frames[self.frame_index]
		else:
			self.image = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/Blocks/' + random_block[0] + '.png').convert_alpha()
#--To cover the field properly I used topleft=, otherwise the first row will be partially uncovered as there's not enough space for it
		self.rect = self.image.get_rect(topleft=(random.randint(0, self.width// TILE)*TILE, random.randint(0, self.height // TILE)*TILE))

#--With defined type of the block, the block should get unique properties:
		self.block_type = random_block[0]
#--Define health system of different blocks:
		match self.block_type:
			case 'block_bushes': self.health = 0
			case 'block_armor': self.health = 99
			case 'block_brick': self.health = 2
			case 'block_ice': self.health = 0
			case 'block_water': self.health = 0
			case 'block_sand': self.health = 0
			

	def update(self): pass
		
#---------------------------------------------------BLOCK-NOTES----------------------------------------------------
#--Grass block: a player should be able to shoot through it and go under it. It does not affect anything. 
#--Ice block: a player should be able to shoot through it and go above it. While going above, it increases speed of a tank by n (optional value) -> may be randint
#--Water block: has 2 images, a player is not able to go through it (maybe able after reaching a certain level) but it able to shoot through it
#--Amor block: a player is not able to shoot through it and destroy it (give it a health of 999 or so) -> maybe with level update it can be destroyed. Not able to go through it
#--Brick block: easy to destroy (1hp) and not possible to go through it
