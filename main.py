# Main program file

# Imports
from playsound import playsound

import random as rng
from pgl import GWindow, GLine, GOval, GRect, GPolygon, GLabel, GCompound
from datastructures import Node, LinkedList, Stack, clear_linkedlist, is_in_linkedlist, shuffle_and_fill
from pglstuff import Timerclass, mode_switch_button, base_frame, create_num_picks_button, create_n_choices, center_phrase_to_draw, phrase_label_and_backup, draw_gw_button_xywhLCFfc, flip_over_vertical_screen_edge, just_draw_label, draw_fun_labels, draw_save_icon, colorsetups, draw_all_save_icons_and_background

import os
import math
import time as tmr

cwd = os.getcwd()  # Get the current working directory (cwd)
# print(f"{cwd}")


# Constants
global ready_to_show
global number_of_picks
phrase_saved = "phrase saved!"
number_of_picks = 3
ready_to_show = True

num_change_TF = True

GWINDOW_WIDTH = 1250
GWINDOW_HEIGHT = 750
TIME_STEP = 500

gw = GWindow(GWINDOW_WIDTH,GWINDOW_HEIGHT)



def what_are_those(easynouns, mediumnouns, hardnouns, easyadjs, mediumadjs, hardadjs, actions):
    # This is the main function that is called for the program to run

    # First initializing all relevant variables
    global next_player_index
    global phrase_to_draw
    global ready_to_show
    global acting_question_mark
    global holding_a_phrase_for_a_moment
    global next_player_phrase

    acting_question_mark = False    
    holding_a_phrase_for_a_moment = ""
    next_player_index = 0
    next_player_phrase = ""

    # Create background to set to dark mode as default
    background = GRect(0,0,GWINDOW_WIDTH,GWINDOW_HEIGHT)
    background.set_filled(True)
    background.set_fill_color("#1e1e1e")
    background.set_color("#1e1e1e")
    gw.add(background)

    # Create Timer
    Timer_on_Screen = Timerclass()
    Timer_on_Screen.draw_compound(gw)
    Timer_on_Screen._compound.set_location(GWINDOW_WIDTH/10-0.5*Timer_on_Screen._Timerlabel.get_width(),5*GWINDOW_HEIGHT/6-6)

    def stop_time(self):
        # This will stop the timer, and is called when the timer hits 00:00

        global num_change_TF
        global countdown

        if Timer_on_Screen != None:
            num_change_TF = True
            Timer_on_Screen._ticking = False
            Timer_on_Screen.play_pause()
            Timer_on_Screen._Timerlabel.set_color(self._unred)

    def incr_decr(Timerlabel1, secs = 1, increasing = True):
        # When called, increases or decreases the timer by 1

        Timerlabel_separated = Timerlabel1.get_label().split(":")
        Timerlabel_mins = int(Timerlabel_separated[0])
        Timerlabel_secs = int(Timerlabel_separated[1])

        if increasing:
            Timerlabel_secs += secs

        else:
            Timerlabel_secs -= secs

        if not 0 <= Timerlabel_secs <= 59:
            if Timerlabel_secs > 59:
                Timerlabel_mins += Timerlabel_secs // 60
                Timerlabel_secs = Timerlabel_secs %60
            else:
                Timerlabel_mins += Timerlabel_secs // 60
                Timerlabel_secs = (Timerlabel_secs) %60
        if not 0 <= Timerlabel_mins <= 59:
            if Timerlabel_mins > 59:
                Timerlabel_mins = Timerlabel_mins %60
            else:
                Timerlabel_mins = (60 + Timerlabel_mins)
                Timerlabel_secs = (Timerlabel_secs) %60

        newtime = []
        for time_part in [Timerlabel_mins,Timerlabel_secs]:
            
            time_part = str(time_part)

            if len(time_part) == 1:
                time_part = f"0{time_part}"

            newtime.append(time_part)
    
        return f"{newtime[0]}:{newtime[1]}"

    def step():
        global num_change_TF
        global countdown

        # First, if the game is not in charades mode, the timer blinks
        if Timer_on_Screen._Timerlabel.get_label() != "??:??":
            Timer_on_Screen.blink()

            # Then, once the timer hits 00:00, the timer is stopped and the sound is played
            if Timer_on_Screen._Timerlabel.get_label() == "00:00":
                
                stop_time(Timer_on_Screen)
                countdown.stop()
                # pip uninstall playsound
                # pip install playsound==1.2.2
                playsound(f"{cwd}\\watsound.mp3", False)
            
            else:
                
                if num_change_TF:
                    Timer_on_Screen._Timerlabel.set_label(incr_decr(Timer_on_Screen._Timerlabel, 1, False))
                    num_change_TF = False

                else:
                    num_change_TF = True

    difficulty_levels = [[easynouns,easyadjs],[mediumnouns,mediumadjs],[hardnouns,hardadjs]]
    # FORMAT [[noun text file name, adjective text file name]]

    for level in difficulty_levels:
        level_nouns = level[0]
        level_adjs = level[1]
        noun_list = read_word_bag(level_nouns)
        adj_list = read_word_bag(level_adjs)
        level[0] = noun_list[:]
        level[1] = adj_list[:]

    # FORMAT [[noun list, adjective list]]

    # Initializes the stacks of nouns, shuffles the order of words
    global noun_list_putback
    noun_list_putback = [difficulty_levels[0][0][:],difficulty_levels[1][0][:]+difficulty_levels[0][0][:],difficulty_levels[2][0][:]+difficulty_levels[1][0][:]+difficulty_levels[0][0][:],[]]
    noun_list_takeout = list(noun_list_putback[:])
    easynounstack = Stack()
    mediumnounstack = Stack()
    hardnounstack = Stack()
    shuffle_and_fill(easynounstack, noun_list_takeout[0])
    shuffle_and_fill(mediumnounstack, noun_list_takeout[1])
    shuffle_and_fill(hardnounstack, noun_list_takeout[2])

    # Initializes the stacks of adjectives, shuffles the order of words

    global adj_list_putback

    adj_list_putback = [list(difficulty_levels[0][1][:]),list(difficulty_levels[1][1][:]+difficulty_levels[0][1][:]),list(difficulty_levels[2][1][:]+difficulty_levels[1][1][:]+difficulty_levels[0][1][:]),[]]
    adj_list_takeout = [list(difficulty_levels[0][1][:]),list(difficulty_levels[1][1][:]+difficulty_levels[0][1][:]),list(difficulty_levels[2][1][:]+difficulty_levels[1][1][:]+difficulty_levels[0][1][:]),[]]
    easyadjstack = Stack()
    mediumadjstack = Stack()
    hardadjstack = Stack()

    shuffle_and_fill(easyadjstack, adj_list_takeout[0])
    shuffle_and_fill(mediumadjstack, adj_list_takeout[1])
    shuffle_and_fill(hardadjstack, adj_list_takeout[2])

    global action_list_putback
    global action_list_takeout
    action_list_putback = read_word_bag(actions)
    action_list_takeout = read_word_bag(actions)
    actionstack = Stack()
    shuffle_and_fill(actionstack, action_list_putback)

    Active_Phrase_Actions = LinkedList()
    Active_Phrase_Adjectives = LinkedList()
    Active_Phrase_Nouns = LinkedList()
    
    # When called, if the stack is empty, then it is shuffled and filled again with words from the list
    def refill_if_empty_then_pop(stack, source):

        if stack.is_empty():
            shuffle_and_fill(stack, source)

        return(stack.pop())

    # This chunk of code here is the initialization of all of the GObjects that are added to the window 

    modebutton, modelabel = mode_switch_button(gw)
    n_change_frame = base_frame(gw, modebutton)
    summon_num_change_UI_button, n_picks_visualized = create_num_picks_button(gw, number_of_picks)
    numberchoices, num_buttons = create_n_choices(gw, n_change_frame)
    phrase_to_draw, backup = phrase_label_and_backup(gw)

    difficulty_button, difficulty_label = draw_gw_button_xywhLCFfc(gw, 2, 2, summon_num_change_UI_button.get_width()*1.5, summon_num_change_UI_button.get_height(), "MEDIUM", "#FFF200", "30pt 'Consolas'")

    zero_button, zero_label = draw_gw_button_xywhLCFfc(gw,Timer_on_Screen._compound.get_x()+155,Timer_on_Screen._compound.get_y()-61,Timer_on_Screen._Timerlabel.get_width()/2,Timer_on_Screen._Timerlabel.get_height()/2+2," ZERO ","lightgrey","15pt 'Consolas'")
    auto_button, auto_label = draw_gw_button_xywhLCFfc(gw,zero_button.get_x(),zero_button.get_y()+50,Timer_on_Screen._Timerlabel.get_width()/2,Timer_on_Screen._Timerlabel.get_height()/2+2," AUTO ","lightgrey","15pt 'Consolas'")
    save_background, save_icon_list, saved_label_list = draw_all_save_icons_and_background(gw, phrase_to_draw)
    saves_bg, SAVES_label = draw_gw_button_xywhLCFfc(gw,GWINDOW_WIDTH/2-87,17*gw.get_height()/20+14,87,Timer_on_Screen._Timerlabel.get_height()/2+2,"SAVES:","Aquamarine","15pt 'Consolas'")
    clear_player_button, clear_player_label = draw_gw_button_xywhLCFfc(gw,saves_bg.get_x()+saves_bg.get_width(),saves_bg.get_y(),Timer_on_Screen._Timerlabel.get_width()/2,Timer_on_Screen._Timerlabel.get_height()/2+2," WIPE ","lightgrey","15pt 'Consolas'")

    info_menu, info_label = draw_gw_button_xywhLCFfc(gw,GWINDOW_WIDTH,0,GWINDOW_WIDTH,GWINDOW_HEIGHT,"HOW TO PLAY:","#1e1e1e","20pt 'Consolas'","#fefefe")
    rules_button, rules_label = draw_gw_button_xywhLCFfc(gw,GWINDOW_WIDTH-100,GWINDOW_HEIGHT-50,Timer_on_Screen._Timerlabel.get_width()/2,Timer_on_Screen._Timerlabel.get_height()/2+2," INFO ","lightgrey","15pt 'Consolas'")
    nightlight_button, nightlight_label = draw_gw_button_xywhLCFfc(gw,rules_button.get_x()-100,GWINDOW_HEIGHT-50,87,Timer_on_Screen._Timerlabel.get_height()/2+2,"LIGHT","lightgrey","15pt 'Consolas'")
    # next_player_button, next_player_label = draw_gw_button_xywhLCFfc(gw,GWINDOW_WIDTH/2-nightlight_button.get_width()-8,17*gw.get_height()/20+14,rules_button.get_width(),rules_button.get_height()," NEXT ","lightgrey","15pt 'Consolas'")
    something_saved_label = just_draw_label(gw,-100,-100,"0")


    info_label.set_location(info_label.get_x(), 1+info_label.get_height())
    fun_label_1, fun_label_2, fun_label_3, fun_label_4, fun_label_5, fun_label_6, fun_label_7, fun_label_8, nothinglabel, glory_label_1,glory_label_2,glory_label_3,glory_label_4,glory_label_5= draw_fun_labels(gw,info_label)
    combined_rules_labels_fun_and_glory = [fun_label_1, fun_label_2, fun_label_3, fun_label_4, fun_label_5, fun_label_6, fun_label_7, fun_label_8, nothinglabel, glory_label_1,glory_label_2,glory_label_3,glory_label_4,glory_label_5]

    def click_action(e):
        # When the screen is clicked, the following code will run 
        
        global phrase_to_draw
        global ready_to_show
        global number_of_picks
        global countdown

        element = gw.get_element_at(e.get_x(),e.get_y())

        def determine_phrase_takeout(difficulty_level):
            #For takeout mode, this function determines the phrase to be shown on screen

            clear_linkedlist(Active_Phrase_Actions)

            # Number of picks is the number of words to display on the screen
            global number_of_picks
            global acting_question_mark

            # Determines which stacks to use based on difficulty level
            if difficulty_level == "ACTING":
                acting_question_mark = True
                difficulty_level = 3

            if difficulty_level == 0:
                adjectivestack = easyadjstack
                nounstack = easynounstack

            elif difficulty_level == 1 or acting_question_mark:
                adjectivestack = mediumadjstack
                nounstack = mediumnounstack

            else:
                adjectivestack = hardadjstack
                nounstack = hardnounstack

            if number_of_picks == "R":  # Chooses a random number from 2-9 for the number of picks
                number_of_picks = rng.randint(2,9)
                set_back_to_R_ping = True
                Timer_on_Screen._Timerlabel.set_label(f"0{number_of_picks}:00")

            else: # Whatever the number of picks is set at, sets that to the number of picks
                number_of_picks = int(number_of_picks)
                set_back_to_R_ping = False

            if number_of_picks > 1: 

                if acting_question_mark:
                    there_is_an_action_tf = True

                else:
                    there_is_an_action_tf = rng.choice([True,False])
                    
                if there_is_an_action_tf:
                    action = refill_if_empty_then_pop(actionstack, action_list_takeout)
                    Active_Phrase_Actions.append(Node(action))
                    action_list_takeout.append(action)

                else:
                    adjective = refill_if_empty_then_pop(adjectivestack, adj_list_takeout[difficulty_level]) # Takes an adjective out of the stack
                    Active_Phrase_Adjectives.append(Node(adjective)) # Adds the adjective to the linked list
                    adj_list_takeout[difficulty_level].append(adjective) # Appends the adjective to adj_list to keep track of which ones were used

            noun = refill_if_empty_then_pop(nounstack,noun_list_takeout[difficulty_level])
            Active_Phrase_Nouns.append(Node(noun))
            noun_list_takeout[difficulty_level].append(noun)

            if number_of_picks > 2:

                # For more than two words, this will choose randomly how many of the in-between words are adjectives or nouns
                for n in range(int(number_of_picks) - 2):
                    
                    if difficulty_level == "ACTING":
                        adj_or_n = rng.choice(["adj","adj","adj","adj","adj","adj","adj","adj","adj","adj","adj","n"])

                    else:
                        adj_or_n = rng.choice(["adj","n"])
                    
                    if adj_or_n == "adj":
                        adjective = refill_if_empty_then_pop(adjectivestack,adj_list_takeout[difficulty_level])
                        Active_Phrase_Adjectives.append(Node(adjective))
                        adj_list_takeout[difficulty_level].append(adjective)

                    else:
                        noun = refill_if_empty_then_pop(nounstack,noun_list_takeout[difficulty_level])
                        Active_Phrase_Nouns.append(Node(noun))
                        noun_list_takeout[difficulty_level].append(noun)

            # Adds the nouns to the adjectives in order to have the full phrase there
            curnode = Active_Phrase_Nouns.head
            while curnode != None:
                Active_Phrase_Adjectives.append(curnode)
                curnode = curnode.get_next()

            curnode = Active_Phrase_Actions.head
            if curnode != None:
                Active_Phrase_Adjectives.append(Node("that is"))
                while curnode != None:
                    Active_Phrase_Adjectives.append(curnode)
                    curnode = curnode.get_next()

            if set_back_to_R_ping:
                number_of_picks = "R"

            return Active_Phrase_Adjectives # Returns the full phrase with the adjectives + nouns
        
        def cycle_text_and_color(label_or_button, textlist = ["TEST", "test"], colorlist = ["#000000", "red"], label_or_button_is_a_labe1 = True):
            # When the button for the difficulty is clicked, the text and color of the button will cycle through

            if label_or_button_is_a_labe1:
                
                if len(textlist) > 1:
                    current = textlist.index(label_or_button.get_label())

                    if current != -1:
                        current = (current+1) % len(textlist)
                        label_or_button.set_label(textlist[current])
                        label_or_button.set_color(colorlist[current])

                else:
                    current = colorlist.index(label_or_button.get_color())

                    if current != -1:
                        current = (current+1) % len(colorlist)
                        label_or_button.set_color(colorlist[current])

            else:
                current = colorlist.index(label_or_button.get_fill_color())

                if current != -1:
                    current = (current+1) % len(colorlist)
                    label_or_button.set_fill_color(colorlist[current])
           
        def determine_phrase_putback(difficulty_level):
            global number_of_picks
            global adj_list_putback
            global noun_list_putback
            global action_list_putback
            

            if noun_list_putback[0]==[]:
                noun_list_putback[0]= read_word_bag(easynouns)
                noun_list_putback[1]= read_word_bag(mediumnouns) + noun_list_putback[0]
                noun_list_putback[2]= read_word_bag(hardnouns) + noun_list_putback[1]
                noun_list_putback[3]= read_word_bag(mediumnouns) + noun_list_putback[0]

            if action_list_putback == []:
                action_list_putback = read_word_bag(actions)
            
            if number_of_picks == "R":  # Chooses a random number from 2-9 for the number of picks
                number_of_picks = rng.randint(2,9)
                set_back_to_R_ping = True
                Timer_on_Screen._Timerlabel.set_label(f"0{number_of_picks}:00")

            else: # Whatever the number of picks is set at, sets that to the number of picks
                number_of_picks = int(number_of_picks)
                set_back_to_R_ping = False

            if number_of_picks > 1: 
                
                adj_or_action = rng.choice(["adj","action"])
                if adj_or_action == "adj":
                    adjective = rng.choice(adj_list_putback[difficulty_level]) # Takes an adjective from the list
                    Active_Phrase_Adjectives.append(Node(adjective)) # Adds the adjective to the linked list
                elif adj_or_action == "action":
                    action = rng.choice(action_list_putback) # Takes an action from the list
                    Active_Phrase_Actions.append(Node(action)) # Adds the adjective to the linked list
                
            noun = rng.choice(noun_list_putback[difficulty_level])
            Active_Phrase_Nouns.append(Node(noun))
            noun_list.append(noun)
            
            if number_of_picks > 2:

                # For more than two words, this will choose randomly how many of the in-between words are adjectives or nouns
                for i in range(int(number_of_picks) - 2):
                    adj_or_n = rng.choice(["adj","n"])
                    
                    if adj_or_n == "adj":
                        adjective = rng.choice(adj_list_putback[difficulty_level])

                        while is_in_linkedlist(Active_Phrase_Adjectives,adjective):
                           adjective = rng.choice(adj_list_putback[difficulty_level]) 

                        Active_Phrase_Adjectives.append(Node(adjective))

                    else:
                        noun = rng.choice(noun_list_putback[difficulty_level])

                        while is_in_linkedlist(Active_Phrase_Nouns,noun):
                           noun = rng.choice(noun_list_putback[difficulty_level]) 

                        Active_Phrase_Nouns.append(Node(noun))
            
            # Adds the nouns to the adjectives in order to have the full phrase there
            curnode = Active_Phrase_Nouns.head
            while curnode != None:
                Active_Phrase_Adjectives.append(curnode)
                curnode = curnode.get_next()

            curnode = Active_Phrase_Actions.head
            if curnode != None:
                Active_Phrase_Adjectives.append(Node("that is"))
                while curnode != None:
                    Active_Phrase_Adjectives.append(curnode)
                    curnode = curnode.get_next()
            
            if set_back_to_R_ping:
                number_of_picks = "R"


            return Active_Phrase_Adjectives # Returns the full phrase with the adjectives + nouns

        def flip_n_change_frame_and_num_buttons():

            # Flips the stuff from outside the GWindow to the inside of the GWindow

            if n_change_frame.get_x() >= GWINDOW_WIDTH:
                n_change_frame.move(-(3*GWINDOW_WIDTH/20 +.5*n_change_frame.get_width()),0)

            else:
                n_change_frame.move(+(3*GWINDOW_WIDTH/20 +.5*n_change_frame.get_width()),0)

            for item in num_buttons:
                item.flip_flop(gw,n_change_frame) # Flip flop is going to bring the stuff from outside the screen onto the screen.

            n_picks_visualized.set_label(number_of_picks)

        if element == modebutton or element == modelabel:
            global difficulty_before_changing_modes
            if Timer_on_Screen._ticking == False:
                # Once the button or label for the mode is clicked, the mode is switched
                # You can now no longer change the mode while the timer is running
                if modelabel.get_label()== "TAKEOUT MODE":
                    modelabel.set_label("PUTBACK MODE")
                    modebutton.set_fill_color("GreenYellow")
                    n_change_frame.set_fill_color("GreenYellow")
                    saves_bg.set_fill_color("GreenYellow")
                
                elif modelabel.get_label() == "PUTBACK MODE":
                    modelabel.set_label("CHARADE MODE")
                    modebutton.set_fill_color("Plum")
                    n_change_frame.set_fill_color("Plum")
                    global difficulty_before_changing_modes
                    difficulty_before_changing_modes = difficulty_label.get_label()
                    difficulty_button.set_fill_color("Plum")
                    difficulty_label.set_label("ACTING")
                    number_of_picks = 2
                    n_picks_visualized.set_label("2")
                    saves_bg.set_fill_color("Plum")

                else:
                    modelabel.set_label("TAKEOUT MODE")
                    modebutton.set_fill_color("Aquamarine")
                    n_change_frame.set_fill_color("Aquamarine")
                    saves_bg.set_fill_color("Aquamarine")

                    difficulty_label.set_label(difficulty_before_changing_modes)
                    pos = [" EASY ", "MEDIUM", " HARD "].index(difficulty_before_changing_modes)
                    difficulty_button.set_fill_color(["#50DF78","#FFF200","#F1595F"][pos])
                
        # (/'^')/ Praise be to the ELIF CHAIN \('^'\)       
        # Basically, if the element, which is the thing that is being clicked, is the same thing as the given label,
        # then the specified code runs

        elif element == difficulty_button or element == difficulty_label:

            if Timer_on_Screen._ticking == False:

                if difficulty_label.get_label() != "ACTING":
                    cycle_text_and_color(difficulty_label,[" EASY ", "MEDIUM", " HARD "], ["#000000","#000000","#000000"])
                    cycle_text_and_color(difficulty_button,["BUTTON"], ["#50DF78","#FFF200","#F1595F"],False)

        elif element == auto_button or element == auto_label:
            
            if Timer_on_Screen._ticking == False:
                
                if n_picks_visualized.get_label() != "R":
                    appropriate_time= int(n_picks_visualized.get_label())
                    Timer_on_Screen._Timerlabel.set_label(f"0{appropriate_time}:00")

                elif ready_to_show:
                    Timer_on_Screen._Timerlabel.set_label(f"??:??")

            # if auto_label.get_label() == " AUTO ":
            #     auto_label.set_label("MANUAL")
            # elif auto_label.get_label() == "MANUAL":
            #     auto_label.set_label(" AUTO ")
        
        elif element == zero_button or element == zero_label:
            if Timer_on_Screen._ticking == False:
                
                Timer_on_Screen._Timerlabel.set_label(f"00:00")

        elif element == rules_button or element == rules_label:
            
            if Timer_on_Screen._ticking == False:
                flip_over_vertical_screen_edge(gw, info_label)
                flip_over_vertical_screen_edge(gw, info_menu)
                cycle_text_and_color(rules_label, [" INFO "," EXIT "], ["#000000","#f0000f"])

                for fun_label in combined_rules_labels_fun_and_glory:
                    flip_over_vertical_screen_edge(gw, fun_label)
            
        elif element == nightlight_button or element == nightlight_label:
            
            if nightlight_label.get_label() == "LIGHT":

                background.set_color("white")
                background.set_fill_color("white")

                for label in saved_label_list:
                    label.set_color("#000000")

                Timer_on_Screen._unred = "#000000"
                info_menu.set_color("white")
                info_menu.set_fill_color("white")

                if Timer_on_Screen._Timerlabel.get_color != Timer_on_Screen._red:
                    Timer_on_Screen._Timerlabel.set_color("#000000")


                
            else:
                background.set_color("#1e1e1e")
                background.set_fill_color("#1e1e1e")

                for label in saved_label_list:
                    label.set_color("#1E1E1E")

                Timer_on_Screen._unred = "#fefefe"
                info_menu.set_color("#1E1E1E")
                info_menu.set_fill_color("#1E1E1E")

                if Timer_on_Screen._Timerlabel.get_color != Timer_on_Screen._red:
                    Timer_on_Screen._Timerlabel.set_color("#fefefe")

            cycle_text_and_color(info_label, [f"{info_label.get_label()}"], ["#000000","#FEFEFE"])
            for fun_label in combined_rules_labels_fun_and_glory:
                cycle_text_and_color(fun_label, ["MADE BY EVAN WYLIE, THOMAS SATO, AND HRIDAY RAJ"],["#000000","#FEFEFE"])

            cycle_text_and_color(nightlight_label,["NIGHT","LIGHT"],["#000000","#000000"])
            cycle_text_and_color(phrase_to_draw, [" :) "], ["#000000","#FEFEFE"])

        elif element in save_icon_list:
            if Timer_on_Screen._ticking == False:
            
                corresponding_label_to_save_icon = saved_label_list[save_icon_list.index(element)]

                if phrase_to_draw.get_label() == "" or phrase_to_draw.get_label() == phrase_saved or phrase_to_draw.get_label() == " ":

                    if type(corresponding_label_to_save_icon) is GLabel and corresponding_label_to_save_icon.get_label() != "" and corresponding_label_to_save_icon.get_label() != phrase_saved:
                        phrase_to_draw.set_label(corresponding_label_to_save_icon.get_label())
                        something_saved_label.set_label(f"{int(something_saved_label.get_label())-1}")
                        corresponding_label_to_save_icon.set_label(phrase_saved)
                    

                        


                elif phrase_to_draw.get_label() != "cleared saves!":
                        something_saved_label.set_label(f"{int(something_saved_label.get_label())+1}")
                        holding_a_phrase_for_a_moment = phrase_to_draw.get_label()
                        phrase_to_draw.set_label(phrase_saved)
                        corresponding_label_to_save_icon.set_label(holding_a_phrase_for_a_moment)
                        

                phrase_to_draw.set_location((gw.get_width() - phrase_to_draw.get_width()) / 2 , y = (gw.get_height() + phrase_to_draw.get_ascent()) / 2)

        # elif element == next_player_button or element == next_player_label:
        #     global next_player_phrase
        #     global next_player_index


        #     print(next_player_index)
        #     if saved_label_list[next_player_index].get_label() != "" and str(saved_label_list[next_player_index]) != phrase_saved:
        #         next_player_phrase = saved_label_list[next_player_index].get_label()
        #         phrase_to_draw.set_label(next_player_phrase)
        #     next_player_index = (next_player_index + 1) % (len(saved_label_list)-1)
        #     if int(something_saved_label.get_label()) > 0:
        #         next_player_base = next_player_index
        #         while saved_label_list[next_player_index].get_label() == "" or saved_label_list[next_player_index].get_label() == phrase_saved:
        #             next_player_index = (next_player_index + 1)
        #             if next_player_index > next_player_index + len(saved_label_list):
        #                 next_player_index = next_player_index % (len(saved_label_list)-1)
        #                 phrase_to_draw.set_location((gw.get_width() - phrase_to_draw.get_width()) / 2 , y = (gw.get_height() + phrase_to_draw.get_ascent()) / 2)


                if phrase_to_draw.get_label() != "":
                    ready_to_show = False
                else:
                    ready_to_show = True

        elif element == clear_player_button or element == clear_player_label:

            if Timer_on_Screen._ticking == False:

                for label in saved_label_list:
                    label.set_label(phrase_saved)

                something_saved_label.set_label("0")
                phrase_to_draw.set_label("cleared saves!")
                phrase_to_draw.set_location((gw.get_width() - phrase_to_draw.get_width()) / 2 , y = (gw.get_height() + phrase_to_draw.get_ascent()) / 2)

                if phrase_to_draw.get_label() != "":
                    ready_to_show = False

                else:
                    ready_to_show = True

        elif type(element) == GCompound:

            TimerCompound = Timer_on_Screen._compound
            Timerlabel = Timer_on_Screen._Timerlabel
            colon = Timer_on_Screen._colon
            
            localx = e.get_x()-TimerCompound.get_x()
            localy = e.get_y()-TimerCompound.get_y()
            if type(TimerCompound.get_element_at(localx,localy)) == GPolygon :
                if Timer_on_Screen.is_pause() and Timerlabel.get_label() != "??:??":
                    
                    if localx < (Timerlabel.get_width()-colon.get_width())/4:

                        if localy > 0:
                            # Timerlabel_mins -= 10
                            Timer_on_Screen._Timerlabel.set_label(incr_decr(Timerlabel,600,False))

                        else:
                            # Timerlabel_mins += 10
                            Timer_on_Screen._Timerlabel.set_label(incr_decr(Timerlabel,600))

                    elif localx < (Timerlabel.get_width()-colon.get_width())/2:

                        if localy > 0:
                            # Timerlabel_mins -= 1
                            Timer_on_Screen._Timerlabel.set_label(incr_decr(Timerlabel,60,False))

                        else:
                            # Timerlabel_mins += 1
                            Timer_on_Screen._Timerlabel.set_label(incr_decr(Timerlabel,60))

                    elif localx < 3*(Timerlabel.get_width()-colon.get_width())/4+colon.get_width():

                        if localy > 0:
                            # Timerlabel_secs -= 10
                            Timer_on_Screen._Timerlabel.set_label(incr_decr(Timerlabel,10,False))

                        else:
                            # Timerlabel_secs += 10
                            Timer_on_Screen._Timerlabel.set_label(incr_decr(Timerlabel,10))

                    else:

                        if localy > 0:
                            # Timerlabel_secs -= 1
                            Timer_on_Screen._Timerlabel.set_label(incr_decr(Timerlabel,1,False))

                        else:
                            # Timerlabel_secs += 1
                            Timer_on_Screen._Timerlabel.set_label(incr_decr(Timerlabel,1))

            elif type(TimerCompound.get_element_at(localx,localy)) == GCompound:

                if not Timer_on_Screen._ticking and Timer_on_Screen._Timerlabel.get_label() != "??:??":
                    countdown= gw.set_interval(step,TIME_STEP)
                    Timer_on_Screen.play_pause()
                    Timer_on_Screen._ticking = True

                elif Timer_on_Screen._ticking:
                    stop_time(Timer_on_Screen)
                    countdown.stop()
                        
        elif element == summon_num_change_UI_button or element == n_picks_visualized:

            # If the top right button is clicked, it will pull up the menu to chancge the number of words in the phrase
            flip_n_change_frame_and_num_buttons()
            
        elif type(element) is GLabel and element.get_label() in numberchoices:

            # This is clicking one of the options for number of words, then pushing the menu off-screen
            number_of_picks = element.get_label()
            flip_n_change_frame_and_num_buttons()
            
        elif ready_to_show and (element == background or element == phrase_to_draw or element == backup or element == None):

            if difficulty_label.get_label() != "ACTING":
                difficulty_level = [" EASY ", "MEDIUM", " HARD "].index(difficulty_label.get_label())

            else:
                difficulty_level = "ACTING"

            # If you click the screen anywhere else, it will run this algorithm and put text on the screen
            if modelabel.get_label() == "TAKEOUT MODE":
                Active_Phrase_Total = determine_phrase_takeout(difficulty_level)
                
            elif modelabel.get_label() == "PUTBACK MODE":
                Active_Phrase_Total = determine_phrase_putback(difficulty_level)

            else:
                Active_Phrase_Total = determine_phrase_takeout("ACTING")

            curnode = Active_Phrase_Total.head
            
            

            phrasetext = ""
            while curnode != None and curnode != []:

                # Traverses the list of the whole phrase and puts that into a string to be displayed on screen
                phrasetext += curnode.get_data()
                phrasetext += " "
                curnode = curnode.next

            phrasetext.removesuffix(" ")
            center_phrase_to_draw(gw, phrase_to_draw, phrasetext,backup)
            

            # Flag that indicates whether text is already on the screen or not is set to False
            ready_to_show = False

        else:

            for list in [Active_Phrase_Adjectives, Active_Phrase_Nouns, Active_Phrase_Actions]:
                clear_linkedlist(list)

            # Flag that indicates whether text is already on the screen or not is set to True
            ready_to_show = True
            phrase_to_draw.set_label("")
            backup.set_label("")

    gw.add_event_listener("click", click_action)


# Borrowed from Professor Roberts' Adventure Project
# Revised noun lists sourced heavily from https://a-z-animals.com/animals/
def read_word_bag(f):
    """Reads the entire word bag from the file."""
    f = open(f"{cwd}\\{f}")
    list = []
    reading = True
    while reading:

        name = f.readline().rstrip()             # Read the word
        if name == "":                           # Returning None at the end
            reading = False
        else:
            list.append(name)

    return list

if __name__ == "__main__":
    what_are_those("easy_nouns.txt",
                   "medium_nouns.txt",
                   "hard_nouns.txt",
                   "easy_adjectives.txt",
                   "medium_adjectives.txt",
                   "hard_adjectives.txt",
                   "verbs_and_more.txt")