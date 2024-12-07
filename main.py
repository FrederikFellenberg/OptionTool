import tkinter
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class OptionTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Title and size of the window
        self.title('Option Tool')

        self.current_font = None

        # Make Window scalable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.lower_bound_abscissa = float(0)
        self.upper_bound_abscissa = float(100)

        self.lower_bound_ordinate = float(-100)
        self.upper_bound_ordinate = float(100)

        self.factor_long_call = float(1)
        self.factor_short_call = float(1)
        self.factor_long_put = float(1)
        self.factor_short_put = float(1)
        self.factor_asset = float(1)
        self.factor_combined = float(1)

        self.long_call_amount = 0
        self.short_call_amount = 0
        self.long_put_amount = 0
        self.short_put_amount = 0
        self.asset_amount = 0

        self.check_long_call_var = tkinter.StringVar(value="off")
        self.check_long_call_state = self.check_long_call_var.get()

        self.check_short_call_var = tkinter.StringVar(value="off")
        self.check_short_call_state = self.check_short_call_var.get()

        self.check_long_put_var = tkinter.StringVar(value="off")
        self.check_long_put_state = self.check_long_put_var.get()

        self.check_short_put_var = tkinter.StringVar(value="off")
        self.check_short_put_state = self.check_short_put_var.get()

        self.check_asset_var = tkinter.StringVar(value="off")
        self.check_asset_state = self.check_asset_var.get()

        self.selected_button_20_fix = False
        self.selected_button_50_fix = False
        self.selected_button_onehalf_relative = False

        self.toggle_button_20_fix = False
        self.toggle_button_50_fix = False
        self.toggle_button_onehalf_relative = False

        # Start Page Initialization
        self.current_frame = None
        self.create_start_page()

    def create_start_page(self):
        self.clear_current_frame()

        self.long_call_amount = 0
        self.short_call_amount = 0
        self.long_put_amount = 0
        self.short_put_amount = 0
        self.asset_amount = 0

        # Standardwert (Platzhalter) definieren
        self.placeholder_text = "0"
        self.amount_placeholder_text = "1"

        self.long_call_strike = 0
        self.long_call_premium = 0

        self.short_call_strike = 0
        self.short_call_premium = 0

        self.long_put_strike = 0
        self.long_put_premium = 0

        self.short_put_strike = 0
        self.short_put_premium = 0

        self.check_long_call_var = tkinter.StringVar(value="off")
        self.check_long_call_state = self.check_long_call_var.get()

        self.check_short_call_var = tkinter.StringVar(value="off")
        self.check_short_call_state = self.check_short_call_var.get()

        self.check_long_put_var = tkinter.StringVar(value="off")
        self.check_long_put_state = self.check_long_put_var.get()

        self.check_short_put_var = tkinter.StringVar(value="off")
        self.check_short_put_state = self.check_short_put_var.get()

        self.check_asset_var = tkinter.StringVar(value="off")
        self.check_asset_state = self.check_asset_var.get()

        # Main frame for start page
        self.current_frame = ctk.CTkFrame(self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame.grid_rowconfigure(2, weight=1)
        self.current_frame.grid_columnconfigure(0, weight=1)

        # ----------------------------------------------------------------------------------------------------------------------

        # Wrapper frame for Buttons (using grid here)
        self.fg_color = self.current_frame.cget("fg_color")
        self.button_wrapper_frame = ctk.CTkFrame(self.current_frame, fg_color=self.fg_color)
        self.button_wrapper_frame.grid(row=0, column=0, pady=15)
        self.button_wrapper_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

# ----------------------------------------------------------------------------------------------------------------------

        self.long_call_button = ctk.CTkCheckBox(self.button_wrapper_frame, text="Long Call", command=self.on_long_call_button_click,
                                                variable=self.check_long_call_var, onvalue="on", offvalue="off")
        self.long_call_button.grid(row=0, column=0, padx=10, pady=10)

        self.settings_long_call = ctk.CTkFrame(self.button_wrapper_frame)
        self.settings_long_call.grid(row=1, column=0, padx=5, pady=5)
        self.settings_long_call.grid_remove()

        self.long_call_strike_label = ctk.CTkLabel(self.settings_long_call, text="Strike Price: ")
        self.long_call_strike_label.grid(row=0, column=0, padx=5, pady=5)

        self.current_font = self.long_call_strike_label.cget("font")
        self.underlined_font = ctk.CTkFont(family=self.current_font, size=14, underline=True)

        self.long_call_strike_entry = ctk.CTkEntry(self.settings_long_call)
        self.long_call_strike_entry.grid(row=1, column=0, padx=5, pady=5)

        # Platzhalter-Text setzen
        self.set_long_call_strike_placeholder()

        # Events für Fokus und Fokusverlust hinzufügen
        self.long_call_strike_entry.bind("<FocusIn>", self.clear_long_call_strike_placeholder)
        self.long_call_strike_entry.bind("<FocusOut>", self.set_long_call_strike_placeholder)

        self.long_call_strike_entry.bind("<Return>", self.set_long_call_strike_value)

        self.long_call_premium_label = ctk.CTkLabel(self.settings_long_call, text="Premium: ")
        self.long_call_premium_label.grid(row=4, column=0, padx=5, pady=5)

        self.long_call_premium_entry = ctk.CTkEntry(self.settings_long_call)
        self.long_call_premium_entry.grid(row=5, column=0, padx=5, pady=5)

        # Platzhalter-Text setzen
        self.set_long_call_premium_placeholder()

        # Events für Fokus und Fokusverlust hinzufügen
        self.long_call_premium_entry.bind("<FocusIn>", self.clear_long_call_premium_placeholder)
        self.long_call_premium_entry.bind("<FocusOut>", self.set_long_call_premium_placeholder)

        self.long_call_premium_entry.bind("<Return>", self.set_long_call_premium_value)

        self.fg_color_amount = self.long_call_strike_label.cget("fg_color")
        self.long_call_amount_frame = ctk.CTkFrame(self.settings_long_call, fg_color=self.fg_color_amount)
        self.long_call_amount_frame.grid(row=10, padx=5, pady=15)
        self.long_call_amount_frame.grid_columnconfigure((0,1), weight=1)

        self.long_call_amount_label = ctk.CTkLabel(self.long_call_amount_frame, text="Amount: ")
        self.long_call_amount_label.grid(row=0, column=0)

        self.long_call_amount_entry = ctk.CTkEntry(self.long_call_amount_frame, width=50)
        self.long_call_amount_entry.grid(row=0, column=1)

        self.set_long_call_amount_placeholder()

        self.long_call_amount_entry.bind("<FocusIn>", self.clear_long_call_amount_placeholder)
        self.long_call_amount_entry.bind("<FocusOut>", self.set_long_call_amount_placeholder)

        self.long_call_amount_entry.bind("<Return>", self.set_long_call_amount_value)

# ----------------------------------------------------------------------------------------------------------------------

        self.short_call_button = ctk.CTkCheckBox(self.button_wrapper_frame, text="Short Call", command=self.on_short_call_button_click,
                                                 variable=self.check_short_call_var, onvalue="on", offvalue="off")
        self.short_call_button.grid(row=0, column=1, padx=10, pady=10)

        self.settings_short_call = ctk.CTkFrame(self.button_wrapper_frame)
        self.settings_short_call.grid(row=1, column=1, padx=5, pady=5)
        self.settings_short_call.grid_remove()

        self.short_call_strike_label = ctk.CTkLabel(self.settings_short_call, text="Strike Price: ")
        self.short_call_strike_label.grid(row=0, column=0, padx=5, pady=5)

        self.short_call_strike_entry = ctk.CTkEntry(self.settings_short_call)
        self.short_call_strike_entry.grid(row=1, column=0, padx=5, pady=5)

        # Platzhalter-Text setzen
        self.set_short_call_strike_placeholder()

        # Events für Fokus und Fokusverlust hinzufügen
        self.short_call_strike_entry.bind("<FocusIn>", self.clear_short_call_strike_placeholder)
        self.short_call_strike_entry.bind("<FocusOut>", self.set_short_call_strike_placeholder)

        self.short_call_strike_entry.bind("<Return>", self.set_short_call_strike_value)

        self.short_call_premium_label = ctk.CTkLabel(self.settings_short_call, text="Premium: ")
        self.short_call_premium_label.grid(row=4, column=0, padx=5, pady=5)

        self.short_call_premium_entry = ctk.CTkEntry(self.settings_short_call)
        self.short_call_premium_entry.grid(row=5, column=0, padx=5, pady=5)

        # Platzhalter-Text setzen
        self.set_short_call_premium_placeholder()

        # Events für Fokus und Fokusverlust hinzufügen
        self.short_call_premium_entry.bind("<FocusIn>", self.clear_short_call_premium_placeholder)
        self.short_call_premium_entry.bind("<FocusOut>", self.set_short_call_premium_placeholder)

        self.short_call_premium_entry.bind("<Return>", self.set_short_call_premium_value)

        self.short_call_amount_frame = ctk.CTkFrame(self.settings_short_call, fg_color=self.fg_color_amount)
        self.short_call_amount_frame.grid(row=10, padx=5, pady=15)
        self.short_call_amount_frame.grid_columnconfigure((0,1), weight=1)

        self.short_call_amount_label = ctk.CTkLabel(self.short_call_amount_frame, text="Amount: ")
        self.short_call_amount_label.grid(row=0, column=0)

        self.short_call_amount_entry = ctk.CTkEntry(self.short_call_amount_frame, width=50)
        self.short_call_amount_entry.grid(row=0, column=1)

        self.set_short_call_amount_placeholder()

        self.short_call_amount_entry.bind("<FocusIn>", self.clear_short_call_amount_placeholder)
        self.short_call_amount_entry.bind("<FocusOut>", self.set_short_call_amount_placeholder)

        self.short_call_amount_entry.bind("<Return>", self.set_short_call_amount_value)

# ----------------------------------------------------------------------------------------------------------------------

        self.long_put_button = ctk.CTkCheckBox(self.button_wrapper_frame, text="Long Put", command=self.on_long_put_button_click,
                                               variable=self.check_long_put_var, onvalue="on", offvalue="off")
        self.long_put_button.grid(row=0, column=2, padx=10, pady=10)

        self.settings_long_put = ctk.CTkFrame(self.button_wrapper_frame)
        self.settings_long_put.grid(row=1, column=2, padx=5, pady=5)
        self.settings_long_put.grid_remove()

        self.long_put_strike_label = ctk.CTkLabel(self.settings_long_put, text="Strike Price: ")
        self.long_put_strike_label.grid(row=0, column=0, padx=5, pady=5)

        self.long_put_strike_entry = ctk.CTkEntry(self.settings_long_put)
        self.long_put_strike_entry.grid(row=1, column=0, padx=5, pady=5)

        # Platzhalter-Text setzen
        self.set_long_put_strike_placeholder()

        # Events für Fokus und Fokusverlust hinzufügen
        self.long_put_strike_entry.bind("<FocusIn>", self.clear_long_put_strike_placeholder)
        self.long_put_strike_entry.bind("<FocusOut>", self.set_long_put_strike_placeholder)

        self.long_put_strike_entry.bind("<Return>", self.set_long_put_strike_value)

        self.long_put_premium_label = ctk.CTkLabel(self.settings_long_put, text="Premium: ")
        self.long_put_premium_label.grid(row=4, column=0, padx=5, pady=5)

        self.long_put_premium_entry = ctk.CTkEntry(self.settings_long_put)
        self.long_put_premium_entry.grid(row=5, column=0, padx=5, pady=5)

        # Platzhalter-Text setzen
        self.set_long_put_premium_placeholder()

        # Events für Fokus und Fokusverlust hinzufügen
        self.long_put_premium_entry.bind("<FocusIn>", self.clear_long_put_premium_placeholder)
        self.long_put_premium_entry.bind("<FocusOut>", self.set_long_put_premium_placeholder)

        self.long_put_premium_entry.bind("<Return>", self.set_long_put_premium_value)

        self.long_put_amount_frame = ctk.CTkFrame(self.settings_long_put, fg_color=self.fg_color_amount)
        self.long_put_amount_frame.grid(row=10, padx=5, pady=15)
        self.long_put_amount_frame.grid_columnconfigure((0, 1), weight=1)

        self.long_put_amount_label = ctk.CTkLabel(self.long_put_amount_frame, text="Amount: ")
        self.long_put_amount_label.grid(row=0, column=0)

        self.long_put_amount_entry = ctk.CTkEntry(self.long_put_amount_frame, width=50)
        self.long_put_amount_entry.grid(row=0, column=1)

        self.set_long_put_amount_placeholder()

        self.long_put_amount_entry.bind("<FocusIn>", self.clear_long_put_amount_placeholder)
        self.long_put_amount_entry.bind("<FocusOut>", self.set_long_put_amount_placeholder)

        self.long_put_amount_entry.bind("<Return>", self.set_long_put_amount_value)

# ----------------------------------------------------------------------------------------------------------------------

        self.short_put_button = ctk.CTkCheckBox(self.button_wrapper_frame, text="Short Put", command=self.on_short_put_button_click,
                                                variable=self.check_short_put_var, onvalue="on", offvalue="off")
        self.short_put_button.grid(row=0, column=3, padx=10, pady=10)

        self.settings_short_put = ctk.CTkFrame(self.button_wrapper_frame)
        self.settings_short_put.grid(row=1, column=3, padx=5, pady=5)
        self.settings_short_put.grid_remove()

        self.short_put_strike_label = ctk.CTkLabel(self.settings_short_put, text="Strike Price: ")
        self.short_put_strike_label.grid(row=0, column=0, padx=5, pady=5)

        self.short_put_strike_entry = ctk.CTkEntry(self.settings_short_put)
        self.short_put_strike_entry.grid(row=1, column=0, padx=5, pady=5)

        # Platzhalter-Text setzen
        self.set_short_put_strike_placeholder()

        # Events für Fokus und Fokusverlust hinzufügen
        self.short_put_strike_entry.bind("<FocusIn>", self.clear_short_put_strike_placeholder)
        self.short_put_strike_entry.bind("<FocusOut>", self.set_short_put_strike_placeholder)

        self.short_put_strike_entry.bind("<Return>", self.set_short_put_strike_value)

        self.short_put_premium_label = ctk.CTkLabel(self.settings_short_put, text="Premium: ")
        self.short_put_premium_label.grid(row=4, column=0, padx=5, pady=5)

        self.short_put_premium_entry = ctk.CTkEntry(self.settings_short_put)
        self.short_put_premium_entry.grid(row=5, column=0, padx=5, pady=5)

        # Platzhalter-Text setzen
        self.set_short_put_premium_placeholder()

        # Events für Fokus und Fokusverlust hinzufügen
        self.short_put_premium_entry.bind("<FocusIn>", self.clear_short_put_premium_placeholder)
        self.short_put_premium_entry.bind("<FocusOut>", self.set_short_put_premium_placeholder)

        self.short_put_premium_entry.bind("<Return>", self.set_short_put_premium_value)

        self.short_put_amount_frame = ctk.CTkFrame(self.settings_short_put, fg_color=self.fg_color_amount)
        self.short_put_amount_frame.grid(row=10, padx=5, pady=15)
        self.short_put_amount_frame.grid_columnconfigure((0, 1), weight=1)

        self.short_put_amount_label = ctk.CTkLabel(self.short_put_amount_frame, text="Amount: ")
        self.short_put_amount_label.grid(row=0, column=0)

        self.short_put_amount_entry = ctk.CTkEntry(self.short_put_amount_frame, width=50)
        self.short_put_amount_entry.grid(row=0, column=1)

        self.set_short_put_amount_placeholder()

        self.short_put_amount_entry.bind("<FocusIn>", self.clear_short_put_amount_placeholder)
        self.short_put_amount_entry.bind("<FocusOut>", self.set_short_put_amount_placeholder)

        self.short_put_amount_entry.bind("<Return>", self.set_short_put_amount_value)

# ----------------------------------------------------------------------------------------------------------------------

        self.asset_button = ctk.CTkCheckBox(self.button_wrapper_frame, text="Underlying Asset", command=self.on_asset_button_click,
                                            variable=self.check_asset_var, onvalue="on", offvalue="off")
        self.asset_button.grid(row=7, column=1, padx=5, pady=0)


        self.asset_amount_entry = ctk.CTkEntry(self.button_wrapper_frame, width=50)
        self.asset_amount_entry.grid(row=7, column=2, padx=5, pady=10)
        self.asset_amount_entry.grid_remove()

        self.set_asset_amount_placeholder()

        self.asset_amount_entry.bind("<FocusIn>", self.clear_asset_amount_placeholder)
        self.asset_amount_entry.bind("<FocusOut>", self.set_asset_amount_placeholder)

        self.asset_amount_entry.bind("<Return>", self.set_asset_amount_value)

# ----------------------------------------------------------------------------------------------------------------------

        self.advanced_settings_button = ctk.CTkButton(self.button_wrapper_frame, text="Advanced Settings", command=self.on_advanced_settings_button_click)
        self.advanced_settings_button.grid(row=7, column=3, padx=5, pady=0)
        self.button_fg_color = self.advanced_settings_button.cget("fg_color")

# ----------------------------------------------------------------------------------------------------------------------

        # Frame for the graph (using grid here)
        self.graph_frame = ctk.CTkFrame(self.current_frame, corner_radius=0)
        self.graph_frame.grid(row=2, column=0, padx=5, pady=0)
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        # Canvas for matplotlib figure with custom background
        self.fig = Figure()
        graph = FigureCanvasTkAgg(self.fig, self.graph_frame)
        graph.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.option_modelling = OptionModelling(self.fig, self)

# ----------------------------------------------------------------------------------------------------------------------

    def on_long_call_button_click(self):
        self.check_long_call_state = self.check_long_call_var.get()

        if self.check_long_call_state == "on":
            # Show Slider
            self.long_call_amount = 1
            self.settings_long_call.grid(row=1, column=0, pady=5)
            self.option_modelling.plot_long_call(long_call_strike=self.long_call_strike,
                                                 long_call_premium=self.long_call_premium)
        else:
            # Hide
            self.long_call_amount = 0
            self.option_modelling.clear_long_call_plot()
            self.settings_long_call.grid_forget()

    def on_short_call_button_click(self):
        self.check_short_call_state = self.check_short_call_var.get()

        if self.check_short_call_state == "on":
            # Show Slider
            self.short_call_amount = 1
            self.settings_short_call.grid(row=1, column=1, pady=5)
            self.option_modelling.plot_short_call(short_call_strike=self.short_call_strike,
                                                  short_call_premium=self.short_call_premium)
        else:
            # Hide
            self.short_call_amount = 0
            self.option_modelling.clear_short_call_plot()
            self.settings_short_call.grid_forget()

    def on_long_put_button_click(self):
        self.check_long_put_state = self.check_long_put_var.get()

        if self.check_long_put_state == "on":
            # Show Slider
            self.long_put_amount = 1
            self.settings_long_put.grid(row=1, column=2, pady=5)
            self.option_modelling.plot_long_put(long_put_strike=self.long_put_strike,
                                                long_put_premium=self.long_put_premium)
        else:
            # Hide
            self.long_put_amount = 0
            self.option_modelling.clear_long_put_plot()
            self.settings_long_put.grid_forget()

    def on_short_put_button_click(self):
        self.check_short_put_state = self.check_short_put_var.get()

        if self.check_short_put_state == "on":
            # Show Slider
            self.short_put_amount = 1
            self.settings_short_put.grid(row=1, column=3, pady=5)
            self.option_modelling.plot_short_put(short_put_strike=self.short_put_strike,
                                                 short_put_premium=self.short_put_premium)
        else:
            # Hide
            self.short_put_amount = 0
            self.option_modelling.clear_short_put_plot()
            self.settings_short_put.grid_forget()

    def on_asset_button_click(self):
        self.check_asset_state = self.check_asset_var.get()

        if self.check_asset_state == "on":
            self.asset_amount = 1
            self.asset_amount_entry.grid(row=7, column=2, padx=5, pady=10)
            self.option_modelling.plot_asset()
        else:
            # Hide
            self.asset_amount = 0
            self.asset_amount_entry.grid_remove()
            self.option_modelling.clear_asset_plot()

    def on_advanced_settings_button_click(self):
        self.clear_current_frame()

        self.current_frame = ctk.CTkFrame(self)
        self.current_frame.grid(row=0, column=0)
        self.current_frame.grid_columnconfigure((0,1), weight=1)

        self.scale_label = ctk.CTkLabel(self.current_frame, text="Settings to scale the coordinate system", font=self.underlined_font)
        self.scale_label.grid(row=0, column=0, columnspan=2)

        self.scale_lower_bound_abscissa_label = ctk.CTkLabel(self.current_frame, text="Specify a lower bound for the abscissa: ")
        self.scale_lower_bound_abscissa_label.grid(row=1, column=0, pady=10)

        self.scale_lower_bound_abscissa_entry = ctk.CTkEntry(self.current_frame, width=50)
        self.scale_lower_bound_abscissa_entry.grid(row=1, column=1, pady=10)
        self.scale_lower_bound_abscissa_entry.insert(0, self.lower_bound_abscissa)

        self.scale_upper_bound_abscissa_label = ctk.CTkLabel(self.current_frame, text="Specify an upper bound for the abscissa: ")
        self.scale_upper_bound_abscissa_label.grid(row=2, column=0, pady=10)

        self.scale_upper_bound_abscissa_entry = ctk.CTkEntry(self.current_frame, width=50)
        self.scale_upper_bound_abscissa_entry.grid(row=2, column=1, pady=10)
        self.scale_upper_bound_abscissa_entry.insert(0, self.upper_bound_abscissa)

        self.scale_lower_bound_ordinate_label = ctk.CTkLabel(self.current_frame, text="Specify a lower bound for the ordinate: ")
        self.scale_lower_bound_ordinate_label.grid(row=3, column=0, pady=10)

        self.scale_lower_bound_ordinate_entry = ctk.CTkEntry(self.current_frame, width=50)
        self.scale_lower_bound_ordinate_entry.grid(row=3, column=1, pady=10)
        self.scale_lower_bound_ordinate_entry.insert(0, self.lower_bound_ordinate)

        self.scale_upper_bound_ordinate_label = ctk.CTkLabel(self.current_frame, text="Specify an upper bound for the ordinate: ")
        self.scale_upper_bound_ordinate_label.grid(row=4, column=0, pady=10)

        self.scale_upper_bound_ordinate_entry = ctk.CTkEntry(self.current_frame, width=50)
        self.scale_upper_bound_ordinate_entry.grid(row=4, column=1, pady=10)
        self.scale_upper_bound_ordinate_entry.insert(0, self.upper_bound_ordinate)

        self.factor_label = ctk.CTkLabel(self.current_frame, text="Specify the factors that are applied to the financial instruments", font=self.underlined_font)
        self.factor_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.factor_long_call_label = ctk.CTkLabel(self.current_frame, text="Factor for Long Call: ")
        self.factor_long_call_label.grid(row=6, column=0, pady=5)

        self.factor_long_call_entry = ctk.CTkEntry(self.current_frame, width=50)
        self.factor_long_call_entry.grid(row=6, column=1, pady=5)
        self.factor_long_call_entry.insert(0, self.factor_long_call)

        self.factor_short_call_label = ctk.CTkLabel(self.current_frame, text="Factor for Short Call: ")
        self.factor_short_call_label.grid(row=7, column=0, pady=5)

        self.factor_short_call_entry = ctk.CTkEntry(self.current_frame, width=50)
        self.factor_short_call_entry.grid(row=7, column=1, pady=5)
        self.factor_short_call_entry.insert(0, self.factor_short_call)
        
        self.factor_long_put_label = ctk.CTkLabel(self.current_frame, text="Factor for Long Put: ")
        self.factor_long_put_label.grid(row=8, column=0, pady=5)

        self.factor_long_put_entry = ctk.CTkEntry(self.current_frame, width=50)
        self.factor_long_put_entry.grid(row=8, column=1, pady=5)
        self.factor_long_put_entry.insert(0, self.factor_long_put)

        self.factor_short_put_label = ctk.CTkLabel(self.current_frame, text="Factor for Short Put: ")
        self.factor_short_put_label.grid(row=9, column=0, pady=5)

        self.factor_short_put_entry = ctk.CTkEntry(self.current_frame, width=50)
        self.factor_short_put_entry.grid(row=9, column=1, pady=5)
        self.factor_short_put_entry.insert(0, self.factor_short_put)

        self.factor_asset_label = ctk.CTkLabel(self.current_frame, text="Factor for Underlying Asset: ")
        self.factor_asset_label.grid(row=10, column=0, pady=5)

        self.factor_asset_entry = ctk.CTkEntry(self.current_frame, width=50)
        self.factor_asset_entry.grid(row=10, column=1, pady=5)
        self.factor_asset_entry.insert(0, self.factor_asset)

        self.factor_combined_label = ctk.CTkLabel(self.current_frame, text="Factor for Combined Graph: ")
        self.factor_combined_label.grid(row=11, column=0, pady=5)

        self.factor_combined_entry = ctk.CTkEntry(self.current_frame, width=50)
        self.factor_combined_entry.grid(row=11, column=1, pady=5)
        self.factor_combined_entry.insert(0, self.factor_combined)

        self.slider_config_label = ctk.CTkLabel(self.current_frame, text="Configure the slider range", font=self.underlined_font)
        self.slider_config_label.grid(row=12, column=0, columnspan=2, pady=10)

        self.toggle_buttons_wrapper_frame = ctk.CTkFrame(self.current_frame, fg_color=self.fg_color)
        self.toggle_buttons_wrapper_frame.grid(row=13, column=0, columnspan=2, pady=10)
        self.toggle_buttons_wrapper_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.button_20_fix = ctk.CTkButton(self.toggle_buttons_wrapper_frame, text="+20", command=self.press_button_20_fix)
        self.button_20_fix.grid(row=0, column=0)
        if self.selected_button_20_fix == True:
            self.toggle_button_20_fix = True
            self.button_20_fix.configure(fg_color="green")

        self.button_50_fix = ctk.CTkButton(self.toggle_buttons_wrapper_frame, text="+50", command=self.press_button_50_fix)
        self.button_50_fix.grid(row=0, column=1)
        if self.selected_button_50_fix == True:
            self.toggle_button_50_fix = True
            self.button_50_fix.configure(fg_color="green")

        self.button_onehalf_relative = ctk.CTkButton(self.toggle_buttons_wrapper_frame, text="x1.5", command=self.press_button_onehalf_relative)
        self.button_onehalf_relative.grid(row=0, column=2)
        if self.selected_button_onehalf_relative == True:
            self.toggle_button_onehalf_relative = True
            self.button_onehalf_relative.configure(fg_color="green")

        self.apply_buttons_wrapper_frame = ctk.CTkFrame(self.current_frame, fg_color=self.fg_color)
        self.apply_buttons_wrapper_frame.grid(row=14, column=0, columnspan=2, pady=10)
        self.apply_buttons_wrapper_frame.grid_columnconfigure((0,1), weight=1)

        self.button_apply_scaling = ctk.CTkButton(self.apply_buttons_wrapper_frame, text="Apply", command=self.apply_scaling)
        self.button_apply_scaling.grid(row=0, column=0, pady=0)

        self.button_reset = ctk.CTkButton(self.apply_buttons_wrapper_frame, text="Reset", command=self.reset)
        self.button_reset.grid(row=0, column=1, pady=0)

        self.button_back = ctk.CTkButton(self.current_frame, text="Back", command=self.press_back)
        self.button_back.grid(row=15, column=0, columnspan=2, pady=10)

    def press_button_20_fix(self):
        # Ändere Farbe je nach ausgewähltem Zustand
        if not self.toggle_button_20_fix:
            self.button_20_fix.configure(fg_color="green")  # Farbe für ausgewählten Zustand
            self.toggle_button_20_fix = True
            if (not self.toggle_button_50_fix) & (not self.toggle_button_onehalf_relative):
                pass
            else:
                self.button_50_fix.configure(fg_color=self.button_fg_color)
                self.toggle_button_50_fix = False
                self.button_onehalf_relative.configure(fg_color=self.button_fg_color)
                self.toggle_button_onehalf_relative = False

        else:
            self.button_20_fix.configure(fg_color=self.button_fg_color)   # Farbe für nicht ausgewählten Zustand
            self.toggle_button_20_fix = False


    def press_button_50_fix(self):
        if not self.toggle_button_50_fix:
            self.button_50_fix.configure(fg_color="green")
            self.toggle_button_50_fix = True
            if (not self.toggle_button_20_fix) & (not self.toggle_button_onehalf_relative):
                pass
            else:
                self.button_20_fix.configure(fg_color=self.button_fg_color)
                self.toggle_button_20_fix = False
                self.button_onehalf_relative.configure(fg_color=self.button_fg_color)
                self.toggle_button_onehalf_relative = False

        else:
            self.button_50_fix.configure(fg_color=self.button_fg_color)   # Farbe für nicht ausgewählten Zustand
            self.toggle_button_50_fix = False

    def press_button_onehalf_relative(self):
        if not self.toggle_button_onehalf_relative:
            self.button_onehalf_relative.configure(fg_color="green")
            self.toggle_button_onehalf_relative = True
            if (not self.toggle_button_20_fix) & (not self.toggle_button_50_fix):
                pass
            else:
                self.button_20_fix.configure(fg_color=self.button_fg_color)
                self.toggle_button_20_fix = False
                self.button_50_fix.configure(fg_color=self.button_fg_color)
                self.toggle_button_50_fix = False

        else:
            self.button_onehalf_relative.configure(fg_color=self.button_fg_color)  # Farbe für nicht ausgewählten Zustand
            self.toggle_button_onehalf_relative = False

    def apply_scaling(self):
        try:
            self.lower_bound_abscissa = float(self.scale_lower_bound_abscissa_entry.get())
            self.upper_bound_abscissa = float(self.scale_upper_bound_abscissa_entry.get())
            self.lower_bound_ordinate = float(self.scale_lower_bound_ordinate_entry.get())
            self.upper_bound_ordinate = float(self.scale_upper_bound_ordinate_entry.get())
            self.factor_long_call = float(self.factor_long_call_entry.get())
            self.factor_short_call = float(self.factor_short_call_entry.get())
            self.factor_long_put = float(self.factor_long_put_entry.get())
            self.factor_short_put = float(self.factor_short_put_entry.get())
            self.factor_asset = float(self.factor_asset_entry.get())
            self.factor_combined = float(self.factor_combined_entry.get())
            self.selected_button_20_fix = self.toggle_button_20_fix
            self.selected_button_50_fix = self.toggle_button_50_fix
            self.selected_button_onehalf_relative = self.toggle_button_onehalf_relative

            if (self.factor_long_call < 0) or (self.factor_short_call < 0) or (self.factor_long_put < 0) or (self.factor_short_put < 0) or (self.factor_asset < 0) or (self.factor_combined < 0):
                self.apply_scaling_error_label = ctk.CTkLabel(self.current_frame, text="Please enter valid numbers.")
                self.apply_scaling_error_label.grid(row=16, column=0, columnspan=2, pady=10)
            else:
                self.create_start_page()
        except:
            # Überprüfe, ob mindestens ein Entry leer ist
            entries = [
                self.scale_lower_bound_abscissa_entry.get(),
                self.scale_upper_bound_abscissa_entry.get(),
                self.scale_lower_bound_ordinate_entry.get(),
                self.scale_upper_bound_ordinate_entry.get(),
                self.factor_long_call_entry.get(),
                self.factor_short_call_entry.get(),
                self.factor_long_put_entry.get(),
                self.factor_short_put_entry.get(),
                self.factor_asset_entry.get(),
                self.factor_combined_entry.get()
            ]

            # Wenn alle Einträge leer sind, Startseite trotzdem erstellen
            if all(entry == "" for entry in entries):
                self.create_start_page()
            else:
                # Andernfalls Fehlermeldung anzeigen, wenn ein ungültiger Wert vorliegt
                self.apply_scaling_error_label = ctk.CTkLabel(self.current_frame, text="Please enter valid numbers.")
                self.apply_scaling_error_label.grid(row=16, column=0, columnspan=2, pady=10)

    def press_back(self):
        self.create_start_page()

    def reset(self):
        self.lower_bound_abscissa = float(0)
        self.upper_bound_abscissa = float(100)

        self.lower_bound_ordinate = float(-100)
        self.upper_bound_ordinate = float(100)

        self.factor_long_call = float(1)
        self.factor_short_call = float(1)
        self.factor_long_put = float(1)
        self.factor_short_put = float(1)
        self.factor_asset = float(1)
        self.factor_combined = float(1)

        self.selected_button_20_fix = False
        self.selected_button_50_fix = False
        self.selected_button_onehalf_relative = False

        self.toggle_button_20_fix = False
        self.toggle_button_50_fix = False
        self.toggle_button_onehalf_relative = False

        self.create_start_page()

# ----------------------------------------------------------------------------------------------------------------------
    def set_long_call_strike_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.long_call_strike_entry.get():
            self.long_call_strike_entry.insert(0, self.placeholder_text)
            self.long_call_strike_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_long_call_strike_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.long_call_strike_entry.get() == self.placeholder_text:
            self.long_call_strike_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.long_call_strike_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.long_call_strike_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

    def set_long_call_premium_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.long_call_premium_entry.get():
            self.long_call_premium_entry.insert(0, self.placeholder_text)
            self.long_call_premium_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_long_call_premium_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.long_call_premium_entry.get() == self.placeholder_text:
            self.long_call_premium_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.long_call_premium_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.long_call_premium_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

    def set_long_call_amount_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.long_call_amount_entry.get():
            self.long_call_amount_entry.insert(0, self.amount_placeholder_text)
            self.long_call_amount_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_long_call_amount_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.long_call_amount_entry.get() == self.amount_placeholder_text:
            self.long_call_amount_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.long_call_amount_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.long_call_amount_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

# ----------------------------------------------------------------------------------------------------------------------

    def set_short_call_strike_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.short_call_strike_entry.get():
            self.short_call_strike_entry.insert(0, self.placeholder_text)
            self.short_call_strike_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_short_call_strike_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.short_call_strike_entry.get() == self.placeholder_text:
            self.short_call_strike_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.short_call_strike_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.short_call_strike_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

    def set_short_call_premium_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.short_call_premium_entry.get():
            self.short_call_premium_entry.insert(0, self.placeholder_text)
            self.short_call_premium_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_short_call_premium_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.short_call_premium_entry.get() == self.placeholder_text:
            self.short_call_premium_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.short_call_premium_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.short_call_premium_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

    def set_short_call_amount_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.short_call_amount_entry.get():
            self.short_call_amount_entry.insert(0, self.amount_placeholder_text)
            self.short_call_amount_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_short_call_amount_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.short_call_amount_entry.get() == self.amount_placeholder_text:
            self.short_call_amount_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.short_call_amount_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.short_call_amount_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

# ----------------------------------------------------------------------------------------------------------------------

    def set_long_put_strike_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.long_put_strike_entry.get():
            self.long_put_strike_entry.insert(0, self.placeholder_text)
            self.long_put_strike_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_long_put_strike_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.long_put_strike_entry.get() == self.placeholder_text:
            self.long_put_strike_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.long_put_strike_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.long_put_strike_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

    def set_long_put_premium_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.long_put_premium_entry.get():
            self.long_put_premium_entry.insert(0, self.placeholder_text)
            self.long_put_premium_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_long_put_premium_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.long_put_premium_entry.get() == self.placeholder_text:
            self.long_put_premium_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.long_put_premium_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.long_put_premium_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

    def set_long_put_amount_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.long_put_amount_entry.get():
            self.long_put_amount_entry.insert(0, self.amount_placeholder_text)
            self.long_put_amount_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_long_put_amount_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.long_put_amount_entry.get() == self.amount_placeholder_text:
            self.long_put_amount_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.long_put_amount_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.long_put_amount_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

# ----------------------------------------------------------------------------------------------------------------------

    def set_short_put_strike_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.short_put_strike_entry.get():
            self.short_put_strike_entry.insert(0, self.placeholder_text)
            self.short_put_strike_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_short_put_strike_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.short_put_strike_entry.get() == self.placeholder_text:
            self.short_put_strike_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.short_put_strike_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.short_put_strike_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

    def set_short_put_premium_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.short_put_premium_entry.get():
            self.short_put_premium_entry.insert(0, self.placeholder_text)
            self.short_put_premium_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_short_put_premium_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.short_put_premium_entry.get() == self.placeholder_text:
            self.short_put_premium_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.short_put_premium_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.short_put_premium_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

    def set_short_put_amount_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.short_put_amount_entry.get():
            self.short_put_amount_entry.insert(0, self.amount_placeholder_text)
            self.short_put_amount_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_short_put_amount_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.short_put_amount_entry.get() == self.amount_placeholder_text:
            self.short_put_amount_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.short_put_amount_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.short_put_amount_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

# ----------------------------------------------------------------------------------------------------------------------

    def set_asset_amount_placeholder(self, event=None):
        # Überprüfen, ob das Feld leer ist und den Platzhalter setzen
        if not self.asset_amount_entry.get():
            self.asset_amount_entry.insert(0, self.amount_placeholder_text)
            self.asset_amount_entry.configure(text_color="grey")  # Hellgraue Farbe für den Platzhalter

    def clear_asset_amount_placeholder(self, event=None):
        # Überprüfen, ob der Platzhalter-Text gesetzt ist, und das Feld leeren
        if self.asset_amount_entry.get() == self.amount_placeholder_text:
            self.asset_amount_entry.delete(0, "end")
            # Setze die Farbe abhängig vom Modus
            current_mode = ctk.get_appearance_mode()  # Abfrage des aktuellen Modus
            if current_mode == "Dark":
                self.asset_amount_entry.configure(text_color="white")  # Weiße Farbe im Darkmode
            else:
                self.asset_amount_entry.configure(text_color="black")  # Schwarze Farbe im Lightmode

# ----------------------------------------------------------------------------------------------------------------------

    def set_long_call_strike_value(self, event=None):
        try:
            # Wert aus dem Entry-Feld holen und in float umwandeln
            self.long_call_strike = float(self.long_call_strike_entry.get())
            if self.long_call_strike < 0:
                self.long_call_strike_error_label = ctk.CTkLabel(self.settings_long_call, text="Please enter a valid number.")
                self.long_call_strike_error_label.grid(row=2, column=0, padx=5, pady=5)
                try:
                    self.long_call_strike_slider.destroy()
                    self.long_call_strike_slider_label.destroy()
                    try:
                        self.long_call_premium_label.grid_configure(row=3, column=0, padx=5, pady=5)
                        self.long_call_premium_entry.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_call_premium_slider.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_call_premium_slider_label.grid_configure(row=6, column=0, padx=5, pady=5)
                    except:
                        pass
                except:
                    try:
                        self.long_call_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_call_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_call_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.long_call_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass
            else:
                self.option_modelling.plot_long_call(long_call_strike=self.long_call_strike,
                                                     long_call_premium=self.long_call_premium)

                if self.selected_button_20_fix == True:
                    self.long_call_strike_from_var = max(0, round(self.long_call_strike) - 20)
                    self.long_call_strike_to_var = round(self.long_call_strike) + 20
                elif self.selected_button_50_fix == True:
                    self.long_call_strike_from_var = max(0, round(self.long_call_strike) - 50)
                    self.long_call_strike_to_var = round(self.long_call_strike) + 50
                elif self.selected_button_onehalf_relative == True:
                    self.long_call_strike_from_var = round(self.long_call_strike * 0.5)
                    self.long_call_strike_to_var = round(self.long_call_strike * 1.5)
                else:
                    self.long_call_strike_from_var = max(0, round(self.long_call_strike) - 20)
                    self.long_call_strike_to_var = round(self.long_call_strike) + 20

                # Fehlermeldung löschen, wenn der Wert gültig ist
                if hasattr(self, 'long_call_strike_error_label'):
                    self.long_call_strike_error_label.destroy()
                    try:
                        self.long_call_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_call_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_call_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.long_call_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

                # Überprüfen, ob Slider und Label schon existieren und ggf. aktualisieren
                if hasattr(self, 'long_call_strike_slider'):
                    # Zerstöre den alten Slider und erstelle einen neuen mit den aktualisierten Grenzen
                    self.long_call_strike_slider.destroy()

                    # Slider neu erstellen mit den aktualisierten `from_` und `to` Werten
                    self.long_call_strike_slider = ctk.CTkSlider(
                        self.settings_long_call,
                        from_=self.long_call_strike_from_var,
                        to=self.long_call_strike_to_var,
                        command=self.long_call_strike_slider_event,
                        number_of_steps=self.long_call_strike_to_var - self.long_call_strike_from_var,
                    )
                    self.long_call_strike_slider.grid(row=2, column=0, padx=5, pady=5)
                    self.long_call_strike_slider.set(self.long_call_strike)  # Setze den Slider-Wert auf den neuen Mittelwert

                    # Label für den aktuellen Wert des Sliders
                    self.long_call_strike_slider_label.destroy()
                    self.long_call_strike_slider_label = ctk.CTkLabel(self.settings_long_call, text=f"Current Value: {self.long_call_strike}")
                    self.long_call_strike_slider_label.grid(row=3, column=0, padx=5, pady=5)

                    try:
                        self.long_call_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_call_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_call_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.long_call_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

                else:
                    # Slider und Label erstellen, wenn sie noch nicht existieren
                    self.long_call_strike_slider = ctk.CTkSlider(
                        self.settings_long_call,
                        from_=self.long_call_strike_from_var,
                        to=self.long_call_strike_to_var,
                        command=self.long_call_strike_slider_event,
                        number_of_steps=self.long_call_strike_to_var - self.long_call_strike_from_var,
                    )
                    self.long_call_strike_slider.grid(row=2, column=0, padx=5, pady=5)

                    # Label für den aktuellen Wert des Sliders
                    self.long_call_strike_slider_label = ctk.CTkLabel(self.settings_long_call, text=f"Current Value: {self.long_call_strike}")
                    self.long_call_strike_slider_label.grid(row=3, column=0, padx=5, pady=5)

                    try:
                        self.long_call_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_call_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_call_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.long_call_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

        except ValueError:
            if not self.long_call_strike_entry.get():
                self.long_call_strike = 0
                if hasattr(self, 'long_call_strike_error_label'):
                    self.long_call_strike_error_label.destroy()
                try:
                    self.long_call_strike_slider.destroy()
                    self.long_call_strike_slider_label.destroy()
                    self.long_call_strike_error_label.destroy()
                except:
                    pass
            else:
                # Fehlermeldung im Label anzeigen
                self.long_call_strike_error_label = ctk.CTkLabel(self.settings_long_call, text="Please enter a valid number.")
                self.long_call_strike_error_label.grid(row=2, column=0, padx=5, pady=5)
                try:
                    self.long_call_strike_slider.destroy()
                    self.long_call_strike_slider_label.destroy()
                    try:
                        self.long_call_premium_label.grid_configure(row=3, column=0, padx=5, pady=5)
                        self.long_call_premium_entry.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_call_premium_slider.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_call_premium_slider_label.grid_configure(row=6, column=0, padx=5, pady=5)
                    except:
                        pass
                except:
                    try:
                        self.long_call_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_call_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_call_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.long_call_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

    def set_long_call_premium_value(self, event=None):
        try:
            # Wert aus dem Entry-Feld holen und in float umwandeln
            self.long_call_premium = float(self.long_call_premium_entry.get())
            if self.long_call_premium < 0:
                self.long_call_premium_error_label = ctk.CTkLabel(self.settings_long_call, text="Please enter a valid number.")
                self.long_call_premium_error_label.grid(row=8, column=0, padx=5, pady=5)
                try:
                    self.long_call_premium_slider.destroy()
                    self.long_call_premium_slider_label.destroy()
                except:
                    pass
            else:
                self.option_modelling.plot_long_call(long_call_strike=self.long_call_strike,
                                                     long_call_premium=self.long_call_premium)

                if self.selected_button_20_fix == True:
                    self.long_call_premium_from_var = max(0, round(self.long_call_premium) - 20)
                    self.long_call_premium_to_var = round(self.long_call_premium) + 20
                elif self.selected_button_50_fix == True:
                    self.long_call_premium_from_var = max(0, round(self.long_call_premium) - 50)
                    self.long_call_premium_to_var = round(self.long_call_premium) + 50
                elif self.selected_button_onehalf_relative == True:
                    self.long_call_premium_from_var = round(self.long_call_premium * 0.5)
                    self.long_call_premium_to_var = round(self.long_call_premium * 1.5)
                else:
                    self.long_call_premium_from_var = max(0, round(self.long_call_premium) - 20)
                    self.long_call_premium_to_var = round(self.long_call_premium) + 20

                # Fehlermeldung löschen, wenn der Wert gültig ist
                if hasattr(self, 'long_call_premium_error_label'):
                    self.long_call_premium_error_label.destroy()

                # Überprüfen, ob Slider und Label schon existieren und ggf. aktualisieren
                if hasattr(self, 'long_call_premium_slider'):
                    # Zerstöre den alten Slider und erstelle einen neuen mit den aktualisierten Grenzen
                    self.long_call_premium_slider.destroy()

                    # Slider neu erstellen mit den aktualisierten `from_` und `to` Werten
                    self.long_call_premium_slider = ctk.CTkSlider(
                        self.settings_long_call,
                        from_=self.long_call_premium_from_var,
                        to=self.long_call_premium_to_var,
                        command=self.long_call_premium_slider_event,
                        number_of_steps=self.long_call_premium_to_var - self.long_call_premium_from_var,
                    )
                    self.long_call_premium_slider.grid(row=6, column=0, padx=5, pady=5)
                    self.long_call_premium_slider.set(self.long_call_premium)  # Setze den Slider-Wert auf den neuen Mittelwert

                    # Label für den aktuellen Wert des Sliders
                    self.long_call_premium_slider_label.destroy()
                    self.long_call_premium_slider_label = ctk.CTkLabel(self.settings_long_call, text=f"Current Value: {self.long_call_premium}")
                    self.long_call_premium_slider_label.grid(row=7, column=0, padx=5, pady=5)

                else:
                    # Slider und Label erstellen, wenn sie noch nicht existieren
                    self.long_call_premium_slider = ctk.CTkSlider(
                        self.settings_long_call,
                        from_=self.long_call_premium_from_var,
                        to=self.long_call_premium_to_var,
                        command=self.long_call_premium_slider_event,
                        number_of_steps=self.long_call_premium_to_var - self.long_call_premium_from_var,
                    )
                    self.long_call_premium_slider.grid(row=6, column=0, padx=5, pady=5)

                    # Label für den aktuellen Wert des Sliders
                    self.long_call_premium_slider_label = ctk.CTkLabel(self.settings_long_call, text=f"Current Value: {self.long_call_premium}")
                    self.long_call_premium_slider_label.grid(row=7, column=0, padx=5, pady=5)

        except ValueError:
            # Label für die Fehlermeldung initialisieren, wird bei Bedarf angezeigt
            if not self.long_call_premium_entry.get():
                self.long_call_premium = 0
                if hasattr(self, 'long_call_premium_error_label'):
                    self.long_call_premium_error_label.destroy()
                try:
                    self.long_call_premium_slider.destroy()
                    self.long_call_premium_slider_label.destroy()
                except:
                    pass
            else:
                self.long_call_premium_error_label = ctk.CTkLabel(self.settings_long_call, text="Please enter a valid number.")
                self.long_call_premium_error_label.grid(row=8, column=0, padx=5, pady=5)
                try:
                    self.long_call_premium_slider.destroy()
                    self.long_call_premium_slider_label.destroy()
                except:
                    pass

# ----------------------------------------------------------------------------------------------------------------------

    def set_short_call_strike_value(self, event=None):
        try:
            # Wert aus dem Entry-Feld holen und in float umwandeln
            self.short_call_strike = float(self.short_call_strike_entry.get())
            if self.short_call_strike < 0:
                self.short_call_strike_error_label = ctk.CTkLabel(self.settings_short_call, text="Please enter a valid number.")
                self.short_call_strike_error_label.grid(row=2, column=0, padx=5, pady=5)
                try:
                    self.short_call_strike_slider.destroy()
                    self.short_call_strike_slider_label.destroy()
                    try:
                        self.short_call_premium_label.grid_configure(row=3, column=0, padx=5, pady=5)
                        self.short_call_premium_entry.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_call_premium_slider.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_call_premium_slider_label.grid_configure(row=6, column=0, padx=5, pady=5)
                    except:
                        pass
                except:
                    try:
                        self.short_call_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_call_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_call_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.short_call_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass
            else:
                self.option_modelling.plot_short_call(short_call_strike=self.short_call_strike,
                                                      short_call_premium=self.short_call_premium)

                if self.selected_button_20_fix == True:
                    self.short_call_strike_from_var = max(0, round(self.short_call_strike) - 20)
                    self.short_call_strike_to_var = round(self.short_call_strike) + 20
                elif self.selected_button_50_fix == True:
                    self.short_call_strike_from_var = max(0, round(self.short_call_strike) - 50)
                    self.short_call_strike_to_var = round(self.short_call_strike) + 50
                elif self.selected_button_onehalf_relative == True:
                    self.short_call_strike_from_var = round(self.short_call_strike * 0.5)
                    self.short_call_strike_to_var = round(self.short_call_strike * 1.5)
                else:
                    self.short_call_strike_from_var = max(0, round(self.short_call_strike) - 20)
                    self.short_call_strike_to_var = round(self.short_call_strike) + 20

                # Fehlermeldung löschen, wenn der Wert gültig ist
                if hasattr(self, 'short_call_strike_error_label'):
                    self.short_call_strike_error_label.destroy()
                    try:
                        self.short_call_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_call_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_call_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.short_call_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

                # Überprüfen, ob Slider und Label schon existieren und ggf. aktualisieren
                if hasattr(self, 'short_call_strike_slider'):
                    # Zerstöre den alten Slider und erstelle einen neuen mit den aktualisierten Grenzen
                    self.short_call_strike_slider.destroy()

                    # Slider neu erstellen mit den aktualisierten `from_` und `to` Werten
                    self.short_call_strike_slider = ctk.CTkSlider(
                        self.settings_short_call,
                        from_=self.short_call_strike_from_var,
                        to=self.short_call_strike_to_var,
                        command=self.short_call_strike_slider_event,
                        number_of_steps=self.short_call_strike_to_var - self.short_call_strike_from_var,
                    )
                    self.short_call_strike_slider.grid(row=2, column=0, padx=5, pady=5)
                    self.short_call_strike_slider.set(self.short_call_strike)  # Setze den Slider-Wert auf den neuen Mittelwert

                    # Label für den aktuellen Wert des Sliders
                    self.short_call_strike_slider_label.destroy()
                    self.short_call_strike_slider_label = ctk.CTkLabel(self.settings_short_call, text=f"Current Value: {self.short_call_strike}")
                    self.short_call_strike_slider_label.grid(row=3, column=0, padx=5, pady=5)

                    try:
                        self.short_call_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_call_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_call_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.short_call_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

                else:
                    # Slider und Label erstellen, wenn sie noch nicht existieren
                    self.short_call_strike_slider = ctk.CTkSlider(
                        self.settings_short_call,
                        from_=self.short_call_strike_from_var,
                        to=self.short_call_strike_to_var,
                        command=self.short_call_strike_slider_event,
                        number_of_steps=self.short_call_strike_to_var - self.short_call_strike_from_var,
                    )
                    self.short_call_strike_slider.grid(row=2, column=0, padx=5, pady=5)

                    # Label für den aktuellen Wert des Sliders
                    self.short_call_strike_slider_label = ctk.CTkLabel(self.settings_short_call, text=f"Current Value: {self.short_call_strike}")
                    self.short_call_strike_slider_label.grid(row=3, column=0, padx=5, pady=5)

                    try:
                        self.short_call_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_call_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_call_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.short_call_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

        except ValueError:
            if not self.short_call_strike_entry.get():
                self.short_call_strike = 0
                if hasattr(self, 'short_call_strike_error_label'):
                    self.short_call_strike_error_label.destroy()
                try:
                    self.short_call_strike_slider.destroy()
                    self.short_call_strike_slider_label.destroy()
                    self.short_call_strike_error_label.destroy()
                except:
                    pass
            else:
                # Fehlermeldung im Label anzeigen
                self.short_call_strike_error_label = ctk.CTkLabel(self.settings_short_call, text="Please enter a valid number.")
                self.short_call_strike_error_label.grid(row=2, column=0, padx=5, pady=5)
                try:
                    self.short_call_strike_slider.destroy()
                    self.short_call_strike_slider_label.destroy()
                    try:
                        self.short_call_premium_label.grid_configure(row=3, column=0, padx=5, pady=5)
                        self.short_call_premium_entry.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_call_premium_slider.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_call_premium_slider_label.grid_configure(row=6, column=0, padx=5, pady=5)
                    except:
                        pass
                except:
                    try:
                        self.short_call_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_call_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_call_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.short_call_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

    def set_short_call_premium_value(self, event=None):
        try:
            # Wert aus dem Entry-Feld holen und in float umwandeln
            self.short_call_premium = float(self.short_call_premium_entry.get())
            if self.short_call_premium < 0:
                self.short_call_premium_error_label = ctk.CTkLabel(self.settings_short_call, text="Please enter a valid number.")
                self.short_call_premium_error_label.grid(row=8, column=0, padx=5, pady=5)
                try:
                    self.short_call_premium_slider.destroy()
                    self.short_call_premium_slider_label.destroy()
                except:
                    pass
            else:
                self.option_modelling.plot_short_call(short_call_strike=self.short_call_strike,
                                                      short_call_premium=self.short_call_premium)

                if self.selected_button_20_fix == True:
                    self.short_call_premium_from_var = max(0, round(self.short_call_premium) - 20)
                    self.short_call_premium_to_var = round(self.short_call_premium) + 20
                elif self.selected_button_50_fix == True:
                    self.short_call_premium_from_var = max(0, round(self.short_call_premium) - 50)
                    self.short_call_premium_to_var = round(self.short_call_premium) + 50
                elif self.selected_button_onehalf_relative == True:
                    self.short_call_premium_from_var = round(self.short_call_premium * 0.5)
                    self.short_call_premium_to_var = round(self.short_call_premium * 1.5)
                else:
                    self.short_call_premium_from_var = max(0, round(self.short_call_premium) - 20)
                    self.short_call_premium_to_var = round(self.short_call_premium) + 20

                # Fehlermeldung löschen, wenn der Wert gültig ist
                if hasattr(self, 'short_call_premium_error_label'):
                    self.short_call_premium_error_label.destroy()

                # Überprüfen, ob Slider und Label schon existieren und ggf. aktualisieren
                if hasattr(self, 'short_call_premium_slider'):
                    # Zerstöre den alten Slider und erstelle einen neuen mit den aktualisierten Grenzen
                    self.short_call_premium_slider.destroy()

                    # Slider neu erstellen mit den aktualisierten `from_` und `to` Werten
                    self.short_call_premium_slider = ctk.CTkSlider(
                        self.settings_short_call,
                        from_=self.short_call_premium_from_var,
                        to=self.short_call_premium_to_var,
                        command=self.short_call_premium_slider_event,
                        number_of_steps=self.short_call_premium_to_var - self.short_call_premium_from_var,
                    )
                    self.short_call_premium_slider.grid(row=6, column=0, padx=5, pady=5)
                    self.short_call_premium_slider.set(self.short_call_premium)  # Setze den Slider-Wert auf den neuen Mittelwert

                    # Label für den aktuellen Wert des Sliders
                    self.short_call_premium_slider_label.destroy()
                    self.short_call_premium_slider_label = ctk.CTkLabel(self.settings_short_call, text=f"Current Value: {self.short_call_premium}")
                    self.short_call_premium_slider_label.grid(row=7, column=0, padx=5, pady=5)

                else:
                    # Slider und Label erstellen, wenn sie noch nicht existieren
                    self.short_call_premium_slider = ctk.CTkSlider(
                        self.settings_short_call,
                        from_=self.short_call_premium_from_var,
                        to=self.short_call_premium_to_var,
                        command=self.short_call_premium_slider_event,
                        number_of_steps=self.short_call_premium_to_var - self.short_call_premium_from_var,
                    )
                    self.short_call_premium_slider.grid(row=6, column=0, padx=5, pady=5)

                    # Label für den aktuellen Wert des Sliders
                    self.short_call_premium_slider_label = ctk.CTkLabel(self.settings_short_call, text=f"Current Value: {self.short_call_premium}")
                    self.short_call_premium_slider_label.grid(row=7, column=0, padx=5, pady=5)

        except ValueError:
            # Label für die Fehlermeldung initialisieren, wird bei Bedarf angezeigt
            if not self.short_call_premium_entry.get():
                self.short_call_premium = 0
                if hasattr(self, 'long_call_premium_error_label'):
                    self.short_call_premium_error_label.destroy()
                try:
                    self.short_call_premium_slider.destroy()
                    self.short_call_premium_slider_label.destroy()
                except:
                    pass
            else:
                self.short_call_premium_error_label = ctk.CTkLabel(self.settings_short_call, text="Please enter a valid number.")
                self.short_call_premium_error_label.grid(row=8, column=0, padx=5, pady=5)
                try:
                    self.short_call_premium_slider.destroy()
                    self.short_call_premium_slider_label.destroy()
                except:
                    pass

# ----------------------------------------------------------------------------------------------------------------------

    def set_long_put_strike_value(self, event=None):
        try:
            # Wert aus dem Entry-Feld holen und in float umwandeln
            self.long_put_strike = float(self.long_put_strike_entry.get())
            if self.long_put_strike < 0:
                self.long_put_strike_error_label = ctk.CTkLabel(self.settings_long_put, text="Please enter a valid number.")
                self.long_put_strike_error_label.grid(row=2, column=0, padx=5, pady=5)
                try:
                    self.long_put_strike_slider.destroy()
                    self.long_put_strike_slider_label.destroy()
                    try:
                        self.long_put_premium_label.grid_configure(row=3, column=0, padx=5, pady=5)
                        self.long_put_premium_entry.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_put_premium_slider.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_put_premium_slider_label.grid_configure(row=6, column=0, padx=5, pady=5)
                    except:
                        pass
                except:
                    try:
                        self.long_put_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_put_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_put_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.long_put_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass
            else:
                self.option_modelling.plot_long_put(long_put_strike=self.long_put_strike,
                                                    long_put_premium=self.long_put_premium)

                if self.selected_button_20_fix == True:
                    self.long_put_strike_from_var = max(0, round(self.long_put_strike) - 20)
                    self.long_put_strike_to_var = round(self.long_put_strike) + 20
                elif self.selected_button_50_fix == True:
                    self.long_put_strike_from_var = max(0, round(self.long_put_strike) - 50)
                    self.long_put_strike_to_var = round(self.long_put_strike) + 50
                elif self.selected_button_onehalf_relative == True:
                    self.long_put_strike_from_var = round(self.long_put_strike * 0.5)
                    self.long_put_strike_to_var = round(self.long_put_strike * 1.5)
                else:
                    self.long_put_strike_from_var = max(0, round(self.long_put_strike) - 20)
                    self.long_put_strike_to_var = round(self.long_put_strike) + 20

                # Fehlermeldung löschen, wenn der Wert gültig ist
                if hasattr(self, 'long_put_strike_error_label'):
                    self.long_put_strike_error_label.destroy()
                    try:
                        self.long_put_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_put_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_put_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.long_put_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

                # Überprüfen, ob Slider und Label schon existieren und ggf. aktualisieren
                if hasattr(self, 'long_put_strike_slider'):
                    # Zerstöre den alten Slider und erstelle einen neuen mit den aktualisierten Grenzen
                    self.long_put_strike_slider.destroy()

                    # Slider neu erstellen mit den aktualisierten `from_` und `to` Werten
                    self.long_put_strike_slider = ctk.CTkSlider(
                        self.settings_long_put,
                        from_=self.long_put_strike_from_var,
                        to=self.long_put_strike_to_var,
                        command=self.long_put_strike_slider_event,
                        number_of_steps=self.long_put_strike_to_var - self.long_put_strike_from_var,
                    )
                    self.long_put_strike_slider.grid(row=2, column=0, padx=5, pady=5)
                    self.long_put_strike_slider.set(self.long_put_strike)  # Setze den Slider-Wert auf den neuen Mittelwert

                    # Label für den aktuellen Wert des Sliders
                    self.long_put_strike_slider_label.destroy()
                    self.long_put_strike_slider_label = ctk.CTkLabel(self.settings_long_put, text=f"Current Value: {self.long_put_strike}")
                    self.long_put_strike_slider_label.grid(row=3, column=0, padx=5, pady=5)

                    try:
                        self.long_put_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_put_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_put_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.long_put_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

                else:
                    # Slider und Label erstellen, wenn sie noch nicht existieren
                    self.long_put_strike_slider = ctk.CTkSlider(
                        self.settings_long_put,
                        from_=self.long_put_strike_from_var,
                        to=self.long_put_strike_to_var,
                        command=self.long_put_strike_slider_event,
                        number_of_steps=self.long_put_strike_to_var - self.long_put_strike_from_var,
                    )
                    self.long_put_strike_slider.grid(row=2, column=0, padx=5, pady=5)

                    # Label für den aktuellen Wert des Sliders
                    self.long_put_strike_slider_label = ctk.CTkLabel(self.settings_long_put, text=f"Current Value: {self.long_put_strike}")
                    self.long_put_strike_slider_label.grid(row=3, column=0, padx=5, pady=5)

                    try:
                        self.long_put_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_put_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_put_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.long_put_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

        except ValueError:
            if not self.long_put_strike_entry.get():
                self.long_put_strike = 0
                if hasattr(self, 'long_put_strike_error_label'):
                    self.long_put_strike_error_label.destroy()
                try:
                    self.long_put_strike_slider.destroy()
                    self.long_put_strike_slider_label.destroy()
                    self.long_put_strike_error_label.destroy()
                except:
                    pass
            else:
                # Fehlermeldung im Label anzeigen
                self.long_put_strike_error_label = ctk.CTkLabel(self.settings_long_put, text="Please enter a valid number.")
                self.long_put_strike_error_label.grid(row=2, column=0, padx=5, pady=5)
                try:
                    self.long_put_strike_slider.destroy()
                    self.long_put_strike_slider_label.destroy()
                    try:
                        self.long_put_premium_label.grid_configure(row=3, column=0, padx=5, pady=5)
                        self.long_put_premium_entry.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_put_premium_slider.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_put_premium_slider_label.grid_configure(row=6, column=0, padx=5, pady=5)
                    except:
                        pass
                except:
                    try:
                        self.long_put_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.long_put_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.long_put_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.long_put_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

    def set_long_put_premium_value(self, event=None):
        try:
            # Wert aus dem Entry-Feld holen und in int umwandeln
            self.long_put_premium = float(self.long_put_premium_entry.get())
            if self.long_put_premium < 0:
                self.long_put_premium_error_label = ctk.CTkLabel(self.settings_long_put, text="Please enter a valid number.")
                self.long_put_premium_error_label.grid(row=8, column=0, padx=5, pady=5)
                try:
                    self.long_put_premium_slider.destroy()
                    self.long_put_premium_slider_label.destroy()
                except:
                    pass
            else:
                self.option_modelling.plot_long_put(long_put_strike=self.long_put_strike,
                                                    long_put_premium=self.long_put_premium)

                if self.selected_button_20_fix == True:
                    self.long_put_premium_from_var = max(0, round(self.long_put_premium) - 20)
                    self.long_put_premium_to_var = round(self.long_put_premium) + 20
                elif self.selected_button_50_fix == True:
                    self.long_put_premium_from_var = max(0, round(self.long_put_premium) - 50)
                    self.long_put_premium_to_var = round(self.long_put_premium) + 50
                elif self.selected_button_onehalf_relative == True:
                    self.long_put_premium_from_var = round(self.long_put_premium * 0.5)
                    self.long_put_premium_to_var = round(self.long_put_premium * 1.5)
                else:
                    self.long_put_premium_from_var = max(0, round(self.long_put_premium) - 20)
                    self.long_put_premium_to_var = round(self.long_put_premium) + 20

                # Fehlermeldung löschen, wenn der Wert gültig ist
                if hasattr(self, 'long_put_premium_error_label'):
                    self.long_put_premium_error_label.destroy()

                # Überprüfen, ob Slider und Label schon existieren und ggf. aktualisieren
                if hasattr(self, 'long_put_premium_slider'):
                    # Zerstöre den alten Slider und erstelle einen neuen mit den aktualisierten Grenzen
                    self.long_put_premium_slider.destroy()

                    # Slider neu erstellen mit den aktualisierten `from_` und `to` Werten
                    self.long_put_premium_slider = ctk.CTkSlider(
                        self.settings_long_put,
                        from_=self.long_put_premium_from_var,
                        to=self.long_put_premium_to_var,
                        command=self.long_put_premium_slider_event,
                        number_of_steps=self.long_put_premium_to_var - self.long_put_premium_from_var,
                    )
                    self.long_put_premium_slider.grid(row=6, column=0, padx=5, pady=5)
                    self.long_put_premium_slider.set(self.long_put_premium)  # Setze den Slider-Wert auf den neuen Mittelwert

                    # Label für den aktuellen Wert des Sliders
                    self.long_put_premium_slider_label.destroy()
                    self.long_put_premium_slider_label = ctk.CTkLabel(self.settings_long_put, text=f"Current Value: {self.long_put_premium}")
                    self.long_put_premium_slider_label.grid(row=7, column=0, padx=5, pady=5)

                else:
                    # Slider und Label erstellen, wenn sie noch nicht existieren
                    self.long_put_premium_slider = ctk.CTkSlider(
                        self.settings_long_put,
                        from_=self.long_put_premium_from_var,
                        to=self.long_put_premium_to_var,
                        command=self.long_put_premium_slider_event,
                        number_of_steps=self.long_put_premium_to_var - self.long_put_premium_from_var,
                    )
                    self.long_put_premium_slider.grid(row=6, column=0, padx=5, pady=5)

                    # Label für den aktuellen Wert des Sliders
                    self.long_put_premium_slider_label = ctk.CTkLabel(self.settings_long_put, text=f"Current Value: {self.long_put_premium}")
                    self.long_put_premium_slider_label.grid(row=7, column=0, padx=5, pady=5)

        except ValueError:
            # Label für die Fehlermeldung initialisieren, wird bei Bedarf angezeigt
            if not self.long_put_premium_entry.get():
                self.long_put_premium = 0
                if hasattr(self, 'long_put_premium_error_label'):
                    self.long_put_premium_error_label.destroy()
                try:
                    self.long_put_premium_slider.destroy()
                    self.long_put_premium_slider_label.destroy()
                except:
                    pass
            else:
                self.long_put_premium_error_label = ctk.CTkLabel(self.settings_long_put, text="Please enter a valid number.")
                self.long_put_premium_error_label.grid(row=8, column=0, padx=5, pady=5)
                try:
                    self.long_put_premium_slider.destroy()
                    self.long_put_premium_slider_label.destroy()
                except:
                    pass

# ----------------------------------------------------------------------------------------------------------------------

    def set_short_put_strike_value(self, event=None):
        try:
            # Wert aus dem Entry-Feld holen und in float umwandeln
            self.short_put_strike = float(self.short_put_strike_entry.get())
            if self.short_put_strike < 0:
                self.short_put_strike_error_label = ctk.CTkLabel(self.settings_short_put, text="Please enter a valid number.")
                self.short_put_strike_error_label.grid(row=2, column=0, padx=5, pady=5)
                try:
                    self.short_put_strike_slider.destroy()
                    self.short_put_strike_slider_label.destroy()
                    try:
                        self.short_put_premium_label.grid_configure(row=3, column=0, padx=5, pady=5)
                        self.short_put_premium_entry.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_put_premium_slider.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_put_premium_slider_label.grid_configure(row=6, column=0, padx=5, pady=5)
                    except:
                        pass
                except:
                    try:
                        self.short_put_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_put_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_put_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.short_put_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass
            else:
                self.option_modelling.plot_short_put(short_put_strike=self.short_put_strike,
                                                     short_put_premium=self.short_put_premium)

                if self.selected_button_20_fix == True:
                    self.short_put_strike_from_var = max(0, round(self.short_put_strike) - 20)
                    self.short_put_strike_to_var = round(self.short_put_strike) + 20
                elif self.selected_button_50_fix == True:
                    self.short_put_strike_from_var = max(0, round(self.short_put_strike) - 50)
                    self.short_put_strike_to_var = round(self.short_put_strike) + 50
                elif self.selected_button_onehalf_relative == True:
                    self.short_put_strike_from_var = round(self.short_put_strike * 0.5)
                    self.short_put_strike_to_var = round(self.short_put_strike * 1.5)
                else:
                    self.short_put_strike_from_var = max(0, round(self.short_put_strike) - 20)
                    self.short_put_strike_to_var = round(self.short_put_strike) + 20

                # Fehlermeldung löschen, wenn der Wert gültig ist
                if hasattr(self, 'short_put_strike_error_label'):
                    self.short_put_strike_error_label.destroy()
                    try:
                        self.short_put_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_put_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_put_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.short_put_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

                # Überprüfen, ob Slider und Label schon existieren und ggf. aktualisieren
                if hasattr(self, 'short_put_strike_slider'):
                    # Zerstöre den alten Slider und erstelle einen neuen mit den aktualisierten Grenzen
                    self.short_put_strike_slider.destroy()

                    # Slider neu erstellen mit den aktualisierten `from_` und `to` Werten
                    self.short_put_strike_slider = ctk.CTkSlider(
                        self.settings_short_put,
                        from_=self.short_put_strike_from_var,
                        to=self.short_put_strike_to_var,
                        command=self.short_put_strike_slider_event,
                        number_of_steps=self.short_put_strike_to_var - self.short_put_strike_from_var,
                    )
                    self.short_put_strike_slider.grid(row=2, column=0, padx=5, pady=5)
                    self.short_put_strike_slider.set(self.short_put_strike)  # Setze den Slider-Wert auf den neuen Mittelwert

                    # Label für den aktuellen Wert des Sliders
                    self.short_put_strike_slider_label.destroy()
                    self.short_put_strike_slider_label = ctk.CTkLabel(self.settings_short_put, text=f"Current Value: {self.short_put_strike}")
                    self.short_put_strike_slider_label.grid(row=3, column=0, padx=5, pady=5)

                    try:
                        self.short_put_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_put_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_put_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.short_put_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

                else:
                    # Slider und Label erstellen, wenn sie noch nicht existieren
                    self.short_put_strike_slider = ctk.CTkSlider(
                        self.settings_short_put,
                        from_=self.short_put_strike_from_var,
                        to=self.short_put_strike_to_var,
                        command=self.short_put_strike_slider_event,
                        number_of_steps=self.short_put_strike_to_var - self.short_put_strike_from_var,
                    )
                    self.short_put_strike_slider.grid(row=2, column=0, padx=5, pady=5)

                    # Label für den aktuellen Wert des Sliders
                    self.short_put_strike_slider_label = ctk.CTkLabel(self.settings_short_put, text=f"Current Value: {self.short_put_strike}")
                    self.short_put_strike_slider_label.grid(row=3, column=0, padx=5, pady=5)

                    try:
                        self.short_put_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_put_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_put_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.short_put_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

        except ValueError:
            if not self.short_put_strike_entry.get():
                self.short_put_strike = 0
                if hasattr(self, 'short_put_strike_error_label'):
                    self.short_put_strike_error_label.destroy()
                try:
                    self.short_put_strike_slider.destroy()
                    self.short_put_strike_slider_label.destroy()
                    self.short_put_strike_error_label.destroy()
                except:
                    pass
            else:
                # Fehlermeldung im Label anzeigen
                self.short_put_strike_error_label = ctk.CTkLabel(self.settings_short_put, text="Please enter a valid number.")
                self.short_put_strike_error_label.grid(row=2, column=0, padx=5, pady=5)
                try:
                    self.short_put_strike_slider.destroy()
                    self.short_put_strike_slider_label.destroy()
                    try:
                        self.short_put_premium_label.grid_configure(row=3, column=0, padx=5, pady=5)
                        self.short_put_premium_entry.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_put_premium_slider.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_put_premium_slider_label.grid_configure(row=6, column=0, padx=5, pady=5)
                    except:
                        pass
                except:
                    try:
                        self.short_put_premium_label.grid_configure(row=4, column=0, padx=5, pady=5)
                        self.short_put_premium_entry.grid_configure(row=5, column=0, padx=5, pady=5)
                        self.short_put_premium_slider.grid_configure(row=6, column=0, padx=5, pady=5)
                        self.short_put_premium_slider_label.grid_configure(row=7, column=0, padx=5, pady=5)
                    except:
                        pass

    def set_short_put_premium_value(self, event=None):
        try:
            # Wert aus dem Entry-Feld holen und in float umwandeln
            self.short_put_premium = float(self.short_put_premium_entry.get())
            if self.short_put_premium < 0:
                self.short_put_premium_error_label = ctk.CTkLabel(self.settings_short_put, text="Please enter a valid number.")
                self.short_put_premium_error_label.grid(row=8, column=0, padx=5, pady=5)
                try:
                    self.short_put_premium_slider.destroy()
                    self.short_put_premium_slider_label.destroy()
                except:
                    pass
            else:
                self.option_modelling.plot_short_put(short_put_strike=self.short_put_strike,
                                                     short_put_premium=self.short_put_premium)

                if self.selected_button_20_fix == True:
                    self.short_put_premium_from_var = max(0, round(self.short_put_premium) - 20)
                    self.short_put_premium_to_var = round(self.short_put_premium) + 20
                elif self.selected_button_50_fix == True:
                    self.short_put_premium_from_var = max(0, round(self.short_put_premium) - 50)
                    self.short_put_premium_to_var = round(self.short_put_premium) + 50
                elif self.selected_button_onehalf_relative == True:
                    self.short_put_premium_from_var = round(self.short_put_premium * 0.5)
                    self.short_put_premium_to_var = round(self.short_put_premium * 1.5)
                else:
                    self.short_put_premium_from_var = max(0, round(self.short_put_premium) - 20)
                    self.short_put_premium_to_var = round(self.short_put_premium) + 20

                # Fehlermeldung löschen, wenn der Wert gültig ist
                if hasattr(self, 'short_put_premium_error_label'):
                    self.short_put_premium_error_label.destroy()

                # Überprüfen, ob Slider und Label schon existieren und ggf. aktualisieren
                if hasattr(self, 'short_put_premium_slider'):
                    # Zerstöre den alten Slider und erstelle einen neuen mit den aktualisierten Grenzen
                    self.short_put_premium_slider.destroy()

                    # Slider neu erstellen mit den aktualisierten `from_` und `to` Werten
                    self.short_put_premium_slider = ctk.CTkSlider(
                        self.settings_short_put,
                        from_=self.short_put_premium_from_var,
                        to=self.short_put_premium_to_var,
                        command=self.short_put_premium_slider_event,
                        number_of_steps=self.short_put_premium_to_var - self.short_put_premium_from_var,
                    )
                    self.short_put_premium_slider.grid(row=6, column=0, padx=5, pady=5)
                    self.short_put_premium_slider.set(self.short_put_premium)  # Setze den Slider-Wert auf den neuen Mittelwert

                    # Label für den aktuellen Wert des Sliders
                    self.short_put_premium_slider_label.destroy()
                    self.short_put_premium_slider_label = ctk.CTkLabel(self.settings_short_put, text=f"Current Value: {self.short_put_premium}")
                    self.short_put_premium_slider_label.grid(row=7, column=0, padx=5, pady=5)

                else:
                    # Slider und Label erstellen, wenn sie noch nicht existieren
                    self.short_put_premium_slider = ctk.CTkSlider(
                        self.settings_short_put,
                        from_=self.short_put_premium_from_var,
                        to=self.short_put_premium_to_var,
                        command=self.short_put_premium_slider_event,
                        number_of_steps=self.short_put_premium_to_var - self.short_put_premium_from_var,
                    )
                    self.short_put_premium_slider.grid(row=6, column=0, padx=5, pady=5)

                    # Label für den aktuellen Wert des Sliders
                    self.short_put_premium_slider_label = ctk.CTkLabel(self.settings_short_put, text=f"Current Value: {self.short_put_premium}")
                    self.short_put_premium_slider_label.grid(row=7, column=0, padx=5, pady=5)

        except ValueError:
            # Label für die Fehlermeldung initialisieren, wird bei Bedarf angezeigt
            if not self.short_put_premium_entry.get():
                self.short_put_premium = 0
                if hasattr(self, 'short_put_premium_error_label'):
                    self.short_put_premium_error_label.destroy()
                try:
                    self.short_put_premium_slider.destroy()
                    self.short_put_premium_slider_label.destroy()
                except:
                    pass
            else:
                self.short_put_premium_error_label = ctk.CTkLabel(self.settings_short_put, text="Please enter a valid number.")
                self.short_put_premium_error_label.grid(row=8, column=0, padx=5, pady=5)
                try:
                    self.short_put_premium_slider.destroy()
                    self.short_put_premium_slider_label.destroy()
                except:
                    pass

# ----------------------------------------------------------------------------------------------------------------------
    def set_long_call_amount_value(self, event=None):
        try:
            self.long_call_amount = float(self.long_call_amount_entry.get())
            if self.long_call_amount < 0:
                self.long_call_amount_error_label = ctk.CTkLabel(self.settings_long_call,
                                                                 text="Please enter a valid number.")
                self.long_call_amount_error_label.grid(row=11, column=0, padx=5, pady=0)
            else:
                self.option_modelling.plot_long_call(long_call_strike=self.long_call_strike,
                                                     long_call_premium=self.long_call_premium)
                if hasattr(self, 'long_call_amount_error_label'):
                    self.long_call_amount_error_label.destroy()
        except:
            self.long_call_amount_error_label = ctk.CTkLabel(self.settings_long_call, text="Please enter a valid number.")
            self.long_call_amount_error_label.grid(row=11, column=0, padx=5, pady=0)

    def set_short_call_amount_value(self, event=None):
        try:
            self.short_call_amount = float(self.short_call_amount_entry.get())
            if self.short_call_amount < 0:
                self.short_call_amount_error_label = ctk.CTkLabel(self.settings_short_call,
                                                                  text="Please enter a valid number.")
                self.short_call_amount_error_label.grid(row=11, column=0, padx=5, pady=0)
            else:
                self.option_modelling.plot_short_call(short_call_strike=self.short_call_strike,
                                                      short_call_premium=self.short_call_premium)
                if hasattr(self, 'short_call_amount_error_label'):
                    self.short_call_amount_error_label.destroy()
        except:
            self.short_call_amount_error_label = ctk.CTkLabel(self.settings_short_call, text="Please enter a valid number.")
            self.short_call_amount_error_label.grid(row=11, column=0, padx=5, pady=0)

    def set_long_put_amount_value(self, event=None):
        try:
            self.long_put_amount = float(self.long_put_amount_entry.get())
            if self.long_put_amount < 0:
                self.long_put_amount_error_label = ctk.CTkLabel(self.settings_long_put,
                                                                text="Please enter a valid number.")
                self.long_put_amount_error_label.grid(row=11, column=0, padx=5, pady=0)
            else:
                self.option_modelling.plot_long_put(long_put_strike=self.long_put_strike,
                                                    long_put_premium=self.long_put_premium)
                if hasattr(self, 'long_put_amount_error_label'):
                    self.long_put_amount_error_label.destroy()
        except:
            self.long_put_amount_error_label = ctk.CTkLabel(self.settings_long_put, text="Please enter a valid number.")
            self.long_put_amount_error_label.grid(row=11, column=0, padx=5, pady=0)

    def set_short_put_amount_value(self, event=None):
        try:
            self.short_put_amount = float(self.short_put_amount_entry.get())
            if self.short_put_amount < 0:
                self.short_put_amount_error_label = ctk.CTkLabel(self.settings_short_put,
                                                                 text="Please enter a valid number.")
                self.short_put_amount_error_label.grid(row=11, column=0, padx=5, pady=0)
            else:
                self.option_modelling.plot_short_put(short_put_strike=self.short_put_strike,
                                                     short_put_premium=self.short_put_premium)
                if hasattr(self, 'short_put_amount_error_label'):
                    self.short_put_amount_error_label.destroy()
        except:
            self.short_put_amount_error_label = ctk.CTkLabel(self.settings_short_put, text="Please enter a valid number.")
            self.short_put_amount_error_label.grid(row=11, column=0, padx=5, pady=0)

    def set_asset_amount_value(self, event=None):
        try:
            self.asset_amount = float(self.asset_amount_entry.get())
            if self.asset_amount < 0:
                self.asset_amount_error_label = ctk.CTkLabel(self.button_wrapper_frame, text="Please enter a valid number.")
                self.asset_amount_error_label.grid(row=8, column=1, columnspan=2, pady=0)
            else:
                self.option_modelling.plot_asset()
                if hasattr(self, 'asset_amount_error_label'):
                    self.asset_amount_error_label.destroy()
        except:
            self.asset_amount_error_label = ctk.CTkLabel(self.button_wrapper_frame, text="Please enter a valid number.")
            self.asset_amount_error_label.grid(row=8, column=1, columnspan=2, pady=0)

# ----------------------------------------------------------------------------------------------------------------------

    def long_call_strike_slider_event(self, value):
        self.long_call_strike = int(value)
        self.long_call_strike_slider_label.configure(text=f"Current Value: {self.long_call_strike}")
        self.option_modelling.plot_long_call(long_call_strike=self.long_call_strike,
                                             long_call_premium=self.long_call_premium)

    def long_call_premium_slider_event(self, value):
        self.long_call_premium = int(value)
        self.long_call_premium_slider_label.configure(text=f"Current Value: {self.long_call_premium}")
        self.option_modelling.plot_long_call(long_call_strike=self.long_call_strike,
                                             long_call_premium=self.long_call_premium)

# ----------------------------------------------------------------------------------------------------------------------

    def short_call_strike_slider_event(self, value):
        self.short_call_strike = int(value)
        self.short_call_strike_slider_label.configure(text=f"Current Value: {self.short_call_strike}")
        self.option_modelling.plot_short_call(short_call_strike=self.short_call_strike,
                                              short_call_premium=self.short_call_premium)

    def short_call_premium_slider_event(self, value):
        self.short_call_premium = int(value)
        self.short_call_premium_slider_label.configure(text=f"Current Value: {self.short_call_premium}")
        self.option_modelling.plot_short_call(short_call_strike=self.short_call_strike,
                                              short_call_premium=self.short_call_premium)

# ----------------------------------------------------------------------------------------------------------------------

    def long_put_strike_slider_event(self, value):
        self.long_put_strike = int(value)
        self.long_put_strike_slider_label.configure(text=f"Current Value: {self.long_put_strike}")
        self.option_modelling.plot_long_put(long_put_strike=self.long_put_strike,
                                            long_put_premium=self.long_put_premium)

    def long_put_premium_slider_event(self, value):
        self.long_put_premium = int(value)
        self.long_put_premium_slider_label.configure(text=f"Current Value: {self.long_put_premium}")
        self.option_modelling.plot_long_put(long_put_strike=self.long_put_strike,
                                            long_put_premium=self.long_put_premium)

# ----------------------------------------------------------------------------------------------------------------------
    def short_put_strike_slider_event(self, value):
        self.short_put_strike = int(value)
        self.short_put_strike_slider_label.configure(text=f"Current Value: {self.short_put_strike}")
        self.option_modelling.plot_short_put(short_put_strike=self.short_put_strike,
                                             short_put_premium=self.short_put_premium)

    def short_put_premium_slider_event(self, value):
        self.short_put_premium = int(value)
        self.short_put_premium_slider_label.configure(text=f"Current Value: {self.short_put_premium}")
        self.option_modelling.plot_short_put(short_put_strike=self.short_put_strike,
                                             short_put_premium=self.short_put_premium)

# ----------------------------------------------------------------------------------------------------------------------
    def clear_current_frame(self):
        if self.current_frame is not None:
            self.current_frame.grid_forget()
            self.current_frame.destroy()

# ----------------------------------------------------------------------------------------------------------------------
class OptionModelling(OptionTool):
    def __init__(self, fig, option_tool):
        self.fig = fig
        self.option_tool = option_tool
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.yaxis.set_ticks_position('left')
        self.ax.set_xlim(float(self.option_tool.lower_bound_abscissa), float(self.option_tool.upper_bound_abscissa))
        self.ax.set_ylim(float(self.option_tool.lower_bound_ordinate), float(self.option_tool.upper_bound_ordinate))
        self.ax.grid(False)
        self.ax.set_title("Options Graph")
        self.ax.set_xlabel("Underlying Price")
        self.ax.set_ylabel("Payoff")
        self.ax.axhline(0, color="black", linewidth=0.5)

        self.fixed_yticks = self.ax.get_yticks()  # Dies sind die ursprünglichen "festen" Ticks
        self.fixed_xticks = self.ax.get_xticks()

        self.underlying = np.linspace(self.option_tool.lower_bound_abscissa, self.option_tool.upper_bound_abscissa, 1000)
        self.payoff_long_call = self.option_tool.factor_long_call * np.maximum(self.underlying, 0)
        self.payoff_short_call = self.option_tool.factor_short_call * np.minimum(-self.underlying, 0)
        self.payoff_long_put = self.option_tool.factor_long_put * np.maximum(-self.underlying, 0)
        self.payoff_short_put = self.option_tool.factor_short_put * np.minimum(self.underlying, 0)
        self.payoff_asset = self.option_tool.factor_asset * self.underlying

        self.hidden_payoff_long_call = np.maximum(self.underlying, 0)
        self.hidden_payoff_short_call = np.minimum(-self.underlying, 0)
        self.hidden_payoff_long_put = np.maximum(-self.underlying, 0)
        self.hidden_payoff_short_put = np.minimum(self.underlying, 0)
        self.hidden_payoff_asset = self.underlying

        # Linien-Objekte für jeden Options-Typ initialisieren (aber nicht zeichnen)
        self.long_call_line, = self.ax.plot([], [], label="Long Call", visible=False)
        self.short_call_line, = self.ax.plot([], [], label="Short Call", visible=False)
        self.long_put_line, = self.ax.plot([], [], label="Long Put", visible=False)
        self.short_put_line, = self.ax.plot([], [], label="Short Put", visible=False)
        self.asset_line, = self.ax.plot([], [], label="Asset", visible=False)
        self.combined_line, = self.ax.plot([], [], label="Combined", visible=False)

        self.scatter_point_long_call = None  # Keine Punkte zu Beginn
        self.scatter_point_short_call = None
        self.scatter_point_long_put = None
        self.scatter_point_short_put = None

    def plot_long_call(self, long_call_strike, long_call_premium):
        self.payoff_long_call = self.option_tool.factor_long_call * (np.maximum(self.underlying - long_call_strike, 0) - long_call_premium)
        self.hidden_payoff_long_call = np.maximum(self.underlying - long_call_strike, 0) - long_call_premium
        self.long_call_line.set_data(self.underlying, self.payoff_long_call)
        self.long_call_line.set_visible(True)
        self.total_amount = self.option_tool.long_call_amount + \
                            self.option_tool.short_call_amount + \
                            self.option_tool.long_put_amount + \
                            self.option_tool.short_put_amount + \
                            self.option_tool.asset_amount
        elements = [self.option_tool.check_long_call_state,
                    self.option_tool.check_short_call_state,
                    self.option_tool.check_long_put_state,
                    self.option_tool.check_short_put_state,
                    self.option_tool.check_asset_state]

        custom_yticks = []  # Liste für benutzerdefinierte Ticks
        # Hinzufügen eines neuen Y-Ticks
        new_ytick_value = self.option_tool.factor_long_call * (-long_call_premium)
        if new_ytick_value not in custom_yticks:
            custom_yticks.append(new_ytick_value)  # Füge den neuen Tick zur Liste der benutzerdefinierten Ticks hinzu
        combined_yticks = np.concatenate((self.fixed_yticks, custom_yticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_yticks(combined_yticks)
        # Aktualisieren der Y-Tick-Beschriftungen und Farben
        ytick_labels = [str(tick) for tick in combined_yticks]
        self.ax.set_yticklabels(ytick_labels)
        self.ax.tick_params(axis='y', which='both', labelcolor='black')
        ylabels = self.ax.get_yticklabels()
        ylabels[-1].set_color('blue')  # Setze den letzten Y-Tick auf blau

        custom_xticks = []  # Liste für benutzerdefinierte Ticks
        # Hinzufügen eines neuen X-Ticks
        new_xtick_value = long_call_strike + long_call_premium
        if new_xtick_value not in custom_xticks:
            custom_xticks.append(new_xtick_value)  # Füge den neuen Tick zur Liste der benutzerdefinierten Ticks hinzu
        # Setzen der kombinierten Ticks auf der X-Achse
        combined_xticks = np.concatenate((self.fixed_xticks, custom_xticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_xticks(combined_xticks)
        # Aktualisieren der X-Tick-Beschriftungen und Farben
        xtick_labels = [str(tick) for tick in combined_xticks]
        self.ax.set_xticklabels(xtick_labels)
        self.ax.tick_params(axis='x', which='both', labelcolor='black')
        xlabels = self.ax.get_xticklabels()
        xlabels[-1].set_color('blue')  # Setze den letzten X-Tick auf blau

        if self.scatter_point_long_call is not None:
            self.scatter_point_long_call.remove()
        self.scatter_point_long_call = self.ax.scatter(new_xtick_value, 0, color='blue')

        if elements.count("on") >= 2:
            self.plot_combined()
        else:
            self.update_legend()

    def plot_short_call(self, short_call_strike, short_call_premium):
        self.payoff_short_call = self.option_tool.factor_short_call * (np.minimum(short_call_strike - self.underlying, 0) + short_call_premium)
        self.hidden_payoff_short_call = np.minimum(short_call_strike - self.underlying, 0) + short_call_premium
        self.short_call_line.set_data(self.underlying, self.payoff_short_call)
        self.short_call_line.set_visible(True)
        self.total_amount = self.option_tool.long_call_amount + \
                            self.option_tool.short_call_amount + \
                            self.option_tool.long_put_amount + \
                            self.option_tool.short_put_amount + \
                            self.option_tool.asset_amount
        elements = [self.option_tool.check_long_call_state,
                    self.option_tool.check_short_call_state,
                    self.option_tool.check_long_put_state,
                    self.option_tool.check_short_put_state,
                    self.option_tool.check_asset_state]

        custom_yticks = []  # Liste für benutzerdefinierte Ticks
        # Hinzufügen eines neuen Y-Ticks
        new_ytick_value = self.option_tool.factor_short_call * short_call_premium
        if new_ytick_value not in custom_yticks:
            custom_yticks.append(new_ytick_value)  # Füge den neuen Tick zur Liste der benutzerdefinierten Ticks hinzu
        combined_yticks = np.concatenate((self.fixed_yticks, custom_yticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_yticks(combined_yticks)
        # Aktualisieren der Y-Tick-Beschriftungen und Farben
        ytick_labels = [str(tick) for tick in combined_yticks]
        self.ax.set_yticklabels(ytick_labels)
        self.ax.tick_params(axis='y', which='both', labelcolor='black')
        ylabels = self.ax.get_yticklabels()
        ylabels[-1].set_color('orange')  # Setze den letzten Y-Tick auf orange

        custom_xticks = []  # Liste für benutzerdefinierte Ticks
        # Hinzufügen eines neuen X-Ticks
        new_xtick_value = short_call_strike + short_call_premium
        if new_xtick_value not in custom_xticks:
            custom_xticks.append(new_xtick_value)  # Füge den neuen Tick zur Liste der benutzerdefinierten Ticks hinzu
        # Setzen der kombinierten Ticks auf der X-Achse
        combined_xticks = np.concatenate((self.fixed_xticks, custom_xticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_xticks(combined_xticks)
        # Aktualisieren der X-Tick-Beschriftungen und Farben
        xtick_labels = [str(tick) for tick in combined_xticks]
        self.ax.set_xticklabels(xtick_labels)
        self.ax.tick_params(axis='x', which='both', labelcolor='black')
        xlabels = self.ax.get_xticklabels()
        xlabels[-1].set_color('orange')  # Setze den letzten X-Tick auf orange

        if self.scatter_point_short_call is not None:
            self.scatter_point_short_call.remove()
        self.scatter_point_short_call = self.ax.scatter(new_xtick_value, 0, color='orange')

        if elements.count("on") >= 2:
            self.plot_combined()
        else:
            self.update_legend()

    def plot_long_put(self, long_put_strike, long_put_premium):
        self.payoff_long_put = self.option_tool.factor_long_put * (np.maximum(long_put_strike - self.underlying, 0) - long_put_premium)
        self.hidden_payoff_long_put = np.maximum(long_put_strike - self.underlying, 0) - long_put_premium
        self.long_put_line.set_data(self.underlying, self.payoff_long_put)
        self.long_put_line.set_visible(True)
        self.total_amount = self.option_tool.long_call_amount + \
                            self.option_tool.short_call_amount + \
                            self.option_tool.long_put_amount + \
                            self.option_tool.short_put_amount + \
                            self.option_tool.asset_amount
        elements = [self.option_tool.check_long_call_state,
                    self.option_tool.check_short_call_state,
                    self.option_tool.check_long_put_state,
                    self.option_tool.check_short_put_state,
                    self.option_tool.check_asset_state]

        custom_yticks = []  # Liste für benutzerdefinierte Ticks
        # Hinzufügen eines neuen Y-Ticks
        new_ytick_value = self.option_tool.factor_long_put * (long_put_strike - long_put_premium)
        if new_ytick_value not in custom_yticks:
            custom_yticks.append(new_ytick_value)  # Füge den neuen Tick zur Liste der benutzerdefinierten Ticks hinzu
        combined_yticks = np.concatenate((self.fixed_yticks, custom_yticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_yticks(combined_yticks)
        # Aktualisieren der Y-Tick-Beschriftungen und Farben
        ytick_labels = [str(tick) for tick in combined_yticks]
        self.ax.set_yticklabels(ytick_labels)
        self.ax.tick_params(axis='y', which='both', labelcolor='black')
        ylabels = self.ax.get_yticklabels()
        ylabels[-1].set_color('green')  # Setze den letzten Y-Tick auf grün

        custom_xticks = []  # Liste für benutzerdefinierte Ticks
        # Hinzufügen eines neuen X-Ticks
        new_xtick_value = long_put_strike - long_put_premium
        if new_xtick_value not in custom_xticks:
            custom_xticks.append(new_xtick_value)  # Füge den neuen Tick zur Liste der benutzerdefinierten Ticks hinzu
        # Setzen der kombinierten Ticks auf der X-Achse
        combined_xticks = np.concatenate((self.fixed_xticks, custom_xticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_xticks(combined_xticks)
        # Aktualisieren der X-Tick-Beschriftungen und Farben
        xtick_labels = [str(tick) for tick in combined_xticks]
        self.ax.set_xticklabels(xtick_labels)
        self.ax.tick_params(axis='x', which='both', labelcolor='black')
        xlabels = self.ax.get_xticklabels()
        xlabels[-1].set_color('green')  # Setze den letzten X-Tick auf grün

        if self.scatter_point_long_put is not None:
            self.scatter_point_long_put.remove()
        self.scatter_point_long_put = self.ax.scatter(new_xtick_value, 0, color='green')

        if elements.count("on") >= 2:
            self.plot_combined()
        else:
            self.update_legend()

    def plot_short_put(self, short_put_strike, short_put_premium):
        self.payoff_short_put = self.option_tool.factor_short_put * (np.minimum(self.underlying - short_put_strike, 0) + short_put_premium)
        self.hidden_payoff_short_put = np.minimum(self.underlying - short_put_strike, 0) + short_put_premium
        self.short_put_line.set_data(self.underlying, self.payoff_short_put)
        self.short_put_line.set_visible(True)
        self.total_amount = self.option_tool.long_call_amount + \
                            self.option_tool.short_call_amount + \
                            self.option_tool.long_put_amount + \
                            self.option_tool.short_put_amount + \
                            self.option_tool.asset_amount
        elements = [self.option_tool.check_long_call_state,
                    self.option_tool.check_short_call_state,
                    self.option_tool.check_long_put_state,
                    self.option_tool.check_short_put_state,
                    self.option_tool.check_asset_state]

        custom_yticks = []  # Liste für benutzerdefinierte Ticks
        # Hinzufügen eines neuen Y-Ticks
        new_ytick_value = self.option_tool.factor_short_put * (short_put_premium - short_put_strike)
        if new_ytick_value not in custom_yticks:
            custom_yticks.append(new_ytick_value)  # Füge den neuen Tick zur Liste der benutzerdefinierten Ticks hinzu
        combined_yticks = np.concatenate((self.fixed_yticks, custom_yticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_yticks(combined_yticks)
        # Aktualisieren der Y-Tick-Beschriftungen und Farben
        ytick_labels = [str(tick) for tick in combined_yticks]
        self.ax.set_yticklabels(ytick_labels)
        self.ax.tick_params(axis='y', which='both', labelcolor='black')
        ylabels = self.ax.get_yticklabels()
        ylabels[-1].set_color('red')  # Setze den letzten Y-Tick auf rot

        custom_xticks = []  # Liste für benutzerdefinierte Ticks
        # Hinzufügen eines neuen X-Ticks
        new_xtick_value = short_put_strike - short_put_premium
        if new_xtick_value not in custom_xticks:
            custom_xticks.append(new_xtick_value)  # Füge den neuen Tick zur Liste der benutzerdefinierten Ticks hinzu
        # Setzen der kombinierten Ticks auf der X-Achse
        combined_xticks = np.concatenate((self.fixed_xticks, custom_xticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_xticks(combined_xticks)
        # Aktualisieren der X-Tick-Beschriftungen und Farben
        xtick_labels = [str(tick) for tick in combined_xticks]
        self.ax.set_xticklabels(xtick_labels)
        self.ax.tick_params(axis='x', which='both', labelcolor='black')
        xlabels = self.ax.get_xticklabels()
        xlabels[-1].set_color('red')  # Setze den letzten X-Tick auf rot

        if self.scatter_point_short_put is not None:
            self.scatter_point_short_put.remove()
        self.scatter_point_short_put = self.ax.scatter(new_xtick_value, 0, color='red')

        if elements.count("on") >= 2:
            self.plot_combined()
        else:
            self.update_legend()

    def plot_asset(self):
        self.payoff_asset = self.option_tool.factor_asset * self.underlying
        self.hidden_payoff_asset = self.underlying
        self.asset_line.set_data(self.underlying, self.payoff_asset)
        self.asset_line.set_visible(True)
        self.total_amount = self.option_tool.long_call_amount + \
                            self.option_tool.short_call_amount + \
                            self.option_tool.long_put_amount + \
                            self.option_tool.short_put_amount + \
                            self.option_tool.asset_amount
        elements = [self.option_tool.check_long_call_state,
                    self.option_tool.check_short_call_state,
                    self.option_tool.check_long_put_state,
                    self.option_tool.check_short_put_state,
                    self.option_tool.check_asset_state]
        if elements.count("on") >= 2:
            self.plot_combined()
        else:
            self.update_legend()

    def plot_combined(self):
        self.total_amount = self.option_tool.long_call_amount + \
                            self.option_tool.short_call_amount + \
                            self.option_tool.long_put_amount + \
                            self.option_tool.short_put_amount + \
                            self.option_tool.asset_amount
        self.payoff_combined = (self.option_tool.factor_combined *
                                ((self.option_tool.long_call_amount / self.total_amount) * self.hidden_payoff_long_call +
                                (self.option_tool.short_call_amount / self.total_amount) * self.hidden_payoff_short_call +
                                (self.option_tool.long_put_amount / self.total_amount) * self.hidden_payoff_long_put +
                                (self.option_tool.short_put_amount / self.total_amount) * self.hidden_payoff_short_put +
                                (self.option_tool.asset_amount / self.total_amount) * self.hidden_payoff_asset))
        self.combined_line.set_data(self.underlying, self.payoff_combined)
        self.combined_line.set_visible(True)

        self.update_legend()

    def clear_long_call_plot(self):
        states = [self.option_tool.check_long_call_state,
                  self.option_tool.check_short_call_state,
                  self.option_tool.check_long_put_state,
                  self.option_tool.check_short_put_state,
                  self.option_tool.check_asset_state]
        self.long_call_line.set_visible(False)

        custom_yticks = []  # Liste für benutzerdefinierte Ticks
        combined_yticks = np.concatenate((self.fixed_yticks, custom_yticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_yticks(combined_yticks)
        # Aktualisieren der Y-Tick-Beschriftungen und Farben
        ytick_labels = [str(tick) for tick in combined_yticks]
        self.ax.set_yticklabels(ytick_labels)
        self.ax.tick_params(axis='y', which='both', labelcolor='black')

        custom_xticks = []  # Liste für benutzerdefinierte Ticks
        # Setzen der kombinierten Ticks auf der X-Achse
        combined_xticks = np.concatenate((self.fixed_xticks, custom_xticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_xticks(combined_xticks)
        # Aktualisieren der X-Tick-Beschriftungen und Farben
        xtick_labels = [str(tick) for tick in combined_xticks]
        self.ax.set_xticklabels(xtick_labels)
        self.ax.tick_params(axis='x', which='both', labelcolor='black')

        self.scatter_point_long_call.remove()
        self.scatter_point_long_call = None

        if states.count("on") < 2:
            self.clear_combined_plot()
        else:
            self.update_legend()

    def clear_short_call_plot(self):
        states = [self.option_tool.check_long_call_state,
                  self.option_tool.check_short_call_state,
                  self.option_tool.check_long_put_state,
                  self.option_tool.check_short_put_state,
                  self.option_tool.check_asset_state]
        self.short_call_line.set_visible(False)

        custom_yticks = []  # Liste für benutzerdefinierte Ticks
        combined_yticks = np.concatenate((self.fixed_yticks, custom_yticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_yticks(combined_yticks)
        # Aktualisieren der Y-Tick-Beschriftungen und Farben
        ytick_labels = [str(tick) for tick in combined_yticks]
        self.ax.set_yticklabels(ytick_labels)
        self.ax.tick_params(axis='y', which='both', labelcolor='black')

        custom_xticks = []  # Liste für benutzerdefinierte Ticks
        # Setzen der kombinierten Ticks auf der X-Achse
        combined_xticks = np.concatenate((self.fixed_xticks, custom_xticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_xticks(combined_xticks)
        # Aktualisieren der X-Tick-Beschriftungen und Farben
        xtick_labels = [str(tick) for tick in combined_xticks]
        self.ax.set_xticklabels(xtick_labels)
        self.ax.tick_params(axis='x', which='both', labelcolor='black')

        self.scatter_point_short_call.remove()
        self.scatter_point_short_call = None

        if states.count("on") < 2:
            self.clear_combined_plot()
        else:
            self.update_legend()

    def clear_long_put_plot(self):
        states = [self.option_tool.check_long_call_state,
                  self.option_tool.check_short_call_state,
                  self.option_tool.check_long_put_state,
                  self.option_tool.check_short_put_state,
                  self.option_tool.check_asset_state]
        self.long_put_line.set_visible(False)

        custom_yticks = []  # Liste für benutzerdefinierte Ticks
        combined_yticks = np.concatenate((self.fixed_yticks, custom_yticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_yticks(combined_yticks)
        # Aktualisieren der Y-Tick-Beschriftungen und Farben
        ytick_labels = [str(tick) for tick in combined_yticks]
        self.ax.set_yticklabels(ytick_labels)
        self.ax.tick_params(axis='y', which='both', labelcolor='black')

        custom_xticks = []  # Liste für benutzerdefinierte Ticks
        # Setzen der kombinierten Ticks auf der X-Achse
        combined_xticks = np.concatenate((self.fixed_xticks, custom_xticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_xticks(combined_xticks)
        # Aktualisieren der X-Tick-Beschriftungen und Farben
        xtick_labels = [str(tick) for tick in combined_xticks]
        self.ax.set_xticklabels(xtick_labels)
        self.ax.tick_params(axis='x', which='both', labelcolor='black')

        self.scatter_point_long_put.remove()
        self.scatter_point_long_put = None

        if states.count("on") < 2:
            self.clear_combined_plot()
        else:
            self.update_legend()

    def clear_short_put_plot(self):
        states = [self.option_tool.check_long_call_state,
                  self.option_tool.check_short_call_state,
                  self.option_tool.check_long_put_state,
                  self.option_tool.check_short_put_state,
                  self.option_tool.check_asset_state]
        self.short_put_line.set_visible(False)

        custom_yticks = []  # Liste für benutzerdefinierte Ticks
        combined_yticks = np.concatenate((self.fixed_yticks, custom_yticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_yticks(combined_yticks)
        # Aktualisieren der Y-Tick-Beschriftungen und Farben
        ytick_labels = [str(tick) for tick in combined_yticks]
        self.ax.set_yticklabels(ytick_labels)
        self.ax.tick_params(axis='y', which='both', labelcolor='black')

        custom_xticks = []  # Liste für benutzerdefinierte Ticks
        # Setzen der kombinierten Ticks auf der X-Achse
        combined_xticks = np.concatenate((self.fixed_xticks, custom_xticks))  # Feste + benutzerdefinierte Ticks
        self.ax.set_xticks(combined_xticks)
        # Aktualisieren der X-Tick-Beschriftungen und Farben
        xtick_labels = [str(tick) for tick in combined_xticks]
        self.ax.set_xticklabels(xtick_labels)
        self.ax.tick_params(axis='x', which='both', labelcolor='black')

        self.scatter_point_short_put.remove()
        self.scatter_point_short_put = None

        if states.count("on") < 2:
            self.clear_combined_plot()
        else:
            self.update_legend()

    def clear_asset_plot(self):
        states = [self.option_tool.check_long_call_state,
                  self.option_tool.check_short_call_state,
                  self.option_tool.check_long_put_state,
                  self.option_tool.check_short_put_state,
                  self.option_tool.check_asset_state]
        self.asset_line.set_visible(False)
        if states.count("on") < 2:
            self.clear_combined_plot()
        else:
            self.update_legend()

    def clear_combined_plot(self):
        self.combined_line.set_visible(False)
        self.update_legend()


    def update_legend(self):
        # Erstelle eine Liste der sichtbaren Linien und deren Labels
        visible_lines = [line for line in [self.long_call_line, self.short_call_line,
                                           self.long_put_line, self.short_put_line,
                                           self.asset_line, self.combined_line] if line.get_visible()]
        visible_labels = [line.get_label() for line in visible_lines]

        # Aktualisiere die Legende nur, wenn es sichtbare Linien gibt
        if visible_lines:
            self.ax.legend(visible_lines, visible_labels)
        else:
            self.ax.get_legend().remove()  # Entferne die Legende, wenn keine Linien sichtbar sind

        self.fig.canvas.draw_idle()

def center_window(root, width=900, height=780):
    # Berechne Bildschirmgröße
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Berechne x und y für die obere linke Ecke des Fensters
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Setze Fenstergröße und Position
    root.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == '__main__':
    ctk.set_appearance_mode("System")  # Adjusts CustomTkinter to the system theme
    option_graphical_tool = OptionTool()
    center_window(option_graphical_tool)
    option_graphical_tool.mainloop()
