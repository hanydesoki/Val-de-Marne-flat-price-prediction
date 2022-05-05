from sklearn.metrics import confusion_matrix, classification_report, mean_squared_error, mean_absolute_error, accuracy_score, r2_score
import seaborn as sns
import matplotlib.pyplot as plt

def evaluate_class(model, X, y):
    y_pred = model.predict(X)

    print(classification_report(y, y_pred))

    plt.figure()
    sns.heatmap(confusion_matrix(y, y_pred), annot=True)
    plt.xlabel('y_pred')
    plt.ylabel('y_true')
    plt.show()

    return y_pred

def evaluate_reg(model, X, y):
    y_pred = model.predict(X)
    print('Accuracy:', accuracy_score(y, y_pred))
    print('MAE:', mean_absolute_error(y, y_pred))
    print('RMSE:', mean_squared_error(y, y_pred, squared=False))
    print('R²:', r2_score(y, y_pred))

    return y_pred


