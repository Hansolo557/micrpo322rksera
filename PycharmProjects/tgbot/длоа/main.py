import kivy
from kivy.app import App
from kivy.uix.button import Button

# Указываем версию Kivy
kivy.require('2.1.0')


class MyApp(App):
    def build(self):
        # Создаем кнопку и возвращаем ее как виджет корневого уровня
        self.button = Button(text='Нажми меня')
        self.button.bind(on_press=self.on_button_press)
        return self.button

    def on_button_press(self, instance):
        # Меняем текст кнопки при нажатии
        self.button.text = 'Ты нажал  меня!'


# Запускаем приложение
if __name__ == '__main__':
    MyApp().run()
