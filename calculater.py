import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Calculate dimensions based on screen size and orientation
        is_portrait = screen_height > screen_width
        if is_portrait:
            width = min(400, int(screen_width * 0.95))  # 95% of screen width for portrait
            height = min(800, int(screen_height * 0.7))  # 70% of screen height
        else:
            width = min(500, int(screen_width * 0.4))  # 40% of screen width for landscape
            height = min(600, int(screen_height * 0.8))  # 80% of screen height
        
        # Calculate position for center of screen
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set window size and position
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Set minimum sizes based on orientation
        if is_portrait:
            min_width = min(300, int(screen_width * 0.8))
            min_height = min(450, int(screen_height * 0.5))
        else:
            min_width = min(400, int(screen_width * 0.3))
            min_height = min(300, int(screen_height * 0.4))
            
        self.root.minsize(min_width, min_height)
        
        # Make window resizable
        self.root.resizable(True, True)
        self.root.configure(bg="#1E1E1E")
        
        # Make sure window is visible and on top initially
        self.root.attributes('-topmost', True)
        self.root.update()
        self.root.attributes('-topmost', False)
        
        # Set calculator icon (using ⌘ symbol as a simple calculator icon)
        self.root.iconbitmap() if hasattr(self.root, 'iconbitmap') else None
        
        # Make the calculator window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Configure styles
        self.configure_styles()
        
        # Create display variables
        self.expression = tk.StringVar()
        self.result = tk.StringVar()
        self.expression.set("")
        self.result.set("0")
        
        # Main container
        main_container = ttk.Frame(root, style="Main.TFrame")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Calculator display frame
        display_frame = ttk.Frame(main_container, style="Display.TFrame")
        display_frame.pack(padx=10, pady=(10, 5), fill="x")
        
        # Expression display (shows the calculation)
        expression_display = ttk.Entry(
            display_frame,
            textvariable=self.expression,
            justify="right",
            font=("Helvetica", 18),
            style="Expression.TEntry",
            state="readonly"
        )
        expression_display.pack(fill="x", pady=(5, 0))
        
        # Result display
        result_display = ttk.Entry(
            display_frame,
            textvariable=self.result,
            justify="right",
            font=("Helvetica", 36, "bold"),
            style="Display.TEntry",
            state="readonly"
        )
        result_display.pack(fill="x", ipady=10)
        
        # Button frame
        btn_frame = ttk.Frame(main_container, style="Main.TFrame")
        btn_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Calculator buttons with their styles
        buttons = [
            ("C", 0, 0, "Clear.TButton"), ("←", 0, 1, "Clear.TButton"), 
            ("^", 0, 2, "Operator.TButton"), ("/", 0, 3, "Operator.TButton"),
            ("7", 1, 0, "Num.TButton"), ("8", 1, 1, "Num.TButton"), 
            ("9", 1, 2, "Num.TButton"), ("*", 1, 3, "Operator.TButton"),
            ("4", 2, 0, "Num.TButton"), ("5", 2, 1, "Num.TButton"), 
            ("6", 2, 2, "Num.TButton"), ("-", 2, 3, "Operator.TButton"),
            ("1", 3, 0, "Num.TButton"), ("2", 3, 1, "Num.TButton"), 
            ("3", 3, 2, "Num.TButton"), ("+", 3, 3, "Operator.TButton"),
            ("0", 4, 0, "Num.TButton"), (".", 4, 1, "Num.TButton"), 
            ("=", 4, 2, "Equal.TButton", 2)
        ]
        
        # Create and configure buttons
        self.buttons_dict = {}  # Store button references
        for button in buttons:
            if len(button) == 5:  # Button with columnspan
                text, row, col, style, colspan = button
                btn = ttk.Button(
                    btn_frame,
                    text=text,
                    style=style,
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row, column=col, columnspan=colspan, padx=4, pady=4, sticky="nsew")
            else:
                text, row, col, style = button
                btn = ttk.Button(
                    btn_frame,
                    text=text,
                    style=style,
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            self.buttons_dict[text] = btn
        
        # Configure grid weights
        for i in range(5):
            btn_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            btn_frame.grid_columnconfigure(i, weight=1)
            
        # Bind keyboard events
        self.bind_keyboard_events()
    
    def bind_keyboard_events(self):
        """Bind keyboard events and touch events to calculator functions"""
        self.root.bind('<Key>', self.handle_keypress)
        self.root.bind('<Return>', lambda e: self.button_click('='))
        self.root.bind('<BackSpace>', lambda e: self.button_click('←'))
        self.root.bind('<Delete>', lambda e: self.button_click('C'))
        self.root.bind('<Escape>', lambda e: self.button_click('C'))
        
        # Add touch event bindings
        self.root.bind('<Button-1>', self.handle_touch)
        self.root.bind('<ButtonRelease-1>', self.handle_touch_release)
    
    def handle_keypress(self, event):
        """Handle keyboard input"""
        key = event.char
        valid_chars = '0123456789.+-*/^'
        if key in valid_chars:
            self.button_click(key)
            # Flash the corresponding button
            if key in self.buttons_dict:
                self.flash_button(self.buttons_dict[key])
    
    def handle_touch(self, event):
        """Handle touch/click events"""
        widget = event.widget
        if isinstance(widget, ttk.Button):
            self.flash_button(widget)
    
    def handle_touch_release(self, event):
        """Handle touch/click release events"""
        widget = event.widget
        if isinstance(widget, ttk.Button):
            text = widget.cget('text')
            self.button_click(text)
    
    def flash_button(self, button):
        """Create a visual feedback when a button is pressed"""
        current_style = button.cget('style')
        button.configure(style=current_style + '.Active')
        self.root.after(100, lambda: button.configure(style=current_style))
    
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Color scheme
        colors = {
            'background': '#1A1A2E',  # Dark blue background
            'display_bg': '#16213E',  # Slightly lighter blue for display
            'text_primary': '#FFFFFF',  # White text
            'text_secondary': '#A7A7A7',  # Light gray text
            'accent_blue': '#0F3460',    # Deep blue for operators
            'accent_blue_hover': '#1A4B8C',
            'number_btn': '#2A2A4A',     # Dark purple for number buttons
            'number_btn_hover': '#3A3A5A',
            'clear_btn': '#950101',      # Red for clear buttons
            'clear_btn_hover': '#BC1823',
            'equal_btn': '#1B5E20',      # Green for equals
            'equal_btn_hover': '#2E7D32',
            'border_color': '#E94560'     # Accent color for borders
        }
        
        # Calculate dynamic font sizes based on screen resolution and device type
        screen_height = self.root.winfo_screenheight()
        screen_width = self.root.winfo_screenwidth()
        
        # Detect if likely touch device based on resolution and ratio
        is_touch_device = screen_height / screen_width < 2
        
        # Adjust base font size for touch devices
        if is_touch_device:
            base_font_size = max(14, min(18, int(screen_height / 80)))
            button_padding = int(base_font_size * 1.2)
        else:
            base_font_size = max(10, min(14, int(screen_height / 100)))
            button_padding = int(base_font_size * 0.8)
            
        large_font_size = base_font_size + 4
        
        # Configure root background
        self.root.configure(bg=colors['background'])
        
        # Frame styles with borders
        style.configure("Display.TFrame",
                       background=colors['display_bg'],
                       borderwidth=2,
                       relief="solid")
        
        style.configure("Main.TFrame",
                       background=colors['background'])
        
        # Entry styles with enhanced visibility
        style.configure("Display.TEntry",
                       fieldbackground=colors['display_bg'],
                       foreground=colors['text_primary'],
                       insertcolor=colors['text_primary'],
                       borderwidth=0,
                       relief="flat",
                       font=('Helvetica', large_font_size + 10, 'bold'))
        
        style.configure("Expression.TEntry",
                       fieldbackground=colors['display_bg'],
                       foreground=colors['text_secondary'],
                       insertcolor=colors['text_primary'],
                       borderwidth=0,
                       relief="flat",
                       font=('Helvetica', large_font_size))
        
        # Enhanced button styles with new color scheme
        button_settings = {
            'Num.TButton': (colors['text_primary'], colors['number_btn'], colors['number_btn_hover']),
            'Operator.TButton': (colors['text_primary'], colors['accent_blue'], colors['accent_blue_hover']),
            'Clear.TButton': (colors['text_primary'], colors['clear_btn'], colors['clear_btn_hover']),
            'Equal.TButton': (colors['text_primary'], colors['equal_btn'], colors['equal_btn_hover'])
        }
        
        # Configure button styles with enhanced visual feedback
        for btn_style, (fg, bg, active_bg) in button_settings.items():
            style.layout(btn_style,
                        [('Button.padding', {'children':
                            [('Button.label', {'sticky': 'nswe'})],
                            'sticky': 'nswe'})])
            
            style.configure(btn_style,
                          foreground=fg,
                          background=bg,
                          font=('Helvetica', base_font_size, 'bold'),
                          padding=button_padding,
                          relief='flat',
                          borderwidth=2,
                          highlightthickness=1,
                          highlightcolor=colors['border_color'])
            
            # Enhanced visual feedback for interactions
            style.map(btn_style,
                     foreground=[('pressed', colors['text_primary']), 
                                ('active', colors['text_primary'])],
                     background=[('pressed', active_bg), 
                                ('active', active_bg)],
                     relief=[('pressed', 'sunken'), 
                            ('active', 'flat')])
            
            style.configure(f"{btn_style}.Active",
                          background=active_bg,
                          relief="sunken")
    
    def format_number(self, num):
        """Format number to remove trailing zeros after decimal"""
        if isinstance(num, float):
            # Convert to string and remove trailing zeros
            str_num = f"{num:.10f}".rstrip('0')
            # Remove trailing dot if present
            if str_num.endswith('.'):
                str_num = str_num[:-1]
            return str_num
        return str(num)
    
    def calculate(self, expression):
        try:
            # Replace ^ with ** for power operation
            expression = expression.replace('^', '**')
            result = eval(expression)
            return self.format_number(result)
        except ZeroDivisionError:
            return "Cannot divide by zero"
        except Exception as e:
            return "Error"
            
    def button_click(self, value):
        current_expr = self.expression.get()
        current_result = self.result.get()
        
        if value == "C":
            # Clear everything
            self.expression.set("")
            self.result.set("0")
        
        elif value == "←":
            # Handle backspace
            if current_expr:
                self.expression.set(current_expr[:-1])
                if current_expr[:-1]:
                    self.result.set(self.calculate(current_expr[:-1]))
                else:
                    self.result.set("0")
        
        elif value == "=":
            # Calculate final result
            if current_expr:
                result = self.calculate(current_expr)
                self.expression.set("")
                self.result.set(result)
        
        else:
            # Handle numbers and operators
            new_expr = current_expr + value
            self.expression.set(new_expr)
            
            # Try to calculate intermediate result
            if new_expr:
                try:
                    result = self.calculate(new_expr)
                    self.result.set(result)
                except:
                    # If calculation fails, just show the expression
                    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

