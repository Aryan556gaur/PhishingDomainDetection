import os,sys
from flask import request,send_file
from src.logger import logging
from src.exception import CustomException
from src.utils import load_obj
from dataclasses import dataclass

class PredictionPipelineConfig:
    input_file_path=os.path.join()