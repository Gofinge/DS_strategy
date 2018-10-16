from env import *
from strategy import *
from config import *

conf_team1 = Config1a()
conf_team1.update(save_filename='save/RecordBook_case3_team1.xlsx',
                  if_sys_exist_break=1)

conf_team2 = Config1b()
conf_team2.update(save_filename='save/RecordBook_case3_team2.xlsx',
                  if_sys_exist_break=1)

conf_team3 = Config1c()
conf_team3.update(save_filename='save/RecordBook_case3_team3.xlsx',
                  if_sys_exist_break=1)

env = Env1(conf_team3)
stg = Strategy(conf_team3)
while True:
    cnc_status, rgv_loc = env.return_status()
    instruction = stg.nearest_neighbour_env1(cnc_status, rgv_loc)
    env.update_status(instruction)


