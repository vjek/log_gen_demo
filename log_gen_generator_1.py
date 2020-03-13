#!/usr/bin/env python3
###
# script to generate parseable logfile data, simulating a multi-player game.
# formats in general would be somewhat like ISO 8601, for date/time, although not precisely
# logline will be YYYYMMDD-HHMMSS:zzz charname action target value type via proxy
# examples would be..
# 20181212140901:782 warrior hits goblin with Mighty Strike for 256 piercing damage.
# 20181212152458:001 cleric casts Heal on warrior for 100 divine healing.
# 20180101015901:999 ranger hits orc for 150 critical slashing damage via pet_panther.
# 20180101015903:478 rogue misses orc with Backstab.
# 20180202223030:500 magician casts Summon Food on warrior for a stack of 5 apple food.
# 20180303190545:250 cleric casts Glory on all nearby.
# 20181224081629:351 Orc Shaman starts casting Sleepwalking on Warrior.
# 20181224081632:354 Orc Shaman finishes casting Sleepwalking on Warrior.
# 20181224081632:460 Warrior resists Orc Shaman's Sleepwalking.
# .. maybe instant abilities are always on the same line
# .. while abilities with a cast time always have three lines. start, finish, result.
###
# first version by vjek on 20181227, updated 20190112 to handle MS-Windows issues
# next update 20190213 to make time calc more elegant
###
# usage would be to place both scripts in the same folder/directory, then 
# ./log_gen_generator_1.py > outfile1.txt &
# and then ./log_gen_gui_1.py and then click "Start monitoring log file"
# if you don't redirect the output, you can see the raw log being generated.
###
import random
import datetime
import time
# first, damage types and other globals
my_melee_damage_types = ["piercing","slashing","crushing"]
my_magic_damage_types = ["Heat","Cold","Electrical","Poison","Disease","Divine"]
my_melee_actions = ["stabs","cuts","bashes"]
my_magic_actions = ["burns","freezes","shocks","injects","sickens","smites"]
my_class_names = ["Cleric","Paladin","Warrior","Dire Lord","Ranger","Rogue","Monk","Summoner","Enchanter","Wizard","Druid","Shaman"]
my_enemy_names = ["Giant Spider","Giant Ant","Wolf","Badger","Bear","Orc","Goblin","Kobold","Sprite","Wisp","Pixie","Bandit","Mercenary","Thug"]
my_melee_attacks = ["Tendon Slice","Shield Bash","Puncture","Backstab","Throat Punch","Mighty Strike"]
my_magic_attacks = ["Flame Strike","Ice Comet","Chain Lightning","Toxic Blast","Infection","Wrath"]
min_crit_bonus_damage_percentage = 10
max_crit_bonus_damage_percentage = 50
max_lines_per_second = 20 # typical max values would be 10-50, more than 150 doesn't work as expected
max_lines_output = 1000 # typical values would be 100-1000, but you can create however many lines you want.

# generate a random damage value
def generate_random_damage_value(min_val,max_val,critbool):
	dmg_val = random.randint(min_val,max_val)
	if critbool == True:
		# percentage of damage bonus from crit 
		crit_percentage = random.randint(min_crit_bonus_damage_percentage,max_crit_bonus_damage_percentage)
		dmg_val = dmg_val * (1 + (crit_percentage / 100))
	return str(int(dmg_val))

# print out a certain number of loglines, for this particular second
# TODO:
# need to add a shuffle of line types, instant cast magic, misses, resists, and abilities plus melee auto attack
# might need to create profiles for skills, for things like casting time
# this might necessitate temporal variables instead of a static 1 second, to accomodate casting times
# also, DoT's, HoT's..
def print_loglines(count,inter_line_delay):
    for a in range(count):
        critbool = False
        crit_str = ""
        #generate 10% critical hits
        if random.randint(1,10) == 10:
            critbool = True
            crit_str = "critical "

        char_name = random.choice(my_class_names)
        action = random.choice(my_melee_actions + my_magic_actions)
        target = random.choice(my_enemy_names)
        dmg_val = generate_random_damage_value(80,100,critbool)
        dmg_type = random.choice(my_melee_damage_types + my_magic_damage_types)
        attack_type = random.choice(my_melee_attacks + my_magic_attacks)
        now = datetime.datetime.now()
        date_str = str(now.year)+"{:02d}".format(now.month)+"{:02d}".format(now.day)
        time_str = ('%02d%02d%02d.%03d'%(now.hour,now.minute,now.second,now.microsecond/1000))
        logline="{}{} {} {} a {} with {} for {} {}{} damage."\
        .format(date_str,time_str,char_name,action,target,attack_type,dmg_val,crit_str,dmg_type)
        print(logline, flush=True)
        time.sleep(inter_line_delay/1000)
		
# main program starts here
#
now = int(time.time()) #update now for check
the_future = now + 1 # setup for the next second

linecount = 0
while linecount <= max_lines_output:
    now = int(time.time()) #update now for check
    if now >= the_future: #check now against future
        number_of_lines = random.randint(0,max_lines_per_second) # generate a random number of lines from 0 to max, per second
#        print("now:" + " linecount:",str(linecount) + " number of lines:",str(number_of_lines))
        if number_of_lines != 0: # if we have lines to print..
                inter_line_delay = 1000 / (number_of_lines) # to get milliseconds, and add one so it doesn't exceed one second
        else:
                inter_line_delay = 1000 # or if it's zero, wait a full second
        print_loglines(number_of_lines,inter_line_delay) #add time tracking/minutes/seconds to input vars for this function
        the_future = now + 1 # setup for the next second
        linecount = linecount + number_of_lines #and only do this until we reach however many lines of output, total
