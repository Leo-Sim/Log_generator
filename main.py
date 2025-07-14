
from config import Config
from generator import LogGeneratorFactory
from sender import LogSender


config = Config()

log_type = config.get_log_type()

interval = config.get_transfer_interval()
count = config.get_transfer_count()
target_servers = config.get_transfer_target_servers()


log_generator = LogGeneratorFactory.get_log_generator(log_type)
sender = LogSender(log_generator, interval, count, target_servers)

result = sender.send_logs()




