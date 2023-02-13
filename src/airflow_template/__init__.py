import configparser
import logging
import logging.config

# setup
logging.config.fileConfig('conf/logging.conf', defaults={'fileHandlerLog': 'logs/airflow_template.log'})

# objects to make available when this package is imported
cparser = configparser.ConfigParser()

# # __all__ applies to the situation where from foo.bar import *
# __all__ = [
#     'logger'
# ]