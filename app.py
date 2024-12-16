from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.app import App

class ChatApp(App):
    def build(self):
        # Configuration principale
        self.messages = []
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical')
        
        # Zone de messages
        self.chat_history = ScrollView(size_hint=(1, 0.9))
        self.message_layout = BoxLayout(orientation='vertical', size_hint_y=None)
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
            # Création du message
            message = Label(
                text=f"Vous: {self.message_input.text}",
                size_hint_y=None,
                text_size=(Window.width * 0.9, None),
                halign='right',
                padding=(10, 10)
            )
            message.bind(texture_size=message.setter('size'))
            
            # Ajout du message
            self.message_layout.add_widget(message)
            self.messages.append(message)
            
            # Simulation d'une réponse automatique
            Clock.schedule_once(lambda dt: self.receive_message(
                f"Bot: Je réponds à '{self.message_input.text}'"), 1)
            
            # Nettoyage
            self.message_input.text = ''
            Clock.schedule_once(self.scroll_to_bottom, 0.1)

    def receive_message(self, text):
        message = Label(
            text=text,
            size_hint_y=None,
            text_size=(Window.width * 0.9, None),
            halign='left',
            padding=(10, 10)
        )
        message.bind(texture_size=message.setter('size'))
        self.message_layout.add_widget(message)
        self.messages.append(message)
        Clock.schedule_once(self.scroll_to_bottom, 0.1)

    def scroll_to_bottom(self, dt):
        self.chat_history.scroll_to(self.messages[-1])

if __name__ == '__main__':
    ChatApp().run()