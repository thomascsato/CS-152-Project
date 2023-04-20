

import math
import random as rng
from pgl import GWindow, GLine, GOval, GRect, GPolygon, GLabel, GCompound

import os

import time as tmr

"""Used to get directory from which the code pulls text files from by default."""
# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))

global ready_to_show
global number_of_picks
number_of_picks = 3
ready_to_show = True

num_change_TF = True
GWINDOW_WIDTH = 1250
GWINDOW_HEIGHT = 500
TIME_STEP = 500

gw = GWindow(GWINDOW_WIDTH,GWINDOW_HEIGHT)


#########################################################################################################----------------->TIMER

class Timerclass:
    def __init__(self, gw):

        self._text = None
        self._ticking = False
        self._display_time = "00:00"
        self._compound = None
        self._Timerlabel = None

        self._black = "#000000"
        self._red = "#F0000F"
        self._play = "⏵"
        self._pause = "⏹"

        self.gw = gw



    def draw_compound(self):
        self._compound = GCompound()
        self._Timerlabel = GLabel(self._display_time,0,-3)
        self._Timerlabel.set_font("40pt 'Consolas','bold'")
        self._compound.set_location(GWINDOW_WIDTH/10-0.5*self._Timerlabel.get_width(),5*GWINDOW_HEIGHT/6-6)
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
        self.gw.add(self._compound)

    def is_pause(self):
            if self.ss_text.get_label() == self._play:
                return True
            else:
                return False

    def play_pause(self):
        if self.is_pause():
            self.ss_text.set_label(self._pause)

        else:
            self.ss_text.set_label(self._play)

        
    

    def blink(self):

        if self._Timerlabel.get_color() != self._red:
            self._Timerlabel.set_color(self._red)
        else:
            self._Timerlabel.set_color(self._black)

    def stop_time(self):
        global num_change_TF
        if timer != None:
            timer.stop()
            num_change_TF = True
            self._ticking = False
            self.play_pause()
            self._Timerlabel.set_color(self._black)


#########################################################################################################----------------->TIMER








def timer(nouns,adjs, gw, Timer_on_Screen):
    # Timer_on_Screen is a TimerClass object that is composed of the whole timer and whatnot.

    global num_change_TF
    global thereisatimercurrentlyactive
 
    thereisatimercurrentlyactive = False

    Timer_on_Screen.draw_compound()

    

    def incr_decr(Timerlabel1,secs = 1,increasing=True):
            Timerlabel_separated = Timerlabel1.get_label().split(":")
            Timerlabel_mins = int(Timerlabel_separated[0])
            Timerlabel_secs = int(Timerlabel_separated[1])

            if increasing:
                Timerlabel_secs += secs
                # if Timerlabel_secs > 59:
                #     Timerlabel_mins += Timerlabel_secs // 60
                #     Timerlabel_secs = Timerlabel_secs % 60
                #     if Timerlabel_mins > 59:
                #         Timerlabel_mins = Timerlabel_mins % 60
            else:
                Timerlabel_secs -= secs
                # if Timerlabel_secs < 0:
                #     Timerlabel_mins -= Timerlabel_secs // 60
                #     Timerlabel_secs = (60 - Timerlabel_secs) % 60
                #     if Timerlabel_mins < 0:
                #         Timerlabel_mins = Timerlabel_mins % 60
                

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
        Timer_on_Screen.blink()
        if Timer_on_Screen._Timerlabel.get_label() == "00:00":
            Timer_on_Screen.stop_time()
        else:

            if num_change_TF:
                Timer_on_Screen._Timerlabel.set_label(incr_decr(Timer_on_Screen._Timerlabel,1,False))
                num_change_TF = False
            else:
                num_change_TF = True


   

    def click_action(e):
        global num_change_TF

                


        element = gw.get_element_at(e.get_x(),e.get_y())
        
        


        if type(element) == GCompound:

            TimerCompound = Timer_on_Screen._compound
            Timerlabel = Timer_on_Screen._Timerlabel
            colon = Timer_on_Screen._colon
            localx = e.get_x()-TimerCompound.get_x()
            localy = e.get_y()-TimerCompound.get_y()
            if type(TimerCompound.get_element_at(localx,localy)) == GPolygon :
                if Timer_on_Screen.is_pause():

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

                

                if not Timer_on_Screen._ticking:
                    global timer
                    timer = gw.set_interval(step,TIME_STEP)
                    Timer_on_Screen.play_pause()
                    
                    Timer_on_Screen._ticking = True
                elif Timer_on_Screen._ticking:
                    Timer_on_Screen.stop_time()
                    

                    


                
                

 
           
        # if timer is not going, start timer, otherwise stop timer
        
    gw.add_event_listener("click", click_action)





if __name__ == "__main__":
    timer("nouns.txt", "adjectives.txt")