from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
import cv2, kivy, backend
url = 'https://100.76.109.95:8080/video' 

kivy.require('1.9.0')

class main(MDApp):
    
    def build(self):
        # self.theme_cls.theme_style = 'Dark'
        self.layout = MDBoxLayout(orientation= "vertical")
        self.image = Image(pos_hint={'top':1},allow_stretch=True)
        self.layout.add_widget(self.image)

        self.butt = Button(text='',background_normal='button.png',pos_hint = {'center_x':.5,'center_y':.7},size_hint=(None,None))
        self.butt.bind(on_press = self.save_image)
        self.layout.add_widget(self.butt) 

        self.capture = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.load_video, 1.0/30.0)

        return self.layout
    
    def load_video(self,*arg):
        ret, frame = self.capture.read()

        self.image_frame = frame

        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1],frame.shape[0]), colorfmt = 'bgr')
        texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
        self.image.texture = texture

    def save_image(self, *arg):
        path = 'test.png'
        cv2.imwrite(path,self.image_frame)
        disease = backend.disease_finder(path)
        self.info_scr()

    def info_scr(self):
        self.layout.clear_widgets()
        # Label()
        # self.event.cancel()

if __name__ == "__main__":
    main().run()