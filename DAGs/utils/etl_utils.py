import os
import pandas as pd

def create_filepath(kwargs, table_name, stage):
    time_partition = kwargs.get('execution_date').strftime("%Y/%m/%d/%H")
    filename = kwargs.get('execution_date').strftime("%Y-%m-%d_%H:%M:%S")
    path = f"/tmp/{stage}/{table_name}/{time_partition}/{filename}.csv"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def transform_appointments(app_path):
    app_cols = ['appointment_id', 'last_updated', 'appointment_date', "appointment_status", "patient_id", "staff_id", "notes"]

    app_df = pd.read_csv(app_path, names=app_cols)

    app_df['appointment_status'] = app_df['appointment_status'].fillna('upcoming')
    app_df.loc[app_df['appointment_status'].isin(['pending', 'booked', 'scheduled']), 'appointment_status'] = 'upcoming'

    return app_df

def transform_patients(pat_path):
    pat_cols = ['last_updated', 'first_name', 'last_name', 'date_of_birth', 'sex', 'height', 'weight', 'phone_number', 'address']

    pat_df = pd.read_csv(pat_path, names=pat_cols)

    sex_map = {'male': 'm', 'female': 'f'}

    pat_df['sex'] = pat_df['sex'].replace(sex_map)

    pat_df['weight_kg'] = pat_df['weight'].apply(lambda x: lbs_to_kg(x) if 'lbs' in x else int(x[:-2]))

    pat_df['height_cm'] = pat_df['height'].apply(lambda x: ft_to_cm(x) if '\'' in x else int(x[:-2]))
 
    pat_df['bmi'] = pat_df['weight_kg'] / (pat_df['height_cm'] / 100) ** 2

    pat_df.drop(inplace=True, columns=['height', 'weight'])

    return pat_df

def lbs_to_kg(lbs):
    return int(int(lbs[:-3]) * 0.45359237)

def ft_to_cm(ft):
    ft_to_inches = int(ft[0]) * 12
    inches = int(ft.split("'")[1][:-1])
    return int((ft_to_inches + inches) * 2.54)

