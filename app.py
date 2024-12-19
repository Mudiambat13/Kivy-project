from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock

class ChatApp(App):
    def build(self):
        # Configuration principale
        self.messages = []

        # Layout principal
        main_layout = BoxLayout(orientation='vertical')

        # Barre de titre
        title_bar = BoxLayout(size_hint=(1, 0.1), padding=(10, 10))
        title_label = Label(text="Messenger", font_size=24, halign="center", valign="middle")
        title_bar.add_widget(title_label)
        main_layout.add_widget(title_bar)

        # Zone de messages
        self.chat_history = ScrollView(size_hint=(1, 0.8))
        self.message_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=10, spacing=10)
        self.message_layout.bind(minimum_height=self.message_layout.setter('height'))
        self.chat_history.add_widget(self.message_layout)

        # Zone de saisie
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.message_input = TextInput(multiline=False, size_hint=(0.8, 1))
        self.message_input.bind(on_text_validate=self.send_message)
        send_button = Button(text='Envoyer', size_hint=(0.2, 1))
        send_button.bind(on_press=self.send_message)

        # Assemblage
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(send_button)
        main_layout.add_widget(self.chat_history)
        main_layout.add_widget(input_layout)

        return main_layout

    def send_message(self, instance):
        if self.message_input.text.strip():
            # Création d'une bulle de message
            self.add_message(self.message_input.text, "user")

            # Simulation d'une réponse automatique
            Clock.schedule_once(lambda dt: self.add_message(
                f"Je réponds à '{self.message_input.text}'", "bot"), 1)

            # Nettoyage
            self.message_input.text = ''
            Clock.schedule_once(self.scroll_to_bottom, 0.1)

    def add_message(self, text, sender):
        # Layout pour une ligne de message
        message_line = AnchorLayout(anchor_x="left" if sender == "bot" else "right", size_hint_y=None)
        message_line.height = 60

        # Bulle avec avatar
        bubble_layout = BoxLayout(orientation="horizontal", padding=10, spacing=10, size_hint_y=None)
        bubble_layout.height = 60
        bubble_layout.width = Window.width * 0.8

        # Avatar
        avatar = Image(source="user.png" if sender == "user" else "bot.png", size_hint=(None, None), size=(40, 40))

        # Message stylisé
        message = Label(
            text=text,
            size_hint_y=None,
            text_size=(Window.width * 0.6, None),
            valign="middle",
            halign="left" if sender == "bot" else "right",
            padding=(10, 10),
            color=(0, 0, 0, 1) if sender == "user" else (1, 1, 1, 1),
        )
        message.bind(texture_size=message.setter('size'))

        # Ajout au layout
        if sender == "bot":
            bubble_layout.add_widget(avatar)
            bubble_layout.add_widget(message)
        else:
            bubble_layout.add_widget(message)
            bubble_layout.add_widget(avatar)

        message_line.add_widget(bubble_layout)
        self.message_layout.add_widget(message_line)
        self.messages.append(message_line)

    def scroll_to_bottom(self, dt):
        if self.messages:
            self.chat_history.scroll_to(self.messages[-1])

if __name__ == '__main__':
    ChatApp().run()