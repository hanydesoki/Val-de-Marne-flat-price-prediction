import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline


def boxplot_groupes(df, categ_column, target_column, figsize=(20, 10)):
    '''Boxplot the target column for all classes in the target columns in a DataFrame

            Parameters:
                    df (DataFrame): A DataFrame
                    categ_column (str): The name of the column which contains all classes
                    target_columns (str): The name of the column which contains values
                    figsize (tuple): Tuple representing the figure size
    '''
    groupes = []
    for cat in list(df[categ_column].unique()):
        groupes.append(df[df[categ_column] == cat][target_column])

    medianprops = {'color': "black"}
    meanprops = {'marker': 'o', 'markeredgecolor': 'black',
                 'markerfacecolor': 'firebrick'}

    plt.figure(figsize=figsize)
    plt.boxplot(groupes, labels=list(df[categ_column].unique()), showfliers=False, medianprops=medianprops,
                vert=False, patch_artist=True, showmeans=True, meanprops=meanprops)
    plt.ylabel(categ_column)
    plt.title(target_column)
    plt.show()


def plot_map(df, y_name, figsize=(12, 10), lat_long=('Long', 'Lat'), boundaries=None, interquartile=True, alpha=1):
    '''Get a geographical representation of all data points (with scatter) based on coordinates columns with a value associated

            Parameters:
                    df (DataFrame): A DataFrame
                    y_name ('str'): column name representing some continuous values which will be represented with colors in the plot
                    figsize (tuple): Tuple representing the figure size
                    lat_long (tuple): Tuple containing coord column names
                    boundaries (tuple): Tuple containing tuples defining boundaries of the map
                    interquartiles (bool): If True, the min and max of the colormap will be the interquartile
                    alpha ('float'): Value between 0 and 1 for the transparency
    '''
    
    plt.figure(figsize=figsize)
    desc_df = df.describe()
    if interquartile:
        vmin = desc_df.loc['25%', y_name]
        vmax = desc_df.loc['75%', y_name]
    else:
        vmin = desc_df.loc['min', y_name]
        vmax = desc_df.loc['max', y_name]

    points = plt.scatter(df[lat_long[0]], df[lat_long[1]], c=df[y_name], cmap='jet', lw=0, s=10, vmin=vmin, vmax=vmax,
                         alpha=alpha)
    if boundaries != None:
        plt.xlim(boundaries[0])
        plt.ylim(boundaries[1])
    plt.xlabel(lat_long[0])
    plt.ylabel(lat_long[1])
    plt.colorbar(points)
    plt.show()


def plot_map_categ(df, categ_column, figsize=(12, 10), lat_long=('Long', 'Lat'), boundaries=None, alpha=1):
    '''Get a geographical representation of all data points (with scatter) based on coordinates columns with a category associated

            Parameters:
                    df (DataFrame): A DataFrame
                    categ_columns ('str'): column name representing some categories which will be represented with colors in the plot
                    figsize (tuple): Tuple representing the figure size
                    lat_long (tuple): Tuple containing coord column names
                    boundaries (tuple): Tuple containing tuples defining boundaries of the map
                    alpha ('float'): Value between 0 and 1 for the transparency
    '''
    plt.figure(figsize=figsize)
    for classe in df[categ_column].sort_values().unique():
        df_classe = df[df[categ_column] == classe]
        plt.scatter(df_classe[lat_long[0]], df_classe[lat_long[1]], lw=0, s=10, label=classe, alpha=alpha)
    if boundaries != None:
        plt.xlim(boundaries[0])
        plt.ylim(boundaries[1])
    plt.legend()
    plt.show()


def corr_matrix(df, figsize=(30, 20), maptype='heatmap', absolute=False, crit_value=None,
                annot=True, save=False, filename='corr_matrix'):
    '''Plot the correlation matrix with seaborn of the DataFrame

            Parameters:
                    df (DataFrame): A DataFrame
                    figsize (tuple): Tuple representing the figure size
                    maptype (str): String representing the style of the matrix ('heatmap', 'clustermap')
                    absolute (bool): Correlation matrix with absolute values if True
                    crit_value (float): Highlight features with a correlation value greater than crit value
                    annot (bool): Dsplay values if True
                    save (bool): Save figure if True
                    filename (str): Filename if save=True

    '''
    matrix_corr = df.corr()

    if absolute:
        matrix_corr = matrix_corr.abs()
    if crit_value != None:
        matrix_corr = matrix_corr >= crit_value
    plt.figure(figsize=figsize)
    if maptype == 'heatmap':
        sns.heatmap(matrix_corr, annot=annot)
    elif maptype == 'clustermap':
        sns.clustermap(matrix_corr, annot=annot)

    if save:
        plt.savefig(filename)
    plt.show()
    
    
class MultiDimVisualization:

    '''Class for a 2D representation of a multidimensional dataset with PCA'''

    def __init__(self, transformer=None):
        self.transformer = transformer
        if transformer is None:
            self.pca_vizualisation = PCA(n_components=2)
        else:
            self.steps = [('transformer', transformer), ('pca', PCA(n_components=2))]
            self.pca_vizualisation = Pipeline(steps=self.steps)

        self.__isfitted = False

    def fit(self, X):
        self.pca_vizualisation.fit(X)
        self.__isfitted = True

        return self

    def transform_plot(self, X, y=None, figsize=(8, 6), title='2D representation of data', save=False, filename='data_2d.jpeg', **kwargs):
        self.check_isfitted()

        X_reduced = self.pca_vizualisation.transform(X)

        plt.figure(figsize=figsize)
        plt.scatter(X_reduced[:,0], X_reduced[:,1], c=y, **kwargs)

        plt.xlabel('PC0')
        plt.ylabel('PC1')
        plt.colorbar()
        plt.title(title)
        plt.show()

        if save:
            plt.savefig(filename)

        return X_reduced

    def fit_transform_plot(self, X, y=None, figsize=(8, 6), title='2D representation of data', save=False, filename='data_2d.jpeg', **kwargs):
        return self.fit(X).transform_plot(X, y=y, figsize=figsize, title=title, save=save, filename=filename, **kwargs)

    def get_transformer(self):
        return self.transformer

    def get_full_pipeline(self):
        return self.pca_vizualisation

    def check_isfitted(self):
        if not self.__isfitted:
            raise Exception(f'{self.__class__.__name__} not fitted yet.')

    def __repr__(self):
        return f"{self.__class__.__name__}(transformer={self.transformer})"
