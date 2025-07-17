
import socket
import logging
import random
import time
from generator import CommonGenerator
from datetime import datetime



class LogSender:

    def __init__(self, log_generator: CommonGenerator, generate_interval, generate_num, target_servers):
        self.log_generator = log_generator


        self.generate_interval = generate_interval
        self.generate_num = generate_num
        self.target_servers = self._get_target_server_info(target_servers)

    def _get_target_server_info(self, target_servers):

        if target_servers is not None:
            target_servers = target_servers.split(",")

            result = []

            for target_server in target_servers:
                i = {}
                ip_port = target_server.split(":")

                i["ip"] = ip_port[0]
                i["port"] = ip_port[1]

                result.append(i)

            return result


    def send_logs(self):
        """
        This function sends logs with given batch size and interval
        :return:
        """

        while True:
            log_list = self.create_log()

            for target_server in self.target_servers:
                ip = target_server["ip"]


                port = int(target_server["port"])

                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((ip, port))
                        for log in log_list:
                            s.sendall((log + '\n').encode())
                            print(f"[sent] {log.strip()} → {ip}:{port}")
                except Exception as e:
                    print(f"[error] Failed to send to {ip}:{port} → {e}")

            time.sleep(self.generate_interval)


    def create_log(self) -> list:

        log_list = []

        syslog_header = self.create_syslog_header()

        for i in range(self.generate_num):
            log_body = self.log_generator.generate()
            log_list.append(syslog_header + log_body)

        return log_list



    def create_syslog_header(self):

        SEVERITY_MAP = {
            "EMERG": 0, "ALERT": 1, "CRIT": 2, "ERROR": 3,
            "WARN": 4, "NOTICE": 5, "INFO": 6, "DEBUG": 7
        }

        FACILITY_CODES = {
            "kern": 0, "user": 1, "mail": 2, "daemon": 3,
            "auth": 4, "syslog": 5, "lpr": 6, "news": 7,
            "uucp": 8, "cron": 9, "authpriv": 10, "ftp": 11,
            "ntp": 12, "security": 13, "console": 14,
            "local0": 16, "local1": 17, "local2": 18, "local3": 19,
            "local4": 20, "local5": 21, "local6": 22, "local7": 23
        }

        severity = random.choice(list(SEVERITY_MAP.keys()))
        facility = random.choice(list(FACILITY_CODES.keys()))

        pri_value = FACILITY_CODES[facility] * 8 + SEVERITY_MAP[severity]
        pri = f"<{pri_value}>"

        timestamp = datetime.now().strftime("%b %d %H:%M:%S")
        hostname = random.choice(["web-01", "api-02", "db-03"])
        app_name = random.choice(["sshd", "nginx", "login", "custom-agent"])
        pid = random.randint(1000, 9999)

        return f"{pri}{timestamp} {hostname} {app_name}[{pid}]:"

