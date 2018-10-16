
class Strategy:
    def __init__(self, conf):
        self._process = conf['process']
        self._CNC_process_information = conf['CNC_process_information']
        self._flag = 0

    @staticmethod
    def nearest_neighbour_env1(cnc_status, rgv_loc):
        min_dis = 4
        instruction = 0
        for i in range(8):
            if cnc_status[i] == 0:
                cnc = i + 1
                cnc_locate = [int((cnc + 1)/2), cnc % 2]
                dis = abs(cnc_locate[0] - rgv_loc)
                if cnc_locate[1] == 0:
                    dis += 0.5
                if dis <= min_dis:
                    min_dis = dis
                    instruction = cnc
        return instruction

    def nearest_neighbour_env2(self, cnc_status, rgv_loc):
        if self._process == 0:
            cnc_status_a = cnc_status[0]
            min_dis = 4
            instruction = 0
            for i in range(len(cnc_status_a)):
                if cnc_status_a[i] == 0:
                    cnc = self._CNC_process_information[0][i]
                    cnc_locate = [int((cnc + 1) / 2), cnc % 2]
                    dis = abs(cnc_locate[0] - rgv_loc)
                    if cnc_locate[1] == 0:
                        dis += 0.5
                    if dis <= min_dis:
                        min_dis = dis
                        instruction = cnc
            if instruction != 0:
                self._process = 1
            return instruction
        elif self._process == 1:
            cnc_status_b = cnc_status[1]
            min_dis = 4
            instruction = 0
            for i in range(len(cnc_status_b)):
                if cnc_status_b[i] == 0:
                    cnc = self._CNC_process_information[1][i]
                    cnc_locate = [int((cnc + 1) / 2), cnc % 2]
                    dis = abs(cnc_locate[0] - rgv_loc)
                    if cnc_locate[1] == 0:
                        dis += 0.5
                    if dis <= min_dis:
                        min_dis = dis
                        instruction = cnc
            if instruction != 0:
                self._process = 0
            return instruction

    def nearest_neighbour_env3(self, cnc_status, rgv_loc):
        if self._process == 0:
            if self._flag == 1:
                self._process = 1 - self._process
                instruction = self.nearest_neighbour_env3(cnc_status, rgv_loc)
                return instruction
            self._flag = 1
            cnc_status_a = cnc_status[0]
            min_dis = 4
            instruction = 0
            for i in range(len(cnc_status_a)):
                if cnc_status_a[i] == 0:
                    cnc = self._CNC_process_information[0][i]
                    cnc_locate = [int((cnc + 1) / 2), cnc % 2]
                    dis = abs(cnc_locate[0] - rgv_loc)
                    if cnc_locate[1] == 0:
                        dis += 0.5
                    if dis <= min_dis:
                        min_dis = dis
                        instruction = cnc
            if instruction != 0:
                self._process = 1
            return instruction
        elif self._process == 1:
            if self._flag == 0:
                self._process = 1 - self._process
                instruction = self.nearest_neighbour_env3(cnc_status, rgv_loc)
                return instruction
            self._flag = 0
            cnc_status_b = cnc_status[1]
            min_dis = 4
            instruction = 0
            for i in range(len(cnc_status_b)):
                if cnc_status_b[i] == 0:
                    cnc = self._CNC_process_information[1][i]
                    cnc_locate = [int((cnc + 1) / 2), cnc % 2]
                    dis = abs(cnc_locate[0] - rgv_loc)
                    if cnc_locate[1] == 0:
                        dis += 0.5
                    if dis <= min_dis:
                        min_dis = dis
                        instruction = cnc
            if instruction != 0:
                self._process = 0
            return instruction
