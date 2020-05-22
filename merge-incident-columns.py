import pandas as pd

filepath = 'scrubber/data_scrubbed.csv'
df = pd.read_csv(filepath)
pd.set_option('display.max_columns', None)
# create new column and add to end of DataFrame
df['INCIDENT_TYPE'] = df['INCIDENT_1_OLD'].fillna(
    '') + df['INCIDENT_TYPE_1'].fillna('')
# preprocess, replace nan with empty string
df['INCIDENT_TYPE_2'] = df['INCIDENT_TYPE_2'].fillna('')
# for "Other" 2nd types, set to description instead of "Other"
df['INCIDENT_TYPE_2ND'] = df.apply(
    lambda r: (r['INCIDENT_TYPE_OTHER'] if r['INCIDENT_TYPE_2'].lower() == 'other'
                else r['INCIDENT_TYPE_2']),
    axis=1)

# make blank if matching first incident type
df['INCIDENT_TYPE_2ND'] = df.apply(
    lambda r: (r['INCIDENT_TYPE_2ND'] if r['INCIDENT_TYPE'] != r['INCIDENT_TYPE_2ND'] else ''),
    axis=1)

# remove old columns, add new ones
df = df[[col for col in df if col not in ['INCIDENT_TYPE_1',
                                          'INCIDENT_TYPE_2', 'INCIDENT_1_OLD', 'INCIDENT_TYPE_OTHER']]]

df.to_csv('merged-data/merged_data.csv')
