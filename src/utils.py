import sys
import pandas as pd
import pickle,yaml
import pymongo
from src.logger import logging
from src.exception import CustomException

def import_data_as_Dataframe(database,collection):
    try:
        logging.info('Data importing Started')

        client = pymongo.MongoClient('mongodb+srv://aryangaur556:Abhishek@cluster0.pfi4w9l.mongodb.net/?retryWrites=true&w=majority')
        data = client[database][collection]
        df = pd.DataFrame(data.find())

        if 'id' in df.columns:
            df.drop('id',axis=1)
        return df

    except Exception as e:
        logging.info('Error occurred in Data importing')
        raise CustomException(e,sys)

def load_obj(filepath:str):
    try:
        with open(filepath,'rb') as file:
            return pickle.load(file)
    except Exception as e:
        logging.info('Error occurred in object loading')
        raise CustomException(e,sys)        
    
def save_obj(filepath:str,file_obj):
    try:
        with open(filepath, 'wb') as file:
            pickle.dump(file_obj,file=file)
    except Exception as e:
        logging.info('Error occurred in object saving')
        raise CustomException(e,sys)      
    

def read_yaml(filepath:str):
    try:
        return yaml.safe_load(filepath)
    except Exception as e:
        logging.info('Error occurred in reading yaml file')
        raise CustomException(e,sys)  