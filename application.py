import sys
from flask import Flask,render_template,send_file,request
from src.logger import logging
from src.exception import CustomException
from src.pipelines.TrainingPipeline import TrainingPipeline
from src.pipelines.PredictionPipeline import BatchPrediction

app= Flask(__name__)
application=app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('train')
def train_data():
    try:
        trainPipeline= TrainingPipeline()
        trainPipeline.run_training_pipeline()
        return render_template('index1.html')
    except Exception as e:
        raise CustomException(e,sys)

#To avoid time delay run this route directly without running /train_data (if artifacts is present)
@app.route('/predict_file',methods=['GET','POST'])
def predict_file():
    try:
        if request.method=='POST':

            logging.info('Prediction Initiated')

            trainPipeline= TrainingPipeline()
            trainPipeline.run_training_pipeline()
            predictpipeline=BatchPrediction()
            input_data_path=predictpipeline.save_file(request)
            predicted_data_path=predictpipeline.initiate_file_prediction(input_data_path)

            return send_file(path_or_file=predicted_data_path,download_name=predicted_data_path,as_attachment=True)

        else:
            return render_template('upload.html')
        
    except Exception as e:
        logging.info('Prediction Failed')
        raise CustomException(e,sys)

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
