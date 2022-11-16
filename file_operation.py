import os
import json
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
            self.file = open("settings.json")
            self.settings = json.load(self.file)
            #print(self.settings)
        except:
            self.file = open("settings.json",'x',)
            self.settings = dict()
            #print("Created settings.json")
        os.system( "attrib +h settings.json" ) #hidden setting file
        os.chmod("settings.json",0o666)
        #print(oct(os.stat("settings.json").st_mode))
        #print(os.access("settings.json",os.X_OK))
        self.file.close()

    #Take dictionary
    def save_settings(self, settings):
        self.settings = settings
        try:
            os.system( "attrib -h settings.json" )
            self.file = open("settings.json",'w')
        except:
            #Just in case user manually delete the file
            self.file = open("settings.json",'x')
            self.file.close()
            self.file = open("settings.json",'w')
        json.dump(settings,self.file,indent=4)
        self.file.close()
        os.system( "attrib +h settings.json" )

    def export_game(self):
        pass
