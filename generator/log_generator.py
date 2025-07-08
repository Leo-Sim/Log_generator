from abc import abstractmethod

from generator import StandardLogInfo
import os
import json

class LogGeneratorFactory:

    @staticmethod
    def get_log_generator(log_type):

        if log_type == StandardLogInfo.LOG_TYPE_LEEF:
            return LeefGenerator()



class LogFormatReader:

    def __init__(self):
        self.base_dir_path = os.path.dirname(os.path.realpath(__file__))



    @abstractmethod
    def generate(self):
        """
        This function is responsible for reading config file and assembling each part of log
        :return:
        """
        pass

    @abstractmethod
    def _make_log_body(self):
        """
        This function is responsible for generating the log body
        :return:
        """
        pass

    @abstractmethod
    def _make_log_header(self):
        """
        This function is responsible for generating the log header
        :return:
        """
        pass

    @abstractmethod
    def _make_log_footer(self):
        """
        This function is responsible for generating the log footer
        :return:
        """
        pass



class LeefGenerator(LogFormatReader):

    def __init__(self):
        super().__init__()

        self.format_dir_path = os.path.join(self.base_dir_path, "..", "config", "log_format", StandardLogInfo.LOG_TYPE_LEEF + ".json")

    def generate(self):
        print(self.format_dir_path)


        with open(self.format_dir_path, "r") as file:
            log_format = json.load(file)
            print(log_format)


    def _make_log_body(self):
        return ""

    def _make_log_header(self):
        return ""


    def _make_log_footer(self):
        return ""




