from pgl import GWindow, GLine, GOval, GRect, GPolygon, GLabel, GCompound

# Window Dimensions
GWINDOW_WIDTH = 1250
GWINDOW_HEIGHT = 500

#gw = GWindow(GWINDOW_WIDTH,GWINDOW_HEIGHT)


class n_picks_switch_key:
    
    def __init__(self, name):
        self._name = name
        self._text = None

    def form_sub_button(self, gw, x, y):  # Adds button to the GWindow with x and y coordinates
        self._text = GLabel(f"{self._name}")

        self._text.set_font("20pt 'Comic Sans MS','Serif','bold'")
        self._text.set_color("black")

        gw.add(self._text, x, y)

    def flip_flop(self, n_change_frame):
        if self._text.get_x() >= GWINDOW_WIDTH:
            self._text.move(-(3*GWINDOW_WIDTH/20 +.5*n_change_frame.get_width()),0)
        else:
            self._text.move(+(3*GWINDOW_WIDTH/20 +.5*n_change_frame.get_width()),0)

# Creating mode switch button
def mode_switch_button(gw):
    # Returns tuple containing the GObjects for both the button and the label

    # Adds the mode button to the screen ("Takeout Mode" or "Putback mode")
    modebutton = GRect(gw.get_width()/4,2,gw.get_width()/2,gw.get_height()/10)
    modebutton.set_filled(True)
    modebutton.set_fill_color("Aquamarine")
    gw.add(modebutton) #create button visuals

    # Adds the label itself to the screen
    modelabel = GLabel(f"Takeout Mode")
    modelabel.set_font("20pt 'Comic Sans MS','Serif','bold'")
    modelabel.set_color("black")
    x = (gw.get_width() - modelabel.get_width()) / 2 
    y = (2 + .75*gw.get_height()/10)   
    gw.add(modelabel, x, y)

    return (modebutton, modelabel)

# Initializes and adds the phrase label to the screen
def phrase_label(gw):

    phrase_to_draw = GLabel(f" ")
    phrase_to_draw.set_font("20pt 'Century Schoolbook','Serif','bold'")
    phrase_to_draw.set_color("black")
    x = (gw.get_width() - phrase_to_draw.get_width()) / 2 
    y = (gw.get_height() + phrase_to_draw.get_ascent()) / 2 
    gw.add(phrase_to_draw, x, y)
        
    return phrase_to_draw

# Centers the text on the screen
def center_phrase_to_draw(gw, phrase_to_draw, new_text):

    phrase_to_draw.set_label(new_text)
    phrase_to_draw.set_location((gw.get_width() - phrase_to_draw.get_width()) / 2 ,
                                y = (gw.get_height() + phrase_to_draw.get_ascent()) / 2)

def create_num_picks_button(gw, number_of_picks):

    # GRect object for the number of picks button
    summon_num_change_UI_button = GRect(17*gw.get_width()/20, 2, 2*gw.get_width()/20, gw.get_height()/10)
    summon_num_change_UI_button.set_filled(True)
    summon_num_change_UI_button.set_fill_color("lightgrey")
    gw.add(summon_num_change_UI_button)

    # Label on the number of picks button, R-9
    n_picks_visualized = GLabel(f"{number_of_picks}")
    n_picks_visualized.set_font("20pt 'Comic Sans MS','Serif','bold'")
    n_picks_visualized.set_color("black")
    x = (18*gw.get_width()/20 - n_picks_visualized.get_width()/2)  
    y = (2 + .75*gw.get_height()/10)   
    gw.add(n_picks_visualized, x, y)

    return (summon_num_change_UI_button, n_picks_visualized) # Returns these two for the elif statement later on in the main program

# Adds a base frame to the GWindow in order for it to be manipulated when adding the 10 other boxes to it
def base_frame(gw, modebutton):

    n_change_frame = GRect(GWINDOW_WIDTH, GWINDOW_HEIGHT/10+6, 194, 60)
    n_change_frame.set_filled(True)
    n_change_frame.set_fill_color(modebutton.get_fill_color())
    gw.add(n_change_frame)

    return n_change_frame

def create_n_choices(gw, n_change_frame):
    numberchoices = ["R","1","2","3","4","5","6","7","8","9",]
    num_buttons = []
    x = n_change_frame.get_x() + 2

    for item in range(len(numberchoices)):

        num_buttons.append(n_picks_switch_key(numberchoices[item]))

        if item <= 4 : 
            y = (n_change_frame.get_y()+gw.get_height()/20 +2)
            
        else:
            y = n_change_frame.get_y() + n_change_frame.get_height()-4

        x = n_change_frame.get_x() + 8 + 40 * (item%5)
        
        num_buttons[item].form_sub_button(gw, x, y) # Adds the button corresponding with the given item in numberchoices to the GWindow

    return numberchoices, num_buttons
