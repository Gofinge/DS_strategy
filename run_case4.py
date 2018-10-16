from env import *
from strategy import *
from config import *


conf_team1 = Config2a()
conf_team1.update(save_filename='save/RecordBook_case4_team1.xlsx',
                  if_sys_exist_break=1)

conf_team2 = Config2b()
conf_team2.update(save_filename='save/RecordBook_case4_team2.xlsx',
                  if_sys_exist_break=1)

conf_team3 = Config2c()
conf_team3.update(save_filename='save/RecordBook_case4_team3.xlsx',
                  if_sys_exist_break=1)

env = Env2(conf_team3)
stg = Strategy(conf_team3)
while True:
    cnc_status, rgv_loc = env.return_status()
    instruction = stg.nearest_neighbour_env2(cnc_status, rgv_loc)
    env.update_status(instruction)
