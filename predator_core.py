# predator_core.py
import os
import subprocess
import json

CONFIG_DIR = os.path.expanduser("~/.config/predator/saved profiles")
DEFAULTS_FILE = os.path.expanduser("~/.config/predator/default_settings.json")
os.makedirs(CONFIG_DIR, exist_ok=True)

MODE_MAP = {"static":0,"breath":1,"neon":2,"wave":3,"shifting":4,"zoom":5}

def run_facer(mode, zone=None, color=None, speed=None, brightness=None, direction=None):
    mode_int = MODE_MAP.get(mode, 0)
    cmd = ["./facer_rgb.py", "-m", str(mode_int)]
    if zone: cmd += ["-z", str(zone)]
    if color: cmd += ["-cR", str(color[0]), "-cG", str(color[1]), "-cB", str(color[2])]
    if speed: cmd += ["-s", str(speed)]
    if brightness: cmd += ["-b", str(brightness)]
    if direction: cmd += ["-d", str(direction)]
    subprocess.run(cmd)

def save_profile(profile_name):
    subprocess.run(["./facer_rgb.py", "-save", profile_name])

def load_profile(profile_name):
    subprocess.run(["./facer_rgb.py", "-load", profile_name])

def list_profiles():
    return [f[:-5] for f in os.listdir(CONFIG_DIR) if f.endswith(".json")]

def load_defaults():
    if os.path.exists(DEFAULTS_FILE):
        with open(DEFAULTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_defaults(defaults):
    with open(DEFAULTS_FILE, "w") as f:
        json.dump(defaults, f)

def get_rgb(color_name):
    mapping = {"Red":(255,0,0),"Green":(0,255,0),"Blue":(0,0,255)}
    return mapping.get(color_name,(255,255,255))
