# MP3 Player Kivy
# =============================================================================
import os
import random
import time
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch

Window.size = (400, 600)

class  MP3_PlayerApp(MDApp):
    def build(self):
        layout = MDRelativeLayout(md_bg_color = 'blue')

        self.music_dir = 'C:/final_project/music_directory'
        self.music_files = os.listdir(self.music_dir)

        print(self.music_files)

        self.song_list = [x for x in self.music_files if x.endswith(('mp3'))]
        self.song_count = len(self.song_list)

        print(self.song_list)

        self.songLabel = Label(pos_hint={'center_x':0.5, 'center_y':0.92},
                                size_hint = (1,1),
                                font_size = 25,
                                color = 'black')

        self.currenttime = Label(text = '00:00',
                                 pos_hint = {'center_x':.16, 'center_y':.170},
                                 size_hint = (1,1),
                                 font_size = 18)

        self.totaltime = Label(text='00:00',
                                pos_hint={'center_x': .84, 'center_y': .169},
                                size_hint=(1, 1),
                                font_size=18)
        
        self.shape = Widget(pos_hint={'center_x': 0.5, 'center_y': 0.5})
        with self.shape.canvas:
            Color(.7,.1,.4)
            Ellipse(pos=(100, 280), size=(310, 320), angle_start=0, angle_end=360)
            
        self.singername = Label(pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                font_size = 30,
                                color = 'black')  

        self.progressbar = ProgressBar(max = 100,
                                       value = 0,
                                       pos_hint = {'center_x':0.5, 'center_y':0.15},
                                       size_hint = (.8, .75))

        self.volumeslider = Slider(min=0,
                                   max=1,
                                   value_track = True,
                                   value_track_color = [1,0,1,1],
                                   value=0.5,
                                   orientation='horizontal',
                                   pos_hint= {'center_x':0.7, 'center_y':0.07},
                                   size_hint=(0.4, 0.4))

        self.pausebutton = MDIconButton(pos_hint={'center_x': 0.3, 'center_y': 0.07},
                                        icon='pause',
                                        on_press=self.pauseaudio,
                                        disabled=True)
        
        self.playbutton = MDIconButton(pos_hint={'center_x':0.1, 'center_y':0.07},
                                        icon = 'play',
                                        on_press = self.playaudio)
        
        self.stopbutton = MDIconButton(pos_hint={'center_x': 0.2, 'center_y': 0.07},
                                       icon='stop',
                                       on_press = self.stopaudio, disabled =True)
        layout.add_widget(self.playbutton)
        layout.add_widget(self.pausebutton)
        layout.add_widget(self.stopbutton)
        layout.add_widget(self.songLabel)
        layout.add_widget(self.shape)
        layout.add_widget(self.singername)
        layout.add_widget(self.currenttime)
        layout.add_widget(self.totaltime)
        layout.add_widget(self.progressbar)
        layout.add_widget(self.volumeslider)


        def volume(instance, value):
            print(value)
            self.sound.volume = value

        self.volumeslider.bind(value = volume)

        Clock.schedule_once(self.playaudio)

        return layout

    def playaudio(self, obj):
        self.playbutton.disabled = True
        self.stopbutton.disabled = False
        self.song_title = self.song_list[random.randrange(0, self.song_count)]
        self.songLabel.text = self.song_title[0:-4]
        self.singername.text = self.song_title[0:-18]
        self.sound = SoundLoader.load('{}/{}'.format(self.music_dir, self.song_title))

        self.sound.play()

        self.progressbarEvent = Clock.schedule_interval(self.updateprogressbar, self.sound.length/60)
        self.settimeEvent = Clock.schedule_interval(self.settime, 1)
        self.pausebutton.disabled = False

    def pauseaudio(self, obj):
        if self.sound.state == 'play':
            self.sound.stop()
            self.pausebutton.icon = 'play'
        else:
            self.sound.play()
            self.pausebutton.icon = 'pause'

    def updateprogressbar(self, value):
        if self.progressbar.value < 100:
            self.progressbar.value += 1

    def settime(self, t):
        current_time = time.strftime('%M:%S', time.gmtime(self.progressbar.value))
        total_time = time.strftime('%M:%S', time.gmtime(self.sound.length))

        self.currenttime.text = current_time
        self.totaltime.text = total_time

    def stopaudio(self, obj):
        self.playbutton.disabled = False
        self.stopbutton.disabled = True

        self.progressbarEvent.cancel()
        self.settimeEvent.cancel()
        self.progressbar.value = 0
        self.currenttime.text = '00:00'
        self.totaltime.text = '00:00'

        self.sound.stop()


if __name__ == '__main__':
    MP3_PlayerApp().run()
# =============================================================================