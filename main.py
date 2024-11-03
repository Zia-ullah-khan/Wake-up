from ETS2LA.Plugin import *
from ETS2LA.UI import *
import time
import math
import requests

class Plugin(ETS2LAPlugin):
    author = [
        Author(
            name="Zia",
            url="https://github.com/Zia-ullah-khan",
            icon="https://avatars.githubusercontent.com/u/88408107?v=4"
        )
    ]

    description = PluginDescription(
        name="Wake Up You Sleepy Bastard",
        version="1.0.0",
        description="You Need to Wake the fuck up",
        compatible_os=["Windows", "Linux"],
        compatible_game=["ETS2"],
        modules = ["TruckSimAPI"],
        update_log={
            "1.0.0": "Everything is working as it should"
        }
    )
    
    warningShown = False

    def imports(self):
        global torch, np, OpenShockAPI
        import numpy as np
        import torch
        from Wake-up.Camera import camera

    def warning(self):
        if not self.warningShown:
            warning = '''
            <h1>WARNING THIS PLUGIN WILL USE YOUR CAMERA TO SEE IF YOU ARE SLEEPING, THIS DATA IS NOT SENT ANYWHERE, DO YOU AGREE TO USE THIS PLUGIN UNDER YOUR OWN SUPERVISION</h1>
            '''
            answer = self.ask(warning, options=["Yes", "No"], description="WARNING!")
            if answer == "Yes":
                self.notify("Plugin Enabled", type="success")
                self.warningShown = True
            else:
                self.notify("Plugin Disabled", type="error")

    def run(self):
        api_valyes = self.modules.TruckSimAPI.run()
        sleepy = camera()
        if sleepy.is_sleepy == True:
            api_valyes["TruckBool"]["lightsHazard"] = True
            api_valyes["TruckBool"]["gameBrake"] = 1