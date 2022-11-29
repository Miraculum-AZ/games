


#--tank.py
#--1--Create a bigger tank that can be a boss (for instance)
#self.image = pygame.transform.scale(self.image, (64, 64))

#--block.py
#--1--If we make below weights variable, so that the user can set them up, we can get more predictable levels
#random_block = random.choices(block_types, weights=[2,0,0,1,1])


# For enemies: we might have initial enemy spawn (not to collide with blocks -> initial enemy generation -> block generation -> subsequent enemies generation

Add teleport block

enemy spawn -> certain places on the map (if there's a block, it's removed)