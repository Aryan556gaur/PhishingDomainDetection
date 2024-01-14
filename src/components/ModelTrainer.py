import os,sys
import numpy as np
from src.logger import logging
from src.exception import CustomException
from src.utils import save_obj,read_yaml
import xgboost
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,recall_score,precision_score
from dataclasses import dataclass

@dataclass
class ModelTrainerConfig:
    model_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_config=ModelTrainerConfig()

    def initiate_model_trainer(self,x_train,x_test,y_train,y_test):
        try:
            logging.info('Model selection initiated')

            models= {"AdaBoostClassifier" : AdaBoostClassifier(), 
            "DecisionTreeClassifier" : DecisionTreeClassifier(), 
            "RandomForestClassifier" : RandomForestClassifier(), 
            "GradientBoostingClassifier" : GradientBoostingClassifier(),
            "SVC": SVC(), "XGBClassifier": XGBClassifier()}

            model_list={}

            for i in range(len(models)):

                model = list(models.values())[i]

                model.fit(x_train,y_train)
                pred = model.predict(x_test)

                score = accuracy_score(y_test,pred)
                model_list[list(models.keys())[i]] = score

            i = np.argmax(list(model_list.values()))
            best_model_name = list(model_list.keys())[i]
            best_model_obj = models[best_model_name]

            grid = GridSearchCV(best_model_obj,param_grid=read_yaml(os.path.join('config','Model.yaml'))['model_selection']['model'][best_model_name]['search_param_grid'],cv=5)
            grid.fit(x_train,y_train)
            parameters = grid.best_params_
            final_model=best_model_obj(**parameters)
            final_model = RandomForestClassifier(verbose=3,n_estimators=3)
            final_model.fit(x_train,y_train)

            save_obj(self.model_config.model_path,final_model)

            logging.info('Best Model selected')
        
        except Exception as e:
            logging('Error occurred in Model Selection')
            raise CustomException(e,sys)
