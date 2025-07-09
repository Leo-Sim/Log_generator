
from config import Config
from generator import LogGeneratorFactory



config = Config()

log_type = config.get_log_type()


log_generator = LogGeneratorFactory.get_log_generator(log_type)
log1 = log_generator.generate()

print("@@ : ", log1)
