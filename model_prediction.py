import numpy as np
import pandas as pd

from data_science.utils import load_model
from data_science.feature_engineering import distance_coords

all_towns = ['Ablon-sur-Seine',
 'Alfortville',
 'Arcueil',
 'Boissy-Saint-Léger',
 'Bonneuil-sur-Marne',
 'Bry-sur-Marne',
 'Cachan',
 'Champigny-sur-Marne',
 'Charenton-le-Pont',
 'Chennevières-sur-Marne',
 'Chevilly-Larue',
 'Choisy-le-Roi',
 'Créteil',
 'Fontenay-sous-Bois',
 'Fresnes',
 'Gentilly',
 'Ivry-sur-Seine',
 'Joinville-le-Pont',
 "L'Haÿ-les-Roses",
 'La Queue-en-Brie',
 'Le Kremlin-Bicêtre',
 'Le Perreux-sur-Marne',
 'Le Plessis-Trévise',
 'Limeil-Brévannes',
 'Maisons-Alfort',
 'Mandres-les-Roses',
 'Marolles-en-Brie',
 'Nogent-sur-Marne',
 'Noiseau',
 'Orly',
 'Ormesson-sur-Marne',
 'Périgny',
 'Rungis',
 'Saint-Mandé',
 'Saint-Maur-des-Fossés',
 'Saint-Maurice',
 'Santeny',
 'Sucy-en-Brie',
 'Thiais',
 'Valenton',
 'Villecresnes',
 'Villejuif',
 'Villeneuve-Saint-Georges',
 'Villeneuve-le-Roi',
 'Villiers-sur-Marne',
 'Vincennes',
 'Vitry-sur-Seine']

towns_dict = {str(i) :town for i, town in enumerate(all_towns, start=1)}

original_data_columns = ['id_mutation',
 'date_mutation',
 'numero_disposition',
 'nature_mutation',
 'valeur_fonciere',
 'adresse_numero',
 'adresse_suffixe',
 'adresse_nom_voie',
 'adresse_code_voie',
 'code_postal',
 'code_commune',
 'nom_commune',
 'code_departement',
 'ancien_code_commune',
 'ancien_nom_commune',
 'id_parcelle',
 'ancien_id_parcelle',
 'numero_volume',
 'lot1_numero',
 'lot1_surface_carrez',
 'lot2_numero',
 'lot2_surface_carrez',
 'lot3_numero',
 'lot3_surface_carrez',
 'lot4_numero',
 'lot4_surface_carrez',
 'lot5_numero',
 'lot5_surface_carrez',
 'nombre_lots',
 'code_type_local',
 'type_local',
 'surface_reelle_bati',
 'nombre_pieces_principales',
 'code_nature_culture',
 'nature_culture',
 'code_nature_culture_speciale',
 'nature_culture_speciale',
 'surface_terrain',
 'longitude',
 'latitude']

columns_to_keep = ['adresse_numero', 'nom_commune',
                   'nombre_lots', 'lot1_surface_carrez', 'lot2_surface_carrez',
       'lot3_surface_carrez','lot4_surface_carrez', 'lot5_surface_carrez','surface_reelle_bati', 'nombre_pieces_principales',
       'surface_terrain', 'longitude', 'latitude']

asked_columns = ['adresse_numero', 'nom_commune',
          'nombre_lots',
       'surface_reelle_bati', 'nombre_pieces_principales',
       'surface_terrain', 'longitude', 'latitude']



model = load_model('val_de_marne_flat_model.pkl')
encoder = load_model('encoder.pkl')
scaler_y = load_model('scaler_y.pkl')

all_stations = pd.read_csv('localisation_gares_val_de_marne.csv')
median_parking = pd.read_csv('median_parking.csv')
median_parking.set_index('nom_commune', inplace=True)

def numero_addresse():
    while True:
        num = input("Numero d'adresse: ")

        try:
            return float(num)
        except ValueError:
            continue

def nom_commune():
    while True:
        for i, town in towns_dict.items():
            print(f'{i}: {town}')
        num = input("Choisissez le numéro de la commune parmi ces choix: ")

        try:
            return towns_dict[num]
        except KeyError:
            continue

def nombre_lots():
     while True:
        num = input("Nombre de lots (entre 0 et 5): ")

        try:
            num = int(num)

            if num not in list(range(0, 6)):
                continue

            return num

        except ValueError:
            continue

def lot_surface_carrez(i):
    while True:
        num = input(f"Lot surface carrez {i}: ")

        try:
            return float(num)
        except ValueError:
            continue

def surface_reelle_bati():
    while True:
        num = input("Surface réelle batie: ")

        try:
            return float(num)
        except ValueError:
            continue

def nombre_pieces_principales():
    while True:
        num = input("Nombre pieces principales: ")

        try:
            return int(num)
        except ValueError:
            continue

def surface_terrain():
    while True:
        num = input("Surface terrain: ")

        try:
            return float(num)
        except ValueError:
            continue

def longitude():
    while True:
        num = input("Longitude: ")

        try:
            return float(num)
        except ValueError:
            continue

def latitude():
    while True:
        num = input("Latitude: ")

        try:
            return float(num)
        except ValueError:
            continue


def parking():
    while True:
        res = input('Parking (oui / non): ').lower()

        if res not in ['oui', 'non']:
            continue

        return res == 'oui'


def rdc():
    while True:
        res = input('Rez de chaussée (oui / non): ').lower()

        if res not in ['oui', 'non']:
            continue

        return res == 'oui'


all_funcs = [numero_addresse, nom_commune, nombre_pieces_principales,
             surface_reelle_bati, surface_terrain,
             longitude, latitude]


def build_df():

    df = pd.DataFrame({col: [np.nan] for col in original_data_columns})

    for input_func in all_funcs:

        df.loc[0, input_func.__name__] = input_func()


    nmbr_lot = nombre_lots()

    df.loc[0, 'nombre_lots'] = nmbr_lot

    for i in range(1, 6):
        if i <= nmbr_lot:
            df.loc[0, f'lot{i}_surface_carrez'] = lot_surface_carrez(i)

    return df


def get_nearest_station_distance(row):

    m1 = (row['longitude'], row['latitude'])

    min_dist = float('inf')

    for i in all_stations.index:
        station = all_stations.loc[i]
        m2 = tuple(station[['longitude', 'latitude']])

        dist = distance_coords(m1, m2)

        min_dist = min(min_dist, dist)

    return min_dist * 1000

def feature_selection(df: pd.DataFrame):
    return df[columns_to_keep]

def imputation(df: pd.DataFrame):
    df = df[(df['longitude'].notna()) | (df['latitude'].notna())]
    df = df.fillna(0)
    return df

def feature_engineering_(df: pd.DataFrame):
    df['nearest_station_distance (m)'] = df.apply(get_nearest_station_distance, axis=1)
    return df



def predict(df):

    df = feature_selection(df)
    df = imputation(df)
    df = feature_engineering_(df)

    x = df.copy()

    x_encoded = encoder.transform(x)

    y_scaled_pred = model.predict(x_encoded)
    y_pred = scaler_y.inverse_transform(y_scaled_pred.reshape(-1, 1)).ravel()

    return y_pred



