import numpy as np


class Config1a(dict):
    def __init__(self):
        # fixed environmental parameters
        self['RGV_move_time'] = {0: 0, 1: 20, 2: 33, 3: 46}
        self['RGV_handle_time'] = {1: 28, 0: 31}
        self['RGV_cleaning_time'] = 25
        self['CNC_machining_time'] = 560
        self['time_limit'] = 8*60*60
        self['CNC_loc'] = {1: [1, 0], 2: [1, 1], 3: [2, 0], 4: [2, 1], 5: [3, 0], 6: [3, 1], 7: [4, 0], 8: [4, 1]}
        self['process'] = 0
        self['CNC_process_information'] = 0
        self['if_sys_exist_break'] = 0
        self['p_break'] = 0.01
        self['exp_Lambda'] = 0
        self['save_filename'] = 'save/Record_Book.xlsx'

        # status parameter
        self['CNC_status'] = np.array([0, 0, 0, 0, 0, 0, 0, 0])
        self['CNC_break_status'] = np.array([0, 0, 0, 0, 0, 0, 0, 0])
        self['RGV_loc'] = 1
        self['timer'] = 0
        self['instruction'] = 0
        self['production_counter'] = 0

    def update(self, **kwargs):
        for key in kwargs:
            self[key] = kwargs[key]


class Config1b(dict):
    def __init__(self):
        # fixed environmental parameters
        self['RGV_move_time'] = {0: 0, 1: 23, 2: 41, 3: 59}
        self['RGV_handle_time'] = {1: 30, 0: 35}
        self['RGV_cleaning_time'] = 30
        self['CNC_machining_time'] = 580
        self['time_limit'] = 8 * 60 * 60
        self['CNC_loc'] = {1: [1, 0], 2: [1, 1], 3: [2, 0], 4: [2, 1], 5: [3, 0], 6: [3, 1], 7: [4, 0], 8: [4, 1]}
        self['process'] = 0
        self['CNC_process_information'] = 0
        self['if_sys_exist_break'] = 0
        self['p_break'] = 0.01
        self['exp_Lambda'] = 0
        self['save_filename'] = 'save/Record_Book.xlsx'

        # status parameter
        self['CNC_status'] = np.array([0, 0, 0, 0, 0, 0, 0, 0])
        self['CNC_break_status'] = np.array([0, 0, 0, 0, 0, 0, 0, 0])
        self['RGV_loc'] = 1
        self['timer'] = 0
        self['instruction'] = 0
        self['production_counter'] = 0

    def update(self, **kwargs):
        for key in kwargs:
            self[key] = kwargs[key]


class Config1c(dict):
    def __init__(self):
        # fixed environmental parameters
        self['RGV_move_time'] = {0: 0, 1: 18, 2: 32, 3: 46}
        self['RGV_handle_time'] = {1: 27, 0: 32}
        self['RGV_cleaning_time'] = 25
        self['CNC_machining_time'] = 545
        self['time_limit'] = 8 * 60 * 60
        self['CNC_loc'] = {1: [1, 0], 2: [1, 1], 3: [2, 0], 4: [2, 1], 5: [3, 0], 6: [3, 1], 7: [4, 0], 8: [4, 1]}
        self['process'] = 0
        self['CNC_process_information'] = 0
        self['if_sys_exist_break'] = 0
        self['p_break'] = 0.01
        self['exp_Lambda'] = 0
        self['save_filename'] = 'save/Record_Book.xlsx'

        # status parameter
        self['CNC_status'] = np.array([0, 0, 0, 0, 0, 0, 0, 0])
        self['CNC_break_status'] = np.array([0, 0, 0, 0, 0, 0, 0, 0])
        self['RGV_loc'] = 1
        self['timer'] = 0
        self['instruction'] = 0
        self['production_counter'] = 0

    def update(self, **kwargs):
        for key in kwargs:
            self[key] = kwargs[key]


class Config2a(dict):
    def __init__(self):
        # fixed environmental parameters
        self['RGV_move_time'] = {0: 0, 1: 20, 2: 33, 3: 46}
        self['RGV_handle_time'] = {1: 28, 0: 31}
        self['RGV_cleaning_time'] = 25
        self['CNC_machining_time'] = {0: 400, 1: 378}
        self['CNC_status_loc'] = {1: 0, 5: 1, 7: 2, 3: 3, 2: 0, 6: 1, 8: 2, 4: 3}
        self['CNC_process_information'] = {0: [1, 7, 8, 2], 1: [3, 4, 5, 6]}
        self['time_limit'] = 8 * 60 * 60
        self['CNC_loc'] = {1: [1, 0], 2: [1, 1], 3: [2, 0], 4: [2, 1], 5: [3, 0], 6: [3, 1], 7: [4, 0], 8: [4, 1]}
        self['if_sys_exist_break'] = 0
        self['p_break'] = 0.01
        self['exp_Lambda'] = {0: 0, 1: 0}
        self['save_filename'] = 'save/Record_Book.xlsx'

        # status parameter
        self['CNC_status'] = {0: np.array([0, 0, 0, 0]), 1: np.array([0, 0, 0, 0])}
        self['CNC_break_status'] = {0: np.array([0, 0, 0, 0]), 1: np.array([0, 0, 0, 0])}
        self['RGV_loc'] = 1
        self['timer'] = 0
        self['instruction'] = 0
        self['production_counter'] = 0
        self['process'] = 0

    def update(self, **kwargs):
        for key in kwargs:
            self[key] = kwargs[key]


class Config2b(dict):
    def __init__(self):
        # fixed environmental parameters
        self['RGV_move_time'] = {0: 0, 1: 23, 2: 41, 3: 59}
        self['RGV_handle_time'] = {1: 30, 0: 35}
        self['RGV_cleaning_time'] = 30
        self['CNC_machining_time'] = {0: 280, 1: 500}
        self['CNC_status_loc'] = {1: 0, 5: 1, 3: 2, 2: 0, 6: 1, 4: 2, 7: 3, 8: 4}
        self['CNC_process_information'] = {0: [1, 5, 3], 1: [2, 6, 4, 7, 8]}
        self['time_limit'] = 8 * 60 * 60
        self['CNC_loc'] = {1: [1, 0], 2: [1, 1], 3: [2, 0], 4: [2, 1], 5: [3, 0], 6: [3, 1], 7: [4, 0], 8: [4, 1]}
        self['if_sys_exist_break'] = 0
        self['p_break'] = 0.0
        self['exp_Lambda'] = {0: 0, 1: 0}
        self['save_filename'] = 'save/Record_Book.xlsx'

        # status parameter
        self['CNC_status'] = {0: np.array([0, 0, 0]), 1: np.array([0, 0, 0, 0, 0])}
        self['CNC_break_status'] = {0: np.array([0, 0, 0]), 1: np.array([0, 0, 0, 0, 0])}
        self['RGV_loc'] = 1
        self['timer'] = 0
        self['instruction'] = 0
        self['production_counter'] = 0
        self['process'] = 0

    def update(self, **kwargs):
        for key in kwargs:
            self[key] = kwargs[key]


class Config2c(dict):
    def __init__(self):
        # fixed environmental parameters
        self['RGV_move_time'] = {0: 0, 1: 18, 2: 32, 3: 46}
        self['RGV_handle_time'] = {1: 27, 0: 32}
        self['RGV_cleaning_time'] = 25
        self['CNC_machining_time'] = {0: 455, 1: 182}
        self['CNC_status_loc'] = {1: 0, 7: 1, 5: 2, 3: 3, 4: 4, 2: 0, 8: 1, 6: 2}
        self['CNC_process_information'] = {0: [1, 7, 5, 3, 4], 1: [2, 8, 6]}
        self['time_limit'] = 8 * 60 * 60
        self['CNC_loc'] = {1: [1, 0], 2: [1, 1], 3: [2, 0], 4: [2, 1], 5: [3, 0], 6: [3, 1], 7: [4, 0], 8: [4, 1]}
        self['if_sys_exist_break'] = 0
        self['p_break'] = 0.01
        self['exp_Lambda'] = {0: 0, 1: 0}
        self['save_filename'] = 'save/Record_Book.xlsx'

        # status parameter
        self['CNC_status'] = {0: np.array([0, 0, 0, 0, 0]), 1: np.array([0, 0, 0])}
        self['CNC_break_status'] = {0: np.array([0, 0, 0, 0, 0]), 1: np.array([0, 0, 0])}
        self['RGV_loc'] = 1
        self['timer'] = 0
        self['instruction'] = 0
        self['production_counter'] = 0
        self['process'] = 0

    def update(self, **kwargs):
        for key in kwargs:
            self[key] = kwargs[key]

class Config4(dict):
    def __init__(self):
        # fixed environmental parameters
        self['RGV_move_time'] = {0: 0, 1: 20, 2: 33, 3: 46}
        self['RGV_handle_time'] = {1: 28, 0: 31}
        self['RGV_cleaning_time'] = 25
        self['CNC_machining_time'] = {0: 400, 1: 378}
        self['CNC_status_loc'] = {1: 0, 7: 1, 8: 2, 2: 3, 3: 0, 5: 1, 6: 2, 4: 3}
        self['CNC_process_information'] = {0: [1, 7, 8, 2], 1: [3, 5, 6, 4]}
        self['time_limit'] = 8 * 60 * 60
        self['CNC_loc'] = {1: [1, 0], 2: [1, 1], 3: [2, 0], 4: [2, 1], 5: [3, 0], 6: [3, 1], 7: [4, 0], 8: [4, 1]}
        self['if_sys_exist_break'] = 0
        self['p_break'] = 0.01
        self['exp_Lambda'] = {0: 0, 1: 0}
        self['save_filename'] = 'save/Record_Book.xlsx'

        # status parameter
        self['CNC_status'] = {0: np.array([0, 0, 0, 0]), 1: np.array([0, 0, 0, 0])}
        self['CNC_break_status'] = {0: np.array([0, 0, 0, 0]), 1: np.array([0, 0, 0, 0])}
        self['RGV_loc'] = 1
        self['timer'] = 0
        self['instruction'] = 0
        self['production_counter'] = 0
        self['process'] = 0

    def update(self, **kwargs):
        for key in kwargs:
            self[key] = kwargs[key]