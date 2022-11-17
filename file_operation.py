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
            #print(self.settings)
        except:
            file = open("settings.json",'x')
            file.close()
            file = open("settings.json",'w')
            self.settings = dict()
            self.settings["player_name"] = ""
            self.settings["WIDTH"] = 1280
            self.settings["HEIGHT"] = 720
            self.settings["game_full_screen"] = True
            self.settings["popup_enable"] = True
            self.settings["music_on"] = True
            json.dump(self.settings,file,indent=4)
            #print("Created settings.json")
        os.system( "attrib +h settings.json" ) #hidden setting file
        os.chmod("settings.json",0o666)
        #print(oct(os.stat("settings.json").st_mode))
        #print(os.access("settings.json",os.X_OK))
        file.close()

    #Take dictionary
    def save_settings(self, settings):
        self.settings = settings
        try:
            os.system( "attrib -h settings.json" )
            file = open("settings.json",'w')
        except:
            #Just in case user manually delete the file
            file = open("settings.json",'x')
            file.close()
            file = open("settings.json",'w')
        json.dump(settings,self.file,indent=4)
        file.close()
        os.system( "attrib +h settings.json" )

    def export_game(self, game_data, game_id):
        filename = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Exported_Games")
        path +=f"\\Game_{filename}"
        if str(game_id) != '0':
            path+=f"({game_id})"
        path+=".json"
        try:
            file = open(path, 'x')
            file.close()
            file = open(path, 'w')
        except:
            file = open(path, 'w')
        json.dump(game_data,file,indent=4)
        file.close()
