import os
import json
from datetime import datetime
class file_operation:
    
    def __init__(self):
        
        #Create Exported_Games directory if not existed
        try:
            path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"Exported_Games")
            os.mkdir(path)
        except:
            #print("The folder is already created")
            pass
        #Load settings.json
        try:
            file = open("settings.json")
            self.settings = json.load(file)
            file.close()
            #print(self.settings)
        except:
            self.settings = dict()
            self.settings["player_name"] = ""
            self.settings["WIDTH"] = 1280
            self.settings["HEIGHT"] = 720
            self.settings["game_full_screen"] = True
            self.settings["popup_enable"] = True
            self.settings["music_on"] = True
            json_object = json.dumps(self.settings, indent=4)
            with open("settings.json", "w") as outfile:
                outfile.write(json_object)
        os.system( "attrib +h settings.json" ) #hidden setting file
        os.chmod("settings.json",0o666)
        #print(oct(os.stat("settings.json").st_mode))
        #print(os.access("settings.json",os.X_OK))

    def save_settings(self, settings):
        self.settings = settings
        os.system( "attrib -h settings.json" )
        json_object = json.dumps(settings, indent=4)
        with open("settings.json", "w") as outfile:
            outfile.write(json_object)
        os.system( "attrib +h settings.json" )

    def export_game(self, game_data, game_id):
        filename = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Exported_Games")
        path +=f"\\Game_{filename}"
        if str(game_id) != '0':
            path+=f"({game_id})"
        path+=".json"
        json_object = json.dumps(game_data, indent=4)
        with open(path, "w") as outfile:
            outfile.write(json_object)
