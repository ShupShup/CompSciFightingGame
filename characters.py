import pygame
import pgzrun
import random
from pgzhelper import *


class Player():

    def __repr__(self):
        return "Player object that dictates the properties of every unique character in the game, including their sprites, health, jumping height, etc." \
               "This includes basic functionality as well, such as animating the actor, moving, jumping, and flipping."

    # player has attributes for which character is chosen, hit points, speed, how long the punch lasts, how long the kick lasts,
    # idle, walk, jump, punch, and kick frames, punch damage, kick damage, jump height, and scale and win sprites
    def __init__(self, actor, health, speed, punch_time, kick_time, idle, walk, jumping, punch, kick, pun_dmg, kick_dmg, jump_height, act_scale, win):

        self.actor = actor
        self.health = health
        self.speed = speed
        self.punch_time = punch_time
        self.kick_time = kick_time
        self.idle = idle
        self.walk = walk
        self.jumping = jumping
        self.punch = punch
        self.kick = kick
        self.pun_dmg = pun_dmg
        self.kick_dmg = kick_dmg
        self.jump_height = jump_height
        self.act_scale = act_scale
        self.win = win

        #actor's y displacement is 0
        self.actor.dy = 0
        #actor by default is not walking, jumping, punching, kicking, flipped, dead or being hit
        self.is_walking = False
        self.is_jumping = False
        self.is_punching = False
        self.is_kicking = False
        self.is_flipped = False
        self.is_dead = False
        self.is_hit = False


    # when called, the character's scale will be set
    def the_scale(self, act_scale):
        self.actor.scale = act_scale

    # takes images a parameter for the animation function to use
    def sprites(self, images):
        self.actor.images = images

    # animate the sprite
    def animation(self):
        self.actor.animate()

    # flip the actor when called
    def flip(self):
        self.is_flipped = True
        self.actor.flip_x = True

    #if actor goes too far left or right from the screen, they are blocked off
    def screenCheck(self):
        if self.actor.x < 13:
            self.actor.x = 13
        elif self.actor.x > 1014:
            self.actor.x = 1014

    # unflip the actor when called
    def unflip(self):
        self.is_flipped = False
        self.actor.flip_x = False

    #move the actor right by a set speed when called
    def move_right(self):
        self.actor.x += self.speed

    # move the actor left by a set speed when called
    def move_left(self):
        self.actor.x -= self.speed

    def grav(self):
        # gravity physics
        #normally, the y remains the same, because dy is  so small, but when the actor jumps...
        self.actor.y += self.actor.dy * 9.8
        self.actor.dy += 0.05

    #reset the actor's dispacement when called, sets jumping back to false when called
    def reset(self):
        self.actor.dy = 0
        self.is_jumping = False

    #displaces actor into the air when called
    def jump(self):
        self.actor.dy -= self.jump_height
        self.is_jumping = True

    #if actor hits another actor, return true
    def collision_detect(self, obj):
        if self.actor.collide_pixel(obj):
            return True

    #return actor's x value to detect whether a player is to the right or left to the other
    def give_x(self):
        return self.actor.x

    # draw the actor when called
    def draw(self):
        self.actor.draw()

    def minus_health(self, health):
        # give a condition to subtract health
        self.health -= health


