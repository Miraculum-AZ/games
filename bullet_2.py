# cmd /K python "$(FULL_CURRENT_PATH)"

# pip install pygame

import pygame
import sys
import random
 
# size of any object in this game (tank or block)
TILE = 32

#--Creating eagle:
class Bullet(pygame.sprite.Sprite):

	def __init__(self, position):
		super().__init__()
#--Where to find the bullet? Below:		
		self.bullet_image_path ='C:/Users/KOMAROVO/Desktop/Code here/Images/Bullet/bullet.png'
#--self.damage - damage dealt by a bullet
#--self.health - how much damage it can take before being destroyed
#--self.speed - speed of the bullet
		self.damage = 1
		self.health = 1
		self.speed = 6
		
		self.image = pygame.image.load(self.bullet_image_path).convert_alpha()
		self.rect = self.image.get_rect(center=(position))
#--Right - Left - Up - Down--	
		self.position_list = [
			pygame.transform.rotate(self.image, -90),
			pygame.transform.rotate(self.image, 90),
			pygame.transform.rotate(self.image, 0),
			pygame.transform.rotate(self.image, 180)
			]
	
	def change_bullet_position(self):
		if self.image == self.position_list[0] or self.image == pygame.image.load(self.bullet_image_path).convert_alpha(): self.rect.x += self.speed
		elif self.image == self.position_list[1]: self.rect.x -= self.speed
		elif self.image == self.position_list[2]: self.rect.y -= self.speed
		elif self.image == self.position_list[3]:	self.rect.y += self.speed

		
	def update(self):
		self.change_bullet_position()
		
		
		