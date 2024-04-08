from configs.Config import Config
from env.starcraft.StarCraft import StarCraft
import pogema
import importlib

class EnvConfig(Config):
    def __init__(self):
        pass

    def create_env(self):
        pass


class StarCraftConfig(EnvConfig):

    def __init__(self, env_name):
        self.env_name = env_name

    def create_env(self):
        return StarCraft(self.env_name)
    
class PogemaConfig(EnvConfig):
    def __init__(self, env_name):
        self.env_name = env_name
        self.str2env = {
            'Easy8x8': pogema.Easy8x8, 
            'Normal8x8': pogema.Normal8x8, 
            'Hard8x8': pogema.Hard8x8, 
            'ExtraHard8x8': pogema.ExtraHard8x8,
            'Easy16x16': pogema.Easy16x16, 
            'Normal16x16': pogema.Normal16x16, 
            'Hard16x16': pogema.Hard16x16, 
            'ExtraHard16x16': pogema.ExtraHard16x16,
            'Easy32x32': pogema.Easy32x32, 
            'Normal32x32': pogema.Normal32x32, 
            'Hard32x32': pogema.Hard32x32, 
            'ExtraHard32x32': pogema.ExtraHard32x32,
            'Easy64x64': pogema.Easy64x64, 
            'Normal64x64': pogema.Normal64x64, 
            'Hard64x64': pogema.Hard64x64, 
            'ExtraHard64x64': pogema.ExtraHard64x64,
        }
    
    def create_env(self):
        return pogema.pogema_v0(grid_config=self.str2env[self.env_name]())