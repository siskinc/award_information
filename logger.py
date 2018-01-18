import logging

def logging_init():
  logger_name = 'award_information'
  global logger
  logger = logging.getLogger(logger_name)
  logger.setLevel(logging.INFO)

  log_path = './award_information.log'
  fh = logging.FileHandler(log_path, encoding='utf-8')
  fh.setLevel(logging.INFO)

  fmt = '%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s'
  datefmt = '%a %d %b %Y %H:%M:%S'
  formatter = logging.Formatter(fmt, datefmt)

  fh.setFormatter(formatter)
  logger.addHandler(fh)

logger = None
logging_init()
