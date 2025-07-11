
import asyncio
import logging
from config import ConfigInfo
from generator import CommonGenerator




class LogSender:

    def __init__(self, log_generator: CommonGenerator, mode, max_log_per_sec, generate_interval, generate_num, target_servers):
        self.log_generator = log_generator
        self.mode = mode
        self.max_log_per_sec = max_log_per_sec
        self.generate_interval = generate_interval
        self.generate_num = generate_num
        self.target_servers = target_servers

    def create_log(self) -> list:

        log_list = []

        if self.mode == ConfigInfo.MODE_BATCH:

            for i in range(self.generate_num):
                log_list.append(self.log_generator.generate())


        elif self.mode == ConfigInfo.MODE_REALTIME:
            log_list.append(self.log_generator.generate())

        else:
            logging.error("Not Supported mode type")

        return log_list



    def create_syslog_header(self):
        pass