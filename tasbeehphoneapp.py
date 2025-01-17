from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import time

class TasbeehApp(BoxLayout):
    count = 0
    history = []
    start_time = None
    elapsed_time = 0
    timer_running = False
    timer_event = None
    current_theme_index = 0
    themes = [
        {"name": "Light", "bg": [1, 1, 1, 1], "fg": [0, 0, 0, 1], "count_bg": [1, 1, 1, 1]},
        {"name": "Dark", "bg": [0.2, 0.2, 0.2, 1], "fg": [1, 1, 1, 1], "count_bg": [0.2, 0.2, 0.2, 1]},
        {"name": "Blue", "bg": [0.53, 0.81, 0.92, 1], "fg": [0, 0, 0, 1], "count_bg": [0.53, 0.81, 0.92, 1]},
        {"name": "Green", "bg": [0.6, 0.98, 0.6, 1], "fg": [0, 0, 0, 1], "count_bg": [0.6, 0.98, 0.6, 1]},
        {"name": "Pink", "bg": [1, 0.75, 0.8, 1], "fg": [0, 0, 0, 1], "count_bg": [1, 0.75, 0.8, 1]}
    ]
    current_theme = {"name": "Light", "bg": [1, 1, 1, 1], "fg": [0, 0, 0, 1], "count_bg": [1, 1, 1, 1]}

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Counter Label and its background
        self.counter_layout = BoxLayout(size_hint=(1, 0.3), orientation='vertical')
        self.counter_label = Label(text="0", font_size=72, size_hint=(1, 1))
        self.counter_layout.add_widget(self.counter_label)
        self.add_widget(self.counter_layout)

        # Timer Label
        self.timer_label = Label(text="Time: 00:00:00", font_size=24, size_hint=(1, 0.1))
        self.add_widget(self.timer_label)

        button_layout = BoxLayout(size_hint=(1, 0.2))

        # Count Button
        self.increment_button = Button(text="Count")
        self.increment_button.bind(on_press=self.increment)
        button_layout.add_widget(self.increment_button)

        # Decrement Button
        self.decrement_button = Button(text="Decrement")
        self.decrement_button.bind(on_press=self.decrement)
        button_layout.add_widget(self.decrement_button)

        # Reset Button
        self.reset_button = Button(text="Reset")
        self.reset_button.bind(on_press=self.reset)
        button_layout.add_widget(self.reset_button)

        # Theme Button
        self.theme_button = Button(text="Switch Theme")
        self.theme_button.bind(on_press=self.switch_theme)
        button_layout.add_widget(self.theme_button)

        self.add_widget(button_layout)

        # History Button
        self.history_button = Button(text="History", size_hint=(1, 0.1))
        self.history_button.bind(on_press=self.show_history)
        self.add_widget(self.history_button)

        self.update_theme()

    def increment(self, instance):
        if not self.timer_running:
            self.start_timer()
        self.count += 1
        self.history.append(f"Incremented to {self.count} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.counter_label.text = str(self.count)

    def decrement(self, instance):
        if not self.timer_running:
            self.start_timer()
        self.count -= 1
        self.history.append(f"Decremented to {self.count} at {time.strftime('%Y-%m-%d %H:%S')}")
        self.counter_label.text = str(self.count)

    def reset(self, instance):
        self.count = 0
        self.elapsed_time = 0
        self.counter_label.text = "0"
        self.timer_label.text = "Time: 00:00:00"
        self.stop_timer()
        self.history.append(f"Reset to 0 at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    def start_timer(self):
        self.start_time = time.time() - self.elapsed_time
        self.timer_running = True
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_running = False

    def update_timer(self, dt):
        self.elapsed_time = time.time() - self.start_time
        minutes, seconds = divmod(int(self.elapsed_time), 60)
        hours, minutes = divmod(minutes, 60)
        self.timer_label.text = f"Time: {hours:02}:{minutes:02}:{seconds:02}"

    def show_history(self, instance):
        history_layout = GridLayout(cols=1, size_hint_y=None)
        history_layout.bind(minimum_height=history_layout.setter('height'))
        for entry in self.history:
            history_layout.add_widget(Label(text=entry, size_hint_y=None, height=40))
        scroll_view = ScrollView(size_hint=(1, 0.5))
        scroll_view.add_widget(history_layout)
        self.add_widget(scroll_view)

    def switch_theme(self, instance):
        # Switch to the next theme
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        self.current_theme = self.themes[self.current_theme_index]
        self.update_theme()

    def update_theme(self):
        # Apply the theme to the background and text color
        self.background_color = self.current_theme['bg']
        
        # Set text color (white)
        self.counter_label.color = [1, 1, 1, 1]  
        self.timer_label.color = [1, 1, 1, 1]   
        
        # Update counter label background
        self.counter_layout.background_color = self.current_theme['count_bg']

        # Apply theme to buttons
        for button in [self.increment_button, self.decrement_button, self.reset_button, self.theme_button, self.history_button]:
            button.background_color = self.current_theme['bg']
            button.color = [1, 1, 1, 1]  # White text for all buttons


class TasbeehCounterApp(App):
    def build(self):
        return TasbeehApp()

if __name__ == '__main__':
    TasbeehCounterApp().run()
