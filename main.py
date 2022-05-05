import model_prediction



def main():

    df = model_prediction.build_df()

    town = df.loc[0, 'nom_commune']

    flat_price = model_prediction.predict(df)[0]

    if model_prediction.parking():
        flat_price += model_prediction.median_parking.loc[town, 'valeur_fonciere']

    if model_prediction.rdc():
        flat_price *= 0.75

    flat_price = f'{flat_price:,}'.replace(',', ' ')

    print('\nFlat price prediction:', flat_price, '€')


if __name__ == '__main__':
    main()


