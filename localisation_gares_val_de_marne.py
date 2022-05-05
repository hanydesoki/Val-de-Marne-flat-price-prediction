import bs4
import requests

import pandas as pd

def main():
    base_url = 'https://fr.wikipedia.org/wiki/'
    list_url = base_url + 'Liste_des_gares_du_Val-de-Marne'

    source = requests.get(list_url).text

    soup = bs4.BeautifulSoup(source, 'lxml')

    df = {'name':[], 'longitude': [], 'latitude': []}

    lines = soup.find_all('a')

    for line in lines:
        l = line.text

        if 'Gare de Rungis MIN' in l:
            break

        if 'Gare' not in l or 'Gares' in l:
            continue


        nom_gare = l.strip().replace(' ', '_')
        url_gare = base_url + nom_gare

        print(f'Scrapping coordinate of {nom_gare}' + ' ' * 20, end='\r')

        gare_source = requests.get(url_gare).text

        gare_soup = bs4.BeautifulSoup(gare_source, 'lxml')

        loc = gare_soup.find('div', class_="mw-indicators")

        lon = float(loc.a.attrs['data-lon'])
        lat = float(loc.a.attrs['data-lat'])

        nom_gare = nom_gare.replace('_', ' ')

        df['name'].append(nom_gare)
        df['longitude'].append(lon)
        df['latitude'].append(lat)

    df = pd.DataFrame(df)

    df.to_csv('localisation_gares_val_de_marne.csv')
        


if __name__ == '__main__':
    main()
