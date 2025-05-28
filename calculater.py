import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x600")  # Increased initial size
        self.root.minsize(350, 500)    # Set minimum size
        self.root.configure(bg="#1E1E1E")
        
        # Make sure window is visible and on top initially
        self.root.attributes('-topmost', True)  # Make window stay on top initially
        self.root.update()
        self.root.attributes('-topmost', False)  # Disable stay on top after window is shown
        
        # Set calculator icon (using ⌘ symbol as a simple calculator icon)
        self.root.iconbitmap() if hasattr(self.root, 'iconbitmap') else None
        
        # Make sure the calculator window is responsive
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
        """Bind keyboard events to calculator functions"""
        self.root.bind('<Key>', self.handle_keypress)
        self.root.bind('<Return>', lambda e: self.button_click('='))
        self.root.bind('<BackSpace>', lambda e: self.button_click('←'))
        self.root.bind('<Delete>', lambda e: self.button_click('C'))
        self.root.bind('<Escape>', lambda e: self.button_click('C'))
    
    def handle_keypress(self, event):
        """Handle keyboard input"""
        key = event.char
        valid_chars = '0123456789.+-*/^'
        if key in valid_chars:
            self.button_click(key)
            # Flash the corresponding button
            if key in self.buttons_dict:
                self.flash_button(self.buttons_dict[key])
    
    def flash_button(self, button):
        """Create a visual feedback when a button is pressed"""
        current_style = button.cget('style')
        button.configure(style=current_style + '.Active')
        self.root.after(100, lambda: button.configure(style=current_style))
    
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame styles
        style.configure("Display.TFrame", background="#1E1E1E")
        style.configure("Main.TFrame", background="#1E1E1E")
        
        # Entry styles
        style.configure("Display.TEntry", 
                       fieldbackground="#2D2D2D",
                       foreground="#FFFFFF",
                       insertcolor="#FFFFFF",
                       borderwidth=0,
                       relief="flat")
        
        style.configure("Expression.TEntry",
                       fieldbackground="#2D2D2D",
                       foreground="#A0A0A0",
                       insertcolor="#FFFFFF",
                       borderwidth=0,
                       relief="flat")
        
        # Button styles - using element creation
        for btn_style in ['Num.TButton', 'Operator.TButton', 'Clear.TButton', 'Equal.TButton']:
            style.layout(btn_style,
                        [('Button.padding', {'children':
                            [('Button.label', {'sticky': 'nswe'})],
                            'sticky': 'nswe'})])

        # Configure button styles with modern colors and effects
        button_settings = {
            'Num.TButton': ('#FFFFFF', '#424242', '#525252'),
            'Operator.TButton': ('#FFFFFF', '#0066cc', '#0077ee'),
            'Clear.TButton': ('#FFFFFF', '#cc3300', '#dd4411'),
            'Equal.TButton': ('#FFFFFF', '#00994c', '#00aa5c')
        }
        
        for btn_style, (fg, bg, active_bg) in button_settings.items():
            style.configure(btn_style,
                          foreground=fg,
                          background=bg,
                          font=('Helvetica', 14, 'bold'),
                          padding=12,
                          relief='flat',
                          borderwidth=0)
            
            # Add hover and pressed effects
            style.map(btn_style,
                     foreground=[('pressed', '#FFFFFF'), ('active', '#FFFFFF')],
                     background=[('pressed', active_bg), ('active', active_bg)],
                     relief=[('pressed', 'sunken'), ('active', 'flat')])
            
            # Add active state configuration
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

