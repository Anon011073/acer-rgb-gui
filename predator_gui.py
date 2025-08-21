# predator_gui.py
import customtkinter as ctk
import tkinter
from tkinter import messagebox, simpledialog
import random
import os
from predator_core import run_facer, save_profile, load_profile, list_profiles, get_rgb, load_defaults, save_defaults

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class PredatorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Predator Lighting Control")
        self.geometry("580x650")
        self.minsize(580,650)

        # Load defaults
        self.defaults = load_defaults()

        # Variables
        self.mode_var = ctk.StringVar(value=self.defaults.get("mode","static"))
        self.color_var = ctk.StringVar(value=self.defaults.get("color","Red"))
        self.all_zones_var = ctk.BooleanVar(value=self.defaults.get("all_zones",True))
        self.zone_var = ctk.IntVar(value=self.defaults.get("zone",1))
        self.speed_var = ctk.IntVar(value=self.defaults.get("speed",5))
        self.brightness_var = ctk.IntVar(value=self.defaults.get("brightness",100))
        self.direction_var = ctk.IntVar(value=self.defaults.get("direction",0))

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        self.frame_main = ctk.CTkFrame(self, corner_radius=10, fg_color="#1b1b1b")
        self.frame_main.pack(fill="both", expand=True, padx=15, pady=15)
        self.frame_main.columnconfigure(1, weight=1)

        # Mode selection
        ctk.CTkLabel(self.frame_main, text="Effect:", font=("Arial",14)).grid(row=0, column=0, sticky="w", pady=5)
        self.mode_dropdown = ctk.CTkOptionMenu(
            self.frame_main,
            values=list(run_facer.__globals__['MODE_MAP'].keys()),
            variable=self.mode_var,
            command=lambda e: self.update_options(),
            width=140,
            font=("Arial",14)
        )
        self.mode_dropdown.grid(row=0, column=1, sticky="w", pady=5)

        # Options frame
        self.options_frame = ctk.CTkFrame(self.frame_main, corner_radius=10, fg_color="#222222")
        self.options_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew", ipadx=5, ipady=5)
        self.update_options()

        # Buttons frame
        self.btn_frame = ctk.CTkFrame(self.frame_main, corner_radius=10, fg_color="#222222")
        self.btn_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew", ipadx=5, ipady=5)
        ctk.CTkButton(self.btn_frame, text="Preview Effect", command=self.preview, font=("Arial",13)).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.btn_frame, text="Apply Effect", command=self.apply, font=("Arial",13)).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.btn_frame, text="Save Profile", command=self.save, font=("Arial",13)).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.btn_frame, text="Load Profile", command=self.load, font=("Arial",13)).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.btn_frame, text="Random Effect", command=self.random_effect, font=("Arial",13)).grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        # Make columns expand evenly
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)

        # Profiles frame
        self.profile_frame = ctk.CTkFrame(self.frame_main, corner_radius=10, fg_color="#222222")
        self.profile_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew", ipadx=5, ipady=5)
        ctk.CTkLabel(self.profile_frame, text="Saved Profiles:", font=("Arial",14)).grid(row=0, column=0, sticky="w", pady=(5,0))
        self.profile_listbox = tkinter.Listbox(
            self.profile_frame,
            height=6,
            bg="#1c1c1c",
            fg="#eeeeee",
            selectbackground="#1f538d",
            selectforeground="white",
            font=("Arial",14),
            borderwidth=0,
            highlightthickness=0,
            activestyle="none"
        )
        self.profile_listbox.grid(row=1, column=0, columnspan=2, sticky="ew")
        ctk.CTkButton(self.profile_frame, text="Delete Profile", command=self.delete_profile, font=("Arial",13)).grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")
        self.profile_frame.columnconfigure(0, weight=1)

        self.refresh_profiles()

    def update_options(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        row = 0
        mode = self.mode_var.get()

        if mode == "static":
            ctk.CTkCheckBox(self.options_frame, text="All Zones", variable=self.all_zones_var, font=("Arial",13)).grid(row=row, column=0, sticky="w", pady=3)
            ctk.CTkLabel(self.options_frame, text="Zone:", font=("Arial",13)).grid(row=row, column=1, sticky="w")
            ctk.CTkSpinbox(self.options_frame, from_=1, to=4, textvariable=self.zone_var, width=50, font=("Arial",13)).grid(row=row, column=2, sticky="w")
            row+=1

        if mode in ["static", "breath", "shifting", "zoom"]:
            ctk.CTkLabel(self.options_frame, text="Color:", font=("Arial",13)).grid(row=row, column=0, sticky="w", pady=3)
            color_dropdown = ctk.CTkOptionMenu(self.options_frame, values=["Red","Green","Blue"], variable=self.color_var, font=("Arial",13))
            color_dropdown.grid(row=row, column=1, sticky="w")
            row+=1

        if mode in ["wave","shifting","zoom","neon"]:
            ctk.CTkLabel(self.options_frame, text="Speed:", font=("Arial",13)).grid(row=row, column=0, sticky="w", pady=3)
            ctk.CTkSlider(self.options_frame, from_=1, to=9, variable=self.speed_var, orientation="horizontal").grid(row=row, column=1, columnspan=2, sticky="ew")
            row+=1

        ctk.CTkLabel(self.options_frame, text="Brightness:", font=("Arial",13)).grid(row=row, column=0, sticky="w", pady=3)
        ctk.CTkSlider(self.options_frame, from_=0, to=255, variable=self.brightness_var, orientation="horizontal").grid(row=row, column=1, columnspan=2, sticky="ew")
        row+=1

        ctk.CTkLabel(self.options_frame, text="Direction:", font=("Arial",13)).grid(row=row, column=0, sticky="w", pady=3)
        ctk.CTkSlider(self.options_frame, from_=0, to=255, variable=self.direction_var, orientation="horizontal").grid(row=row, column=1, columnspan=2, sticky="ew")
        row+=1

    def preview(self):
        mode = self.mode_var.get()
        color = get_rgb(self.color_var.get()) if mode in ["static","breath","shifting","zoom"] else None
        speed = int(self.speed_var.get()) if mode in ["wave","shifting","zoom","neon"] else None
        brightness = int(self.brightness_var.get())
        direction = int(self.direction_var.get())

        if mode=="static" and self.all_zones_var.get():
            for z in range(1,5):
                run_facer(mode, zone=z, color=color, brightness=brightness, direction=direction)
        else:
            zone = int(self.zone_var.get()) if mode=="static" else None
            run_facer(mode, zone=zone, color=color, speed=speed, brightness=brightness, direction=direction)

    def apply(self):
        self.preview()
        self.defaults = {
            "mode": self.mode_var.get(),
            "color": self.color_var.get(),
            "all_zones": self.all_zones_var.get(),
            "zone": self.zone_var.get(),
            "speed": self.speed_var.get(),
            "brightness": self.brightness_var.get(),
            "direction": self.direction_var.get()
        }
        save_defaults(self.defaults)
        messagebox.showinfo("Applied","Effect applied successfully!")

    def save(self):
        profile_name = simpledialog.askstring("Save Profile","Enter profile name:")
        if profile_name:
            save_profile(profile_name)
            self.refresh_profiles()
            messagebox.showinfo("Saved",f"Profile '{profile_name}' saved!")

    def load(self):
        try:
            selected_index = self.profile_listbox.curselection()[0]
            profile_name = self.profile_listbox.get(selected_index)
            load_profile(profile_name)
            messagebox.showinfo("Loaded",f"Profile '{profile_name}' loaded!")
        except IndexError:
            messagebox.showwarning("No selection","Select a profile to load")

    def delete_profile(self):
        try:
            selected_index = self.profile_listbox.curselection()[0]
            profile_name = self.profile_listbox.get(selected_index)
            if messagebox.askyesno("Confirm Delete", f"Delete profile '{profile_name}'?"):
                os.remove(f"{os.path.expanduser('~/.config/predator/saved profiles')}/{profile_name}.json")
                self.refresh_profiles()
        except IndexError:
            messagebox.showwarning("No selection","Select a profile to delete")

    def refresh_profiles(self):
        self.profile_listbox.delete(0,"end")
        for profile in list_profiles():
            self.profile_listbox.insert("end", profile)

    def random_effect(self):
        self.mode_var.set(random.choice(list(run_facer.__globals__['MODE_MAP'].keys())))
        self.color_var.set(random.choice(["Red","Green","Blue"]))
        self.speed_var.set(random.randint(1,9))
        self.all_zones_var.set(random.choice([True,False]))
        self.update_options()

if __name__=="__main__":
    app = PredatorGUI()
    app.mainloop()

