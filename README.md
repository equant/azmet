# AZMet python library

Python library to access azmet data...

https://cals.arizona.edu/azmet/06.htm


## Usage

```

import azmet
azmet_data = azmet.AZMet(start_date="2020-03-13", end_date="2022-03-21")
azmet_data = azmet.AZMet(start_date="2021-12-01", end_date="2022-04-01", station="06")

print(azmet_data.eto_df)
print(azmet_data.hu_df)
print(azmet_data.daily_df)
print(azmet_data.hourly_df)

print(azmet_data.hourly_df.columns)

print(azmet_data.hourly_df.temp)

print(azmet_data.daily_df.loc['2020-03-13'].vpd_mean)

```

## Docs

```
Reference Evapotranspiration  (ETo) 
Units = Inches
DOY = Day Of Year (1 to 365)
CUM = Accumulated Total Since Jan 1, 2020 
* = Missing data. ETo estimated; based on previous day.

eto_columns = [
        'doy',
        'month',
        'day',
        'original_day',     # original azmet
        'original_cum',     # original azmet
        'penmon_day',      # penman monteith
        'penmon_cum',      # penman monteith
        'precip_day',
        'precip_cum',
]

Heat Units
DOY = Day Of Year (1 to 365)
Max = Maximum Air Temperature 
Min = Minimum Air Temperature 
HU  = Daily Heat Units 
CUM = Accumulated Heat Units : Since Jan 1, 2020 
* = Missing data. Max, Min Temps and Heat Units Estimated.

Temperature and Heat Units are in Fahrenheit Units
Heat Units calculated by Single Sine Method

hu_columns_post_2020 = [
        'doy',
        'month',
        'day',
        'max',
        'min',
        '8655_hu',
        '8655_cum',
        '8650_hu',
        '8650_cum',
        '8645_hu',
        '8645_cum',
        '9455_hu',
        '9455_cum',
        'rh_max',
        'rh_min',
        'rh_ave',
]

hu_columns = [
        'doy',
        'month',
        'day',
        'max',
        'min',
        '8655_hu',
        '8655_cum',
        '8650_hu',
        '8650_cum',
        '8645_hu',
        '8645_cum',
        'rh_max',
        'rh_min',
        'rh_ave',
]


raw_daily_columns = [
                         # Comments from AZMET data format definition page...
    'year',              # 1    A   Year
    'doy',               # 2    B   Day of Year (DOY)
    'station',           # 3    C   Station Number
    'temp_max',          # 4    D   Air Temp - Max
    'temp_min',          # 5    E   Air Temp - Min
    'temp_mean',         # 6    F   Air Temp - Mean
    'rh_max',            # 7    G   RH - Max
    'rh_min',            # 8    H   RH - Min
    'rh_mean',           # 9    I   RH - Mean
    'vpd_mean',          # 10   J   VPD - Mean
    'solar_rad',         # 11   K   Solar Rad. - Total
    'precipitation',     # 12   L   Precipitation - Total
    'soil_temp_4_max',   # 13   M    4" Soil Temp - Max  ( = 2" prior to 1999 )
    'soil_temp_4_min',   # 14   N    4" Soil Temp - Min  ( = 2" prior to 1999 )
    'soil_temp_4_mean',  # 15   O    4" Soil Temp - Mean ( = 2" prior to 1999 )
    'soil_temp_20_max',  # 16   P   20" Soil Temp - Max  ( = 4" prior to 1999 )
    'soil_temp_20_min',  # 17   Q   20" Soil Temp - Min  ( = 4" prior to 1999 )
    'soil_temp_20_mean', # 18   R   20" Soil Temp - Mean ( = 4" prior to 1999 )
    'wind_speed_mean',   # 19   S   Wind Speed - Mean
    'wind_vector_mag',   # 20   T   Wind Vector Magnitude for Day
    'wind_vector_dir',   # 21   U   Wind Vector Direction for Day
    'wind_dir_std',      # 22   V   Wind Direction Standard Deviation for Day
    'wind_speed_max',    # 23   W   Max Wind Speed
    '8655_hu',           # 24   X   Heat Units (30/12.8 C) (86/55 F)
    'ref_eto_original',  # 25   Y   Reference Evapotranspiration (ETo) = Original AZMET
    'ref_eto_penmon',    # 26   Z   Reference Evapotranspiration (ETos) = Penman-Monteith
    'vapor_pressure',    # 27  AA   Actual Vapor Pressure - Daily Mean
    'dewpoint',          # 28  AB   Dewpoint, Daily Mean
]

raw_hourly_columns = [

    "year",                   # 1    A   Year
    "doy",                    # 2    B   Day of Year (DOY)
    "hour",                   # 3    C   Hour of Day
    "temp",                   # 4    D   Air Temperature
    "rh",                     # 5    E   Rel. Humidity
    "vapor_pressure_deficit", # 6    F   Vapor Pressure Deficit
    "solar_rad",              # 7    G   Solar Radiation
    "precipitation",          # 8    H   Precipitation
    "soil_temp_4",            # 9    I    4" Soil Temperature  ( = 2" prior to 1999 )
    "soil_temp_20",           # 10   J   20" Soil Temperature  ( = 4" prior to 1999 )
    "wind_speed_mean",        # 11   K   Wind Speed (Ave)
    "wind_vector_mag",        # 12   L   Wind Vector Magnitude
    "wind_vector_dir",        # 13   M   Wind Vector Direction
    "wind_dir_std",           # 14   N   Wind Direction Standard Deviation
    "wind_speed_max",         # 15   O   Max Wind Speed
    "ref_eto_original",       # 16   P   Reference Evapotranspiration (ETo) - Original AZMET
    "vapor_pressure",         # 17   Q   Actual Vapor Pressure       'New' : 2003 to Present
    "dewpoint",               # 18   R   Dewpoint, Hourly Average    'New' : 2003 to Present

]

```

