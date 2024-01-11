import os,sys
import pandas as pd
import numpy as np
from flask import request,send_file
from src.logger import logging
from src.exception import CustomException
from src.utils import load_obj
from dataclasses import dataclass

@dataclass
class PredictionPipelineConfig:
    preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
    model_path=os.path.join('artifacts','model.pkl')
    input_data_path='input_data'
    predicted_data_path=os.path.join('artifacts','predictions.csv')

class BatchPrediction:
    def __init__(self):
        self.predict_config=PredictionPipelineConfig()

    def save_file(self,request):
        input_file=request.files['file']
        input_file_path=os.path.join(self.predict_config.input_data_path,input_file.filename)
        os.makedirs(os.path.dirname(input_file_path),exist_ok=True)
        input_file.save(input_file_path)

        return input_file_path
    
    def initiate_file_prediction(self,input_data_path):
        try:
            logging.info('Batch Prediction initiated')

            x_df= pd.read_csv(input_data_path)
            print(x_df.head())
            
            redundant_cols = ['qty_slash_domain','qty_questionmark_domain','qty_equal_domain','qty_and_domain',
            'qty_exclamation_domain','qty_space_domain','qty_tilde_domain','qty_comma_domain','qty_plus_domain',
            'qty_asterisk_domain','qty_hashtag_domain','qty_dollar_domain','qty_percent_domain']
            x_df.drop(redundant_cols,axis=1,inplace=True)
            
            preprocessor=load_obj(self.predict_config.preprocessor_path)
            model=load_obj(self.predict_config.model_path)

            x=preprocessor.transform(x_df)
            y=model.predict(x)
            x_df['Phishing']=[i for i in y]
            
            os.makedirs(os.path.dirname(self.predict_config.predicted_data_path),exist_ok=True)
            x_df.to_csv(self.predict_config.predicted_data_path,index=False,header=True)

            logging.info('Batch Prediction Successfull')
            
            return self.predict_config.predicted_data_path

        except Exception as e:
            logging.info('Error occurrred in Batch Prediction')
            raise CustomException(e,sys)