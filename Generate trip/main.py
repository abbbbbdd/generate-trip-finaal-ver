import pandas as pd
from fastapi import FastAPI
import random
import numpy as np
from geopy.distance import great_circle
import datetime

app = FastAPI()

@app.post('/generate_trip')
def generate_trip(data: dict):
    counter = 1
    categories = ['Archaeological museum',
                  'Ancient Egyptian Sites',
                  'Historical landmark',
                  'Cultural Centers',
                  'Religious Sites']

    def get_preferred_categories(preferred_categories):
        preferred_categories_set = set()
        for category in preferred_categories:
            if category in ['Historical Sites', 'Ancient Sites']:
                preferred_categories_set.update(['Historical landmark', 'Ancient Egyptian Sites'])
            elif category in ['Cultural Institutions', 'Archaeological Exhibitions']:
                preferred_categories_set.update(['Cultural Centers', 'Archaeological museum'])
            else:
                preferred_categories_set.add('Religious Sites')
        return list(preferred_categories_set)

    def adding_fun(time1, governorate):
        random_cate = ["Bazaar", 'Malls', 'Entertainment Centers']
        random_index = np.random.randint(0, len(random_cate))
        random_category = random_cate[random_index]
        if len(df[(df['category'] == random_category) & (df['government'] == governorate)]['places']) == 0:
            return adding_fun(time1, governorate)
        fun_place = random.choice(
            df[(df['category'] == random_category) & (df['government'] == governorate)]['places'].tolist())
        placenum = data.get('no_of_places') + 1
        x1 = {
            f'place{placenum}': fun_place,
            'longitude': df[df['places'] == fun_place]['longitude'].iloc[0],
            'latitude': df[df['places'] == fun_place]['latitude'].iloc[0],
            'activity': df[df['places'] == fun_place]['activity'].iloc[0].replace('\xa0', ''),
            'category': df[df['places'] == fun_place]['category'].iloc[0],
            'image_link': df[df['places'] == fun_place]["Image's link"].iloc[0],
            'budget': df[df['places'] == fun_place]["Price range"].iloc[0],
            "time": f"{flo_totime(time1)} - {flo_totime(time1 + 1)}"
        }
        return x1

    def flo_totime(time):
        hours = int(time)
        minutes = int((time - hours) * 60)
        time_obj = datetime.time(hours, minutes)
        time_str = time_obj.strftime("%I:%M%p ")
        return time_str

    clock = [1.5, 1, 2]
    df = pd.read_excel('finalversionof_data.xlsx', index_col=0)
    prefered = get_preferred_categories(data.get('prefered'))
    source = (data.get('latitude'), data.get('longitude'))
    objects_of_objects = {}

    for governorate, iteration in data.get('Government').items():
        distances = []
        dict_ = {}
        places = []
        num_of_day = iteration
        num_of_places = data.get('no_of_places')
        places_required = num_of_day * num_of_places
        placed_according_pref = df[(df['category'].isin(prefered)) & (df['government'] == governorate)]
        if len(placed_according_pref) < places_required:
            for prefered_value in data.get('prefered'):
                if prefered_value in categories:
                    categories.remove(prefered_value)
                else:
                    continue
            placed_according_pref = pd.concat(
                (placed_according_pref, df[(df['category'].isin(categories)) & (df['government'] == governorate)]),
                axis=0)

        for elem in np.arange(len(placed_according_pref)):
            distination = (placed_according_pref.iloc[elem]['latitude'], placed_according_pref.iloc[elem]['longitude'])
            distances.append(great_circle(source, distination).kilometers)
            dict_.update({great_circle(source, distination).kilometers: placed_according_pref.iloc[elem][0]})

        distances.sort()
        for distance in distances:
            places.append(dict_.get(distance))
        random.shuffle(places)
        govern = {governorate: places}
        govern_dict = govern.get(governorate)

        for day in range(1, iteration + 1):
            list_of_objects = []
            if len(govern_dict) >= data.get('no_of_places'):
                time1 = 8
                for place in np.arange(1, data.get('no_of_places') + 1):
                    time2 = time1 + clock[np.random.randint(0, 3)]
                    data_govern = govern.get(governorate)
                    place_index_1 = data_govern.pop(0)
                    x1 = {
                        f'place{place}': place_index_1,
                        'longitude': df[df['places'] == place_index_1]['longitude'].iloc[0],
                        'latitude': df[df['places'] == place_index_1]['latitude'].iloc[0],
                        'activity': df[df['places'] == place_index_1]['activity'].iloc[0].replace('\xa0', ''),
                        'category': df[df['places'] == place_index_1]['category'].iloc[0],
                        'image_link': df[df['places'] == place_index_1]["Image's link"].iloc[0],
                        'budget': df[df['places'] == place_index_1]["Price range"].iloc[0],
                        "time": f"{flo_totime(time1)} - {flo_totime(time2)}"
                    }
                    list_of_objects.append(x1)
                    time1 = time2 + 0.5
                list_of_objects.append(adding_fun(time1, governorate))
                objects_of_objects[f"Day{counter}"]={"governorate":governorate,"places":list_of_objects}
                counter += 1

            elif len(govern_dict) < data.get('no_of_places') and len(govern_dict) != 0:
                time1 = 8
                for place in np.arange(1, len(govern_dict) + 1):
                    time2 = time1 + clock[np.random.randint(0, 3)]
                    data_govern = govern.get(governorate)
                    place_index_1 = data_govern.pop(0)
                    x1 = {
                        f'place{place}': place_index_1,
                        'longitude': df[df['places'] == place_index_1]['longitude'].iloc[0],
                        'latitude': df[df['places'] == place_index_1]['latitude'].iloc[0],
                        'activity': df[df['places'] == place_index_1]['activity'].iloc[0].replace('\xa0', ''),
                        'category': df[df['places'] == place_index_1]['category'].iloc[0],
                        'image_link': df[df['places'] == place_index_1]["Image's link"].iloc[0],
                        'budget': df[df['places'] == place_index_1]["Price range"].iloc[0],
                        "time": f"{flo_totime(time1)} - {flo_totime(time2)}"
                    }
                    list_of_objects.append(x1)
                    time1 = time2 + 0.5
                list_of_objects.append(adding_fun(time1, governorate))
                objects_of_objects[f"Day{counter}"]={"governorate":governorate,"places":list_of_objects}
                counter += 1
            else:
                break

    return objects_of_objects
