from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout

Window.size = (500, 600)

class WaveCircle(Widget):
    color = ListProperty([1, 1, 1, 1])

KV = '''
<WaveCircle>:
    canvas:
        Color:
            rgba: self.color
        Ellipse:
            size: self.size
            pos: self.pos

MDScreen:
    md_bg_color: 0.1, 0.1, 0.1, 1

    MDBoxLayout:
        orientation: "vertical"
        spacing: "10dp"

        MDTopAppBar:
            id: header
            title: "Edge AI for File Management"
            elevation: 4
            md_bg_color: 0.15, 0.15, 0.15, 1
            right_action_items: [["cog", lambda x: app.on_settings_click()]]

        BoxLayout:
            id: content_area
            orientation: "vertical"
            size_hint_y: 1

            ScrollView:
                MDBoxLayout:
                    id: chat_box
                    orientation: "vertical"
                    padding: "10dp"
                    spacing: "10dp"
                    size_hint_y: None
                    height: self.minimum_height

            MDFloatLayout:
                id: wave_container
                size_hint_y: 1
                disabled: True
                opacity: 0

                MDFloatLayout:
                    id: wave_area
                    size_hint: None, None
                    size: dp(300), dp(300)
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}

                    WaveCircle:
                        id: wave1
                        size_hint: None, None
                        size: dp(240), dp(240)
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        color: 0.2, 0.6, 0.9, 0.3

                    WaveCircle:
                        id: wave2
                        size_hint: None, None
                        size: dp(180), dp(180)
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        color: 0.2, 0.6, 0.9, 0.5

                    WaveCircle:
                        id: wave3
                        size_hint: None, None
                        size: dp(120), dp(120)
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        color: 0.2, 0.6, 0.9, 1

                MDIconButton:
                    id: stop_button
                    icon: "close"
                    theme_icon_color: "Custom"
                    icon_color: 1, 1, 1, 1
                    md_bg_color: 1, 0, 0, 1
                    user_font_size: "32sp"
                    pos_hint: {"center_x": 0.5, "y": 0.05}
                    on_release: app.stop_listening_mode()

            MDBoxLayout:
                id: input_box
                size_hint_y: None
                height: "60dp"
                padding: "10dp"
                spacing: "10dp"
                md_bg_color: 0.12, 0.12, 0.12, 1

                MDTextField:
                    id: user_input
                    hint_text: "Type your command"
                    mode: "rectangle"
                    size_hint_x: 0.8
                    text_color: 1, 1, 1, 1
                    hint_text_color: 0.7, 0.7, 0.7, 1
                    line_color_focus: app.theme_cls.primary_color
                    on_text_validate: app.on_send_click()

                MDIconButton:
                    icon: "send"
                    theme_icon_color: "Custom"
                    icon_color: app.theme_cls.primary_color
                    on_release: app.on_send_click()

                MDIconButton:
                    icon: "microphone"
                    theme_icon_color: "Custom"
                    icon_color: 1, 1, 1, 1
                    on_release: app.on_mic_click()
                 
'''

# The Python class code remains unchanged (same as in your post)

class VoicePilotApp(MDApp):
    listening_mode = False

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.root = Builder.load_string(KV)
        Clock.schedule_once(lambda dt: self.init_ui_state(), 0)
        self.hide_wave_area()
        return self.root

    def init_ui_state(self):
        self.root.ids.stop_button.opacity = 0
        self.root.ids.stop_button.disabled = True

    def on_settings_click(self):
        print("⚙️ Settings clicked!")

    def on_send_click(self, *args):
        if self.listening_mode:
            self.stop_listening_mode()
        user_input = self.root.ids.user_input.text.strip()
        if user_input:
            print(f"📤 User typed: {user_input}")
            self.add_chat_bubble(user_input, sender="user")
            self.root.ids.user_input.text = ""

    def on_mic_click(self):
        if self.listening_mode:
            self.stop_listening_mode()
        else:
            self.start_listening_mode()

    def start_listening_mode(self):
        self.listening_mode = True
        self.root.ids.chat_box.clear_widgets()
        self.show_wave_area()
        self.hide_input_controls()
        self.start_wave_animations()
        self.root.ids.stop_button.opacity = 1
        self.root.ids.stop_button.disabled = False
        print("🎙️ Voice assistant activated!")

    def stop_listening_mode(self):
        self.listening_mode = False
        self.hide_wave_area()
        self.show_input_controls()
        self.stop_wave_animations()
        self.root.ids.stop_button.opacity = 0
        self.root.ids.stop_button.disabled = True
        print("🎙️ Voice assistant deactivated")

    def show_wave_area(self):
        self.root.ids.chat_box.disabled = True
        self.root.ids.chat_box.opacity = 0
        self.root.ids.wave_container.disabled = False
        self.root.ids.wave_container.opacity = 1

    def hide_wave_area(self):
        self.root.ids.chat_box.disabled = False
        self.root.ids.chat_box.opacity = 1
        self.root.ids.wave_container.disabled = True
        self.root.ids.wave_container.opacity = 0

    def hide_input_controls(self):
        self.root.ids.input_box.opacity = 0
        self.root.ids.input_box.disabled = True

    def show_input_controls(self):
        self.root.ids.input_box.opacity = 1
        self.root.ids.input_box.disabled = False

    def start_wave_animations(self):
        self.animate_wave(self.root.ids.wave1, scale=1.2, duration=1.5, alpha=0.3)
        self.animate_wave(self.root.ids.wave2, scale=1.15, duration=1.2, alpha=0.5)
        self.animate_wave(self.root.ids.wave3, scale=1.1, duration=1.0, alpha=1.0)

    def stop_wave_animations(self):
        Animation.cancel_all(self.root.ids.wave1)
        Animation.cancel_all(self.root.ids.wave2)
        Animation.cancel_all(self.root.ids.wave3)

    def animate_wave(self, widget, scale, duration, alpha):
        base_size = widget.size[0]
        anim = (
            Animation(
                size=(base_size * scale, base_size * scale),
                color=[*widget.color[:3], 0.05],
                duration=duration,
                t='in_out_quad'
            ) +
            Animation(
                size=(base_size, base_size),
                color=[*widget.color[:3], alpha],
                duration=duration,
                t='in_out_quad'
            )
        )
        anim.repeat = True
        anim.start(widget)

    def add_chat_bubble(self, text, sender="user"):
        if self.listening_mode:
            self.stop_listening_mode()

        chat_box = self.root.ids.chat_box
        bubble_row = MDBoxLayout(
            orientation="horizontal",
            spacing="10dp",
            size_hint_y=None,
            padding = (10, 15, 20, 205),
            size_hint_x=1
        )

        avatar_letter = "A" if sender == "user" else "B"
        avatar_color = (0.2, 0.4, 1, 1) if sender == "user" else (0.3, 0.8, 0.4, 1)

        avatar = MDCard(
            size_hint=(None, None),
            size=("40dp", "40dp"),
            md_bg_color=avatar_color,
            radius=[20],
            elevation=4
        )
        avatar_label = MDLabel(
            text=avatar_letter,
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint=(1, 1)
        )
        avatar.add_widget(avatar_label)

        message = MDCard(
            padding=("10dp", "8dp"),
            radius=[12],
            orientation="vertical",
            size_hint_x=0.7,
            md_bg_color=(0.2, 0.2, 0.2, 1)
        )

        message_label = MDLabel(
            text=text,
            halign="left",
            valign="middle",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            adaptive_height=True,
            text_size=(0, None)
        )

        def set_text_width(dt):
            message_label.text_size = (message.width - 20, None)
            message.height = message_label.height + 20
            bubble_row.height = message.height + 10

        message.add_widget(message_label)

        if sender == "user":
            bubble_row.add_widget(message)
            bubble_row.add_widget(avatar)
        else:
            bubble_row.add_widget(avatar)
            bubble_row.add_widget(message)

        chat_box.add_widget(bubble_row)
        Clock.schedule_once(set_text_width, 0)
        Clock.schedule_once(lambda dt: chat_box.setter("height")(chat_box, chat_box.minimum_height), 0.1)

VoicePilotApp().run()
