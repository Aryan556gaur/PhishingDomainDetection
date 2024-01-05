import os,sys
from datetime import datetime
import logging

log_file_format = f'{datetime.now().strftime("%m_%d_%y_%H_%M_%S")}.logs'
logs = os.path.join(os.getcwd(),'logs',log_file_format)
os.makedirs(logs,exist_ok=True)
log_file = os.path.join(logs,log_file_format)

logging.basicConfig(
    filename=log_file,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s ',
    level=logging.INFO
)