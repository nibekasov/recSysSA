# recSysSoA
My team project on RecSys 

Here should be ML System Design + Integration with other parts of project(FrontEnd, DataEngeneering, simple BackEnd) 

Objective & Key Results:
* Objectives:

  Create an app for marketplace. Architecture includes:
    - RecSys to give customers recommendations for items they could need
    - Simple Backend to connect ML and our project
    - Simle Frontend to show how algorithm is working
  
* Key Results:
    - Model accuracy #ToDo: Specify
    - Retention  #ToDo: Specify
    - LTV/GMV per User/ARPPU/AVG #ToDo: Specify
    - Relaiability/ Service agreement 
MlSystemDesign:
* Tools:clearml/mlflow
* Realisation:

FrontEnd:
* Tools:JavaScript(TypeScript(?)) + HTML/CSS
* Realisation:
  
Data:
* Tools:Airflow
* Realisation:

BackEnd:
* Tools:Python + Flask
* Realisation:


Current results:

In this report, we present an overview of the work done and the results that were achieved.

Data preprocessing: To begin the work, data pre-processing was performed. This step included:

* Running the data preprocessing script (process.py).
* Splitting the data into training and test samples using the split script (split.py).
* Model training

The following steps were carried out to build the recommendation models:

* Training the two models using a training script (train.py).
* Performing inference for the first model according to the inference.py
* Exploratory data analysis

An exploratory data analysis was performed to better understand the characteristics of the original data. 
* This analysis identified key features that can be used to improve the recommendations.

Baseline model

* A baseline model was created to compare with the developed models to serve as a starting point for performance evaluation.

What remains to be done

Many tasks were accomplished during the project, but the following tasks remain:

* Retraining the models to improve recommendation accuracy.
* Containerizing the project to simplify deployment and scaling.
* Implementing metrics to evaluate model performance.
* Developing a second model to compare and select the best model.


Project Launch

The following steps are required to start the project:



* Run the data preprocessing script (preprocessing.py).
* Run the script for data split (train and test sets for two-stage model, split.py)
* Run the script for model training (train.py).
* Run the API script to get recommendations (api.py).
Note: To get recommendations, you need to add a backslash in the address, \login, and go to the recommendations page. 

Conclusion

The recommendation system project is currently under active development. Despite the results achieved, there is potential to improve the models and further optimize the process.We will continue to work on the project by introducing additional features and improving the quality of recommendations.
