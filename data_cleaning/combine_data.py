import os
import pandas as pd
from pathlib import Path

DATA_PATH = Path('./data')
MODEL_TO_TYPE_MAP = Path('./brand_model.csv')

BRAND_NAMES = {
        'audi' : 'Audi',
        'bmw' : 'BMW',
        'vauxhall' : 'Vauxhall',
        'skoda' : 'Skoda',
        'toyota' : 'Toyota',
        'vw' : 'Volkswagen',
        'ford' : 'Ford',
        'hyundi' : 'Hyundai',
        'merc' : 'Mercedes'
        }

COUNTRIES_OF_ORIGIN = {
                      'Audi' : 'Germany',
                      'BMW' : 'Germany',
                      'Vauxhall' : 'UK',
                      'Skoda' : 'Czech Republic',
                      'Toyota' : 'Japan',
                      'Volkswagen' : 'Germany',
                      'Ford' : 'United States',
                      'Hyundai' : 'South Korea',
                      'Mercedes' : 'Germany'
                      }

def combine_data(file_path):
    cols_to_keep = ['brand',
                    'model',
                    'year',
                    'transmission',
                    'fuelType',
                    'engineSize',
                    'mileage',
                    'price',
                    'mpg']
    all_df =[]
    all_files = os.listdir('./data')
    all_files = [DATA_PATH / i for i in all_files]
    for i in all_files:
        brand_df = pd.read_csv(i)
        brand_df['brand'] = str(i).split('/')[-1].split('.')[0]
        try:
            all_df.append(brand_df[cols_to_keep])
        except:
            pass
    output =  pd.concat(all_df)
    output['brand'] = output['brand'].apply(lambda x: BRAND_NAMES[x])
    output['manufacturerOrigin'] = output['brand'].apply(lambda x: COUNTRIES_OF_ORIGIN[x])
    return output


def assign_vehicle_type(cleaned_data, mapping):
    cleaned_data['vehicle model'] = cleaned_data['brand'] + cleaned_data['model']
    map_df = pd.read_csv(mapping)
    map_dict = dict(zip(map_df['vehicle model'].tolist(), map_df['vehicle type'].tolist()))
    cleaned_data['vehicle type'] = cleaned_data['vehicle model'].apply(lambda x: map_dict[x])
    cleaned_data = cleaned_data.drop(columns=['vehicle model'])
    cleaned_data = cleaned_data.rename(columns = {'vehicle type' : 'vehicleType'})
    cleaned_data.to_csv('cleaned_used_car_data.csv', index = False)


if __name__ == '__main__':
    clean_frame = combine_data(DATA_PATH)
    assign_vehicle_type(clean_frame, MODEL_TO_TYPE_MAP)
