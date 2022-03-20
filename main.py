from kivy import animation
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.animation import Animation
from kivymd.uix.list import OneLineIconListItem
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.properties import NumericProperty,ListProperty,StringProperty
from kivy.uix.widget import Widget
from helpers import log_to_database,get_user_password,user_exists,get_user
from kivy.uix.button import Button
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp


Window.size = (800, 650)
Window.borderless = True


class RareStageToggleButton(ToggleButton):
    def __init__(self,**kwargs):
        super(RareStageToggleButton,self).__init__(**kwargs)
        self.group = "rare_stage_toggle_button"  
        
        
class PreferredColorToggleButton(ToggleButton):
    def __init__(self,**kwargs):
        super(PreferredColorToggleButton,self).__init__(**kwargs)
        #self.group = "preferred_color_toggle_button"  

class Ball(Button):
    def move(self):
        self.xp = 3
        self.yp = 3
        self.ybounces = 0
        self.xbounces = 0
        self.movey_direction = True
        Clock.unschedule(self.animate)
        Clock.schedule_interval(self.animate,1/30)
        self.x = 10
        self.y = Window.height//2
        
    def animate(self,dt):
        if self.x <= 0 or self.x+(self.width//2) >= Window.width-20:
            if self.ybounces < 7:
                self.xp *= -1
            self.xbounces += 1
                
        self.x -= self.xp
        #print("X Bounces = ",self.xbounces) 
            
            
class Ball2(Button):
    def move(self):
        self.xp = 3
        self.yp = 3
        self.ybounces = 0
        self.xbounces = 0
        self.movey_direction = True
        Clock.unschedule(self.animate)
        Clock.schedule_interval(self.animate,1/30)
        self.x = Window.width//2
        self.y = 10
        
    def animate(self,dt):
        if self.y <= 0 or self.y+(self.height//2) >= Window.height-20:
            if self.ybounces < 7:
                self.yp *= -1
            self.ybounces += 1
            
        self.y -= self.yp
        #print("Y Bounces = ",self.ybounces)
            
class RectangularBall(Button):
    def initialize_settings_and_move(self):
        self.xp = 3
        self.yp = 3
        self.ybounces = 0
        self.xbounces = 0
        self.movey_direction = True
        
        Clock.unschedule(self.move_randomly)
        Clock.schedule_interval(self.move_randomly,1/30)
        
    def move_randomly(self,delta_time):
        if self.x <= 0 or (self.x+self.width) >= Window.width:
            self.xp *= -1
        if self.y <= 0 or (self.y+self.height) >= Window.height:
            self.yp *= -1
            
        self.x += self.xp
        self.y += self.yp    
                
            
            
      

class RareCviApp(MDApp):
    stage1page3objectangle = NumericProperty(0)
    object_color = ListProperty([1,0,0,1])
    
    gif_file_path1 = StringProperty("apple_blue.GIF")
    gif_file_path2 = StringProperty("book_blue.GIF")
    gif_file_path3 = StringProperty("pencil_blue.GIF")
    
    bg2_1color = ListProperty([1,0,0,1])
    bg2_2color = ListProperty([1,0,0,1])
    bg2_3color = ListProperty([1,0,0,1])
    
    def __init__(self,**kwargs):
        super(RareCviApp,self).__init__(**kwargs)
        self.username = "User"
        self.password = "mypassword123"
        self.fname = "Me"
        self.age = 0
        self.rare_stage = "Stage1"
        self.color_preferred = []
        self.posture_preferred = "straight"
        self.preference = "mild"
        
        self.stage1pageindex = 2
        self.stage1pagenames = ['stage1_1_screen',
                                'stage1_2_screen',
                                'stage1_3_screen',
                                'stage_1_4_screen']
        self.stage2pageindex = 2
        self.stage2pagenames = ['stage2_1_screen',
                                'stage2_2_screen',
                                'stage2_3_screen']
        self.stage3pageindex = 2
        self.stage3pagenames = ['stage3_1_screen',
                                'stage3_2_screen',
                                'stage3_3_screen',
                                'stage3_4_screen']
        self.object_colors = {
            "red":[1,0,0,1],
            "blue":[0,0,1,1],
            "green":[0,1,0,1]
        }
        
    def show_message(self,sc,text):
        snackbar = Snackbar(
            text=text,
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
            duration = 0.3,
            font_size = "16dp"
        )
        snackbar.open()  

    def build(self):
        pass

    def on_start(self):
        self.anim()

    def anim(self):
        ANIM = Animation(pos_hint={"y": 0.6}, duration=0.8)
        ANIM.bind(on_complete=self.trigger_another)
        ANIM.start(self.root.ids.anim_item)

    def trigger_another(self, *args):
        ANIM1 = Animation(opacity=1)
        ANIM1.start(self.root.ids.wel)
        ANIM1 = Animation(opacity=1)
        ANIM1.start(self.root.ids.wel1)

    def login_user(self, sm,sc,username,password):
        result = get_user_password(username.text)
        if result:
            if password.text == result:
                user = get_user(username.text,password.text)
                rare_stage = user[4]
                preferred_color = user[5]
                preferred_color = preferred_color.split("|")
                self.color_preferred = preferred_color
                stage = rare_stage.lower()
                
                if stage == "stage2":
                    if "blue" in self.color_preferred and 'red' in self.color_preferred:
                        self.gif_file_path1 = "apple_blue.GIF"
                        self.bg2_1color = [0,0,1,1]
                        
                    if "red" in self.color_preferred and 'green' in self.color_preferred:
                        self.gif_file_path1 = 'apple_green.GIF'
                        self.bg2_1color = [0,1,0,1]

                    if "blue" in self.color_preferred and 'red' in self.color_preferred:
                        self.gif_file_path2 = "book_blue.GIF"
                        self.bg2_2color = [0,0,1,1]
                    if "red" in self.color_preferred and 'green' in self.color_preferred:
                        self.gif_file_path2 = 'book_green.GIF'
                        self.bg2_2color = [0,1,0,1]

                    if "yellow" in self.color_preferred and 'green' in self.color_preferred:
                        self.gif_file_path3 = "pencil_green.GIF"
                        self.bg2_3color = [0,1,0,1]
                    if "yellow" in self.color_preferred and 'blue' in self.color_preferred:
                        self.gif_file_path3 = 'pencil_blue.GIF' 
                        self.bg2_3color = [0,0,1,1]
                
                sm.current = rare_stage.lower()
                self.root.ids.wel.opacity = 0
                self.root.ids.wel1.opacity = 0
                self.root.ids.anim_item.pos_hint = {"y": 1}
                
                username.text = ""
                password.text = ""
                
            else:
                self.show_message(sc,"Incorrect password")
                password.text = ""
        else:
            self.show_message(sc,"The User does not exist")
            password.text = ""

    def rare_stage_toggle_button_pressed(self,button):
        if button.state == "normal":
            button.state = "down"
        self.rare_stage = button.text

    def preferred_color_toggle_button_pressed(self,button):
        if button.state == 'down' and button.text.lower() not in self.color_preferred:
            self.color_preferred.append(button.text.lower())
        elif button.state == 'normal' and button.text.lower() in self.color_preferred:
            self.color_preferred.remove(button.text.lower())

        #print(self.color_preferred)
        
    def signup(self,sm,sc,username,password,name,age,posture_preferred,preference):
        self.username = username.text
        self.password = password.text
        self.fname = name.text
        self.age = age.text
        self.rare_stage = self.rare_stage
        self.color_preferred = self.color_preferred  
        self.posture_preferred = posture_preferred.text
        self.preference = preference.text
        
        if len(self.username) < 3:
            self.show_message(sc,"The username is too short")
        elif len(self.password) < 8:
            self.show_message(sc,"The password must not be less than 8 characters")
        elif len(self.name) < 3:
            self.show_message(sc,"The Name is too short")
        elif self.age == 0 or not self.age.isnumeric() or self.age.startswith("0"):
            self.show_message(sc,"Invalid age")
        elif user_exists(self.username):
            self.show_message(sc,"The username already exists")
        elif len(self.color_preferred) < 1:
            self.show_message(sc,"You must select at least on preferred color!")
            
        elif self.rare_stage.lower() == "stage2" and ("purple" in self.color_preferred or "neon" in self.color_preferred):
            self.show_message(sc,"The preferred colors you have chosen are not supported for now ('neon' and 'puple').")
        
        else:
            #print(self.color_preferred)
            self.color_preferred = "|".join(self.color_preferred)
            log_to_database(self.username,self.password,self.fname,self.age,self.rare_stage,self.color_preferred,self.posture_preferred,self.preference)
            sm.current = 'signin'

    def change_window1_pages(self,delta_time):
        #print("Changing screen",self.stage1pageindex)
        next_screen = self.stage1pagenames[self.stage1pageindex-1]
        self.root.ids.sm.current = next_screen
        if self.stage1pageindex == len(self.stage1pagenames):
            self.stage1pageindex = 1
        else:
            self.stage1pageindex += 1
        
    def rotatestage1obj(self,delta_time):
        self.root.ids.stage1page3object.background_color = self.object_colors[self.color_preferred.lower()]
        if self.stage1page3objectangle >= 360:
            self.stage1page3objectangle = 0
        else:
            self.stage1page3objectangle += 1

    def eye():
        #print("Thread2 assigned to thread: {}".format(threading.current_thread().name))
        call(["python", "eyetrack.py"])
    
    def animate_ball(self,ball):
        if "red" in self.color_preferred:
            self.color_preferred = "red"
        elif "green" in self.color_preferred:
            self.color_preferred = "green"
        elif "blue" in self.color_preferred:
            self.color_preferred = "blue"
        self.object_color = self.object_colors[self.color_preferred]
        # ball.top = Window.height
        # ball.x = Window.width/2
        ball.move()
        
    def animate_ball2(self,ball):
        if "red" in self.color_preferred:
            self.color_preferred = "red"
        elif "green" in self.color_preferred:
            self.color_preferred = "green"
        elif "blue" in self.color_preferred:
            self.color_preferred = "blue"
        self.object_color = self.object_colors[self.color_preferred]
        # ball.y = Window.height//2
        # ball.x = Window.width/2
        ball.move()
        
    def animate_rectangular_ball(self,ball_rect):
        if "red" in self.color_preferred:
            self.color_preferred = "red"
        elif "green" in self.color_preferred:
            self.color_preferred = "green"
        elif "blue" in self.color_preferred:
            self.color_preferred = "blue"
        self.object_color = self.object_colors[self.color_preferred]
        ball_rect.top = Window.height
        ball_rect.x = Window.width/2
        ball_rect.initialize_settings_and_move()
    
    def init_stage2(self):
        pass
        
        
    def change_window2_pages(self,delta_time):
        # print("Changing screen",self.stage2pageindex)
        next_screen = self.stage2pagenames[self.stage2pageindex-1]
        self.root.ids.sm.current = next_screen
        if self.stage2pageindex == len(self.stage2pagenames):
            self.stage2pageindex = 1
        else:
            self.stage2pageindex += 1      
            
    def init_stage3(self):
        pass
    
    
RareCviApp().run()
