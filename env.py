import numpy as np
import pandas as pd
import sys
import math


class Env1:
    def __init__(self, conf):
        # fixed environmental parameters
        self._RGV_move_time = conf['RGV_move_time']              # {0: 0, 1: a, 2: b, 3: c} (step: time)
        self._RGV_handle_time = conf['RGV_handle_time']          # {1: x, 0: y}  1 - odd; 0 - even
        self._RGV_cleaning_time = conf['RGV_cleaning_time']      # int
        self._CNC_machining_time = conf['CNC_machining_time']    # int
        self._time_limit = conf['time_limit']                    # 8 * 60 * 60
        self._save_filename = conf['save_filename']
        self._CNC1_loc = conf['CNC_loc']
        self._if_sys_exist_break = conf['if_sys_exist_break']
        self._exp_Lambda = conf['exp_Lambda']
        self._p_break = conf['p_break']

        # status parameter
        self._CNC_status = conf['CNC_status']        # [0, 0, 0, 0, 0, 0, 0, 0]
        self._CNC_break_status = conf['CNC_break_status']
        self._RGV_loc = conf['RGV_loc']              # 1
        self._timer = conf['timer']                  # 0
        self._instruction = conf['instruction']      # 0
        self._production_counter = conf['production_counter']       # 0
        self._record_book = []     # for i in book, i = [instruction, up_material_time, down_material_time]
        self._break_list = []
        self._break_record_book = []

        # init the status of CNCs
        if self._if_sys_exist_break == 1:
            self._init_lambda()
            self._init_cnc_break_status()
        self._init_cnc()

    def _init_cnc_break_status(self):
        for i in range(8):
            self._CNC_break_status[i] = np.random.exponential(1 / self._exp_Lambda)

    def _init_lambda(self):
        self._exp_Lambda = - math.log(1 - self._p_break) / self._CNC_machining_time

    def _init_cnc(self):
        for i in [1, 3, 5, 7, 8, 6, 4, 2]:
            self._init_instruction(i)

    def _init_instruction(self, instruction):
        next_rgv_loc = int((instruction + 1) / 2)
        rgv_move_time = self._RGV_move_time[abs(next_rgv_loc - self._RGV_loc)]
        rgv_handle_time = self._RGV_handle_time[instruction % 2]
        rgv_handle_start_time = self._timer + rgv_move_time
        passed_time = rgv_move_time + rgv_handle_time
        new_record = [instruction, rgv_handle_start_time, -instruction]

        self._instruction = instruction
        self._RGV_loc = next_rgv_loc
        self._timer = self._timer + passed_time
        self._record_book.append(new_record)
        self._CNC_status = np.maximum(self._CNC_status - passed_time, 0)
        self._CNC_status[instruction - 1] = self._CNC_machining_time - self._RGV_cleaning_time
        if self._if_sys_exist_break == 1:
            self.update_break_status(instruction)

    def _norm_instruction(self, instruction):
        next_rgv_loc = int((instruction + 1) / 2)
        rgv_move_time = self._RGV_move_time[abs(next_rgv_loc - self._RGV_loc)]
        rgv_handle_time = self._RGV_handle_time[instruction % 2]
        rgv_clean_time = self._RGV_cleaning_time
        rgv_handle_start_time = self._timer + rgv_move_time
        passed_time = rgv_move_time + rgv_handle_time + rgv_clean_time
        new_record = [instruction, rgv_handle_start_time, -instruction]
        pre_loc = np.where(np.array(self._record_book) == -instruction)  # shape of pre_loc is {tuple}([?], [2])
        pre_loc_0 = pre_loc[0][0]
        pre_loc_1 = 2

        self._instruction = instruction
        self._RGV_loc = next_rgv_loc
        self._timer = self._timer + passed_time
        self._production_counter += 1
        self._record_book.append(new_record)
        self._record_book[pre_loc_0][pre_loc_1] = rgv_handle_start_time
        self._CNC_status = np.maximum(self._CNC_status - passed_time, 0)
        self._CNC_status[instruction - 1] = self._CNC_machining_time - self._RGV_cleaning_time

        if self._if_sys_exist_break == 1:
            self.update_break_status(instruction)

    def update_break_status(self, instruction):
        self._CNC_break_status[instruction - 1] -= self._CNC_machining_time
        if self._CNC_break_status[instruction - 1] <= 0:
            break_occur_time = self._CNC_machining_time + self._CNC_break_status[instruction - 1] \
                                  - self._RGV_cleaning_time
            break_occur_time_absolute = break_occur_time + self._timer
            repair_time = np.random.randint(600, 1200)
            break_record = [instruction, break_occur_time_absolute, break_occur_time_absolute + repair_time]
            self._CNC_status[instruction - 1] = break_occur_time + repair_time
            self._CNC_break_status[instruction - 1] = np.random.exponential(1 / self._exp_Lambda)
            self._break_record_book.append(break_record)
            self._break_list.append(instruction)

    def update_status(self, instruction):
        self._instruction = instruction
        if instruction == 0:
            passed_time = np.min(self._CNC_status)
            self._CNC_status -= passed_time
            self._timer += passed_time
        else:
            self._check_time()
            if self._CNC_status[instruction - 1] != 0:
                print('wrong instruction occur on step', self._production_counter)
                sys.exit(1)
            if instruction in self._break_list:
                self._break_list.remove(instruction)
                pre_loc = np.where(np.array(self._record_book) == -instruction)  # shape of pre_loc is {tuple}([?], [2])
                pre_loc_0 = pre_loc[0][0]
                pre_loc_1 = 2
                self._record_book[pre_loc_0][pre_loc_1] = 0
                self._init_instruction(instruction)
            else:
                self._norm_instruction(instruction)

    def return_status(self):
        return self._CNC_status, self._RGV_loc

    def _check_time(self):
        if self._timer >= self._time_limit:
            self._report_record_book()
            if self._if_sys_exist_break == 1:
                self._report_break_record_book()
            self._save_order_book()
            sys.exit(0)

    def _report_record_book(self):
        num_order = 0
        print('+===================================== record book ======================================+')
        for record in self._record_book:
            num_order += 1
            instruction = record[0]
            up_material_time = record[1]
            down_material_time = record[2]
            if down_material_time <= 0:
                down_material_time = 'NaN'
            print('| order: ', num_order, '\tCNC_number: ', instruction,
                  '\t up_material_time: ', up_material_time, '\t down_material_time: ', down_material_time)
        print('+=========================================================================================+')
        print('The total number of completed components in a schedule (8h) is: ', self._production_counter)

    def _report_break_record_book(self):
        num_order = 0
        print('+==================================== break record book =====================================+')
        for record in self._break_record_book:
            num_order += 1
            cnc_order = record[0]
            break_occurred_time = record[1]
            repair_finished_time = record[2]
            print('| order: ', num_order, '\tCNC_number: ', cnc_order,
                  '\t break_occurred_time: ', break_occurred_time,
                  '\t repair_finished_time: ', repair_finished_time,)
        print('+============================================================================================+')
        print('The total number of break occurred in a schedule (8h) is: ', len(self._break_record_book))

    def _save_order_book(self):
        record_book_df = pd.DataFrame(self._record_book)
        index_rb = np.arange(1, len(self._record_book) + 1)
        record_book_df.columns = ['CNC_number', 'up_material_time', 'down_material_time']
        record_book_df.index = index_rb
        filename = pd.ExcelWriter(self._save_filename)
        record_book_df.to_excel(filename, 'record_book')
        if self._if_sys_exist_break == 1:
            break_record_book_df = pd.DataFrame(self._break_record_book)
            index_break_rb = np.arange(1, len(self._break_record_book) + 1)
            break_record_book_df.columns = ['CNC_number', 'break_occurred_time', 'repair_finished_time']
            break_record_book_df.index = index_break_rb
            break_record_book_df.to_excel(filename, 'break_record_book')
        filename.save()


class Env2:
    def __init__(self, conf):
        # fixed environmental parameters
        self._RGV_move_time = conf['RGV_move_time']              # {0: 0, 1: a, 2: b, 3: c} (step: time)
        self._RGV_handle_time = conf['RGV_handle_time']          # {1: x, 0: y}  1 - odd; 0 - even
        self._RGV_cleaning_time = conf['RGV_cleaning_time']      # int
        self._CNC_machining_time = conf['CNC_machining_time']    # int
        self._CNC_process_information = conf['CNC_process_information']
        self._CNC_status_loc = conf['CNC_status_loc']
        self._time_limit = conf['time_limit']                    # 8 * 60 * 60
        self._CNC_loc = conf['CNC_loc']
        self._save_filename = conf['save_filename']
        self._if_sys_exist_break = conf['if_sys_exist_break']
        self._exp_Lambda = conf['exp_Lambda']
        self._p_break = conf['p_break']

        # status parameter
        self._CNC_status = conf['CNC_status']
        self._CNC_break_status = conf['CNC_break_status']
        self._RGV_loc = conf['RGV_loc']              # 1
        self._timer = conf['timer']                  # 0
        self._instruction = conf['instruction']      # 0
        self._production_counter = conf['production_counter']       # 0
        self._record_book_A = []     # for i in book, i = [instruction, up_material_time, down_material_time]
        self._record_book_B = []
        self._break_list = []
        self._break_record_book = []
        self._flag = 0
        self._process = conf['process']

        # init the status of CNCs
        if self._if_sys_exist_break == 1:
            self._init_lambda()
            self._init_cnc_break_status()
        self._init_cnc_b()

    def print_time(self):
        print(self._timer)

    def _init_cnc_break_status(self):
        for i in range(len(self._CNC_break_status[0])):
            self._CNC_break_status[0][i] = np.random.exponential(1 / self._exp_Lambda[0])
        for i in range(len(self._CNC_break_status[1])):
            self._CNC_break_status[1][i] = np.random.exponential(1 / self._exp_Lambda[1])

    def _init_lambda(self):
        self._exp_Lambda[0] = - math.log(1 - self._p_break) / self._CNC_machining_time[0]
        self._exp_Lambda[1] = - math.log(1 - self._p_break) / self._CNC_machining_time[1]

    def _init_cnc(self):
        for i in range(len(self._CNC_process_information[0])):
            self._init_instruction_a(self._CNC_process_information[0][i])
        for i in range(len(self._CNC_process_information[1])):
            self.update_status(0)
            self._init_instruction_a2(self._CNC_process_information[0][i])
            self._init_instruction_b(self._CNC_process_information[1][i])

    def _init_cnc_b(self):
        for i in range(len(self._CNC_process_information[0])):
            self._init_instruction_a(self._CNC_process_information[0][i])
        self.update_status(0)
        self._init_instruction_a2(self._CNC_process_information[0][0])
        self._init_instruction_b(self._CNC_process_information[1][0])
        self.update_status(0)
        self._init_instruction_a2(self._CNC_process_information[0][1])
        self._init_instruction_b(self._CNC_process_information[1][1])
        self.update_status(0)
        self._init_instruction_a2(self._CNC_process_information[0][2])
        self._init_instruction_b(self._CNC_process_information[1][2])
        self.update_status(0)
        self._init_instruction_a2(self._CNC_process_information[0][0])
        self._init_instruction_b(self._CNC_process_information[1][3])
        self.update_status(0)
        self._init_instruction_a2(self._CNC_process_information[0][1])
        self._init_instruction_b(self._CNC_process_information[1][4])

    def _init_instruction_a(self, instruction):
        cnc_loc = self._CNC_status_loc[instruction]
        next_rgv_loc = int((instruction + 1) / 2)
        rgv_move_time = self._RGV_move_time[abs(next_rgv_loc - self._RGV_loc)]
        rgv_handle_time = self._RGV_handle_time[instruction % 2]
        rgv_handle_start_time = self._timer + rgv_move_time
        passed_time = rgv_move_time + rgv_handle_time
        new_record = [instruction, rgv_handle_start_time, -instruction]

        self._instruction = instruction
        self._RGV_loc = next_rgv_loc
        self._timer = self._timer + passed_time
        self._record_book_A.append(new_record)
        self._CNC_status[0] = np.maximum(self._CNC_status[0] - passed_time, 0)
        self._CNC_status[1] = np.maximum(self._CNC_status[1] - passed_time, 0)
        self._CNC_status[0][cnc_loc] = self._CNC_machining_time[0]

    def _init_instruction_a2(self, instruction):
        cnc_loc = self._CNC_status_loc[instruction]
        next_rgv_loc = int((instruction + 1) / 2)
        rgv_move_time = self._RGV_move_time[abs(next_rgv_loc - self._RGV_loc)]
        rgv_handle_time = self._RGV_handle_time[instruction % 2]
        rgv_handle_start_time = self._timer + rgv_move_time
        passed_time = rgv_move_time + rgv_handle_time
        new_record = [instruction, rgv_handle_start_time, -instruction]
        pre_loc = np.where(np.array(self._record_book_A) == -instruction)  # shape of pre_loc is {tuple}([?], [2])
        pre_loc_0 = pre_loc[0][0]
        pre_loc_1 = 2

        self._instruction = instruction
        self._RGV_loc = next_rgv_loc
        self._timer = self._timer + passed_time
        self._record_book_A.append(new_record)
        self._record_book_A[pre_loc_0][pre_loc_1] = rgv_handle_start_time
        self._CNC_status[0] = np.maximum(self._CNC_status[0] - passed_time, 0)
        self._CNC_status[1] = np.maximum(self._CNC_status[1] - passed_time, 0)
        self._CNC_status[0][cnc_loc] = self._CNC_machining_time[0]

    def _init_instruction_b(self, instruction):
        cnc_loc = self._CNC_status_loc[instruction]
        next_rgv_loc = int((instruction + 1) / 2)
        rgv_move_time = self._RGV_move_time[abs(next_rgv_loc - self._RGV_loc)]
        rgv_handle_time = self._RGV_handle_time[instruction % 2]
        rgv_clean_time = self._RGV_cleaning_time
        rgv_handle_start_time = self._timer + rgv_move_time
        passed_time = rgv_move_time + rgv_handle_time + rgv_clean_time
        new_record = [instruction, rgv_handle_start_time, -instruction]

        self._instruction = instruction
        self._RGV_loc = next_rgv_loc
        self._timer = self._timer + passed_time
        self._record_book_B.append(new_record)
        self._CNC_status[0] = np.maximum(self._CNC_status[0] - passed_time, 0)
        self._CNC_status[1] = np.maximum(self._CNC_status[1] - passed_time, 0)
        self._CNC_status[1][cnc_loc] = self._CNC_machining_time[1] - self._RGV_cleaning_time

    def _norm_instruction_a(self, instruction):
        cnc_loc = self._CNC_status_loc[instruction]
        next_rgv_loc = int((instruction + 1) / 2)
        rgv_move_time = self._RGV_move_time[abs(next_rgv_loc - self._RGV_loc)]
        rgv_handle_time = self._RGV_handle_time[instruction % 2]
        rgv_handle_start_time = self._timer + rgv_move_time
        passed_time = rgv_move_time + rgv_handle_time
        new_record = [instruction, rgv_handle_start_time, -instruction]
        pre_loc = np.where(np.array(self._record_book_A) == -instruction)  # shape of pre_loc is {tuple}([?], [2])
        pre_loc_0 = pre_loc[0][0]
        pre_loc_1 = 2

        self._process = 1
        self._instruction = instruction
        self._RGV_loc = next_rgv_loc
        self._timer = self._timer + passed_time
        self._record_book_A.append(new_record)
        self._record_book_A[pre_loc_0][pre_loc_1] = rgv_handle_start_time
        self._CNC_status[0] = np.maximum(self._CNC_status[0] - passed_time, 0)
        self._CNC_status[1] = np.maximum(self._CNC_status[1] - passed_time, 0)
        self._CNC_status[0][cnc_loc] = self._CNC_machining_time[0]
        if self._if_sys_exist_break == 1:
            self.update_break_status_a(instruction)

    def _norm_instruction_b(self, instruction):
        cnc_loc = self._CNC_status_loc[instruction]
        next_rgv_loc = int((instruction + 1) / 2)
        rgv_move_time = self._RGV_move_time[abs(next_rgv_loc - self._RGV_loc)]
        rgv_handle_time = self._RGV_handle_time[instruction % 2]
        rgv_clean_time = self._RGV_cleaning_time
        rgv_handle_start_time = self._timer + rgv_move_time
        passed_time = rgv_move_time + rgv_handle_time + rgv_clean_time
        new_record = [instruction, rgv_handle_start_time, -instruction]
        pre_loc = np.where(np.array(self._record_book_B) == -instruction)  # shape of pre_loc is {tuple}([?], [2])
        pre_loc_0 = pre_loc[0][0]
        pre_loc_1 = 2

        self._process = 0
        self._instruction = instruction
        self._RGV_loc = next_rgv_loc
        self._timer = self._timer + passed_time
        self._production_counter += 1
        self._record_book_B.append(new_record)
        self._record_book_B[pre_loc_0][pre_loc_1] = rgv_handle_start_time
        self._CNC_status[0] = np.maximum(self._CNC_status[0] - passed_time, 0)
        self._CNC_status[1] = np.maximum(self._CNC_status[1] - passed_time, 0)
        self._CNC_status[1][cnc_loc] = self._CNC_machining_time[1] - self._RGV_cleaning_time
        if self._if_sys_exist_break == 1:
            self.update_break_status_b(instruction)

    def update_break_status_a(self, instruction):
        cnc_loc = self._CNC_status_loc[instruction]
        self._CNC_break_status[0][cnc_loc] -= self._CNC_machining_time[0]
        if self._CNC_break_status[0][cnc_loc] <= 0:
            break_occur_time = self._CNC_machining_time[0] + self._CNC_break_status[0][cnc_loc] \
                               - self._RGV_cleaning_time
            break_occur_time_absolute = break_occur_time + self._timer
            repair_time = np.random.randint(600, 1200)
            break_record = [instruction, break_occur_time_absolute, break_occur_time_absolute + repair_time]
            self._CNC_status[0][cnc_loc] = break_occur_time + repair_time
            self._CNC_break_status[0][cnc_loc] = np.random.exponential(1 / self._exp_Lambda[0])
            self._break_record_book.append(break_record)
            self._break_list.append(instruction)

    def update_break_status_b(self, instruction):
        cnc_loc = self._CNC_status_loc[instruction]
        self._CNC_break_status[1][cnc_loc] -= self._CNC_machining_time[1]
        if self._CNC_break_status[1][cnc_loc] <= 0:
            break_occur_time = self._CNC_machining_time[1] + self._CNC_break_status[1][cnc_loc] \
                               - self._RGV_cleaning_time
            break_occur_time_absolute = break_occur_time + self._timer
            repair_time = np.random.randint(600, 1200)
            break_record = [instruction, break_occur_time_absolute, break_occur_time_absolute + repair_time]
            self._CNC_status[1][cnc_loc] = break_occur_time + repair_time
            self._CNC_break_status[1][cnc_loc] = np.random.exponential(1 / self._exp_Lambda[0])
            self._break_record_book.append(break_record)
            self._break_list.append(instruction)

    def update_status(self, instruction):
        self._instruction = instruction
        if instruction == 0:
            passed_time = 0
            if self._process == 0:
                passed_time = np.min(self._CNC_status[0])
            elif self._process == 1:
                passed_time = np.min(self._CNC_status[1])
            self._CNC_status[0] = np.maximum(self._CNC_status[0] - passed_time, 0)
            self._CNC_status[1] = np.maximum(self._CNC_status[1] - passed_time, 0)
            self._timer += passed_time

        elif instruction in self._CNC_process_information[0]:
            self._check_time()
            cnc_loc = self._CNC_status_loc[instruction]
            if self._CNC_status[0][cnc_loc] != 0:
                print('wrong instruction occur on step', self._production_counter)
                sys.exit(1)
            if instruction in self._break_list:
                self._break_list.remove(instruction)
                self._flag = 1
                pre_loc = np.where(np.array(self._record_book_A) == -instruction)
                pre_loc_0 = pre_loc[0][0]
                pre_loc_1 = 2
                self._record_book_A[pre_loc_0][pre_loc_1] = 0
                self._init_instruction_a(instruction)
                self._process = 1
            else:
                self._norm_instruction_a(instruction)

        elif instruction in self._CNC_process_information[1]:
            self._check_time()
            cnc_loc = self._CNC_status_loc[instruction]
            if self._CNC_status[1][cnc_loc] != 0:
                print('wrong instruction occur on process:', self._process, '\ton product:', self._production_counter+1)
                sys.exit(1)
            if self._flag == 1:
                self._flag = 0
            if instruction in self._break_list:
                self._break_list.remove(instruction)
                pre_loc = np.where(np.array(self._record_book_B) == -instruction)
                pre_loc_0 = pre_loc[0][0]
                pre_loc_1 = 2
                self._record_book_B[pre_loc_0][pre_loc_1] = 0
                self._init_instruction_b(instruction)
                self._process = 0
            else:
                self._norm_instruction_b(instruction)

    def return_status(self):
        return self._CNC_status, self._RGV_loc

    def _check_time(self):
        if self._timer >= self._time_limit:
            self._report_result()
            if self._if_sys_exist_break == 1:
                self._report_break_record_book()
            self._save_order_book()
            sys.exit(0)

    def _report_result(self):
        num_order = 0
        print('+===================================== record book A ======================================+')
        for record in self._record_book_A:
            num_order += 1
            instruction = record[0]
            up_material_time = record[1]
            down_material_time = record[2]
            if down_material_time <= 0:
                down_material_time = 'NaN'
            print('| order: ', num_order, '\tCNC_number: ', instruction,
                  '\t up_material_time: ', up_material_time, '\t down_material_time: ', down_material_time)
        print('+==========================================================================================+')
        num_order = 0
        print('+===================================== record book B ======================================+')
        for record in self._record_book_B:
            num_order += 1
            instruction = record[0]
            up_material_time = record[1]
            down_material_time = record[2]
            if down_material_time <= 0:
                down_material_time = 'NaN'
            print('| order: ', num_order, '\tCNC_number: ', instruction,
                  '\t up_material_time: ', up_material_time, '\t down_material_time: ', down_material_time)
        print('+==========================================================================================+')
        print('The total number of completed components in a schedule (8h) is: ', self._production_counter)

    def _report_break_record_book(self):
        num_order = 0
        print('+==================================== break record book =====================================+')
        for record in self._break_record_book:
            num_order += 1
            cnc_order = record[0]
            break_occurred_time = record[1]
            repair_finished_time = record[2]
            print('| order: ', num_order, '\tCNC_number: ', cnc_order,
                  '\t break_occurred_time: ', break_occurred_time,
                  '\t repair_finished_time: ', repair_finished_time,)
        print('+============================================================================================+')
        print('The total number of break occurred in a schedule (8h) is: ', len(self._break_record_book))

    def _save_order_book(self):
        record_book_a_df = pd.DataFrame(self._record_book_A)
        index = np.arange(1, len(self._record_book_A) + 1)
        record_book_a_df.columns = ['CNC_processA_number', 'A_up_material_time', 'A_down_material_time']
        record_book_a_df.index = index

        record_book_b_df = pd.DataFrame(self._record_book_B)
        index = np.arange(1, len(self._record_book_B) + 1)
        record_book_b_df.columns = ['CNC_processB_number', 'B_up_material_time', 'B_down_material_time']
        record_book_b_df.index = index

        record_book_df = pd.concat([record_book_a_df, record_book_b_df], axis=1)

        filename = pd.ExcelWriter(self._save_filename)
        record_book_df.to_excel(filename, 'Record_book')

        if self._if_sys_exist_break == 1:
            break_record_book_df = pd.DataFrame(self._break_record_book)
            index_break_rb = np.arange(1, len(self._break_record_book) + 1)
            break_record_book_df.columns = ['CNC_number', 'break_occurred_time', 'repair_finished_time']
            break_record_book_df.index = index_break_rb
            break_record_book_df.to_excel(filename, 'break_record_book')

        filename.save()

