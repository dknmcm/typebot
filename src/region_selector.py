import tkinter as tk
import time
from typing import Callable, Optional, Tuple


class RegionSelector:
    def __init__(self, on_region_confirmed: Callable[[int, int, int, int], None]):
        self.on_region_confirmed = on_region_confirmed
        self.root = None

    def show_selector(self):
        self.root = tk.Tk()
        self.root.title("Typebot - Position & Resize Window")

        self.root.attributes('-alpha', 0.7)
        self.root.attributes('-topmost', True)

        self.root.geometry("400x200")

        self.create_window_content()

        self.make_resizable()

        self.root.mainloop()

    def create_window_content(self):
        self.root.configure(bg='')

        control_frame = tk.Frame(self.root, bg='')
        control_frame.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

        self.duration_var = tk.StringVar(value="30s")
        duration_dropdown = tk.OptionMenu(control_frame, self.duration_var,
                                        "10s", "15s", "30s", "60s", "90s", "120s")
        duration_dropdown.config(
            bg='black', fg='black',
            relief='flat', bd=0,
            highlightthickness=0,
            font=('Arial', 10, 'bold')
        )
        duration_dropdown['menu'].config(
            bg='black', fg='black',
            relief='flat', bd=0
        )
        duration_dropdown.pack(side='left', padx=(0, 5))

        start_btn = tk.Button(control_frame, text="Start",
                            command=self.confirm_selection,
                            bg='black', fg='black',
                            relief='flat',
                            bd=0,
                            highlightthickness=0,
                            padx=0, pady=0,
                            font=('Arial', 10, 'bold'))

        start_btn.pack(side='left')

    def make_resizable(self):
        self.root.resizable(True, True)
    
    def get_selected_duration(self) -> float:
        """Get selected duration in seconds"""
        duration_str = self.duration_var.get()
        return float(duration_str[:-1])

    def confirm_selection(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y() + 30
        width = self.root.winfo_width()
        height = self.root.winfo_height() - 30
        duration = self.get_selected_duration()

        self.root.attributes('-alpha', 0.01)
        self.root.update()

        self.root.destroy()
        self.on_region_confirmed(x, y, width, height, duration)

    def restore_transparency(self):
        """Restore window transparency for next session"""
        if self.root and self.root.winfo_exists():
            self.root.attributes('-alpha', 0.7)
            self.root.update()

    def cancel_selection(self):
        self.root.destroy()
