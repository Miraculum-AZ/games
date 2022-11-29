# BATTLE_CITY IMITATION WITH PYGAME
### Video Demo: https://youtu.be/hO06GrhbMH4
### Description:
The idea was to recreate the Battle City game in Python, using pygame module as a basis.
All pictures are taken from the internet, though some of them are slightly modified by me.
All underlying logic of the game is created by me, though some tutorials of how to use pygame have obviously been watched.

The game requires two characters to work together and defeat as many enemy tanks as possible.
Enemy tanks consist of the inital spawn and regular semi-randomized spawn in the top screen borders. Enemy spawn is indefinite.

Enemies are subdivided into 4 different classes, which affects their characteristics e.g. speed, health, bullet speed, etc.
Which class is being spawn depends on a simple random function with different weights.

Player's tank's characteristic are temporary/permanently updates upon collecting different bonuses that are generated on the field.

Bonuses are generated randomly after a certain timespan and affect player/game field.
They can frieze the enemies, destroy them, update player's level, give an extra life, create a defensive shield or even call an ally.

An ally is a green tank, which is generated after a certain bonus is picked up. It does not interact with player, yet can destroy enemies or be destoyed by them.

There are many many more interesting tweaks in the code that you are welcome to explore.
The total number of lines is more than 2 thousands, the notion of classes and inheritance is widely used.

The game is not created for the purpose of a monetary gain and can be freely distributed.

Oleksandr 29/11/2022