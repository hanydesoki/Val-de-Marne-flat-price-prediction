import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import tqdm

def param_range_model(model, X_train, y_train, X_test, y_test, param_range, scoring):

    '''Plot scores fro a parameter range for train and test set 

            Parameters:
                    model (sklearn model): A model that can use fit and predict
                    X_train (DataFrame or numpy array): Train data
                    y_train (Series, list or numpy array): Train target
                    X_test (DataFrame or numpy array): Test data
                    y_test (Series, list or numpy array): Test target
                    param_range (dict): Dict with one param key and it's range values
                    scoring (function): Function that accept y_true and y_pred and return a score

            Return:
                    score_train, score_test
    '''

    if len(param_range) != 1:
        raise Exception(f'Only accept one parameter to optimize, got {len(param_range)} instead')

    Rnge = list(param_range.values())[0]

    param_name = list(param_range.keys())[0]

    train_scores = []
    test_scores = []

    for p in tqdm.tqdm(Rnge):
        # Setup
        model_p = deepcopy(model)
        params = {param_name : p}
        model_p.set_params(**params)
        
        # Training
        model_p.fit(X_train, y_train)

        # Evaluation
        y_pred_train = model_p.predict(X_train)
        y_pred_test = model_p.predict(X_test)

        train_scores.append(scoring(y_train, y_pred_train))
        test_scores.append(scoring(y_test, y_pred_test))

    # Plotting
    plt.figure(figsize=(12, 8))
    plt.plot(Rnge, train_scores, label='Train set')
    plt.plot(Rnge, test_scores, label='Test set')
    plt.legend()
    plt.grid(True)
    plt.xlabel(param_name)
    plt.ylabel(scoring.__name__)
    plt.title(f'Evolution of {scoring.__name__}')
    plt.show()

    return train_scores, test_scores




        


    
