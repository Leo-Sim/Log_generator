from abc import abstractmethod

from generator import StandardLogInfo
import os
import json
import random
import logging

class LogGeneratorFactory:

    @staticmethod
    def get_log_generator(log_type):
        log_type = log_type.lower()

        if log_type == StandardLogInfo.LOG_TYPE_LEEF:
            return LeefGenerator()

        elif log_type == StandardLogInfo.LOG_TYPE_CUSTOM:
            return CustomGenerator()

        elif log_type == StandardLogInfo.LOG_TYPE_CEF:
            return CefGenerator()




        else:
            logging.error("Not supported log format.  Leef, Cef and Custom formats are supported")



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

class CefGenerator(CommonGenerator):

    def __init__(self):
        super().__init__()
        self.format_dir_path = os.path.join(self.base_dir_path, "..", "config", "log_format",
                                            StandardLogInfo.LOG_TYPE_CEF + ".json")

        with open(self.format_dir_path, "r") as file:
            self.log_format = json.load(file)


    def _make_log_body(self, body):

        body_string = ""

        for i, b in enumerate(body):
            if i != 0:
                body_string += " "

            key = b.get(StandardLogInfo.LOG_INFO_KEY_NAME, "")
            value = self.get_random_value(b.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))

            body_string += key + "=" + value

        return body_string


    def _make_log_header(self, header):
        d = "|"
        prefix = "CEF:"

        version = vendor = product = product_version = signature = _name = severity = ""

        for h in header:
            name = h.get(StandardLogInfo.LOG_INFO_KEY_NAME, "")
            if name == StandardLogInfo.HEADER_VERSION:
                version = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))
            elif name == StandardLogInfo.HEADER_VENDOR:
                vendor = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))
            elif name == StandardLogInfo.HEADER_PRODUCT:
                product = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))
            elif name == StandardLogInfo.HEADER_PRODUCT_VERSION:
                product_version = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))
            elif name == StandardLogInfo.HEADER_SIGNATURE:
                signature = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))
            elif name == StandardLogInfo.HEADER_NAME:
                _name = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))
            elif name == StandardLogInfo.HEADER_SEVERITY:
                severity = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))

            header_string = (
                    prefix + version + d + vendor + d + product + d + product_version + d
                    + signature + d + _name + d + severity + d
            )

        return header_string


    def _make_log_footer(self, footer):
        return footer


class CustomGenerator(CommonGenerator):

    def __init__(self):
        super().__init__()
        self.format_dir_path = os.path.join(self.base_dir_path, "..", "config", "log_format",
                                            StandardLogInfo.LOG_TYPE_CUSTOM + ".json")

        with open(self.format_dir_path, "r") as file:
            self.log_format = json.load(file)

        self.delimiter = self.log_format.get(StandardLogInfo.LOG_INFO_KEY_DELIMITER, None)
        self.include_header = self.log_format.get("include_field_header", False)
        self.header_separator = self.log_format.get("header_separator", None)

        if self.include_header and self.header_separator is None:
            logging.error("Key 'header_separator' in custom.json is not defined")

        if self.delimiter is None:
            logging.error("Delimiter not defined")

    def _make_log_body(self, body):


        body_string = ""
        field_list = []

        for i, b in enumerate(body):
            field = b.get("name", None)
            field_list.append(field)

            if field is None:
                logging.error("Field name is not defined")
                return ""

            value = self.get_random_value(b.get("value", []))

            body_string += value

            if i + 1 < len(body):
                body_string += self.delimiter

        result = ""

        if self.include_header:
            result += ",".join(field_list) + self.header_separator

        result += body_string

        return result


    def _make_log_header(self, header):
        return header


    def _make_log_footer(self, footer):
        return footer


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
            if name == StandardLogInfo.HEADER_VENDOR:
                vendor = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))
            elif name == StandardLogInfo.HEADER_PRODUCT:
                product = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))
            elif name == StandardLogInfo.HEADER_PRODUCT_VERSION:
                product_version = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))
            elif name == StandardLogInfo.HEADER_EVENT_ID:
                event_id = self.get_random_value(h.get(StandardLogInfo.LOG_INFO_KEY_VALUE, []))

        header_string = prefix + self.leef_version + d + vendor + d + product + d + product_version + d + event_id + d

        # add custom delimiter to version 2.0
        if self.is_custom_delimiter and self.custom_delimiter != "":
            header_string = header_string + self.custom_delimiter + d
            self.delimiter = self.custom_delimiter

        return header_string


    def _make_log_footer(self, footer):
        return ""





