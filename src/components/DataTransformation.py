import os,sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from src.logger import logging
from src.exception import CustomException
from src.utils import save_obj
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    preprocessor_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.transformation_config=DataTransformationConfig()

    def get_preprocessor(self,x_train):

        scaler=StandardScaler()
        x_train_experimental=scaler.fit_transform(x_train)
        pca=PCA()
        pca.fit(x_train_experimental)
        explained_variance_ratio = pca.explained_variance_ratio_
        cum_explained_variance = np.cumsum(explained_variance_ratio)
        n = np.argmax(cum_explained_variance>=0.95)+1

        preprocessor= Pipeline(steps=[
            ('scaler',StandardScaler()),
            ('PCA',PCA(n_components=n))
        ])

        return preprocessor


    def initiate_data_transformation(self,raw_data_path):
        try:
            logging.info('Data Transformation initiated')

            df = pd.DataFrame(raw_data_path)

            x=df.drop('phishing',axis=1)
            y=df['phishing']

            redundant_cols = np.var(x).keys()[np.var(x).values==0]
            x.drop(redundant_cols,axis=1,inplace=True)

            x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.33,random_state=42)

            preprocessor=self.get_preprocessor(x_train)
            x_train=preprocessor.fit_transform(x_train)
            x_test=preprocessor.transform(x_test)

            os.makedirs(os.path.dirname(self.transformation_config.preprocessor_path),exist_ok=True)
            save_obj(self.transformation_config.preprocessor_path, preprocessor)

            logging.info('Data Transformation Completed Successfully')

            return x_train,x_test,y_train,y_test
        
        except Exception as e:
            logging.info('Error occurred in Data Transformation')
            raise CustomException(e,sys)

