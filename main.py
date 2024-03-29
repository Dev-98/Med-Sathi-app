from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
import cv2, kivy, easyocr 
import pandas as pd
from thefuzz import fuzz
from string import digits, punctuation
from playsound import playsound
from kivy.config import Config
from kivy.core.window import Window
# Window.size = (400, 600)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
url = 'https://100.76.109.95:8080/video' 

kivy.require('1.9.0')
        

class MedApp(MDApp):
    
    def build(self):

        self.theme_cls.theme_style = 'Dark'
        
        self.layout = MDBoxLayout(orientation= "vertical")
        # self.layout.add_widget(Image(source='logo.png',pos_hint={"center":1}))
        
        self.image = Image(allow_stretch=True)
        self.layout.add_widget(self.image)
        # self.image.size_hint_x = 0.5
        # self.image.size_hint_y = 3
        self.butt = Button(text='',background_normal='button.png',pos_hint = {'center_x':.5,'center_y':.7},size_hint=(None,None))
        self.butt.bind(on_press = self.save_image)
        self.layout.add_widget(self.butt) 
        # added
        self.image.allow_stretch = True
        # add
        self.capture = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.load_video, 1.0/30.0)
        

        return self.layout
    
    def load_video(self,*arg):
        ret, frame = self.capture.read()

        self.image_frame = frame

        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1],frame.shape[0]), colorfmt = 'bgr')
        texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
        self.image.texture = texture

    def save_image(self, *arg):
        path = 'test.png'
        cv2.imwrite(path,self.image_frame)

        self.disease = self.disease_finder(path)
        self.info_scr()

    def info_scr(self):
        self.layout.clear_widgets()
        
        self.layout.add_widget(Image(source='logo.png'))
        
        lab = Label(
            text=f'[color=#00FFFF][b]Disease[/b][/color] : {self.disease[0]} ', 
            font_size='30', 
            markup=True)
        
        self.layout.add_widget(lab)

        img = Image(source='test.png',pos_hint={'top':1},)
       
        self.layout.add_widget(img)
        # self.voice_model(self.disease[0])
        
    def image_reader(self,data, path):
        reader = easyocr.Reader(['en'])

        results = reader.readtext(path)
        p = '='*10
        text = ' ' 
        for result in results:
            text += result[1] + ' '

        # print(p,'\n',text,'\n',p)

        remove_digits = str.maketrans('', '', punctuation)
        remove_digits2 = str.maketrans('', '', digits)

        res = text.translate(remove_digits)
        res = res.translate(remove_digits2)

        self.new_text = ""
        for txt in str(res).split():
            if (len(txt) > 4):
                self.new_text += txt + " "
    
        # print(p,'\n',self.new_text,'\n',p)

        l=[]
        for i in data["Medicine"]:
            score = fuzz.partial_token_sort_ratio(i, self.new_text)
            l.append(score)
            index = sorted(list(enumerate(l)), reverse=True, key=lambda x: x[1])[0][0]
            if max(l) >= 70:
                bimari = data["Disease"][index]
                dawai = data["Medicine"][index]
            else :
                bimari = 'Not available in database'
                dawai = 'Unreadable image'
                
        return bimari,dawai,desc

    def voice_model(self, bimari):
        if bimari == 'Asthama':
            playsound('asthama.mp3')

        elif bimari == 'Headache':
            playsound('head.mp3')

        elif bimari == 'Kidney':
            playsound('kidney.mp3')

        elif bimari == 'Body Pain':
            playsound('body.mp3')

        elif bimari == 'Fever':
            playsound('fever.mp3')

        elif bimari == 'Allergy':        
            playsound('allergy.mp3')
        elif bimari == 'Gas':           
            playsound('gas.mp3')
        else:
            playsound('none.mp3')

    def disease_finder(self, img_path):
        
        data = pd.read_csv("medicine data.csv")
        
        bimari = self.image_reader(data,img_path)

        # print(bimari) 
        # self.voice_model(bimari[0])  
        return bimari
    
        

if __name__ == "__main__":
    MedApp().run()