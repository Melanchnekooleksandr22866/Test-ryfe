from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

class ScrButton(Button):
    def __init__(self, screen, direction='right', goal='main', **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.direction = direction
        self.goal = goal
        self.background_color = (1, 0, 0, 1)
        self.color = (0, 0, 0, 1)

    def on_press(self):
        if hasattr(self.screen, 'validate'):
            if self.screen.validate():
                self.screen.manager.transition.direction = self.direction
                self.screen.manager.current = self.goal
        else:
            self.screen.manager.transition.direction = self.direction
            self.screen.manager.current = self.goal

class CountdownTimer(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = 60
        self.text = str(self.time)
        self.font_size = '48sp'
        self.sound = SoundLoader.load('music.mp3')
        if self.sound:
            self.sound.volume = 1.0

    def start(self):
        self.time = 60
        self.text = str(self.time)
        self.event = Clock.schedule_interval(self.update, 1)

    def update(self, dt):
        self.time -= 1
        self.text = str(self.time)
        if self.time <= 0:
            self.event.cancel()
            if self.sound:
                self.sound.play()

    def reset(self):
        self.time = 60
        self.text = str(self.time)
        if hasattr(self, 'event'):
            self.event.cancel()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = RelativeLayout() 
        text = "Здраствуйте, це додаток, який вимірює ваш індекс Руф'є."
        text_2 = "Щоб програма виміряла ваш індекс, натисніть на кнопку 'Старт' і заповніть всю інформацію."
        label = Label(text=text, size_hint=(1, 1.4))
        label_2 = Label(text=text_2, size_hint=(1, 0.5))
        start_button = Button(text='Старт', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        start_button.bind(on_press=self.start_pressed)
        img = Image(source='img.png', size_hint=(None, None), size=(300, 300), pos_hint={'center_x': 0.5, 'center_y': 0.5}) 

        layout.add_widget(img)
        layout.add_widget(label)
        layout.add_widget(label_2)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def start_pressed(self, instance):
        self.manager.current = 'second'

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label_name = Label(text="Напиши своє ім'я:", size_hint=(1, 0.1))
        self.text_input_name = TextInput(hint_text="Введіть ім'я", multiline=False, size_hint=(0.8, 0.1))
        label_age = Label(text='Напиши свій вік:', size_hint=(1, 0.1))
        self.text_input_age = TextInput(hint_text='Введіть вік', multiline=False, size_hint=(0.8, 0.1))
        continue_button = ScrButton(screen=self, text='Продовжити', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5}, goal='third')
        layout.add_widget(label_name)
        layout.add_widget(self.text_input_name)
        layout.add_widget(label_age)
        layout.add_widget(self.text_input_age)
        layout.add_widget(continue_button)
        self.add_widget(layout)

    def validate(self):
        return True

    def reset(self):
        self.text_input_name.text = ''
        self.text_input_age.text = ''

class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        top_label = Label(text="Виміряйте пульс 15 секунд і напишіть результат:", size_hint=(1, 0.1))
        self.text_input = TextInput(hint_text='Введіть результат пульсу', multiline=False, size_hint=(0.8, 0.1))
        self.error_label = Label(text='', color=(1, 0, 0, 1), size_hint=(1, 0.1))
        continue_button = ScrButton(screen=self, text='Продовжити', size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5}, goal='fourth')
        layout.add_widget(top_label)
        layout.add_widget(self.text_input)
        layout.add_widget(self.error_label)
        layout.add_widget(continue_button)
        self.add_widget(layout)

    def validate(self):
        try:
            pulse = int(self.text_input.text)
            if pulse > 150 or pulse < 9:
                self.error_label.text = 'Пульс не може буть таким!'
                return False
            else:
                self.error_label.text = ''
                return True
        except ValueError:
            self.error_label.text = 'Введіть вірні дані!'
            return False

    def reset(self):
        self.text_input.text = ''
        self.error_label.text = ''
class FourthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = RelativeLayout() 
        label = Label(text='Зроби 30 присідань за 60 секунд', size_hint=(1, 1.5))
        
        self.timer = CountdownTimer(size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        bottom_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        start_timer_button = Button(text='Запуск таймера', size_hint=(0.5, 1.7), background_color=(1, 0, 0, 1), color=(0, 0, 0, 1))
        start_timer_button.bind(on_press=self.start_timer)
        continue_button = ScrButton(screen=self, text='Продовжити', size_hint=(0.5, 1.7), goal='fifth')
        img = Image(source='img.png', size_hint=(None, None), size=(500, 500), pos_hint={'center_x': 0.5, 'center_y': 0.5}) 

        bottom_layout.add_widget(start_timer_button)
        bottom_layout.add_widget(continue_button)

        layout.add_widget(img)        
        layout.add_widget(label)
        layout.add_widget(self.timer)
        layout.add_widget(bottom_layout)
        
        self.add_widget(layout)

    def start_timer(self, instance):
        self.timer.start()

    def reset(self):
        self.timer.reset()

class FifthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        top_label = Label(text="Протягом хвилини заміряйте пульс двічі: за перші 15 секунд, потім відпочинь 1 минуту і замірь пульс.", size_hint=(1, 0.2))
        top_label1 = Label(text="Напиши результат в полях в першому результат першого пульсу, а в другому результат пульсу після відпочинку.", size_hint=(1, 0.1))
        self.text_input_first = TextInput(hint_text='Результат', multiline=False, size_hint=(0.8, 0.2))
        self.text_input_second = TextInput(hint_text='Результат після відпочинку', multiline=False, size_hint=(0.8, 0.2))
        self.error_label = Label(text='', color=(1, 0, 0, 1), size_hint=(1, 0.1))
        continue_button = ScrButton(screen=self, text='Продовжити', size_hint=(0.3, 0.16), pos_hint={'center_x': 0.5}, goal='sixth')
        layout.add_widget(top_label)
        layout.add_widget(top_label1)
        layout.add_widget(self.text_input_first)
        layout.add_widget(self.text_input_second)
        layout.add_widget(self.error_label)
        layout.add_widget(continue_button)
        self.add_widget(layout)

    def validate(self):
        try:
            pulse1 = int(self.text_input_first.text)
            pulse2 = int(self.text_input_second.text)
            if pulse1 > 150 or pulse2 > 150 or pulse1 < 9 or pulse2 < 9:  
                self.error_label.text = 'Пульс не може буть таким!'
                return False
            else:
                self.error_label.text = ''
                return True
        except ValueError:
            self.error_label.text = 'Введіть вірні дані!'
            return False

    def reset(self):
        self.text_input_first.text = ''
        self.text_input_second.text = ''
        self.error_label.text = ''

class SixthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.result_label = Label(text='', size_hint=(1, 0.2))
        back_button = ScrButton(screen=self, text='Назад в меню', size_hint=(0.3, 0.05), pos_hint={'center_x': 0.5, 'y': 0}, goal='main')
        back_button.bind(on_press=self.reset_all)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(back_button)
        self.add_widget(self.layout)

    def on_enter(self):
        try:
            pulse1 = int(App.get_running_app().root.get_screen('third').text_input.text)
            pulse2 = int(App.get_running_app().root.get_screen('fifth').text_input_first.text)
            pulse3 = int(App.get_running_app().root.get_screen('fifth').text_input_second.text)
            result = (4 * (pulse1 + pulse2 + pulse3) - 200) / 10
            self.result_label.text = f'Результат: {result}'
        except ValueError:
            self.result_label.text = 'Будь ласка, введіть числові дані для пульсу.'

    def reset_all(self, instance):
        app = App.get_running_app()
        app.root.get_screen('second').reset()
        app.root.get_screen('third').reset()
        app.root.get_screen('fourth').reset()
        app.root.get_screen('fifth').reset()

class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(ThirdScreen(name='third'))
        sm.add_widget(FourthScreen(name='fourth'))
        sm.add_widget(FifthScreen(name='fifth'))
        sm.add_widget(SixthScreen(name='sixth'))
        return sm

if __name__ == '__main__':
    TestApp().run()