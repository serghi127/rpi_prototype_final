# Documentation

# Story credit: https://www.youtube.com/watch?v=QhtGolDZsKY 
# Music credit: https://www.youtube.com/watch?v=cYF393DGfgs

# still need to program motors - are they servos or motors?
import os
os.system("aplay /home/ssft/Desktop/sound.wav")
from gpiozero import Button
import pygame
from pygame import mixer
from pygame.mixer import Sound
from signal import pause
from time import sleep
import random

pygame.init()
mixer.init()

# for the future game: use a dictionary 
# button_sounds = {
#     Button(2): Sound("samples/drum_tom_mid_hard.wav"),
#     Button(3): Sound("samples/drum_cymbal_open.wav"),
# }

#reference (ignore this)
yellow = Button(2)
blue = Button(5)
black = Button(17) #green
white = Button(3)
#orange = Button(22)

buttons = [yellow, blue, black, white]

#variables
on = False
on1 = False

prompt = False
gameSelect = False
first = True
reading = 0
prevPrompt = ""
file = ""
r = 0

#voice
riddles = ["creole_sounds/riddles/r/r1.wav", 
"creole_sounds/riddles/r/r2.wav", 
"creole_sounds/riddles/r/r3.wav", 
"creole_sounds/riddles/r/r4.wav",
"creole_sounds/riddles/r/r5.wav"
]

answers = [
"creole_sounds/riddles/a/a1.wav", 
"creole_sounds/riddles/a/a2.wav", 
"creole_sounds/riddles/a/a3.wav", 
"creole_sounds/riddles/a/a4.wav",
"creole_sounds/riddles/a/a5.wav"
]

hints = [
"creole_sounds/riddles/h/h1.wav", 
"creole_sounds/riddles/h/h2.wav", 
"creole_sounds/riddles/h/h3.wav", 
"creole_sounds/riddles/h/h4.wav",
"creole_sounds/riddles/h/h5.wav"
]

twister = [
"creole_sounds/tt/t1.wav", 
"creole_sounds/tt/t2.wav", 
"creole_sounds/tt/t3.wav", 
"creole_sounds/tt/t4.wav", 
"creole_sounds/tt/t5.wav", 
"creole_sounds/tt/t6.wav", 
"creole_sounds/tt/t7.wav", 
"creole_sounds/tt/t8.wav", 
"creole_sounds/tt/t9.wav", 
"creole_sounds/tt/t10.wav", 
]

#functions

#waits + retursn number of first button pressed
def readButtons(num):
    while True:
        for i in range(num):
            if (buttons[i].is_pressed):
                return i+1

#play a longer file until file is done
def playFile(file1):
    mixer.music.load(file1)
    mixer.music.set_volume(1)
    mixer.music.play()
    a = mixer.Sound(file1).get_length()
    sleep(a)
    mixer.music.unload()

#play a single sound until sound is done 
def playSound(file1):
    mixer.Sound.play(mixer.Sound(file1))
    sleep(mixer.Sound(file1).get_length())

#play song; allow user to pause, resume, stop music
def playSong(file1):
   # playFile("") #INSERT LISTENING INSTRAUCTIONS HERE
    global r
    mixer.music.load(file1)
    mixer.music.set_volume(1)
    mixer.music.play()
    music = True
    sleep(1)
    while music:
        r = readButtons(4)
        if (r==1):
            mixer.music.pause()
            playSound("creole_sounds/paused_song.wav") #music paused
            sleep(1)
        elif (r==4):
            playSound("creole_sounds/resume_song.wav") #music resumed
            mixer.music.unpause()
            sleep(1)
        elif (r==3):
            mixer.music.stop()
            music=False
            break
    playSound("creole_sounds/Left_the_song.wav") #music stopped
    mixer.music.unload()

#plays the file "file" variable is set to, and repeats that file until user presses any button other than 4, or repeat
def input1(num):
    global prompt
    global r
    prompt=False
    playFile(file)
    while (prompt==False):
        r = readButtons(num)
        print(r)
        if (r==4):
            playFile(file)
        else:
            prompt=True
            break

#same function as input1 but plays a "repeat" file so the user knows what to press 
def input2(num, repeat_file):
    global prompt
    global r
    prompt=False
    playFile(file)
    playFile(repeat_file)
    while (prompt==False):
        r = readButtons(num)
        print(r)
        if (r==4):
            playFile(file)
            playFile(repeat_file)
        else:
            prompt=True
            break
        

#loop seeing if the user wants to keep talking or quit 
def keepTalking():
    global file
    global gameSelect
    global first
    global r
    input2(4, "creole_sounds/1rep.wav")
    if (r==1 or r==3):
        gameSelect = True
        first = False
    else:
        file = "creole_sounds/I_see_do_you_want_to_keep_talking.wav"
        input2(4, "creole_sounds/1rep.wav") #press yellow for yes, blue for no 
        if (r==1 or r==3):
            gameSelect = True
            first = False
        else:
            file = "creole_sounds/off.wav" #has both repeat files & off statement
            input1(2)
            if (r==1):
                gameSelect = True
                first = False
            else:
                print("Shutting down.... ")
                first = False
                gameSelect = False

def keepTalkingM():
    global file
    global gameSelect
    global first
    global r
    input1(4)
    if (r==1 or r==3):
        gameSelect = True
        first = False
    else:
        file = "mam_sounds/i_see.mp3"
        input1(4) #press yellow for yes, blue for no 
        if (r==1 or r==3):
            gameSelect = True
            first = False
        else:
            file = "mam_sounds/stop.mp3" #has both repeat files & off statement
            input1(2)
            if (r==1):
                gameSelect = True
                first = False
            else:
                print("Shutting down.... ")
                first = False
                gameSelect = False

def playGames():
    global file
    global riddles
    global answers
    global r
    file = "creole_sounds/riddles/riddles_intro.wav"
    input1(4)
    
    if (r==1):
        order = [0, 1, 2, 3, 4]
        playFile("creole_sounds/riddles/try_your_best.wav")
        file = "creole_sounds/riddles/hints.wav"
        playFile(file)
        random.shuffle(order)
        for index in order:
            file = riddles[index]
            riddle_time = True
            while (riddle_time):
                input2(2, "creole_sounds/riddles/hints.wav")
                if (r==1):
                    playFile(answers[index])
                    sleep(1)
                    riddle_time = False
                elif (r==2):
                    playFile(hints[index])
                    sleep(3)
    elif (r==2):
        order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        points = 0
        file="creole_sounds/tt/twister_intro.wav"
        input1(4)
        random.shuffle(order)
        for index in order:
            playFile(twister[index])
            twister_time = True
            while (twister_time):
                r = readButtons(4)
                if (r==1):
                    playFile("creole_sounds/tt/correct.mp3")
                    sleep(1)
                    points += 1
                    twister_time = False
                elif (r==2):
                    playFile("creole_sounds/tt/incorrect.mp3")
                    sleep(1)
                    twister_time = False
                elif (r==4):
                    playFile(twister[index])
                    sleep(1)
                r = 0
        if (points>7):
            playFile("creole_sounds/tt/correct.wav")
        elif (points>3):
            playFile("creole_sounds/tt/okay.wav")
        else:
            playFile("creole_sounds/tt/better.wav")
        
    elif (r==3):
        playFile("creole_sounds/riddles/not_available.wav")
        #adventure game code
    file = "creole_sounds/tt/tyfp.wav"

playFile("converse.mp3")
r = readButtons(2)
if (r==1):
    playFile("mam.mp3")
    on1 = True
elif (r==2):
    playFile("creole.mp3")
    on = True
r = 0

#main loop - repeat for as many times as user wants game select
while on: 
    if (first==True):
        while (prompt==False):
            playFile("creole_sounds/intro.wav") #has both repeat files & intro statement
            r = readButtons(4)
            print(r)
            if (r!=4):
                prompt = True
            else:
                continue
        if (r==1):
            file = "creole_sounds/1resY.wav"
        elif (r==2):
            file = "creole_sounds/1resB.wav"
        elif (r==3):
            file = "creole_sounds/1resBl.wav"
        keepTalking()

    while (gameSelect):
        print("gameselect again")
        file = "creole_sounds/2resY_Bl.wav" #would you like to hear a story, play a game... 
        input2(4, "creole_sounds/2rep.wav") #press buttons + white to repeat... 

        if (r==1):
            playSong("creole_sounds/creole_story.wav") #story audio here
            file = "creole_sounds/creole_story_intro.wav" #that was the story titled _____!
        elif (r==2):
            playGames()
            file = ""
        elif (r==3):
            print("3")
            playSong("creole_sounds/creole_alphabet_song.wav") 
            file = "creole_sounds/creole_song_intro.wav" #that was a song, titled _____ !
        playFile(file)
        file="creole_sounds/keep_talking.wav" #would you like to do something else? 
        keepTalking()

    print("Shut down successful")
    playFile("creole_sounds/goodbye.wav")
    playFile("creole_sounds/shut_down.mp3")
    sleep(1)
    on = False
    break
    
while on1: 
    if (first==True):
        while (prompt==False):
            playFile("mam_sounds/intro.mp3") #has both repeat files & intro statement
            r = readButtons(4)
            print(r)
            if (r!=4):
                prompt = True
            else:
                continue
        if (r==1):
            file = "mam_sounds/res1_good.mp3"
        elif (r==2):
            file = "mam_sounds/res2_okay.mp3"
        elif (r==3):
            file = "mam_sounds/res3_bad.mp3"
        keepTalkingM()

    while (gameSelect):
        print("gameselect again")
        file = "mam_sounds/gameselect.mp3" #would you like to hear a story, play a game... 
        input2(4, "mam_sounds/gameselect_rep.mp3") #press buttons + white to repeat... 

        if (r==1):
            playSong("mam_sounds/flood.mp3") #story audio here
        elif (r==2):
            playFile("mam_sounds/unavailable.mp3")
        elif (r==3):
            playSong("mam_sounds/song.mp3") 
        keepTalkingM()

    print("Shut down successful")
    playFile("creole_sounds/goodbye.wav")
    playFile("creole_sounds/shut_down.mp3")
    sleep(1)
    on = False
    break
