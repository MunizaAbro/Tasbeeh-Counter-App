import tkinter as tk
import time

class TasbeehApp:
    def __init__(self, master=None):
        self.count = 0
        self.history = []  # To store the history of actions
        self.start_time = None  # To track the start time for the timer
        self.elapsed_time = 0  # To track the total elapsed time
        self.timer_running = False  # To keep track of timer status
        self.timer_paused = False  # To keep track of the pause status
        self.themes = [
            {"name": "Light", "bg": "#FFF", "fg": "#000"},
            {"name": "Dark", "bg": "#333", "fg": "#FFF"},
            {"name": "Blue", "bg": "#87CEEB", "fg": "#000"},
            {"name": "Green", "bg": "#98FB98", "fg": "#000"},
            {"name": "Pink", "bg": "#FFC0CB", "fg": "#000"}
        ]
        self.current_theme_index = 0
        
        if master:
            self.master = master
            self.master.title("Tasbeeh Counter")
            self.master.geometry("350x450")  # Slightly larger window for better display
            
            self.label = tk.Label(master, text="0", font=("Helvetica", 80, "bold"), fg="green")
            self.label.pack(pady=10)
            
            self.timer_label = tk.Label(master, text="Time: 00:00:00", font=("Helvetica", 14))
            self.timer_label.pack(pady=10)

            self.increment_button = tk.Button(master, text="Count", command=self.increment, width=10, height=2)
            self.increment_button.pack(pady=5)
            
            self.decrement_button = tk.Button(master, text="Decrement", command=self.decrement, width=10, height=2)
            self.decrement_button.pack(pady=5)
            
            self.reset_button = tk.Button(master, text="Reset", command=self.reset, width=10, height=2)
            self.reset_button.pack(pady=5)
            
            self.theme_button = tk.Button(master, text="Switch Theme", command=self.switch_theme, width=10, height=2)
            self.theme_button.pack(pady=5)

            self.history_button = tk.Button(master, text="History", command=self.show_history, width=10, height=2)
            self.history_button.pack(pady=5)
            
            self.pause_button = tk.Button(master, text="Pause", command=self.pause_timer, width=10, height=2)
            self.pause_button.pack(pady=5)
            
            self.apply_theme()
        else:
            print("Running in a non-GUI environment. Use 'increment', 'decrement', 'reset', 'pause_timer', and 'switch_theme' methods manually.")
    
    def increment(self):
        if not self.timer_running:
            self.start_timer()  # Start the timer when counting begins
        self.count += 1
        self.history.append(f"Incremented to {self.count} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.update_display()
        
    def decrement(self):
        if not self.timer_running:
            self.start_timer()  # Start the timer when counting begins
        self.count -= 1
        self.history.append(f"Decremented to {self.count} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.update_display()
        
    def reset(self):
        self.count = 0
        self.elapsed_time = 0  # Reset elapsed time
        self.update_timer()
        self.history.append(f"Reset to 0 at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.update_display()
        self.stop_timer()  # Stop the timer when reset
    
    def start_timer(self):
        self.start_time = time.time() - self.elapsed_time  # Calculate the elapsed time from last reset
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.elapsed_time = time.time() - self.start_time  # Store the elapsed time
        self.timer_running = False

    def pause_timer(self):
        if self.timer_paused:
            self.start_time = time.time() - self.elapsed_time  # Resume from where we paused
            self.timer_running = True
            self.timer_paused = False
            self.pause_button.config(text="Pause")
        else:
            self.stop_timer()
            self.timer_paused = True
            self.pause_button.config(text="Resume")
        self.update_timer()  # Update the timer display after pause or resume

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time = time.time() - self.start_time
            self.master.after(100, self.update_timer)  # Call this function every 100ms to update the timer
        self.display_time()

    def display_time(self):
        # Convert elapsed time to HH:MM:SS format
        minutes, seconds = divmod(int(self.elapsed_time), 60)
        hours, minutes = divmod(minutes, 60)
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.timer_label.config(text=f"Time: {time_str}")
    
    def switch_theme(self):
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        self.apply_theme()
    
    def apply_theme(self):
        if tk and hasattr(self, 'master'):
            theme = self.themes[self.current_theme_index]
            bg_color = theme["bg"]
            fg_color = theme["fg"]
            
            self.master.configure(bg=bg_color)
            self.label.config(bg=bg_color, fg=fg_color)
            self.timer_label.config(bg=bg_color, fg=fg_color)
            self.increment_button.config(bg=bg_color, fg=fg_color)
            self.decrement_button.config(bg=bg_color, fg=fg_color)
            self.reset_button.config(bg=bg_color, fg=fg_color)
            self.theme_button.config(bg=bg_color, fg=fg_color)
            self.history_button.config(bg=bg_color, fg=fg_color)
            self.pause_button.config(bg=bg_color, fg=fg_color)
    
    def update_display(self):
        if tk and hasattr(self, 'label'):
            self.label.config(text=str(self.count))
        else:
            print(f"Count: {self.count}")
    
    def show_history(self):
        # Create a new window to display the history
        history_window = tk.Toplevel(self.master)
        history_window.title("Counting History")
        history_window.geometry("400x400")
        
        # Create a Text widget to display the history, which is scrollable
        history_text = tk.Text(history_window, wrap=tk.WORD, width=40, height=15)
        history_text.pack(pady=10)
        
        # Insert history entries into the Text widget
        for entry in self.history:
            history_text.insert(tk.END, entry + '\n')
        
        # Make the text widget read-only
        history_text.config(state=tk.DISABLED)
if __name__ == "__main__":
    if tk:
        root = tk.Tk()
        app = TasbeehApp(root)
        root.mainloop()
    else:
        app = TasbeehApp()
        app.increment()
        app.decrement()
        app.reset()
        app.switch_theme()