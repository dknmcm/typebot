import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Tuple


class RegionSelector:
    def __init__(self, on_region_selected: Callable[[int, int, int, int], None]):
        self.on_region_selected = on_region_selected
        self.root = None
        self.canvas = None
        self.selection_rect = None
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.dragging = False

    def show_selector(self):
        """Create transparent overlay for region selection"""
        self.root = tk.Tk()
        self.root.title("Select Screen Region")
        self.root.attributes('-alpha', 0.3)  # Transparency
        self.root.attributes('-topmost', True)  # Stay on top

        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.overrideredirect(True)  # Remove window decorations

        # Create canvas for drawing selection
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.configure(bg='black')

        # Bind mouse events
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)

        # Create control panel
        self.create_control_panel()

        self.root.mainloop()

    def create_control_panel(self):
        """Create control buttons"""
        control_frame = tk.Frame(self.root, bg='white', relief='raised', bd=2)
        control_frame.place(x=10, y=10)

        tk.Label(control_frame, text="Draw rectangle to select region",
                font=('Arial', 12), bg='white').pack(pady=5, padx=10)

        button_frame = tk.Frame(control_frame, bg='white')
        button_frame.pack(pady=5, padx=10)

        tk.Button(button_frame, text="Start Monitoring",
                command=self.confirm_selection, bg='green', fg='white',
                font=('Arial', 10, 'bold')).pack(side='left', padx=5)

        tk.Button(button_frame, text="Cancel",
                command=self.cancel_selection, bg='red', fg='white',
                font=('Arial', 10)).pack(side='left', padx=5)

        # Coordinates display
        self.coord_label = tk.Label(control_frame, text="No selection",
                                    font=('Arial', 10), bg='white')
        self.coord_label.pack(pady=5)

    def on_mouse_down(self, event):
        """Start drawing selection rectangle"""
        self.start_x = event.x
        self.start_y = event.y
        self.dragging = True

        # Remove previous rectangle if exists
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)

    def on_mouse_drag(self, event):
        """Update selection rectangle while dragging"""
        if self.dragging:
            self.end_x = event.x
            self.end_y = event.y

            # Remove previous rectangle
            if self.selection_rect:
                self.canvas.delete(self.selection_rect)

            # Draw new rectangle
            self.selection_rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, self.end_x, self.end_y,
                outline='red', width=3, fill='', stipple='gray25'
            )

            # Update coordinates display
            width = abs(self.end_x - self.start_x)
            height = abs(self.end_y - self.start_y)
            x = min(self.start_x, self.end_x)
            y = min(self.start_y, self.end_y)

            self.coord_label.config(text=f"Region: {x},{y} ({width}x{height})")

    def on_mouse_up(self, event):
        """Finish drawing selection rectangle"""
        self.dragging = False
        self.end_x = event.x
        self.end_y = event.y

    def confirm_selection(self):
        """User confirmed the selection - start monitoring"""
        if self.selection_rect:
            # Calculate final coordinates
            x = min(self.start_x, self.end_x)
            y = min(self.start_y, self.end_y)
            width = abs(self.end_x - self.start_x)
            height = abs(self.end_y - self.start_y)

            if width > 10 and height > 10:  # Minimum size validation
                # Convert to screen coordinates (add window offset)
                screen_x = x + self.root.winfo_rootx()
                screen_y = y + self.root.winfo_rooty()

                self.root.destroy()
                self.on_region_selected(screen_x, screen_y, width, height)
            else:
                tk.messagebox.showwarning("Invalid Selection",
                                        "Please select a larger region")

    def cancel_selection(self):
        """User cancelled selection"""
        self.root.destroy()
