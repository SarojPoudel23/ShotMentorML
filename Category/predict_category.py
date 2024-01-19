import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from statistics import mode

def predict_category(X_test):
    logistic_regression = joblib.load('logistic_regression_model.joblib')
    logistic_regression_scaled = joblib.load('logistic_regression_scaled_model.joblib')
    svm = joblib.load('support_vector_machine_scaled_model.joblib')
    scaler = joblib.load('scaler.joblib')

    # X_test = pd.read_csv('test/test_9_testing.csv')
    X_test_scaled = scaler.transform(X_test)

    logreg = logistic_regression.predict(X_test)
    logreg1 = logistic_regression_scaled.predict(X_test_scaled)
    svm_predict = svm.predict(X_test_scaled)

    all_predict= np.array([logreg,logreg1,svm_predict])
    combined_predict = np.apply_along_axis(mode, axis=0, arr=all_predict)

    predict_df = pd.DataFrame({'category':combined_predict})

    return predict_df

    # predict_9_new = pd.read_csv('test/predict_9.csv')
    #
    # predict_9_new['new_combined']=combined_predict
    #
    # predict_9_new.to_csv('test/predict_new_9.csv',index=False)