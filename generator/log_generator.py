from abc import abstractmethod

from generator import StandardLogInfo
import os
import json
import random

class LogGeneratorFactory:

    @staticmethod
    def get_log_generator(log_type):

        if log_type == StandardLogInfo.LOG_TYPE_LEEF:
            return LeefGenerator()



class CommonGenerator:

    def __init__(self):
        self.base_dir_path = os.path.dirname(os.path.realpath(__file__))

    def generate(self):
        """
        This function is responsible for reading config file and assembling each part of log
        :return:
        """

        header = self._make_log_header(self.log_format.get(StandardLogInfo.LOG_PART_HEADER, ""))
        body = self._make_log_body(self.log_format.get(StandardLogInfo.LOG_PART_BODY, ""))
        footer =  self._make_log_footer(self.log_format.get(StandardLogInfo.LOG_PART_FOOTER, ""))

        return header + body + footer


    def get_random_value(self, values: list):
        """
        This function selects a random value for given log field
        :param values:
        :return:
        """

        return random.choice(values)



    @abstractmethod
    def _make_log_body(self, body):
        """
        This function is responsible for generating the log body
        :return:
        """
        pass

    @abstractmethod
    def _make_log_header(self, header):
        """
        This function is responsible for generating the log header
        :return:
        """
        pass

    @abstractmethod
    def _make_log_footer(self, footer):
        """
        This function is responsible for generating the log footer
        :return:
        """
        pass


class LeefGenerator(CommonGenerator):

    def __init__(self):
        super().__init__()

        self.format_dir_path = os.path.join(self.base_dir_path, "..", "config", "log_format", StandardLogInfo.LOG_TYPE_LEEF + ".json")

        with open(self.format_dir_path, "r") as file:
            self.log_format = json.load(file)

        # Set leef version and delimiter
        self.leef_version = self.log_format.get(StandardLogInfo.LOG_INFO_KEY_VERSION, "2.0")
        self.delimiter = "\t"

        self.custom_delimiter = self.log_format.get(StandardLogInfo.LOG_INFO_KEY_DELIMITER, "")
        self.is_custom_delimiter = self.leef_version != "1.0"

    def _make_log_body(self, body):

        body_string = ""

        for i, b in enumerate(body):
            key = b.get(StandardLogInfo.LOG_INFO_KEY_NAME, "")
            value = self.get_random_value(b.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))

            if i > 0:
                body_string += self.delimiter

            if key != None and value != None:
                body_string = body_string + key + "=" + value

        return body_string

    def _make_log_header(self, header):

        d = "|"
        prefix = "LEEF:"

        vendor = product = product_version = event_id = ""

        for h in header:
            name = h.get(StandardLogInfo.LOG_INFO_KEY_NAME, "")
            if name == StandardLogInfo.HEADER_LEEF_VENDOR:
                vendor = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))
            elif name == StandardLogInfo.HEADER_LEEF_PRODUCT:
                product = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))
            elif name == StandardLogInfo.HEADER_LEEF_PRODUCT_VERSION:
                product_version = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))
            elif name == StandardLogInfo.HEADER_LEEF_EVENT_ID:
                event_id = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))

        header_string = prefix + self.leef_version + d + vendor + d + product + d + product_version + d + event_id + d

        # add custom delimiter to version 2.0
        if self.is_custom_delimiter and self.custom_delimiter != "":
            header_string = header_string + self.custom_delimiter + d
            self.delimiter = self.custom_delimiter

        return header_string


    def _make_log_footer(self, footer):
        return ""





