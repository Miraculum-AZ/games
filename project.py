# cmd /K python "$(FULL_CURRENT_PATH)"
# python -i "$(FULL_CURRENT_PATH)"

# pip install pygame

#--Check block notes in block.py for characteristics of the blocks.

import pygame
import sys
import random

from tank import Tank
from tank_2 import Tank_2

from block import Block
from eagle import Eagle
from enemy import Enemy
from bang import Bang
from bonus import Bonus
from bonus import Bonus_time

from ally import Ally
from ally import Ally_Big
from spawn import Spawn

#----------------------------------------SETTINGS--------------------------------
unable_ice_blocks_under_other_blocks = True
unable_sand_blocks_under_other_blocks = False
using_second_player = True
game_start = False
#--------------------------------------------------------------------------------
class Game():
	def __init__(self, screen_width, screen_height):
	
		self.x = False
		self.y = False
	
#--Tracking the score:
		self.score = 0
		
		self.game_over_font = pygame.font.Font('C:/Users/KOMAROVO/Desktop/Code here/Images/Font/Pixeltype.ttf', 150)
		self.final_score_font = pygame.font.Font('C:/Users/KOMAROVO/Desktop/Code here/Images/Font/Pixeltype2.ttf', 100)
		
		self.game_over_surface = self.game_over_font.render('GAME OVER', False, (33,4,196))
		self.game_over_rect = self.game_over_surface.get_rect(center = (screen_width // 2, screen_height // 2))
	
		self.final_score_surface = self.final_score_font.render(f'Score: {self.score}', False, (68,50,168))
		self.final_score_rect = self.final_score_surface.get_rect(center = (screen_width // 2, screen_height // 2 + 130))
#--Outline:		
		self.game_over_font2 = pygame.font.Font('C:/Users/KOMAROVO/Desktop/Code here/Images/Font/Pixeltype.ttf', 155)
		self.game_over_surface2 = self.game_over_font2.render('GAME OVER', False, (245,245,245))
		self.game_over_rect2 = self.game_over_surface2.get_rect(center = (screen_width // 2, screen_height // 2))

		self.final_score_font2 = pygame.font.Font('C:/Users/KOMAROVO/Desktop/Code here/Images/Font/Pixeltype2.ttf', 105)
		self.final_score_surface2 = self.final_score_font2.render(f'Score: {self.score}', False, (245,245,245))
		self.final_score_rect2 = self.final_score_surface2.get_rect(center = (screen_width // 2, screen_height // 2 + 130))
	
		self.screen_width = screen_width
		self.screen_height = screen_height
		
		
		global player_sprite
		player_sprite = Tank((screen_width, screen_height))
		self.player_tank = pygame.sprite.GroupSingle(player_sprite)

#--Creating second player:
		if using_second_player == True:
			global player_sprite_2
			player_sprite_2 = Tank_2((screen_width, screen_height))
			self.player_tank_2 = pygame.sprite.GroupSingle(player_sprite_2)
		
		

#--Define variable for bonus duration:
		self.bonus_active_time = 6000
		
		self.enemy_stop = False
		
		self.blinking = False
		self.blinking_2 = False
		
		
		self.eagle_sprite = Eagle((screen_width, screen_height))
		self.eagle_group = pygame.sprite.GroupSingle(self.eagle_sprite)
		
#--Creating initial spawn of enemies:
		# group for initial enemies:
		self.enemy_initial_spawn_group = pygame.sprite.Group()
		# group for bangs:
		self.bang_group = pygame.sprite.Group()
		# group for spawns:
		self.spawn_group = pygame.sprite.Group()
		# group for bonuses:
		self.bonus_group = pygame.sprite.Group()
		self.bonus_group2 = pygame.sprite.Group()
		# self.bonus_group.add(self.bonus)
		# group for bonus_times
		self.bonus_time_group = pygame.sprite.Group()
		self.bonus_time_group2 = pygame.sprite.Group()
		# self.bonus_time_group.add(self.bonus_time_group)
		# group for allies:
		self.ally_group = pygame.sprite.Group()
		
#--Initial player spawn:
		
		
		if using_second_player == True:
			self.spawn = Spawn(self.screen_width // 2 - 35, self.screen_height)
			self.spawn_group.add(self.spawn)
		
		self.spawn = Spawn(self.screen_width // 2 + 35, self.screen_height)
		self.spawn_group.add(self.spawn)
#--Spawn zones:
		self.spawn_image1 = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/spawn.png').convert_alpha()
		self.spawn_rect1 = self.spawn_image1.get_rect(center=(0, 0))
		
		self.spawn_image2 = pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/spawn.png').convert_alpha()
		self.spawn_rect2 = self.spawn_image2.get_rect(center=(self.screen_width, 0))
		
		self.spawn_pos_list = [self.spawn_rect1, self.spawn_rect2]
		
		
#--Initial enemy spawn:
		
		for _ in range(2):
			self.enemy_sprite = Enemy((screen_width, screen_height), 400, 100)
			self.enemy_initial_spawn_group.add(self.enemy_sprite)
		
		
#--Initiate a list to store all blocks. This list will not be changed after creation (apart when blocks are destroyed)
#--Hence, we can run def run(self) function as many times as we want without overwriting blocks.
#--So that the blocks do not overlay, I used pygame.sprite.spritecollideany while appending them to the list.
#--If already in the list, then there'll be a collision
#--Additionally, we check whether newly created block collides with self.player_tank
		self.block_list = []
		self.ice_block_list = []
		self.sand_block_list = []
#--Above logic allows generation of ice blocks below other blocks, which can be either seen as a bug or as a feature
		for _ in range(200):
			while True:
				block_sprite = Block((screen_width, screen_height))
				block_found = False
				for block in self.block_list:
					for enemy in self.enemy_initial_spawn_group.sprites():
						if block_sprite.rect.colliderect(block) or block_sprite.rect.colliderect(player_sprite.rect) or block_sprite.rect.colliderect(player_sprite_2.rect) or block_sprite.rect.colliderect(self.eagle_sprite) or block_sprite.rect.colliderect(enemy.rect) or block_sprite.rect.colliderect(self.spawn_rect1) or block_sprite.rect.colliderect(self.spawn_rect2): block_found = True	
#--!!!--Fixing ice blocks generation under other blocks-------------------------------------->
				if unable_ice_blocks_under_other_blocks == False:
					for block in self.ice_block_list:
						if block_sprite.rect.colliderect(block): block_found = True
#<--------------------------------------------------------------------------------------------
#--!!!--Fixing sand blocks generation under other blocks------------------------------------->
				if unable_sand_blocks_under_other_blocks == False:
					for block in self.sand_block_list:
						if block_sprite.rect.colliderect(block): block_found = True
#<--------------------------------------------------------------------------------------------
#--So far sand block can be generated on top of ice blocks. Can be fixed but it's a very small bug
				if not block_found: break
			if block_sprite.block_type not in ['block_ice', 'block_sand']:
				self.block_list.append(block_sprite)
			elif block_sprite.block_type == 'block_sand': 
				self.sand_block_list.append(block_sprite)
			else: 
				self.ice_block_list.append(block_sprite)
		self.block_group = pygame.sprite.Group(self.block_list)
		self.ice_block_group = pygame.sprite.Group(self.ice_block_list)
		self.sand_block_group = pygame.sprite.Group(self.sand_block_list)

			
	
#--If our tank meets a block, it should not be able to surpass it.
#--current.x and current.y come from tank.py and store the most recent coordinates of the tank
	def check_collision(self):
		for block in self.block_group.sprites():
#--The only exception is grass block, we can move through it:
			if (pygame.sprite.groupcollide(self.player_tank, self.block_group, False, False) and player_sprite.rect.colliderect(block) and 
				block.block_type not in ['block_bushes']):
				player_sprite.rect.topleft = player_sprite.current_x, player_sprite.current_y
#--Coding ice blocks, so that the speed temporary increases:
		if pygame.sprite.groupcollide(self.player_tank, self.ice_block_group, False, False): 
			player_sprite.speed = player_sprite.speed_mode[3] + 1
#--Coding sand blocks, so that the speed temporary descreases:
		elif pygame.sprite.groupcollide(self.player_tank, self.sand_block_group, False, False):
			player_sprite.speed = 1
		else:
			player_sprite.speed = player_sprite.level_speed

			
#--We cannot overlap with the eagle:
		# if self.player_tank.sprite:
		# if pygame.sprite.groupcollide(self.player_tank, self.eagle_group, False, False):
			# player_sprite.rect.topleft = player_sprite.current_x, player_sprite.current_y

#--Collision between bullet and blocks:
		if self.player_tank.sprite:
			if self.player_tank.sprite.bullet_group:
				for bullet in self.player_tank.sprite.bullet_group:
					if pygame.sprite.spritecollide(bullet, self.block_group, False):
						for block in self.block_group.sprites():
							if bullet.rect.colliderect(block) and block.block_type in ['block_brick', 'block_armor']:
#--Explosion
								self.bang = Bang(bullet.rect.x, bullet.rect.y)
								self.bang_group.add(self.bang)
#---
								block.health -= (bullet.damage + self.player_tank.sprite.damage)
								bullet.health -= 1
								if block.health <= 0: block.kill()
								if bullet.health <= 0: bullet.kill()
								
#--Collision between player bullets and eagle:
		if self.player_tank.sprite:
			if self.player_tank.sprite.bullet_group:
				for bullet in self.player_tank.sprite.bullet_group:
					if pygame.sprite.spritecollide(bullet, self.eagle_group, False):
						self.bang = Bang(bullet.rect.x, bullet.rect.y)
						self.bang_group.add(self.bang)
						self.eagle_group.sprite.health -= 1
						bullet.health -= 1
						if self.eagle_group.sprite.health <= 0:
							self.eagle_group.sprite.image = self.eagle_group.sprite.eagle_frames[1]
						if bullet.health <= 0: bullet.kill()
					
#--Collision between player and bonus:
		if self.player_tank.sprite:
			for bonus in self.bonus_group:
				if bonus.rect.colliderect(player_sprite.rect):
					self.score += 100
					if bonus.selected_bonus == 'bonus_star':
						self.player_tank.sprite.level += 1
						self.player_tank.sprite.player_tank_level_check()
						print(f"Your current level is {self.player_tank.sprite.level}")
					elif bonus.selected_bonus == 'bonus_tank':
						self.player_tank.sprite.lives += 1
						print(f'You have {self.player_tank.sprite.lives} live(s) left')
						print(f'You have {self.player_tank.sprite.health} hp(s) left')
					elif bonus.selected_bonus == 'bonus_bomb':
						for enemy in self.enemy_initial_spawn_group.sprites():
							self.bang = Bang(enemy.rect.x, enemy.rect.y)
							self.bang_group.add(self.bang)
							enemy.kill()
					elif bonus.selected_bonus == 'bonus_time':
						bonus.bonus_activation_time = pygame.time.get_ticks()
					#--Before bonus dies, it should pass the time and type to Bonus_time group:
						self.bonus_time = Bonus_time()
						self.bonus_time.bonus_time_reference_time = bonus.bonus_activation_time
						self.bonus_time.bonus_type = bonus.selected_bonus
						self.bonus_time_group.add(self.bonus_time)
					elif bonus.selected_bonus == 'bonus_shovel':
						bonus.bonus_activation_time = pygame.time.get_ticks()
						self.bonus_time = Bonus_time()
						self.bonus_time.bonus_time_reference_time = bonus.bonus_activation_time
						self.bonus_time.bonus_type = bonus.selected_bonus
						self.bonus_time_group.add(self.bonus_time)
						self.eagle_group.sprite.init_health += 1
						
					elif bonus.selected_bonus == 'bonus_helmet':
						bonus.bonus_activation_time = pygame.time.get_ticks()
						self.bonus_time = Bonus_time()
						self.bonus_time.bonus_time_reference_time = bonus.bonus_activation_time
						self.bonus_time.bonus_type = bonus.selected_bonus
						self.bonus_time_group.add(self.bonus_time)
						
					elif bonus.selected_bonus == 'bonus_ally':
#--Ally is generated at player's position:
						self.ally = Ally((self.screen_width, self.screen_height),(self.player_tank.sprite.rect.x, self.player_tank.sprite.rect.y))
						self.ally_group.add(self.ally)
						

					bonus.kill()
					print("Bonus consumed")
					
#--Function to check whether a bonus is active:
	def bonus_in_action(self):
		if self.player_tank:
			for bonus_time in self.bonus_time_group:
				self.bonus_current_time = pygame.time.get_ticks()
				if self.bonus_current_time - bonus_time.bonus_time_reference_time > self.bonus_active_time and self.bonus_time.bonus_type == 'bonus_time':
					#Bonus stops working
					self.enemy_stop = False
					bonus_time.kill()
				elif self.bonus_current_time - bonus_time.bonus_time_reference_time <= self.bonus_active_time and self.bonus_time.bonus_type == 'bonus_time':
					#Bonus works:
					self.enemy_stop = True
					for enemy in self.enemy_initial_spawn_group:
								# enemy.speed = 0
						for bullet in enemy.bullet_group:
							bullet.kill()			
				elif self.bonus_current_time - bonus_time.bonus_time_reference_time <= self.bonus_active_time and self.bonus_time.bonus_type == 'bonus_shovel':
					self.eagle_group.sprite.image = self.eagle_group.sprite.eagle_frames[2]
					self.eagle_group.sprite.health = self.eagle_group.sprite.max_health
				elif self.bonus_current_time - bonus_time.bonus_time_reference_time > self.bonus_active_time and self.bonus_time.bonus_type == 'bonus_shovel':
					self.eagle_group.sprite.image = self.eagle_group.sprite.eagle_frames[0]
					self.eagle_group.sprite.health = self.eagle_group.sprite.init_health
					bonus_time.kill()
				
				elif self.bonus_current_time - bonus_time.bonus_time_reference_time <= self.bonus_active_time and self.bonus_time.bonus_type == 'bonus_helmet':
					self.player_tank.sprite.health = self.player_tank.sprite.max_health
					self.blinking = True
				elif self.bonus_current_time - bonus_time.bonus_time_reference_time > self.bonus_active_time and self.bonus_time.bonus_type == 'bonus_helmet':
					self.player_tank.sprite.player_tank_level_check()
					self.blinking = False
					bonus_time.kill()
				
				else: pass
				
#--Bullets, which leave the screen shall be destroyed not to overload memory			
	def destroy_bullets(self):
		if self.player_tank.sprite:
			for bullet in self.player_tank.sprite.bullet_group:
				if bullet.rect.left <= 5: 
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()
				elif bullet.rect.right > self.screen_width:
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)			
					bullet.kill()
				elif bullet.rect.bottom > self.screen_height: 
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()
				elif bullet.rect.top < 0: 
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()

				
				
#-----------------------------------------------------ENEMY_TANK_PART---------------------------------------------
#--If enemy tank meets a block, it should not be able to surpass it.
#--current.x and current.y come from enemy.py and store the most recent coordinates of the tank
	def check_collision_enemy(self):
		for block in self.block_group.sprites():
			for enemy in self.enemy_initial_spawn_group.sprites():
#--The only exception is grass block, we can move through it:
				if (enemy.rect.colliderect(block) and 
					block.block_type not in ['block_bushes']):
					match enemy.direction[0]:
						case 'go_right': 
							enemy.rect.x -= 5
							enemy.direction[0] = random.choice(['go_left', 'go_up', 'go_down'])
						case 'go_left': 
							enemy.rect.x += 5
							enemy.direction[0] = random.choice(['go_right', 'go_up', 'go_down'])
						case 'go_up': 
							enemy.rect.y += 5
							enemy.direction[0] = random.choice(['go_right', 'go_left', 'go_down'])
						case 'go_down': 
							enemy.rect.y -= 5
							enemy.direction[0] = random.choice(['go_right', 'go_left', 'go_up'])
							
#--Coding ice blocks, so that the speed temporary increases:			
		for enemy in self.enemy_initial_spawn_group.sprites():
			if pygame.sprite.groupcollide(self.enemy_initial_spawn_group, self.ice_block_group, False, False): 
				for block in self.ice_block_group.sprites():
					if enemy.rect.colliderect(block):
						enemy.speed = enemy.speed_mode[3] + 1
#--Coding sand blocks, so that the speed temporary decreases:
			elif pygame.sprite.groupcollide(self.enemy_initial_spawn_group, self.sand_block_group, False, False):
				for block in self.sand_block_group.sprites():
					if enemy.rect.colliderect(block):
						enemy.speed = 1
			elif self.enemy_stop == True:
				enemy.speed = 0
			else:
				enemy.speed = enemy.level_speed	
				
				
	
#--Collision between enemy bullet and blocks:
		for enemy in self.enemy_initial_spawn_group.sprites():
			if enemy.bullet_group:
				for bullet in enemy.bullet_group:
					if pygame.sprite.spritecollide(bullet, self.block_group, False):
						for block in self.block_group.sprites():
							if bullet.rect.colliderect(block) and block.block_type in ['block_brick', 'block_armor']:
#--Explosion
								self.bang = Bang(bullet.rect.x, bullet.rect.y)
								self.bang_group.add(self.bang)
#---
								block.health -= (bullet.damage + enemy.damage)
								bullet.health -= 1
								if block.health <= 0: block.kill()
								if bullet.health <= 0: bullet.kill()
								
#--Collision between player bullet and enemy bullet:
		if self.player_tank.sprite:
			for enemy in self.enemy_initial_spawn_group.sprites():
				pygame.sprite.groupcollide(enemy.bullet_group, self.player_tank.sprite.bullet_group, True, True)


#--Collision between player bullet and enemy tank:
		if self.player_tank.sprite:
			for enemy in self.enemy_initial_spawn_group.sprites():
				for bullet in self.player_tank.sprite.bullet_group:
					if bullet.rect.colliderect(enemy):
						self.bang = Bang(bullet.rect.x, bullet.rect.y)
						self.bang_group.add(self.bang)
						bullet.health -= 1
						enemy.health -= 1
						if bullet.health <= 0: bullet.kill()
						if enemy.health <= 0:
							match enemy.random_tank_enemy[0]:
								case 'tank_basic': self.score += 100
								case 'tank_fast': self.score += 200
								case 'tank_power': self.score += 300
								case 'tank_armor': self.score += 400
							enemy.kill()
						
#--Collision between enemy bullet and player tank:
		if self.player_tank.sprite:
			for enemy in self.enemy_initial_spawn_group.sprites():
				if enemy.bullet_group:
					for bullet in enemy.bullet_group:
						if bullet.rect.colliderect(self.player_tank.sprite.rect): #and self.player_tank.sprite.rect != None:
							bullet.health -= 1
							self.player_tank.sprite.health -= 1
							if bullet.health <= 0: bullet.kill()
							if self.player_tank.sprite.health <= 0: 
								self.player_tank.sprite.lives -= 1
								print(f'You have {self.player_tank.sprite.lives} live(s) left')
								print(f'You have {self.player_tank.sprite.health} hp(s) left')
								self.player_tank.sprite.level = 1
								self.player_tank.sprite.player_tank_level_check()
								
								print(f"Your current level is {self.player_tank.sprite.level}")
								if self.player_tank.sprite.lives <= 0:
									for bullet in self.player_tank.sprite.bullet_group:
										bullet.kill()
									#self.player_tank.sprite.kill()
									self.player_tank.sprite.speed = 0
									#self.player_tank.image = pygame.transform.scale(pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/spawn.png').convert_alpha(), (23, 23))
									self.player_tank.sprite.rect =self.player_tank.sprite.image.get_rect(bottomleft=(self.screen_width +100, self.screen_height))
									self.x = True
									print(self.player_tank.sprite.rect)
								else:	
	#--Spawn is finally working:
									self.spawn = Spawn(self.screen_width // 2 + 35, self.screen_height)
									self.spawn_group.add(self.spawn)
									self.player_tank.sprite.rect =self.player_tank.sprite.image.get_rect(bottomleft=(self.screen_width // 2 + 35, self.screen_height))  
							
#--Bullets, which leave the screen shall be destroyed not to overload memory			
	def destroy_bullets_enemy(self):
		for enemy in self.enemy_initial_spawn_group.sprites():
			for bullet in enemy.bullet_group:
				if bullet.rect.left < 0: 
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()
				elif bullet.rect.right > self.screen_width: 
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()
				elif bullet.rect.bottom > self.screen_height:
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()
				elif bullet.rect.top < 0: 
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()

#-------------------------------------------------------------------------------------------------------------					
#---------------------------------------------------------ALLY_PART-------------------------------------------
#-------------------------------------------------------------------------------------------------------------
	def check_collision_ally(self):
		for block in self.block_group.sprites():
			for ally in self.ally_group.sprites():
#--The only exception is grass block, we can move through it:
				if (ally.rect.colliderect(block) and 
					block.block_type not in ['block_bushes']):
					match ally.direction[0]:
						case 'go_right': 
							ally.rect.x -= 5
							ally.direction[0] = random.choice(['go_left', 'go_up', 'go_down'])
						case 'go_left': 
							ally.rect.x += 5
							ally.direction[0] = random.choice(['go_right', 'go_up', 'go_down'])
						case 'go_up': 
							ally.rect.y += 5
							ally.direction[0] = random.choice(['go_right', 'go_left', 'go_down'])
						case 'go_down': 
							ally.rect.y -= 5
							ally.direction[0] = random.choice(['go_right', 'go_left', 'go_up'])
		#--Coding ice blocks, so that the speed temporary increases:			
		for ally in self.ally_group.sprites():
			if pygame.sprite.groupcollide(self.ally_group, self.ice_block_group, False, False): 
				for block in self.ice_block_group.sprites():
					if ally.rect.colliderect(block):
						ally.speed = ally.speed_mode[3] + 1
#--Coding sand blocks, so that the speed temporary decreases:
			elif pygame.sprite.groupcollide(self.ally_group, self.sand_block_group, False, False):
				for block in self.sand_block_group.sprites():
					if ally.rect.colliderect(block):
						ally.speed = 1
			else:
				ally.speed = ally.level_speed

				
#--Collision between bullet and blocks:
		for ally in self.ally_group.sprites():
			if ally.bullet_group:
				for bullet in ally.bullet_group:
					if pygame.sprite.spritecollide(bullet, self.block_group, False):
						for block in self.block_group.sprites():
							if bullet.rect.colliderect(block) and block.block_type in ['block_brick', 'block_armor']:
#--Explosion
								self.bang = Bang(bullet.rect.x, bullet.rect.y)
								self.bang_group.add(self.bang)
#---
								block.health -= (bullet.damage + ally.damage)
								bullet.health -= 1
								if block.health <= 0: block.kill()
								if bullet.health <= 0: bullet.kill()
								
								
#--Collision between ally bullet and player tank:
		if self.player_tank.sprite:
			for ally in self.ally_group.sprites():
				if ally.bullet_group:
					for bullet in ally.bullet_group:
						if bullet.rect.colliderect(self.player_tank.sprite.rect):
							bullet.health -= 1
							self.bang = Bang(bullet.rect.x, bullet.rect.y)
							self.bang_group.add(self.bang)
							if bullet.health <= 0: bullet.kill()
							
#--Collision between ally bullet and enemy tank:							
		for ally in self.ally_group.sprites():
			for bullet in ally.bullet_group:
				for enemy in self.enemy_initial_spawn_group.sprites():
					if bullet.rect.colliderect(enemy):
						self.bang = Bang(bullet.rect.x, bullet.rect.y)
						self.bang_group.add(self.bang)
						bullet.health -= 1
						enemy.health -= ally.damage
						if bullet.health <= 0: bullet.kill()
						if enemy.health <= 0: 
							self.score += 500
							print("Enemy tank destroyed by ally!")
							enemy.kill()

#--Collision between ally bullet and player bullet:
		if self.player_tank.sprite:
			for ally in self.ally_group.sprites():
				pygame.sprite.groupcollide(ally.bullet_group, self.player_tank.sprite.bullet_group, True, True)				
				
				
#--Collision between ally bullet and enemy bullet:
		for ally in self.ally_group.sprites():
			for enemy in self.enemy_initial_spawn_group.sprites():
				pygame.sprite.groupcollide(ally.bullet_group, enemy.bullet_group, True, True)	


#--Collision between ally tank and player bullet:
		if self.player_tank.sprite:
			for ally in self.ally_group.sprites():
				for bullet in self.player_tank.sprite.bullet_group:
					if bullet.rect.colliderect(ally):
						bullet.health -= 1
						self.bang = Bang(bullet.rect.x, bullet.rect.y)
						self.bang_group.add(self.bang)
						if bullet.health <= 0: bullet.kill()			

#--Collision betwee ally tank and enemy bullet:	
		for ally in self.ally_group.sprites():
			for enemy in self.enemy_initial_spawn_group.sprites():
				for bullet in enemy.bullet_group:
					if bullet.rect.colliderect(ally):
						bullet.health -= 1
						self.bang = Bang(bullet.rect.x, bullet.rect.y)
						self.bang_group.add(self.bang)
						ally.health -= enemy.damage
						if bullet.health <= 0: bullet.kill()
						if ally.health <= 0: ally.kill()
						
		#--Collision between ally and bonus:
		for ally in self.ally_group:
			for bonus in self.bonus_group:
				if bonus.rect.colliderect(ally.rect):
					self.score += 50
					if bonus.selected_bonus == 'bonus_bomb':
						for enemy in self.enemy_initial_spawn_group.sprites():
							self.bang = Bang(enemy.rect.x, enemy.rect.y)
							self.bang_group.add(self.bang)
							enemy.kill()
							
					elif bonus.selected_bonus == 'bonus_time':
						bonus.bonus_activation_time = pygame.time.get_ticks()
					#--Before bonus dies, it should pass the time and type to Bonus_time group:
						self.bonus_time = Bonus_time()
						self.bonus_time.bonus_time_reference_time = bonus.bonus_activation_time
						self.bonus_time.bonus_type = bonus.selected_bonus
						self.bonus_time_group.add(self.bonus_time)
						
					elif bonus.selected_bonus == 'bonus_shovel':
						bonus.bonus_activation_time = pygame.time.get_ticks()
						self.bonus_time = Bonus_time()
						self.bonus_time.bonus_time_reference_time = bonus.bonus_activation_time
						self.bonus_time.bonus_type = bonus.selected_bonus
						self.bonus_time_group.add(self.bonus_time)
						self.eagle_group.sprite.init_health += 1
						
					elif bonus.selected_bonus == 'bonus_ally':
#--Ally is generated at player's position:
						self.ally = Ally_Big((self.screen_width, self.screen_height),(ally.rect.x, ally.rect.y))
						self.ally_group.add(self.ally)
		
					bonus.kill()
					print("Bonus consumed by ally")
				

#--Bullets, which leave the screen shall be destroyed not to overload memory			
	def destroy_bullets_ally(self):
		for ally in self.ally_group.sprites():
			for bullet in ally.bullet_group:
				if bullet.rect.left < 0: 
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()
				elif bullet.rect.right > self.screen_width: 
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()
				elif bullet.rect.bottom > self.screen_height:
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()
				elif bullet.rect.top < 0: 
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()

#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------	
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------SECOND_PLAYER_PART------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#--If our tank meets a block, it should not be able to surpass it.
#--current.x and current.y come from tank.py and store the most recent coordinates of the tank
	def check_collision_second_player(self):
		if self.player_tank_2.sprite:
			for block in self.block_group.sprites():
	#--The only exception is grass block, we can move through it:
				if (pygame.sprite.groupcollide(self.player_tank_2, self.block_group, False, False) and player_sprite_2.rect.colliderect(block) and 
					block.block_type not in ['block_bushes']):
					player_sprite_2.rect.topleft = player_sprite_2.current_x, player_sprite_2.current_y
	#--Coding ice blocks, so that the speed temporary increases:
			if pygame.sprite.groupcollide(self.player_tank_2, self.ice_block_group, False, False): 
				player_sprite_2.speed = player_sprite_2.speed_mode[3] + 1
	#--Coding sand blocks, so that the speed temporary descreases:
			elif pygame.sprite.groupcollide(self.player_tank_2, self.sand_block_group, False, False):
				player_sprite_2.speed = 1
			else:
				player_sprite_2.speed = player_sprite_2.level_speed

			
#--We cannot overlap with the eagle:
		# if self.player_tank_2.sprite:
			# if pygame.sprite.groupcollide(self.player_tank_2, self.eagle_group, False, False):
				# player_sprite_2.rect.topleft = player_sprite_2.current_x, player_sprite_2.current_y

#--Collision between second player bullet and blocks:
		if self.player_tank_2.sprite:
			if self.player_tank_2.sprite.bullet_group:
				for bullet in self.player_tank_2.sprite.bullet_group:
					if pygame.sprite.spritecollide(bullet, self.block_group, False):
						for block in self.block_group.sprites():
							if bullet.rect.colliderect(block) and block.block_type in ['block_brick', 'block_armor']:
#--Explosion
								self.bang = Bang(bullet.rect.x, bullet.rect.y)
								self.bang_group.add(self.bang)
#---
								block.health -= (bullet.damage + self.player_tank_2.sprite.damage)
								bullet.health -= 1
								if block.health <= 0: block.kill()
								if bullet.health <= 0: bullet.kill()
								
#--Collision between second player bullets and eagle:
		if self.player_tank_2.sprite:
			if self.player_tank_2.sprite.bullet_group:
				for bullet in self.player_tank_2.sprite.bullet_group:
					if pygame.sprite.spritecollide(bullet, self.eagle_group, False):
						self.bang = Bang(bullet.rect.x, bullet.rect.y)
						self.bang_group.add(self.bang)
						self.eagle_group.sprite.health -= 1
						bullet.health -= 1
						if self.eagle_group.sprite.health <= 0:
							self.eagle_group.sprite.image = self.eagle_group.sprite.eagle_frames[1]
						if bullet.health <= 0: bullet.kill()
						
#--Collision between second player bullet and enemy tank:
		if self.player_tank_2.sprite:
			for bullet in self.player_tank_2.sprite.bullet_group:
				for enemy in self.enemy_initial_spawn_group.sprites():
					if bullet.rect.colliderect(enemy):
						self.bang = Bang(bullet.rect.x, bullet.rect.y)
						self.bang_group.add(self.bang)
						bullet.health -= 1
						enemy.health -= self.player_tank_2.sprite.damage
						if bullet.health <= 0: bullet.kill()
						if enemy.health <= 0: 
							match enemy.random_tank_enemy[0]:
								case 'tank_basic': self.score += 100
								case 'tank_fast': self.score += 200
								case 'tank_power': self.score += 300
								case 'tank_armor': self.score += 400
							enemy.kill()
						
#--Collision between second player tank and enemy bullet:
		if self.player_tank_2.sprite:
			for enemy in self.enemy_initial_spawn_group.sprites():
				if enemy.bullet_group:
					for bullet in enemy.bullet_group:
						if bullet.rect.colliderect(self.player_tank_2.sprite.rect):
						
							self.bang = Bang(bullet.rect.x, bullet.rect.y)
							self.bang_group.add(self.bang)
							
							bullet.health -= 1
							self.player_tank_2.sprite.health -= 1
							if bullet.health <= 0: bullet.kill()
							if self.player_tank_2.sprite.health <= 0: 
								self.player_tank_2.sprite.lives -= 1
								print(f'You have {self.player_tank_2.sprite.lives} live(s) left')
								print(f'You have {self.player_tank_2.sprite.health} hp(s) left')
								self.player_tank_2.sprite.level = 1
								self.player_tank_2.sprite.player_tank_level_check()
								
								print(f"Your current level is {self.player_tank_2.sprite.level}")
								if self.player_tank_2.sprite.lives <= 0:
									for bullet in self.player_tank_2.sprite.bullet_group:
										bullet.kill()
									#self.player_tank_2.sprite.kill()
									self.player_tank_2.sprite.speed = 0
									#self.player_tank_2.image = pygame.transform.scale(pygame.image.load('C:/Users/KOMAROVO/Desktop/Code here/Images/spawn.png').convert_alpha(), (23, 23))
									self.player_tank_2.sprite.rect =self.player_tank_2.sprite.image.get_rect(bottomleft=(self.screen_width +100, self.screen_height))
									self.y = True
									print(self.player_tank_2.sprite.rect)
									
								else:	
	#--Spawn is finally working:
									self.spawn = Spawn(self.screen_width // 2 - 35, self.screen_height)
									self.spawn_group.add(self.spawn)
									self.player_tank_2.sprite.rect =self.player_tank_2.sprite.image.get_rect(bottomleft=(self.screen_width // 2 - 35, self.screen_height))  
					
#--Collision between second player and bonus:
		if self.player_tank_2.sprite:
			for bonus in self.bonus_group:
				if bonus.rect.colliderect(player_sprite_2.rect):
					self.score += 100
					if bonus.selected_bonus == 'bonus_star':
						self.player_tank_2.sprite.level += 1
						self.player_tank_2.sprite.player_tank_level_check()
						print(f"Your current level is {self.player_tank_2.sprite.level}")
					elif bonus.selected_bonus == 'bonus_tank':
						self.player_tank_2.sprite.lives += 1
						print(f'You have {self.player_tank_2.sprite.lives} live(s) left')
						print(f'You have {self.player_tank_2.sprite.health} hp(s) left')
					elif bonus.selected_bonus == 'bonus_bomb':
						for enemy in self.enemy_initial_spawn_group.sprites():
							self.bang = Bang(enemy.rect.x, enemy.rect.y)
							self.bang_group.add(self.bang)
							enemy.kill()
					elif bonus.selected_bonus == 'bonus_time':
						bonus.bonus_activation_time = pygame.time.get_ticks()
					#--Before bonus dies, it should pass the time and type to Bonus_time group:
						self.bonus_time = Bonus_time()
						self.bonus_time.bonus_time_reference_time = bonus.bonus_activation_time
						self.bonus_time.bonus_type = bonus.selected_bonus
						self.bonus_time_group.add(self.bonus_time)
					elif bonus.selected_bonus == 'bonus_shovel':
						bonus.bonus_activation_time = pygame.time.get_ticks()
						self.bonus_time = Bonus_time()
						self.bonus_time.bonus_time_reference_time = bonus.bonus_activation_time
						self.bonus_time.bonus_type = bonus.selected_bonus
						self.bonus_time_group.add(self.bonus_time)
						self.eagle_group.sprite.init_health += 1
						
					elif bonus.selected_bonus == 'bonus_helmet':
						bonus.bonus_activation_time = pygame.time.get_ticks()
						self.bonus_time = Bonus_time()
						self.bonus_time.bonus_time_reference_time = bonus.bonus_activation_time
						self.bonus_time.bonus_type = bonus.selected_bonus
						self.bonus_time_group.add(self.bonus_time)
						
					elif bonus.selected_bonus == 'bonus_ally':
#--Ally is generated at player's position:
						self.ally = Ally((self.screen_width, self.screen_height),(self.player_tank_2.sprite.rect.x, self.player_tank_2.sprite.rect.y))
						self.ally_group.add(self.ally)
						

					bonus.kill()
					print("Bonus consumed")
					
#--Function to check whether a bonus is active:
#--Redundant function seems to be not needed.
	def bonus_in_action_2(self):
		pass
		
				
#--Bullets, which leave the screen shall be destroyed not to overload memory			
	def destroy_bullets_2(self):
		if self.player_tank_2.sprite:
			for bullet in self.player_tank_2.sprite.bullet_group:
				if bullet.rect.left <= 5: 
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()
				elif bullet.rect.right > self.screen_width:
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)			
					bullet.kill()
				elif bullet.rect.bottom > self.screen_height: 
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()
				elif bullet.rect.top < 0: 
					self.bang = Bang(bullet.rect.x, bullet.rect.y)
					self.bang_group.add(self.bang)
					bullet.kill()
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------


	def create_bonus(self):
		self.bonus = Bonus((self.screen_width, self.screen_height))
		self.bonus_group.add(self.bonus)
		

	
				

		
	def run(self):
		self.ice_block_group.draw(screen)
		self.sand_block_group.draw(screen)
		
		if self.player_tank.sprite:
			self.player_tank.draw(screen)
			self.player_tank.update()
			
			self.check_collision()
			self.destroy_bullets()
			
		self.destroy_bullets_enemy()
		self.destroy_bullets_ally()
		
		if using_second_player == True:
			if self.player_tank_2.sprite:
				self.player_tank_2.draw(screen)
				self.player_tank_2.update()
				self.check_collision_second_player()
				self.destroy_bullets_2()
		
		self.eagle_group.draw(screen)
		
		if self.player_tank.sprite:
			self.player_tank.sprite.bullet_group.draw(screen)
			
		if using_second_player == True:
			if self.player_tank_2.sprite:
				self.player_tank_2.sprite.bullet_group.draw(screen)
		
#--Drawing allies:
		self.ally_group.draw(screen)
		self.check_collision_ally()
		self.ally_group.update()
		
		for ally in self.ally_group.sprites():
			ally.bullet_group.draw(screen)
#-----------------		
		self.enemy_initial_spawn_group.draw(screen)
		self.check_collision_enemy()
		self.enemy_initial_spawn_group.update()
		
		for enemy in self.enemy_initial_spawn_group.sprites():
			enemy.bullet_group.draw(screen)
		
		self.block_group.draw(screen)
		
		for bang in self.bang_group:
			screen.blit(self.bang.draw(), self.bang.rect)
			bang.update()
			
		# self.check_spawn()	
		
		for spawn in self.spawn_group:
			screen.blit(self.spawn.image, self.spawn.rect)
			spawn.update()
			
			
		self.bonus_group.draw(screen)	
		for bonus in self.bonus_group:
			bonus.update()
		
		self.bonus_in_action()
		
		if using_second_player == True: 
			self.bonus_in_action_2()
		
		if self.blinking == True:
			screen.blit(self.player_tank.sprite.shield_image, self.player_tank.sprite.shield_rect)
			
		if using_second_player == True: 	
			if self.blinking_2 == True:
				screen.blit(self.player_tank_2.sprite.shield_image, self.player_tank_2.sprite.shield_rect)
		
		if self.x == True and self.y == True:
		#if self.player_tank.sprite.rect.x == 900 and self.player_tank_2.sprite.rect.x == 900: #and self.player_tank.sprite.speed == 0 and self.player_tank_2.sprite.speed == 0:
			screen.blit(self.game_over_surface2, self.game_over_rect2)
			screen.blit(self.game_over_surface, self.game_over_rect)
			screen.blit(self.final_score_font.render(f'Score: {self.score}', False, (245,245,245)), self.final_score_rect2)
			screen.blit(self.final_score_font.render(f'Score: {self.score}', False, (33,4,196)), self.final_score_rect)
		



if __name__ == "__main__":
	#--Starting the game:
	pygame.init()
	screen_width = 800
	screen_height = 400
	screen = pygame.display.set_mode((screen_width,screen_height))
	clock = pygame.time.Clock()
	game = Game(screen_width, screen_height)
#--Timers:
	water_animation_timer = pygame.USEREVENT + 1
	pygame.time.set_timer(water_animation_timer, 300)
	
	bonus_creation_timer = pygame.USEREVENT + 2
	pygame.time.set_timer(bonus_creation_timer, random.randint(7000, 18000))
	
	bonus_animation_timer = pygame.USEREVENT + 3
	pygame.time.set_timer(bonus_animation_timer, 300)
	
#--Make it very depending on the difficulty:
	enemy_creation_timer = pygame.USEREVENT + 4
	pygame.time.set_timer(enemy_creation_timer, random.randint(7000, 18000))
	
	block_creation_timer = pygame.USEREVENT + 5
	pygame.time.set_timer(block_creation_timer, random.randint(5000, 8000))
	
	shield_animation_timer = pygame.USEREVENT + 6
	pygame.time.set_timer(shield_animation_timer, 300)
	
	shield_animation_timer_2 = pygame.USEREVENT + 7
	pygame.time.set_timer(shield_animation_timer_2, 300)
	

	#game_active = True


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit("Closing the game")
#--Water animation timer:			
			if event.type == water_animation_timer:
				for block in game.block_group.sprites():
					if block.block_type == 'block_water':
						if block.frame_index == 0: block.frame_index = 1
						else: block.frame_index = 0
						block.image = block.water_frames[block.frame_index]
#---
#--Bonus creation timer:						
			if event.type == bonus_creation_timer and game.eagle_group.sprite.health > 0:
				game.create_bonus()
#---
#--Bonus animation timer:						
			if event.type == bonus_animation_timer:
				for bonus in game.bonus_group.sprites():
					if bonus.bonus_frame_index == 0: bonus.bonus_frame_index = 1
					else: bonus.bonus_frame_index = 0
					bonus.image = bonus.bonus_frames[bonus.bonus_frame_index]
#---
#--Enemy creation timer:					
			if event.type == enemy_creation_timer:
				random_x = random.choices([0, screen_width])
				random_y = random.choices([0,0])
				print(random_x, random_y)
				game.enemy_sprite = Enemy((screen_width, screen_height), random_x[0], random_y[0])
				game.enemy_initial_spawn_group.add(game.enemy_sprite)
				game.spawn = Spawn(random_x[0], random_y[0])
				game.spawn_group.add(game.spawn)
#---
#--Block creation timer:
			if event.type == block_creation_timer:
				for _ in range(1):
					while True:
						block_sprite = Block((screen_width, screen_height))
						block_found_2 = False
						for block in game.block_group.sprites():
							for enemy in game.enemy_initial_spawn_group.sprites():
								if game.player_tank and game.player_tank_2:
									if block_sprite.rect.colliderect(block) or block_sprite.rect.colliderect(game.player_tank.sprite.rect) or block_sprite.rect.colliderect(game.player_tank_2.sprite.rect) or block_sprite.rect.colliderect(game.eagle_sprite) or block_sprite.rect.colliderect(enemy.rect) or block_sprite.rect.colliderect(game.spawn_rect1) or block_sprite.rect.colliderect(game.spawn_rect2) or block_sprite.block_type != 'block_brick': block_found_2 = True	

						if not block_found_2: break
					print(block_sprite.block_type)
					if block_sprite.block_type == 'block_brick':
						game.block_group.add(block_sprite)
					else: pass

#---
#--Shield animation timer:
			if event.type == shield_animation_timer and game.blinking == True:
				if game.player_tank.sprite.shield_index == 0:
					game.player_tank.sprite.shield_index = 1
				else:
					game.player_tank.sprite.shield_index = 0
				game.player_tank.sprite.shield_image = game.player_tank.sprite.shield_frames[game.player_tank.sprite.shield_index]
				
#---				
#--Shield animation timer_2:
			if event.type == shield_animation_timer_2 and game.blinking == True:
				if game.player_tank_2.sprite.shield_index == 0:
					game.player_tank_2.sprite.shield_index = 1
				else:
					game.player_tank_2.sprite.shield_index = 0
				game.player_tank_2.sprite.shield_image = game.player_tank_2.sprite.shield_frames[game.player_tank_2.sprite.shield_index]
#---			
			

			
		screen.fill((30,30,30))
		
		if game_start == True:
			game.run()
		else: 
			game_start_font = pygame.font.Font('C:/Users/KOMAROVO/Desktop/Code here/Images/Font/Pixeltype.ttf', 155)
			game_start_surface = game_start_font.render('PRESS ENTER', False, (33,4,196))
			game_start_rect = game_start_surface.get_rect(center = (screen_width // 2, screen_height // 2))
			keys = pygame.key.get_pressed()
			
			
			game_start_font2 = pygame.font.Font('C:/Users/KOMAROVO/Desktop/Code here/Images/Font/Pixeltype.ttf', 158)
			game_start_surface2 = game_start_font2.render('PRESS ENTER', False, (245,245,245))
			game_start_rect2 = game_start_surface2.get_rect(center = (screen_width // 2, screen_height // 2))
			
			screen.blit(game_start_surface2, game_start_rect2)
			screen.blit(game_start_surface, game_start_rect)
			
			if keys[pygame.K_RETURN]:
				game_start = True
		
		pygame.display.flip()
		clock.tick(60)
		
#-----------------------------
		
def useless_function_one(x, y, z):
	return x + y - z	
		
def useless_function_two(x, y, z):
	return x - y + z
	
def useless_function_three(x, y, z):
	return x * y - z
		
