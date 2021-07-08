import json
import os
class Config:
    def __init__(self):
        print("Que está pasando")
        with open('config_real.json') as file:
            self.config = json.load(file)
            print("Se ha leido el config")

        if(os.path.basename(file.name) == 'config_sim.json'):
            print("El archivo es:", file.name)
        else:
            print("Si funciona jejeje")

if __name__ == "__main__":
    config = Config()
