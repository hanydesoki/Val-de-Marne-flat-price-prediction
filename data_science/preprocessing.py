import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator
import numpy as np
from warnings import warn

class DfEncoderOneHot(TransformerMixin, BaseEstimator):
    '''Encoding class. Work only for pandas DataFrame.
     Encoding with 0 and 1 all categorical columns with only 2 classes and 
     do a one hot encoding with the other categorical columns.
     Compatible with sklearn pipelines.'''
    def __init__(self, nan_as_category=False, return_array=False):
        self.return_array = return_array
        self.nan_as_category = nan_as_category
        self.initialisation()

    def initialisation(self):
        self.original_categorical_columns = []
        self.binary_columns = {}
        self.other_categorical_columns = {}
        self.original_columns = None
        self.encoded_columns = []

    def fit(self, df, y=None):
        
        self.initialisation()

        self.original_columns = list(df.columns)

        self.original_categorical_columns += list(df.select_dtypes('object')) + list(df.select_dtypes('category')) + list(df.select_dtypes('bool'))

        for col in self.original_categorical_columns:
            if self.nan_as_category:
                classes = list(df[col].unique())
            else:
                classes = list(df[col].dropna().unique())

            if len(classes) == 2:
                if df[col].dtype == 'bool':
                    code = {False: 0.0, True: 1.0}
                else:
                    code = {classes[0]: 0.0, classes[1]: 1.0}
                self.binary_columns[col] = code
            else:
                self.other_categorical_columns[col] = classes

        for i, col in enumerate(self.original_columns):
            if col not in self.other_categorical_columns:
                self.encoded_columns.append(col)
            else:
                for c in self.other_categorical_columns[col]:
                    if pd.isnull(c):
                        self.encoded_columns.append(f'{col}_na')
                    else:
                        self.encoded_columns.append(f'{col}_{c}') 
              
        return self

    def transform(self, df):
        df_encoded = df.copy()
        for col, code in self.binary_columns.items():
            for c in df_encoded[col].dropna().unique():
                if c not in code:
                    warn(f'It seems that there is more than 2 categories ({c}) in {col} which was considered a binary column in the fit.\n\
                    this new category will be replaced with 0.0')
                    code[c] = 0.0
                    self.binary_columns[col][c] = 0.0
            df_encoded[col].replace(code, inplace=True)

        for col, classes in self.other_categorical_columns.items():
            for c in classes:
                if pd.isnull(c):
                    df_encoded[f'{col}_na'] = (df[col].isna()).astype('float')
                else:   
                    df_encoded[f'{col}_{c}'] = (df[col] == c).astype('float')

            del df_encoded[col]

        df_encoded = df_encoded[self.encoded_columns]

        if self.return_array:
            df_encoded = df_encoded.values

        return df_encoded


    def get_binary_columns(self):
        return self.binary_columns

    def get_other_categorical_columns(self):
        return self.other_categorical_columns

    def get_original_categorical_columns(self):
        return self.original_categorical_columns

    def get_original_columns(self):
        return self.original_columns

    def get_encoded_columns(self):
        return self.encoded_columns

    def get_new_columns(self):
        return [col for col in self.get_encoded_columns() if col not in self.get_original_columns()]

    def __repr__(self):
        return f"{self.__class__.__name__}(nan_as_category={self.nan_as_category}, return_array={self.return_array})"
    
class FillImputer(TransformerMixin, BaseEstimator):
    '''Imputer class that will fill with different strategy depending on the column type. Work with pandas DataFrame only'''
    def __init__(self):
        self.initialisation()

    def initialisation(self):
        self.fill_code = {}

    def fit(self, df, y=None):
        for col in df.columns:
            if df[col].dtype in ['object', 'category', 'bool']:
                value = df[col].value_counts(ascending=False).index[0]

            else:
                if df[col].isna().mean() == 1:
                    value = 0
                else:
                    value = df[col].median()

            self.fill_code[col] = value
        
        return self

    def transform(self, df):
        df_filled = df.copy()
        for col in df_filled.columns:
            df_filled[col].fillna(self.fill_code[col], inplace=True)

        return df_filled

    def __repr__(self):
        return f"{self.__class__.__name__}()"
    
class Log(TransformerMixin, BaseEstimator):
    '''Logarithme transformer. Used for a pipeline'''
    def __init__(self, eps=0.01):
        self.eps = eps

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        X_log = X.copy()
        mask = X_log <= 0
        X_log[mask] = self.eps

        return np.log(X_log)

    def __repr__(self):
        return f"{self.__class__.__name__}(eps={self.eps})"
