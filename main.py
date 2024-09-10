"""This is a 2 player fighting game that features people in RCI! By taking videos of people, and
going frame by frame in the video, pgz Helper's .images and .animation allow for these characters to come to life in the game!
The players can punch, kick, and jump, all done from an imported player class."""

# window setup with positions
x = 150
y = 50
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'

# imports
import pygame
import pgzrun
import random
from characters import Player
from pgzhelper import *

#open file with each character's number of wins
win_reader = open("win_counter.txt").readlines()
win_reader = eval(win_reader[0])

"""a file is opened, and inside is a dictionary with each playable character's total wins. When called, the function will use bubble sort
to sort the dictionary within the file and return the sorted dictionary to eventually be rewritten over the old dictionary
in the file."""
def bubble_sort_dict(d):
    #takes a dictionary and convertes it into a 2d list
    items = list(d.items())
    n = len(items)

    #1 less than the length of the list
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            #this is a 2d list, thus if item j is less than the next item, swap the two
            if items[j][1] < items[j + 1][1]:
                items[j], items[j + 1] = items[j + 1], items[j]

    return dict(items)


# setting up width and height of window, along with window title
TITLE = 'COMP SCI BRAWL'
WIDTH = 1024
HEIGHT = 768

#gamestate at startscreen, player 1's choice of character first
startstate = "start"
p2_choice = False

#play select screen music
music.play('select_screen')

#variables that can be called to allow something to run once despite being in def update
"""Global variables were used, however this is due to the fact that they have numeric or True/False values 
that need to be changed, and it would not make sense to add these into a class. Any important functionality is done
within a class."""

#detects when the players collide with the ground, so that the sprites can properly change
col_det1 = 0
col_det2 = 0

#detects when the player is walking
walk_det1 = 0
walk_det2 = 0

#detects when player is idle
notwalk_det1 = 0
notwalk_det2 = 0

#dictates how long the punch attack lasts, allows for the sprite to change, and applies damage once when target is hit
punch_timer1 = 0
punch_count1 = 0
punch_amount1 = 0

punch_timer2 = 0
punch_count2 = 0
punch_amount2 = 0

#dictates how long the kick attack lasts, allows for the sprite to change, and applies damage once when target is hit
kick_timer1 = 0
kick_count1 = 0
kick_amount1 = 0

kick_timer2 = 0
kick_count2 = 0
kick_amount2 = 0

#runs once to switch sprites to winning animation
death_timer = 0

#empty health bar actor
p1_emptyhp = Actor('health_bar.png', (150, 200))
p1_emptyhp.scale = 0.5

p2_emptyhp = Actor('health_bar.png', (850, 200))
p2_emptyhp.scale = 0.5

#health remaining in health bar
p1_hp_remain = 180
p2_hp_remain = 180
#colour of health bar
yellow = 250, 191, 0

#initialize hp bars
p1_hp = None
p2_hp = None

# ground actors
ground_left = Actor('stage_1_ground.png', (150, 750))
ground_right = Actor('stage_1_ground.png', (400, 750))
ground_right2 = Actor('stage_1_ground.png', (600, 750))
ground_left2 = Actor('stage_1_ground.png', (100, 750))
ground_right3 = Actor('stage_1_ground.png', (800, 750))
ground_right4 = Actor('stage_1_ground.png', (1000, 750))
grounds = [ground_left, ground_right, ground_right2, ground_left2, ground_right3, ground_right4]

#retry button actor
retry_button = Actor('retry.png', (500, 400))

#adam's pfp in start screen
adam = Actor('adam_pfp.png', (100, 100))
adam.scale = 0.1

#brian's pfp in start screen
brian = Actor('brian_pfp.png', (200, 100))
brian.scale = 0.02


#mahir's pfp in start screen
mahir = Actor('mahir_pfp.png', (320, 100))
mahir.scale = 0.02


#daniel's pfp in start screen
daniel = Actor('daniel_pfp.png', (420, 100))
daniel.scale = 0.2


#anthony's pfp in start screen
ant = Actor('ant_pfp.png', (520, 100))
ant.scale = 0.2


#colin's pfp in start screen
colin = Actor('colin_pfp.png', (620, 100))
colin.scale = 0.15


#kai's pfp in start screen
kai = Actor('kai_pfp.png', (720, 100))
kai.scale = 0.2


# load in the background
startup_menu = pygame.image.load("images\\stage1_background.png")
startup_menu = pygame.transform.scale(startup_menu, (WIDTH, HEIGHT))

#player select
select = pygame.image.load("images\\start_screen.png")
select = pygame.transform.scale(select, (WIDTH, HEIGHT))

#player 2 background winscreen
p2win = pygame.image.load("images\\p2win.png")
p2win = pygame.transform.scale(p2win, (WIDTH, HEIGHT))

#player1 background winscreen
p1win = pygame.image.load("images\\p1win.png")
p1win = pygame.transform.scale(p1win, (WIDTH, HEIGHT))

#adam idle, walking, jumping, punching, and kicking frames
a_idle = ['a_idle0', 'a_idle1', 'a_idle2', 'a_idle3', 'a_idle4']
a_walk = ['a_walk0', 'a_walk1', 'a_walk2', 'a_walk3', 'a_walk4', 'a_walk5', 'a_walk6', 'a_walk7', 'a_walk8']
a_jump = ['a_jump0', 'a_jump1', 'a_jump2', 'a_jump3', 'a_jump4', 'a_jump5']
a_punch = ['a_punch0', 'a_punch1', 'a_punch2', 'a_punch3']
a_kick = ['a_kick0', 'a_kick1', 'a_kick2', 'a_kick3', 'a_kick4', 'a_kick5', 'a_kick6']

#brian idle, walking, jumping, punching, and kicking frames
b_idle = ['b_idle0', 'b_idle1', 'b_idle2', 'b_idle3', 'b_idle4', 'b_idle5', 'b_idle6']
b_walk = ['b_walk0', 'b_walk1', 'b_walk2', 'b_walk3', 'b_walk4', 'b_walk5', 'b_walk6', 'b_walk7', 'b_walk8', 'b_walk9']
b_jump = ['b_jump0', 'b_jump1', 'b_jump2', 'b_jump3', 'b_jump4']
b_punch = ['b_punch0', 'b_punch1', 'b_punch2', 'b_punch3', 'b_punch4', 'b_punch5', 'b_punch6', 'b_punch7', 'b_punch8', 'b_punch9', 'b_punch10']
b_kick = ['b_kick0', 'b_kick1', 'b_kick2', 'b_kick3', 'b_kick4', 'b_kick5', 'b_kick6', 'b_kick7', 'b_kick8', 'b_kick9', 'b_kick10']

#mahir idle, walking, jumping, punching, and kicking frames
m_idle = ['m_idle0', 'm_idle1', 'm_idle2']
m_walk = ['m_walk0', 'm_walk1', 'm_walk2', 'm_walk3']
m_jump = ['m_jump0', 'm_jump1', 'm_jump2', 'm_jump3', 'm_jump4', 'm_jump5']
m_punch = ['m_punch0', 'm_punch1', 'm_punch2', 'm_punch3', 'm_punch4']
m_kick = ['m_kick0', 'm_kick1', 'm_kick2', 'm_kick3', 'm_kick4', 'm_kick5','m_kick6']
m_win = ['m_win0', 'm_win1', 'm_win2', 'm_win3', 'm_win4', 'm_win5','m_win6', 'm_win7', 'm_win8', 'm_win9', 'm_win10']

#daniel idle, walking, jumping, punching, and kicking frames
d_idle = ['d_idle0', 'd_idle1', 'd_idle2']
d_walk = ['d_walk0', 'd_walk1', 'd_walk2', 'd_walk3', 'd_walk4', 'd_walk5', 'd_walk6', 'd_walk7', 'd_walk8', 'd_walk9', 'd_walk10']
d_jump = ['d_jump0', 'd_jump1', 'd_jump2', 'd_jump3', 'd_jump4', 'd_jump5']
d_punch = ['d_punch0', 'd_punch1', 'd_punch2', 'd_punch3', 'd_punch4', 'd_punch5']
d_kick = ['d_kick0', 'd_kick1', 'd_kick2', 'd_kick3', 'd_kick4', 'd_kick5','d_kick6']

#anthony idle, walking, jumping, punching, and kicking frames
ant_idle = ['ant_idle0', 'ant_idle1']
ant_walk = ['ant_walk0', 'ant_walk1', 'ant_walk2', 'ant_walk3', 'ant_walk4']
ant_jump = ['ant_jump0', 'ant_jump1', 'ant_jump2']
ant_punch = ['ant_punch0', 'ant_punch1', 'ant_punch2', 'ant_punch3', 'ant_punch4']
ant_kick = ['ant_kick0', 'ant_kick1', 'ant_kick2', 'ant_kick3']

#colin idle, walking, jumping, punching, and kicking frames
c_idle = ['c_idle0', 'c_idle1', 'c_idle2']
c_walk = ['c_walk0', 'c_walk1', 'c_walk2', 'c_walk3', 'c_walk4', 'c_walk5']
c_jump = ['c_jump0', 'c_jump1', 'c_jump2', 'c_jump3', 'c_jump4']
c_punch = ['c_punch0', 'c_punch1', 'c_punch2', 'c_punch3', 'c_punch4', 'c_punch5', 'c_punch6', 'c_punch7']
c_kick = ['c_kick0', 'c_kick1', 'c_kick2', 'c_kick3', 'c_kick4', 'c_kick5','c_kick6', 'c_kick7']
c_win = ['c_win0', 'c_win1', 'c_win2', 'c_win3', 'c_win4', 'c_win5','c_win6', 'c_win7', 'c_win8']

#kai idle, walking, jumping, punching, and kicking frames
k_idle = ['k_idle0', 'k_idle1', 'k_idle2']
k_walk = ['k_walk0', 'k_walk1', 'k_walk2', 'k_walk3', 'k_walk4', 'k_walk5']
k_jump = ['k_jump0', 'k_jump1', 'k_jump2', 'k_jump3', 'k_jump4', 'k_jump5']
k_punch = ['k_punch0', 'k_punch1', 'k_punch2', 'k_punch3', 'k_punch4', 'k_punch5']
k_kick = ['k_kick0', 'k_kick1', 'k_kick2', 'k_kick3', 'k_kick4', 'k_kick5']
k_win = ['k_win0', 'k_win1', 'k_win2', 'k_win3', 'k_win4', 'k_win5']


#empty variables that dictate which character player1 and player2 will use
p1 = ""
p2 = ""

#empty variables that are set to objects
player1 = None
player2 = None

#when mouse is clicked
def on_mouse_down(pos):
    global startstate
    global p2_choice
    global p1
    global p2
    global player1
    global player2
    global p1_hp_remain
    global p2_hp_remain

    global col_det1
    global col_det2

    global walk_det1
    global walk_det2

    global notwalk_det1
    global notwalk_det2

    global punch_timer1
    global punch_count1

    global punch_timer2
    global punch_count2

    global punch_amount1
    global punch_amount2

    global kick_timer1
    global kick_count1

    global kick_timer2
    global kick_count2

    global kick_amount1
    global kick_amount2

    global death_timer

    global p1_hp_remain
    global p2_hp_remain

    global p1_hp
    global p2_hp
    global yellow

    global a_walk
    global a_idle
    global a_punch
    global a_kick

    """Dictates the events that occur on the event that the mouse clicks on the screen. Useful for buttons, especially in
    the startscreen."""

    #if the game is on startscreen
    if startstate == "start":
        #if it's player 1's choice
        if not p2_choice:
            #if the player1 clicks on Adam's pfp, player 1 is adam, switch to player 2's choice
            if adam.collidepoint(pos):
                p2_choice = True
                p1 = "adam"

            #if the player1 clicks on Brian's pfp, player 1 is adam, switch to player 2's choice
            elif brian.collidepoint(pos):
                p2_choice = True
                p1 = "brian"

            #if the player1 clicks on Mahir's pfp, player 1 is adam, switch to player 2's choice
            elif mahir.collidepoint(pos):
                p2_choice = True
                p1 = "mahir"

            #if the player1 clicks on daniel's pfp, player 1 is adam, switch to player 2's choice
            elif daniel.collidepoint(pos):
                p2_choice = True
                p1 = "daniel"

            #if the player1 clicks on anthony's pfp, player 1 is adam, switch to player 2's choice
            elif ant.collidepoint(pos):
                p2_choice = True
                p1 = "ant"

            #if the player1 clicks on colin's pfp, player 1 is adam, switch to player 2's choice
            elif colin.collidepoint(pos):
                p2_choice = True
                p1 = "colin"

            #if the player1 clicks on kai's pfp, player 1 is adam, switch to player 2's choice
            elif kai.collidepoint(pos):
                p2_choice = True
                p1 = "kai"


    #if the player2 clicks on Adam's pfp, player 2 is adam
        elif p2_choice:
            if adam.collidepoint(pos):
                p2 = "adam"
                # start the game
                startstate = "game"
                #play main fighting theme music
                music.stop()
                music.play('fight_music')
    # if the player2 clicks on Brian's pfp, player 2 is Brian
            elif brian.collidepoint(pos):
                p2 = "brian"
                # start the game
                startstate = "game"
                #play main music
                music.stop()
                music.play('fight_music')

    # if the player2 clicks on mahir's pfp, player 2 is mahir
            elif mahir.collidepoint(pos):
                p2 = "mahir"
                # start the game
                startstate = "game"
                #play main music
                music.stop()
                music.play('fight_music')

                # if the player2 clicks on daniel's pfp, player 2 is daniel
            elif daniel.collidepoint(pos):
                p2 = "daniel"
                # start the game
                startstate = "game"
                #play game music
                music.stop()
                music.play('fight_music')

                # if the player2 clicks on anthony's pfp, player 2 is anthony
            elif ant.collidepoint(pos):
                p2 = "ant"
                # start the game
                startstate = "game"
                #start game music
                music.stop()
                music.play('fight_music')

            # if the player2 clicks on colin's pfp, player 2 is colin
            elif colin.collidepoint(pos):
                p2 = "colin"
                # start the game
                startstate = "game"
                #start game music
                music.stop()
                music.play('fight_music')

            # if the player2 clicks on kai's pfp, player 2 is kai
            elif kai.collidepoint(pos):
                p2 = "kai"
                # start the game
                startstate = "game"
                #begin game music
                music.stop()
                music.play('fight_music')


    #if player1 choose adam, player1 is now adam
        if p1 == "adam":
            player1 = Player(Actor("a_idle0", (50, 650)), 100, 3, 90, 80, a_idle, a_walk, a_jump, a_punch, a_kick, 18,
                             5, 1.5, 0.7, a_punch)
            player1.the_scale(player1.act_scale)
    #if player1 choose brian, player 1 is now brian
        elif p1 == "brian":
            player1 = Player(Actor("b_idle0", (50, 650)), 100, 0.8, 70, 200, b_idle, b_walk, b_jump, b_punch, b_kick,
                             10, 25, 0.5, 0.8, b_jump)
            player1.the_scale(player1.act_scale)

    # if player1 choose mahir, player 1 is now mahir
        elif p1 == "mahir":
            player1 = Player(Actor("m_idle0", (50, 650)), 100, 1.5, 75, 120, m_idle, m_walk, m_jump, m_punch, m_kick,
                             14, 12, 1.8, 0.8, m_win)
            player1.the_scale(player1.act_scale)

    # if player1 choose daniel, player 1 is now daniel
        elif p1 == "daniel":
            player1 = Player(Actor("d_idle0", (50, 650)), 100, 3, 80, 130, d_idle, d_walk, d_jump, d_punch, d_kick,
                             7, 19, 1.3, 0.5, d_punch)
            player1.the_scale(player1.act_scale)

    # if player1 choose anthony, player 1 is now anthony
        elif p1 == "ant":
            player1 = Player(Actor("ant_idle0", (50, 650)), 100, 1.2, 110, 140, ant_idle, ant_walk, ant_jump, ant_punch, ant_kick,
                             13, 13, 1.2, 0.4, ant_idle)
            player1.the_scale(player1.act_scale)

    # if player1 choose colin, player 1 is now colin
        elif p1 == "colin":
            player1 = Player(Actor("c_idle0", (50, 650)), 100, 2.5, 90, 100, c_idle, c_walk, c_jump, c_punch, c_kick,
                             17, 9, 1.5, 0.6, c_win)
            player1.the_scale(player1.act_scale)

    # if player1 choose kai, player 1 is now kai
        elif p1 == "kai":
            player1 = Player(Actor("k_idle0", (50, 650)), 100, 3.5, 70, 90, k_idle, k_walk, k_jump, k_punch, k_kick,
                             14, 10, 2, 0.6, k_win)
            player1.the_scale(player1.act_scale)

        # if player2 choose adam, player2 is now adam, flip the character
        if p2 == "adam":
            player2 = Player(Actor("a_idle0", (900, 650)), 100, 3, 90, 80, a_idle, a_walk, a_jump, a_punch, a_kick, 18,
                             5, 1.5, 0.7,a_punch)
            player2.flip()
            player2.the_scale(player2.act_scale)

        # if player2 choose brian, player 2 is now brian, flip the character
        elif p2 == "brian":
            player2 = Player(Actor("b_idle0", (900, 650)), 100, 0.8, 70, 200, b_idle, b_walk, b_jump, b_punch, b_kick,
                             10, 25, 0.5, 0.8, b_jump)
            player2.flip()
            player2.the_scale(player2.act_scale)

        # if player2 choose mahir, player 2 is now mahir, flip the character
        elif p2 == "mahir":
            player2 = Player(Actor("m_idle0", (900, 650)), 100, 2.5, 75, 120, m_idle, m_walk, m_jump, m_punch, m_kick,
                             14, 12, 1.8, 0.8, m_win)
            player2.flip()
            player2.the_scale(player2.act_scale)
        # if player2 choose daniel, player 2 is now daniel, flip the character
        elif p2 == "daniel":
            player2 = Player(Actor("d_idle0", (900, 650)), 100, 3, 80, 130, d_idle, d_walk, d_jump, d_punch, d_kick,
                             7, 19, 1.3, 0.5, d_punch)
            player2.flip()
            player2.the_scale(player2.act_scale)
        # if player2 choose anthony, player 2 is now anthony, flip the character
        elif p2 == "ant":
            player2 = Player(Actor("ant_idle0", (900, 650)), 100, 1.2, 110, 140, ant_idle, ant_walk, ant_jump, ant_punch, ant_kick,
                             13, 13, 1.2, 0.4,ant_idle)
            player2.flip()
            player2.the_scale(player2.act_scale)

            # if player2 choose colin, player 2 is now colin
        elif p2 == "colin":
            player2 = Player(Actor("c_idle0", (900, 650)), 100, 2.5, 90, 100, c_idle, c_walk, c_jump, c_punch, c_kick,
                             17, 9, 1.5, 0.6, c_win)
            player2.flip()
            player2.the_scale(player2.act_scale)

            # if player2 choose kai, player 2 is now kai
        elif p2 == "kai":
            player2 = Player(Actor("k_idle0", (900, 650)), 100, 3.5, 70, 90, k_idle, k_walk, k_jump, k_punch, k_kick,
                             14, 10, 2, 0.6, k_win)
            player2.flip()
            player2.the_scale(player2.act_scale)

    #if the gamestate is in "win" (a player has just won)
    elif startstate == "W":
        #if the retry button is clicked:
        if retry_button.collidepoint(pos):
            #reset each variable
            startstate = "start"
            # detects when the players collide with the ground, so that the sprites can properly change
            col_det1 = 0
            col_det2 = 0

            # detects when the player is walking
            walk_det1 = 0
            walk_det2 = 0

            # detects when player is idle
            notwalk_det1 = 0
            notwalk_det2 = 0

            # dictates how long the punch attack lasts, allows for the sprite to change, and applies damage once when target is hit
            punch_timer1 = 0
            punch_count1 = 0
            punch_amount1 = 0

            punch_timer2 = 0
            punch_count2 = 0
            punch_amount2 = 0

            # dictates how long the kick attack lasts, allows for the sprite to change, and applies damage once when target is hit
            kick_timer1 = 0
            kick_count1 = 0
            kick_amount1 = 0

            kick_timer2 = 0
            kick_count2 = 0
            kick_amount2 = 0

            death_timer = 0

            p1_hp_remain = 180
            p2_hp_remain = 180
            #if a player was in a state of punching, kicking or jumping right before the "win" state was reached, reset back to false
            player1.is_punching = False
            player1.is_kicking = False
            player1.is_jumping = False
            player1.is_walking = False
            player1.is_hit = False

            player2.is_punching = False
            player2.is_kicking = False
            player2.is_jumping = False
            player2.is_walking = False
            player2.is_hit = False

            player1.is_dead = False
            player2.is_dead = False
            player1 = None
            player2 = None
            p2_choice = False
            #play select screen music
            music.stop()
            music.play('select_screen')



# see if the player pressed a key, but only once
def on_key_down(key):

    global col_det1
    global col_det2
    global punch_timer1
    global punch_timer2

    global a_jump
    global startstate

    """Dictates action that occurs when a key is pressed down, whether it is space, shift, the 'f' key, etc.
    not used for player movement, as it is less easy to detect if the key is being held down."""

    if startstate == "game":

        #if spacebar is pressed, and the player isn't already jumping
        if key == keys.SPACE and not player1.is_jumping:
            #switch sprites
            player1.sprites(player1.jumping)
            #player jumps
            player1.jump()
            #set ground collision detection to 0
            col_det1 = 0

        #if j key is pressed, and the player is not already punching or jumping or kicking
        if key == keys.F and not player1.is_punching and not player1.is_kicking and not player1.is_jumping:
            #player is now punching
            player1.is_punching = True

        # if u key is pressed, and the player is not already punching, kicking, or jumping
        if key == keys.G and not player1.is_punching and not player1.is_kicking and not player1.is_jumping:
            #player is kicking
            player1.is_kicking = True

        # same deal for player 2
        if key == keys.UP and not player2.is_jumping and not player2.is_dead:
            player2.sprites(player2.jumping)
            player2.jump()
            col_det2 = 0

        #if user hits right shift, and player 2 is not punching, kicking, jumping, begin punching
        if key == keys.RSHIFT and not player2.is_punching and not player2.is_kicking and not player2.is_jumping:
            player2.is_punching = True

        if key == keys.PERIOD and not player2.is_punching and not player2.is_kicking and not player2.is_jumping:
            #begin kicking
            player2.is_kicking = True




def update():

    global startstate

    global p1
    global p2

    global col_det1
    global col_det2

    global walk_det1
    global walk_det2

    global notwalk_det1
    global notwalk_det2

    global punch_timer1
    global punch_count1

    global punch_timer2
    global punch_count2

    global punch_amount1
    global punch_amount2

    global kick_timer1
    global kick_count1

    global kick_timer2
    global kick_count2

    global kick_amount1
    global kick_amount2

    global death_timer

    global p1_hp_remain
    global p2_hp_remain

    global p1_hp
    global p2_hp
    global yellow

    global a_walk
    global a_idle
    global a_punch
    global a_kick

    global win_reader

    """Controls the main functionality of the game. Player objects move, punch, kick and damage other players inside of the
    update function. Due to the amount of events that begin and end in the update function, animation changes occur here as well
    however due to the nature of update being similar to a while True loop, numeric variables are used to ensure that some events only
    run once."""

    #if state is in select screen: pass, (otherwise, the code will see player1 and 2 = None, and crash)
    if startstate == "start":
        pass

    #if the game isn't on the start screen
    elif startstate == "game":
        p1_hp = Rect((80, 180), (p1_hp_remain, 40))
        p2_hp = Rect((780, 180), (p2_hp_remain, 40))

        # prevent the player from going offscreen, apply gravity to player
        player1.screenCheck()
        player2.screenCheck()

        player1.grav()
        player2.grav()


        # if a is pressed on the keyboard, the player's attribute to move left is called, and the actor is flipped
        if keyboard.A and not player1.is_kicking:
            #idle detections set to zero, walking detection increases by 1
            notwalk_det1 = 0
            walk_det1 += 1
            player1.is_walking = True
            player1.move_left()
            player1.flip()

            #ONLY WHEN WALK DETECTION = 1 (only runs once despite being in essentially a while loop)
            if walk_det1 == 1 and player1.is_walking and not player1.is_jumping and not player1.is_punching and not player1.is_kicking:
                #player is walking
                player1.sprites(player1.walk)

        # if d is pressed on the keyboard, the player's attribute to move right is called, and the actor is unflipped
        elif keyboard.D and not player1.is_kicking:
            notwalk_det1 = 0
            walk_det1 += 1
            player1.is_walking = True
            player1.move_right()
            player1.unflip()

            #detects if player1 is walking, but it's called once. Change sprites to walking
            if walk_det1 == 1 and player1.is_walking and not player1.is_jumping and not player1.is_punching and not player1.is_kicking:
                player1.sprites(player1.walk)

        #if a or d on keyboard isn't being pressed, player is not walking, walking detection = 0
        else:
            player1.is_walking = False
            walk_det1 = 0

        #same deal with left and right key for player 2
        if keyboard.LEFT and not player2.is_kicking:
            notwalk_det2 = 0
            walk_det2 += 1
            player2.is_walking = True
            player2.move_left()
            player2.flip()

            if walk_det2 == 1 and player2.is_walking and not player2.is_jumping and not player2.is_punching and not player2.is_kicking:
                player2.sprites(player2.walk)

        elif keyboard.RIGHT and not player2.is_kicking:
            notwalk_det2 = 0
            walk_det2 += 1
            player2.is_walking = True
            player2.move_right()
            player2.unflip()

            if walk_det2 == 1 and player2.is_walking and not player2.is_jumping and not player2.is_punching and not player2.is_kicking:
                player2.sprites(player2.walk)

        else:
            player2.is_walking = False
            walk_det2 = 0

        #if player is idle
        if not player1.is_walking:
            #idle counter increases
            notwalk_det1 += 1
            if notwalk_det1 == 1:
                #sets sprites to idle BUT ONLY ONCE
                player1.sprites(player1.idle)

        if not player2.is_walking:
            notwalk_det2 += 1
            if notwalk_det2 == 1:
                player2.sprites(player2.idle)


        for ground in grounds:
            #if player collides with any of the ground drawn:
            if player1.collision_detect(ground):
                #ground collision counter increases, player is not jumping and dy is 0
                col_det1 += 1
                player1.reset()
            if col_det1 == 1:
                #if player is colliding with ground, sprites return to idle (important for jumping)
                player1.the_scale(player1.act_scale)
                player1.sprites(player1.idle)

            if player2.collision_detect(ground):
                col_det2 += 1
                player2.reset()
            if col_det2 == 1:
                player2.the_scale(player2.act_scale)
                player2.sprites(player2.idle)

        if punch_timer1 < player1.punch_time and player1.is_punching:
            #if punch timer is less than 100, and a punch has begun to be thrown
            player1.the_scale(player1.act_scale)
            #start timer, punch detector increases
            punch_count1 += 1
            punch_timer1 += 1
            if punch_count1 == 1:
                #set actor sprites to punch (only called once)
                player1.sprites(player1.punch)

        elif punch_timer1 >= player1.punch_time:
            #when timer is up, reset punch variables
            punch_count1 = 0
            punch_timer1 = 0
            punch_amount1 = 0
            player1.the_scale(player1.act_scale)
            #return to idle
            player1.sprites(player1.idle)
            player1.is_punching = False


        if punch_timer2 < player2.punch_time and player2.is_punching:
            player2.the_scale(player2.act_scale)
            punch_count2 += 1
            punch_timer2 += 1
            if punch_count2 == 1:
                player2.sprites(player2.punch)

        elif punch_timer2 >= player2.punch_time:
            punch_count2 = 0
            punch_timer2 = 0
            punch_amount2 = 0
            player2.the_scale(player2.act_scale)
            player2.sprites(player2.idle)
            player2.is_punching = False

    #same code as punch
        if kick_timer1 < player1.kick_time and player1.is_kicking:
            #if punch timer is less than 150, and a kick has begun to be thrown
            player1.the_scale(player1.act_scale)
            #start timer, kick detector increases
            kick_count1 += 1
            kick_timer1 += 1
            if kick_count1 == 1:
                #set actor sprites to kick (only called once)
                player1.sprites(player1.kick)

        elif kick_timer1 >= player1.kick_time:
            #when timer is up, reset kick variables
            kick_count1 = 0
            kick_timer1 = 0
            kick_amount1 = 0
            player1.the_scale(player1.act_scale)
            #return to idle
            player1.sprites(player1.idle)
            player1.is_kicking = False


        if kick_timer2 < player2.kick_time and player2.is_kicking:
            player2.the_scale(player2.act_scale)
            kick_count2 += 1
            kick_timer2 += 1
            if kick_count2 == 1:
                player2.sprites(player2.kick)

        elif kick_timer2 >= player2.kick_time:
            kick_count2 = 0
            kick_timer2 = 0
            kick_amount2 = 0
            player2.the_scale(player2.act_scale)
            player2.sprites(player2.idle)
            player2.is_kicking = False

        #if player 1 collides with player 2 while punching
        if player1.collision_detect(player2.actor) and player1.is_punching:
            #if player 1 is facing right, and player 2 is facing right, and player 1's x value is less than player 2's, (meaning player 1 is behind player 2)
            if player1.is_flipped == False and player2.is_flipped == False and player1.give_x() < player2.give_x():
                #set player2 punching and kicking states to false
                player2.is_punching = False
                player2.is_kicking = False

            elif player1.is_flipped == True and player2.is_flipped == True and player1.give_x() > player2.give_x():
                player2.is_punching = False
                player2.is_kicking = False


        elif player1.collision_detect(player2.actor) and player1.is_kicking:
            #if player 1 is facing right, and player 2 is facing right, and player 1's x value is less than player 2's, (meaning player 1 is behind player 2)
            if player1.is_flipped == False and player2.is_flipped == False and player1.give_x() < player2.give_x():
                player2.is_punching = False
                player2.is_kicking = False

            elif player1.is_flipped == True and player2.is_flipped == True and player1.give_x() > player2.give_x():
                player2.is_punching = False
                player2.is_kicking = False



        if player2.collision_detect(player1.actor) and player2.is_punching:
            #if player 1 is facing right, and player 2 is facing right, and player 1's x value is less than player 2's, (meaning player 1 is behind player 2)
            if player2.is_flipped == False and player1.is_flipped == False and player2.give_x() < player1.give_x():
                player1.is_punching = False
                player1.is_kicking = False

            elif player2.is_flipped == True and player1.is_flipped == True and player2.give_x() > player1.give_x():
                player1.is_punching = False
                player1.is_kicking = False


        elif player2.collision_detect(player1.actor) and player2.is_kicking:
            #if player 1 is facing right, and player 2 is facing right, and player 1's x value is less than player 2's, (meaning player 1 is behind player 2)
            if player2.is_flipped == False and player1.is_flipped == False and player2.give_x() < player1.give_x():
                player1.is_punching = False
                player1.is_kicking = False

            elif player2.is_flipped == True and player1.is_flipped == True and player2.give_x() > player1.give_x():
                player1.is_punching = False
                player1.is_kicking = False


        #if player 1 collides with player 2 while punching
        if player1.collision_detect(player2.actor) and player1.is_punching:
            punch_amount1 += 1
            #we have to check whether player1 is still punching, as it's possible that player1 is being attacked from behind, in which case damage will not be dealt
            if punch_amount1 == 1 and player1.is_punching:
                # subract 20 health from opponent once per punch
                player2.minus_health(player1.pun_dmg)
                #subtract length from player 2 healthbar based on punch damage from player 1
                p2_hp_remain -= player1.pun_dmg * 1.8


        elif player1.collision_detect(player2.actor) and player1.is_kicking:
            kick_amount1 += 1
            if kick_amount1 == 1 and player1.is_kicking:
                # subract 20 health from opponent once per punch
                player2.minus_health(player1.kick_dmg)
                # subtract length from player 2 healthbar based on kick damage from player 1
                p2_hp_remain -= player1.kick_dmg * 1.8


        if player2.collision_detect(player1.actor) and player2.is_punching:
            punch_amount2 += 1
            if punch_amount2 == 1 and player2.is_punching:
                player1.minus_health(player2.pun_dmg)
                p1_hp_remain -= player2.pun_dmg * 1.8


        elif player2.collision_detect(player1.actor) and player2.is_kicking:
            kick_amount2 += 1
            if kick_amount2 == 1 and player2.is_kicking:
                player1.minus_health(player2.kick_dmg)
                p1_hp_remain -= player2.kick_dmg * 1.8


        if player1.health <= 0:
            #player is dead when health = 0
            player1.is_dead = True
            #set gamestate to a "player wins" state
            startstate = "W"

        if player2.health <= 0:
            player2.is_dead = True
            startstate = "W"

        #animate players
        player1.animation()
        player2.animation()

    #if the gamestate is in winstate
    elif startstate == "W":
        #start death timer (to allow for sprites to be changed once)
        death_timer += 1
        #if player2 is dead and player1 is adam
        if player2.is_dead:
            if p1 == "adam" and death_timer == 1:
                #add 1 to "adam" key in file
                win_reader['adam'] += 1
                #call the sort method to sort the dictionary, assign a variable to it
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                #write the sorted dictionary into the file to replace the previous text
                out.write(str(sorted))
                out.close()

                music.stop()
                #play adam's win music and win sprites
                music.play('a_win')
                player1.sprites(player1.win)

            #if brian wins
            elif p1 == "brian" and death_timer == 1:
                # add 1 win to "brian" key in file
                win_reader['brian'] += 1
                # call the sort method to sort the dictionary, assign a variable to it
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                # write the sorted dictionary into the file to replace the previous text
                out.write(str(sorted))
                out.close()

                music.stop()
                # play brian's win music and win sprites
                music.play('b_win')
                player1.sprites(player1.win)


            #if mahir wins
            elif p1 == "mahir" and death_timer == 1:
                # add 1 win to "mahir" key in file
                win_reader['mahir'] += 1
                # call the sort method to sort the dictionary, assign a variable to it
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                # write the sorted dictionary into the file to replace the previous text
                out.write(str(sorted))
                out.close()

                music.stop()
                # play mahir's win music and win sprites
                music.play('m_win')
                player1.sprites(player1.win)

            #if daniel wins
            elif p1 == "daniel" and death_timer == 1:
                #add 1 win to daniel key
                win_reader['daniel'] += 1
                # call the sort method to sort the dictionary, assign variable "sorted" to it
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                # write the sorted dictionary into the file to replace the previous text
                out.write(str(sorted))
                out.close()

                music.stop()
                #play daniel's win animation and sprites
                music.play('d_win')
                player1.sprites(player1.win)

            #if anthony wins
            elif p1 == "ant" and death_timer == 1:
                #add 1 to anthony's win count in the file
                win_reader['anthony'] += 1
                #sort dictionary
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                #rewrite file with sorted dictionary
                out.write(str(sorted))
                out.close()

                music.stop()
                #play anthony music/win sprites
                music.play('ant_win')
                player1.sprites(player1.win)

            #if colin wins
            elif p1 == "colin" and death_timer == 1:
                #add 1 to colin's wins
                win_reader['colin'] += 1
                #sort the dictionary in the file
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                #rewrite file
                out.write(str(sorted))
                out.close()

                music.stop()
                #play colin's music/winning sprites
                music.play('c_win')
                player1.sprites(player1.win)

            #if kai wins
            elif p1 == "kai" and death_timer == 1:
                #add 1 win for kai
                win_reader['kai'] += 1
                #sort dictionary
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                #rewrite dictionary in file with sorted one
                out.write(str(sorted))
                out.close()

                music.stop()
                #kai win music/sprites
                music.play('k_win')
                player1.sprites(player1.win)

        #if player 2 is dead, repeat process with player 1
        if player1.is_dead:
            if p2 == "adam" and death_timer == 1:

                win_reader['adam'] += 1
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                out.write(str(sorted))
                out.close()

                music.stop()
                music.play('a_win')
                player2.sprites(player2.win)

            elif p2 == "brian" and death_timer == 1:
                win_reader['brian'] += 1
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                out.write(str(sorted))
                out.close()

                music.stop()
                music.play('b_win')
                player2.sprites(player2.win)

            elif p2 == "mahir" and death_timer == 1:
                win_reader['mahir'] += 1
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                out.write(str(sorted))
                out.close()

                music.stop()
                music.play('m_win')
                player2.sprites(player2.win)
            elif p2 == "daniel" and death_timer == 1:
                win_reader['daniel'] += 1
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                out.write(str(sorted))
                out.close()

                music.stop()
                music.play('d_win')
                player2.sprites(player2.win)

            elif p2 == "ant" and death_timer == 1:
                win_reader['anthony'] += 1
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                out.write(str(sorted))
                out.close()

                music.stop()
                music.play('ant_win')
                player2.sprites(player2.win)

            elif p2 == "colin" and death_timer == 1:
                win_reader['colin'] += 1
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                out.write(str(sorted))
                out.close()

                music.stop()
                music.play('c_win')
                player2.sprites(player2.win)

            elif p2 == "kai" and death_timer == 1:
                win_reader['kai'] += 1
                sorted = bubble_sort_dict(win_reader)
                out = open('win_counter.txt', 'w')
                out.write(str(sorted))
                out.close()

                music.stop()
                music.play('k_win')
                player2.sprites(player2.win)

        #animate players for win animation
        player1.animation()
        player2.animation()


def draw():
    """draw actors and text on the screen"""

    #if the screen is on the start menu, draw some text
    if startstate == "start":
        screen.clear()
        #draw adam's stats
        screen.blit(select, (0, 0))
        screen.draw.text("ADAM", (60, 150), color = "black", fontsize=30)
        screen.draw.text("speed: 2", (60, 170), color = "black", fontsize=20)
        screen.draw.text("punch: 10", (60, 180), color="black", fontsize=20)
        screen.draw.text("kick: 15", (60, 190), color="black", fontsize=20)
        screen.draw.text("jump: 1.5", (60, 200), color="black", fontsize=20)
        #draw brian's stats
        screen.draw.text("Brian", (160, 150), color = "black", fontsize=30)
        screen.draw.text("speed: 1", (160, 170), color = "black", fontsize=20)
        screen.draw.text("punch: 8", (160, 180), color="black", fontsize=20)
        screen.draw.text("kick: 23", (160, 190), color="black", fontsize=20)
        screen.draw.text("jump: 0.9", (160, 200), color="black", fontsize=20)
        #draw mahir's stats
        screen.draw.text("Mahir", (280, 150), color = "black", fontsize=30)
        screen.draw.text("speed: 1.5", (280, 170), color = "black", fontsize=20)
        screen.draw.text("punch: 14", (280, 180), color="black", fontsize=20)
        screen.draw.text("kick: 12", (280, 190), color="black", fontsize=20)
        screen.draw.text("jump: 1.8", (280, 200), color="black", fontsize=20)
        #draw daniel's stats
        screen.draw.text("Daniel", (380, 150), color = "black", fontsize=30)
        screen.draw.text("speed: 3", (380, 170), color = "black", fontsize=20)
        screen.draw.text("punch: 7", (380, 180), color="black", fontsize=20)
        screen.draw.text("kick: 19", (380, 190), color="black", fontsize=20)
        screen.draw.text("jump: 1.3", (380, 200), color="black", fontsize=20)
        #draw anthony's stats
        screen.draw.text("Anthony", (480, 150), color = "black", fontsize=30)
        screen.draw.text("speed: 1.2", (480, 170), color = "black", fontsize=20)
        screen.draw.text("punch: 13", (480, 180), color="black", fontsize=20)
        screen.draw.text("kick: 13", (480, 190), color="black", fontsize=20)
        screen.draw.text("jump: 1.2", (480, 200), color="black", fontsize=20)
        #draw colin's stats
        screen.draw.text("Colin", (580, 150), color = "black", fontsize=30)
        screen.draw.text("speed: 2.5", (580, 170), color = "black", fontsize=20)
        screen.draw.text("punch: 17", (580, 180), color="black", fontsize=20)
        screen.draw.text("kick: 9", (580, 190), color="black", fontsize=20)
        screen.draw.text("jump: 1.5", (580, 200), color="black", fontsize=20)
        #draw kai's stats
        screen.draw.text("Kai", (680, 150), color = "black", fontsize=30)
        screen.draw.text("speed: 3.5", (680, 170), color = "black", fontsize=20)
        screen.draw.text("punch: 14", (680, 180), color="black", fontsize=20)
        screen.draw.text("kick: 10", (680, 190), color="black", fontsize=20)
        screen.draw.text("jump: 2", (680, 200), color="black", fontsize=20)

        #draw character's start screen profile pic
        adam.draw()
        brian.draw()
        mahir.draw()
        daniel.draw()
        ant.draw()
        colin.draw()
        kai.draw()

    elif startstate == "game":
        #fit the games starts, clear screen, draw background
        screen.clear()
        screen.blit(startup_menu, (0, 0))

        #draw the hp bars
        screen.draw.filled_rect(p1_hp, yellow)
        screen.draw.filled_rect(p2_hp, yellow)
        #draw the empty hp bars
        p1_emptyhp.draw()
        p2_emptyhp.draw()

        # draw the ground
        for ground in grounds:
            ground.draw()

        #draw the players
        player1.draw()
        player2.draw()

    elif startstate == "W":
        #fit the games starts, clear screen, draw background
        screen.clear()
        screen.blit(startup_menu, (0, 0))

        #draw HP bars
        screen.draw.filled_rect(p1_hp, yellow)
        screen.draw.filled_rect(p2_hp, yellow)
        #draw empty hp bars
        p1_emptyhp.draw()
        p2_emptyhp.draw()

        # draw the ground
        for ground in grounds:
            ground.draw()
        #draw retry button
        retry_button.draw()

        if player1.is_dead:
            #draw p2 win on screen
            screen.draw.text("PLAYER 2 WINS", (200, 150), color="black", fontsize=100)
            player2.draw()
        elif player2.is_dead:
            #draw p1 win on screen
            screen.draw.text("PLAYER 1 WINS", (200, 150), color="black", fontsize=100)
            player1.draw()

pgzrun.go()