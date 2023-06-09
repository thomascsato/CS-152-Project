import math
from pgl import GWindow, GLine, GOval, GRect, GPolygon, GLabel, GCompound

# Window Dimensions


#gw = GWindow(GWINDOW_WIDTH,GWINDOW_HEIGHT)


class n_picks_switch_key:
    
    def __init__(self, name):
        self._name = name
        self._text = None

    def form_sub_button(self, gw, x, y):  # Adds button to the GWindow with x and y coordinates
        self._text = GLabel(f"{self._name}")

        self._text.set_font("30pt 'Consolas','bold'")
        self._text.set_color("black")

        gw.add(self._text, x, y)

    def flip_flop(self,gw, n_change_frame):
        # This function brings the off-screen object and brings it onto the screen so it is visible.

        if self._text.get_x() >= gw.get_width():
            self._text.move(-(3*gw.get_width()/20 +.5*n_change_frame.get_width()),0)

        else:
            self._text.move(+(3*gw.get_width()/20 +.5*n_change_frame.get_width()),0)

# Creating function to cause "Info" menu to appear/ disappear
def flip_over_vertical_screen_edge(gw, GObject):


    if GObject.get_x() >= gw.get_width(): 
        GObject.set_location( GObject.get_x() % gw.get_width() ,GObject.get_y())
    elif 0 <= GObject.get_x() < gw.get_width():
        GObject.set_location(gw.get_width() + GObject.get_x(),GObject.get_y()) 

# Creating mode switch button
def mode_switch_button(gw):
    # Returns tuple containing the GObjects for both the button and the label

    # Adds the mode button to the screen ("TAKEOUT MODE" or "PUTBACK MODE")
    modebutton = GRect(gw.get_width()/4,2,gw.get_width()/2,gw.get_height()/10)
    modebutton.set_filled(True)
    modebutton.set_fill_color("Aquamarine")
    gw.add(modebutton) #create button visuals

    # Adds the label itself to the screen
    modelabel = GLabel(f"TAKEOUT MODE")
    modelabel.set_font("30pt 'Consolas','bold'")
    modelabel.set_color("black")
    x = (gw.get_width() - modelabel.get_width()) / 2 
    y = (2 + .75*gw.get_height()/10)   
    gw.add(modelabel, x, y)

    return (modebutton, modelabel)

# Initializes and adds the phrase label to the screen
def phrase_label_and_backup(gw):

    phrase_to_draw = GLabel(f" ")
    phrase_to_draw.set_font("30pt 'Century Schoolbook','Serif','bold'")
    phrase_to_draw.set_color("#FEFEFE")
    x = (gw.get_width() - phrase_to_draw.get_width()) / 2 
    y = (gw.get_height() + phrase_to_draw.get_ascent()) / 2 
    gw.add(phrase_to_draw, x, y)
    backup = GLabel(f" ")
    backup.set_font("30pt 'Century Schoolbook','Serif','bold'")
    backup.set_color("#FEFEFE")
    x = (gw.get_width() - backup.get_width()) / 2 
    y = (gw.get_height() + backup.get_ascent()) / 2 
    gw.add(backup, x, y)
        
    return phrase_to_draw, backup

# From Todd Gamblin on stackoverflow
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start




# Centers the text on the screen
def center_phrase_to_draw(gw, phrase_to_draw, new_text, backup = None):

    phrase_to_draw.set_label(new_text)
    if phrase_to_draw.get_width() >= 11*gw.get_width()/12:
        number_of_spaces = new_text.count(" ")

        if number_of_spaces % 2 != 0:
            number_of_spaces += 1

        position_of_midway_space = find_nth(new_text," ",number_of_spaces//2)
        phrase_first_half = new_text[0:position_of_midway_space]
        phrase_second_half = new_text[position_of_midway_space:]

        phrase_to_draw.set_label(phrase_first_half)
        phrase_to_draw.set_location((gw.get_width() - phrase_to_draw.get_width())/2,
                                y = (gw.get_height())/2-15)
        if backup != None:
            backup.set_label(phrase_second_half)
            backup.set_location((gw.get_width() - backup.get_width()) / 2 ,
                                    y = (gw.get_height()+phrase_to_draw.get_ascent())/2+15)
            
    else:
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
    n_picks_visualized.set_font("30pt 'Consolas','bold'")
    n_picks_visualized.set_color("black")
    x = (18*gw.get_width()/20 - n_picks_visualized.get_width()/2)  
    y = (2 + .75*gw.get_height()/10)   
    gw.add(n_picks_visualized, x, y)

    return (summon_num_change_UI_button, n_picks_visualized) # Returns these two for the elif statement later on in the main program

# Adds a base frame to the GWindow in order for it to be manipulated when adding the 10 other boxes to it
def base_frame(gw, modebutton):

    n_change_frame = GRect(21*gw.get_width()/20, 2+gw.get_height()/10+6, 194, 96)
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
            y = n_change_frame.get_y() + n_change_frame.get_height()-8

        x = n_change_frame.get_x() + 8 + 40 * (item%5)
        
        num_buttons[item].form_sub_button(gw, x, y) # Adds the button corresponding with the given item in numberchoices to the GWindow

    return numberchoices, num_buttons

class Timerclass:
    def __init__(self):

        self._text = None
        self._ticking = False
        self._display_time = "00:00"
        self._compound = None
        self._Timerlabel = None
        self._color_change_ok = True
        self._unred = "#fefefe"
        self._red = "#F0000F"
        self._play = "  ⏵  "
        self._pause = "  ⏹  "



    def draw_compound(self,gw):
        self._compound = GCompound()
        self._Timerlabel = GLabel(self._display_time,0,-3)
        self._Timerlabel.set_font("40pt 'Consolas','bold'")
        self._Timerlabel.set_color(self._unred)
        self._compound.set_location(gw.get_width()/10-0.5*self._Timerlabel.get_width(),5*gw.get_height()/6-6)
        self._compound.add(self._Timerlabel)
        negation_when_needed_for_timer_setup = 1
        for i in range(8):
            up_down_button = GPolygon()
            zero = GLabel("0")
            zero.set_font(self._Timerlabel.get_font())
            self._colon = GLabel(":")
            self._colon.set_font(self._Timerlabel.get_font())

            if i >= 4:
                negation_when_needed_for_timer_setup = -1

            if i % 4 >= 2:
                offset_with_colon = self._colon.get_width()

            else:
                offset_with_colon = 0

            up_down_button.add_vertex(i%4*zero.get_width()+offset_with_colon,(-self._Timerlabel.get_height()/2)*negation_when_needed_for_timer_setup-10-10*(1-negation_when_needed_for_timer_setup))
            for b in range(3):
                up_down_button.add_polar_edge(zero.get_width(),120*b*negation_when_needed_for_timer_setup)

            up_down_button.set_filled(True)
            up_down_button.set_fill_color(f"lightgrey")

            self._compound.add(up_down_button)
        
        start_stop_button = GCompound()
        start_stop_button.set_location((self._Timerlabel.get_width())/4,40)
        ss_button_boundary = GRect(self._Timerlabel.get_width()/2,self._Timerlabel.get_height()/2+2)
        ss_button_boundary.set_color("#000000")
        ss_button_boundary.set_filled(True)
        ss_button_boundary.set_fill_color("lightgrey")
        start_stop_button.add(ss_button_boundary)
        self.ss_text = GLabel(self._play)
        self.ss_text.set_font("20pt 'Consolas','bold'")
        self.ss_text.set_location(ss_button_boundary.get_width()/2-self.ss_text.get_width()/2,ss_button_boundary.get_height()-6)
        start_stop_button.add(self.ss_text)
        self._compound.add(start_stop_button)
        gw.add(self._compound)
        

    def is_pause(self):
        # Returns a boolean flag that tells if the timer is paused or not
            
        if self.ss_text.get_label() == self._play:
            return True
        
        else:
            return False

    def play_pause(self):
        # Switches between having the timer count down, and having the timer in a pasued state

        if self.is_pause():
            self.ss_text.set_label(self._pause)
            self._color_change_ok = True

        else:
            self.ss_text.set_label(self._play)
            self._color_change_ok = False

    def blink(self):
        # If the timer is going, it will make the timer "blink," or change colors from red to black or black to red 

        if self._color_change_ok:

            if self._Timerlabel.get_color() != self._red:
                self._Timerlabel.set_color(self._red)

            else:
                self._Timerlabel.set_color(self._unred)
        
def draw_gw_button_xywhLCFfc(gw, x = 0, y = 0, width = 10, height = 10, labeltext = "", color = "lightgrey", font = "20pt 'Consolas'", fontcolor = "black", ycorfa = 2):
    # Returns tuple containing the GObjects for both the button and the label

    # Adds the mode button to the screen ("TAKEOUT MODE" or "PUTBACK MODE")
    button = GRect(x,y,width,height)
    button.set_filled(True)
    button.set_fill_color(color)
    gw.add(button) #create button visuals

    # Adds the label itself to the screen
    label = GLabel(labeltext)
    label.set_font(font)
    label.set_color(fontcolor)
    midline = label.get_height()/2

    if width <= label.get_width():
        width = label.get_width() + 20
        labx = x + 10

    else:
        labx = x+(width -label.get_width())/2

    if height < label.get_height():
        height= label.get_height() + 20
        laby = y+ midline + 10

    else:
        laby = y+ height/2 + midline -ycorfa

    gw.add(label, labx, laby)

    return (button, label)

def just_draw_label(gw, x, y, labeltext, font="20pt 'Consolas'", ycorfa = 2, part_of_something_greater = False):
    # Initializes a GLabel with specified parameters

    label = GLabel(labeltext)
    label.set_font(font)
    label.set_color("black")

    labx = x
    laby = y
    gw.add(label, labx, laby)

    return label

def draw_fun_labels(gw, info):
    # Initializes the labels for the info screen

    fun_label_1 = just_draw_label(gw, gw.get_width()+11, info.get_y() + info.get_height()+10,"PLAYING, SOLO STYLE:")
    fun_label_2 = just_draw_label(gw, gw.get_width()+11, fun_label_1.get_y() + fun_label_1.get_height()+10,"> Set the timer in the lower left corner.")
    fun_label_3 = just_draw_label(gw, gw.get_width()+11, fun_label_2.get_y() + fun_label_2.get_height()+10,"> Set the phrase length in the top right corner.")
    fun_label_4 = just_draw_label(gw, gw.get_width()+11, fun_label_3.get_y() + fun_label_3.get_height()+10,"> Click the screen, and a phrase will appear.")
    fun_label_5 = just_draw_label(gw, gw.get_width()+11, fun_label_4.get_y() + fun_label_4.get_height()+10,"> Remember your phrase, click again to hide your phrase.")
    fun_label_6 = just_draw_label(gw, gw.get_width()+11, fun_label_5.get_y() + fun_label_5.get_height()+10,"> Pass the device to the next person.")
    fun_label_7 = just_draw_label(gw, gw.get_width()+11, fun_label_6.get_y() + fun_label_6.get_height()+10,"> Start the timer after all players have a phrase.")
    fun_label_8 = just_draw_label(gw, gw.get_width()+11, fun_label_7.get_y() + fun_label_7.get_height()+10,"> Once the timer is up, guess other players' phrases!")
    nothinglabel = just_draw_label(gw, gw.get_width()+11, fun_label_8.get_y() + fun_label_8.get_height()+10,"")
    glory_label_1 = just_draw_label(gw, gw.get_width()+11, nothinglabel.get_y() + nothinglabel.get_height()+10,"PLAYING, ALLPLAY STYLE:")
    glory_label_2 = just_draw_label(gw, gw.get_width()+11, glory_label_1.get_y() + glory_label_1.get_height()+10,"> Set the timer and phrase length, then click the screen as above.")
    glory_label_3 = just_draw_label(gw, gw.get_width()+11, glory_label_2.get_y() + glory_label_2.get_height()+10,"> Everyone draws the same phrase.")
    glory_label_4 = just_draw_label(gw, gw.get_width()+11, glory_label_3.get_y() + glory_label_3.get_height()+10,"> Whoever\'s drawing is the best wins!")
    glory_label_5 = just_draw_label(gw, gw.get_width()+11, glory_label_4.get_y() + glory_label_4.get_height()+10,"> (What \"the best\" means is up to the players.)")
    for fun_label in [fun_label_1, fun_label_2, fun_label_3, fun_label_4, fun_label_5, fun_label_6, fun_label_7,fun_label_8, nothinglabel, glory_label_1,glory_label_2,glory_label_3,glory_label_4,glory_label_5]:
                fun_label.set_color("#FEFEFE")
    return(fun_label_1,fun_label_2,fun_label_3,fun_label_4,fun_label_5,fun_label_6,fun_label_7,fun_label_8,nothinglabel,glory_label_1,glory_label_2,glory_label_3,glory_label_4,glory_label_5)

def draw_save_icon(gw,TLC_x = 0, TLC_y = 0, color = ["#c61111","#0XC3224"], scale_factor = 1):
    # Initializes the save icon with its associated label

    scale_factor = int(scale_factor)
    backdimension = 40 * scale_factor
    saveicon = GCompound()
    back = GPolygon()
    back.add_vertex(-backdimension/2,-backdimension/2)
    back.add_polar_edge(backdimension-6*scale_factor,0)
    back.add_edge(6*scale_factor,8*scale_factor)
    back.add_polar_edge(backdimension-8*scale_factor,-90)
    back.add_polar_edge(-backdimension,0)
    
    back.set_color("#000000")
    back.set_filled(True)
    back.set_fill_color(color[0])
    saveicon.add(back)
    

    top_rectangle = GRect(-10,-18,20,14)
    top_rectangle.set_fill_color("#95cadc")
    top_rectangle.set_filled(True)
    saveicon.add(top_rectangle)

    bottom_rectangle = GRect(-17,1,34,16)
    bottom_rectangle.set_fill_color(color[1])
    bottom_rectangle.set_filled(True)
    saveicon.add(bottom_rectangle)  

    little_rectangle = GRect(4,-16,4,10)
    little_rectangle.set_fill_color("#fcfcfc")
    little_rectangle.set_filled(True)
    saveicon.add(little_rectangle)  


    gw.add(saveicon)
    saveicon.set_location(TLC_x,TLC_y)

    savelabel = GLabel("phrase saved!")
    savelabel.set_location(TLC_x,gw.get_height()+100)


    return saveicon, savelabel
    
colorsetups = [["#c61111","#daf6ff"],
               ["#132ed2","#daf6ff"],
               ["#11802d","#daf6ff"],
               ["#ee54bb","#daf6ff"],
               ["#f07d0d","#daf6ff"],
               ["#f6f657","#daf6ff"],
               ["#3f474e","#daf6ff"],
               ["#d7e1f1","#daf6ff"],
               ["#6b2fbc","#daf6ff"],
               ["#71491e","#daf6ff"],
               ["#38ffdd","#daf6ff"],
               ["#50f039","#daf6ff"],
               ["#5f1d2e","#daf6ff"],
               ["#ecc0d3","#daf6ff"],
               ["#ffffbe","#d2bc89"],# light yellow
               ["#758593","#daf6ff"],
               ["#918877","#daf6ff"],
               ["#d76464","#daf6ff"]]

def draw_all_save_icons_and_background(gw, phrase_to_draw):
    # This will store the background, icons, and labels in a tuple for easy access

    saved_label_list = []
    save_icon_list = []
    horizontal_shim1 = 6
    save_background = GRect(3*gw.get_width()/16-horizontal_shim1,
                            gw.get_height(),
                            44*len(colorsetups)+horizontal_shim1*2,
                            -gw.get_height()/10+14)
    save_background.set_filled(True)
    save_background.set_fill_color("#9a9a9a")
    gw.add(save_background)

    saves_base = save_background.get_x()+4

    for number in range(len(colorsetups)):
        index = number

        saveicon,saved_label = draw_save_icon(gw,saves_base+24+(index)*44,
                                              720,
                                              colorsetups[index])
        save_icon_list.append(saveicon)
        saved_label.set_font(phrase_to_draw.get_font())
        saved_label.set_color(phrase_to_draw.get_color())
        saved_label_list.append(saved_label)

    return (save_background, save_icon_list, saved_label_list)