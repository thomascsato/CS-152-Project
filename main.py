# Main program file

# Imports
import random as rng
from pgl import GWindow, GLine, GOval, GRect, GPolygon, GLabel, GCompound
from datastructures import Node, LinkedList, Stack, clear_linkedlist, is_in_linkedlist, shuffle_and_fill
from pglstuff import mode_switch_button, base_frame, create_num_picks_button, create_n_choices, center_phrase_to_draw, phrase_label

# Constants
global ready_to_show
global number_of_picks
number_of_picks = 3
ready_to_show = True

GWINDOW_WIDTH = 1250
GWINDOW_HEIGHT = 500

gw = GWindow(GWINDOW_WIDTH,GWINDOW_HEIGHT)

def what_are_those(nouns,adjs):
    global phrase_to_draw
    global ready_to_show    

    # Lists of words that will be displayed in the program
    noun_list = ['penguin', 'elephant', 'lion', 'tortoise', 'dog', 'bee', 'monkey', 'alligator', 'dolphin', 'badger', 'snake', 'ant', 'wolf', 'armadillo', 'beetle', 'pelican', 'axolotl', 'fish', 'squid', 'ferret', 'spider', 'rhino', 'shark', 'octopus', 'whale', 'worm', 'mouse', 'mole', 'cat', 'butterfly', 'moth', 'scorpion', 'goose', 'fox', 'capybara', 'centipede', 'chicken', 'wasp', 'frog', 'toad', 'hippo', 'lizard', 'newt', 'seal', 'snail', 'hawk', 'crab', 'crocodile', 'pig', 'dragonfly', 'dragon', 'platypus', 'otter', 'fungus', 'amongus', 'eel', 'seaturtle', 'bat', 'orca', 'iguana', 'ray', 'whaleshark', 'anteater', 'panda', 'bear', 'gorilla', 'scarab', 'hermitcrab', 'jellyfish', 'cobra', 'mongoose', 'llama', 'mantisshrimp', 'opossum', 'piranha', 'mantis', 'rabbit', 'seaurchin', 'lobster', 'walrus', 'tank', 'mecha', 'jetplane', 'flytrap', 'hedgehog', 'goat', 'human', 'cactus', 'plesiosaur', 'chamelion', 'gecko', 'propellerplane', 'rat', 'seacucumber', 'hummingbird', 'trex', 'raptor', 'triceratops', 'pteranodon', 'motorcycle', 'armor', 'pufferfish', 'catfish', 'groundhog', 'cicada', 'president', 'warrior', 'toilet', 'ent', 'chandelier', 'clam', 'cow', 'clock', 'virus', 'racecar', 'bus', 'towtruck', 'sloth', 'scarecrow', 'palmtree', 'barrel', 'safe', 'rug', 'crane']
    noun_list = ["pig", "cow"]
    adj_list = ['icy', 'burning', 'metallic', 'stretchy', 'steampunk', 'fancy', 'round', 'stony', 'artistic', 'lasering', 'shielded', 'sneaky', 'psychic', 'devious', 'ghostly', 'bladed', 'spectacled', 'venomous', 'strong', 'mechanical', 'magical', 'armed', 'dangerous', 'cool', 'explosive', 'electric', 'slimy', 'armored', 'eccentric', 'smoky', 'crystalline', 'spotted', 'striped', 'frightening', 'frightened', 'shaded', 'skeletal', 'royal', 'abstract', 'futuristic', 'ancient', 'prehistoric', 'triangular', 'scrap-iron', 'armored', 'blanketed']

    # Initializes the stack of nouns, shuffles the order of words
    nounstack = Stack()
    shuffle_and_fill(nounstack, noun_list)

    # Initializes the stack of adjectives, shuffles the order of words
    adjectivestack = Stack()
    shuffle_and_fill(adjectivestack,adj_list)

    # Creating the linked lists for the adjectives and nouns in the phrase to be shown on screen
    Active_Phrase_Adjectives = LinkedList()
    Active_Phrase_Nouns = LinkedList()
    
    # When called, if the stack is empty, then it is shuffled and filled again with words from the list
    def refill_if_empty_then_pop(stack, source):

        if stack.isempty():
            shuffle_and_fill(stack, source)

        return(stack.pop())


    def click_action(e):
        # When the screen is clicked, the following code will run

        global phrase_to_draw
        global ready_to_show
        global number_of_picks

        def determine_phrase():
            global number_of_picks
            if number_of_picks == "R":  # Chooses a random number from 2-9 for the number of picks
                number_of_picks = rng.randint(2,9)
                set_back_to_R_ping = True

            else: # Whatever the number of picks is set at, sets that to the number of picks
                number_of_picks = int(number_of_picks)
                set_back_to_R_ping = False

            if number_of_picks > 1: 
                adjective = refill_if_empty_then_pop(adjectivestack, adj_list) # Takes an adjective out of the stack
                Active_Phrase_Adjectives.append(Node(adjective)) # Adds the adjective to the linked list
                adj_list.append(adjective) # Appends the adjective to adj_list to keep track of which ones were used

            noun = refill_if_empty_then_pop(nounstack,noun_list)
            Active_Phrase_Nouns.append(Node(noun))
            noun_list.append(noun)
            
            if number_of_picks > 2:

                # For more than two words, this will choose randomly how many of the in-between words are adjectives or nouns
                for n in range(int(number_of_picks) - 2):
                    adj_or_n = rng.choice(["adj","n"])
                    
                    if adj_or_n == "adj":
                        adjective = refill_if_empty_then_pop(adjectivestack,adj_list)
                        Active_Phrase_Adjectives.append(Node(adjective))
                        adj_list.append(adjective)

                    else:
                        noun = refill_if_empty_then_pop(nounstack,noun_list)
                        Active_Phrase_Nouns.append(Node(noun))
                        noun_list.append(noun)

            # Adds the nouns to the adjectives in order to have the full phrase there
            curnode = Active_Phrase_Nouns.head
            while curnode != None:
                Active_Phrase_Adjectives.append(curnode)
                curnode = curnode.get_next()

            if set_back_to_R_ping:
                number_of_picks = "R"

            return Active_Phrase_Adjectives # Returns the full phrase with the adjectives + nouns
            
        modebutton, modelabel = mode_switch_button(gw)
        n_change_frame = base_frame(gw, modebutton)
        summon_num_change_UI_button, n_picks_visualized = create_num_picks_button(gw, number_of_picks)
        numberchoices, num_buttons = create_n_choices(gw, n_change_frame)
        phrase_to_draw = phrase_label(gw)
        element = gw.get_element_at(e.get_x(),e.get_y())

        def flip_n_change_frame_and_num_buttons():

            if n_change_frame.get_x() >= GWINDOW_WIDTH:
                        n_change_frame.move(-(3*GWINDOW_WIDTH/20 +.5*n_change_frame.get_width()),0)

            else:
                n_change_frame.move(+(3*GWINDOW_WIDTH/20 +.5*n_change_frame.get_width()),0)

            for item in num_buttons:
                item.flip_flop()

            n_picks_visualized.set_label(number_of_picks)

        if element == modebutton or element == modelabel:

            # Once the button or label for the mode is clicked, the mode is switched
            if modelabel.get_label() == "Putback Mode":
                modelabel.set_label("Takeout Mode")
                modebutton.set_fill_color("Aquamarine")
                n_change_frame.set_fill_color("Aquamarine")

            else:
                modelabel.set_label("Putback Mode")
                modebutton.set_fill_color("GreenYellow")
                n_change_frame.set_fill_color("GreenYellow")

        elif element == summon_num_change_UI_button or element == n_picks_visualized:
            flip_n_change_frame_and_num_buttons()
            
                
        elif type(element) is GLabel and element.get_label() in numberchoices:
            number_of_picks = element.get_label()
            flip_n_change_frame_and_num_buttons()
            
            
        elif ready_to_show and element != n_change_frame:
            Active_Phrase_Total = determine_phrase()
            curnode = Active_Phrase_Total.head
            
            phrasetext = ""
            while curnode != None:
                print(curnode.get_data())
                phrasetext += curnode.get_data()
                phrasetext += " "
                curnode = curnode.next

            phrasetext.removesuffix(" ")
            center_phrase_to_draw(gw, phrasetext)
            print(phrasetext)
            ready_to_show = False

        else:
            for list in [Active_Phrase_Adjectives, Active_Phrase_Nouns]:
                clear_linkedlist(list)

            ready_to_show = True
            phrase_to_draw.set_label(" ")
        

    gw.add_event_listener("click", click_action)

if __name__ == "__main__":
    what_are_those("nouns.txt", "adjectives.txt")