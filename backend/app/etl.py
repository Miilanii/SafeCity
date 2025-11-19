import pandas as pd
from db import engine
from sqlalchemy import text
import argparse
def load_csv(path):
    return pd.read_csv(path, parse_dates=['incident_date'])
def insert_raw(df):
    insert_sql = text('''INSERT INTO incidents_raw(incident_date, incident_time, latitude, longitude, province, district, crime_category, victim_gender, victim_age, reported_to_police)
    VALUES(:incident_date, :incident_time, :latitude, :longitude, :province, :district, :crime_category, :victim_gender, :victim_age, :reported_to_police)''')
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(insert_sql, {
                'incident_date': row['incident_date'].date() if not pd.isna(row['incident_date']) else None,
                'incident_time': row.get('incident_time'),
                'latitude': float(row.get('latitude')) if not pd.isna(row.get('latitude')) else None,
                'longitude': float(row.get('longitude')) if not pd.isna(row.get('longitude')) else None,
                'province': row.get('province'),
                'district': row.get('district'),
                'crime_category': row.get('crime_category'),
                'victim_gender': row.get('victim_gender'),
                'victim_age': int(row['victim_age']) if not pd.isna(row.get('victim_age')) else None,
                'reported_to_police': bool(row.get('reported_to_police'))
            })
def build_daily_hotspots():
    agg_sql = text('''INSERT INTO daily_hotspots (agg_date, district, lat, lon, incident_count, rolling_7d_avg, alert)
    SELECT incident_date::date as agg_date, district,
      AVG(latitude) as lat, AVG(longitude) as lon, COUNT(*) as incident_count,
      0.0 as rolling_7d_avg, false as alert
    FROM incidents_raw
    GROUP BY 1,2
    ON CONFLICT (agg_date, district) DO UPDATE
      SET incident_count = EXCLUDED.incident_count, lat = EXCLUDED.lat, lon = EXCLUDED.lon, rolling_7d_avg = EXCLUDED.rolling_7d_avg, alert = EXCLUDED.alert
    ''')
    with engine.begin() as conn:
        conn.execute(agg_sql)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', required=True)
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    df = load_csv(args.csv)
    if args.commit:
        insert_raw(df)
        build_daily_hotspots()
        print('ETL committed')
    else:
        print('Dry run rows:', len(df))
