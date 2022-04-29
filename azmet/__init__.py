import os.path
import pdb
import urllib.request
import numpy as np
import pandas as pd
from datetime import date

#azmet_data_dir = os.path.join(raw_data_dir, "azmet")
azmet_data_dir = "azmet_cache"

#import phytooracle_data.seasons as seasons

from scipy.interpolate import CubicSpline

def interpolate(df_column, dt_to_interpolate, How=CubicSpline):
    """
    datetime_to_interpolate should be a string like this...
        "2020-03-13 13:33:00"
    ... or a Timestamp like this...
        Timestamp('2020-03-13 13:33:00')
    ... or a numpy.datetime64

    # Single datetime as string...
    azmet.interpolate(azmet_data.hourly_df.temp, "2020-03-13 00:33:00")

    list_of_times_as_string = ["2020-03-13 02:33:00", "2020-03-13 02:44:00"]
    azmet.interpolate(azmet_data.hourly_df.temp, list_of_times_as_string)

    # A column of dates from a df...
    azmet.interpolate(azmet_data.hourly_df.temp, azmet_data.hourly_df.index)
    # The results of the above should be the same as azmet_data.hourly_df.temp
    # since it's not really doing any interpolation, but it's a useful
    # test and sanity check.

    """

    terp = How(df_column.index, df_column)

    # Is it a single date?
    if type(dt_to_interpolate) is str:
        dt_to_interpolate = pd.Timestamp(dt_to_interpolate)
    if type(dt_to_interpolate) is list:
        if type(dt_to_interpolate[0]) is str:
            dt_to_interpolate = pd.Series([pd.Timestamp(x) for x in dt_to_interpolate])
    # Is it one or more pandas Timestamps (i.e. a column from a dataframe)
    #if type(dt_to_interpolate) is pd._libs.tslibs.timestamps.Timestamp:
    dt_to_interpolate = dt_to_interpolate.to_numpy()

    return terp(dt_to_interpolate)


class AZMet(object):
    """
    https://cals.arizona.edu/azmet/06.htm
    
    import azmet
    azmet_data = azmet.AZMet(start_date="2020-03-13", end_date="2022-03-21")

    print(azmet_data.eto_df)
    print(azmet_data.hu_df)
    print(azmet_data.daily_df)
    print(azmet_data.hourly_df)

    print(azmet_data.hourly_df.columns)

    print(azmet_data.hourly_df.temp)

    # https://stackoverflow.com/questions/27926669/how-do-you-interpolate-from-an-array-containing-datetime-objects
    from scipy.interpolate import CubicSpline
    cs = CubicSpline(azmet_data.hourly_df.index, azmet_data.hourly_df.temp.values)
    azmet_data.hourly_df.loc[pd.to_datetime("2022-03-21 23:01:00")] = None
    """


    """
    Reference Evapotranspiration  (ETo) 
    Units = Inches
    DOY = Day Of Year (1 to 365)
    CUM = Accumulated Total Since Jan 1, 2020 
    * = Missing data. ETo estimated; based on previous day.
    """

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

    """
    Heat Units
    DOY = Day Of Year (1 to 365)
    Max = Maximum Air Temperature 
    Min = Minimum Air Temperature 
    HU  = Daily Heat Units 
    CUM = Accumulated Heat Units : Since Jan 1, 2020 
    * = Missing data. Max, Min Temps and Heat Units Estimated.

    Temperature and Heat Units are in Fahrenheit Units
    Heat Units calculated by Single Sine Method
    """
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

    def __init__(self, start_date=None, end_date=None, station="06"):
        """
        station 06 -> Maricopa https://cals.arizona.edu/azmet/06.htm
        """
        self.station = station

        self.start_date = date.fromisoformat(start_date)
        self.end_date   = date.fromisoformat(end_date)

        # Since we may have to build dataframes from one or more CSVs (e.g.
        # seasons that span multiple years), we read the csv files into dfs
        # and store them as a list.  Then later we concatenate the dfs
        # together.

        azmet_report_keys = [
            "rd",  # Raw Data Daily
            "rh",  # Raw Data Hourly
            "hu",  # Heat Units
            "et",  # ETo
            #"ch", # Chill hours span two dates, so will require
        ]

        temp_df_lists = {}
        for key in azmet_report_keys:
            temp_df_lists[key] = []


        # Let's loop through each year.  DL data if needed, and read csv files into
        # pandas dataframes

        #for y in self.season.years():
        for y in range(self.start_date.year, self.end_date.year+1):
            #ystr = str(y)[:-2]
            ystr = str(y)[2:]          # last two digits of year.
            # Build a dictionary of filenames we need for this station/year combination
            azmet_filenames = {}
            for key in azmet_report_keys:
                azmet_filenames[key] = f"{station}{ystr}{key}.txt"

            # Let's see if we have downloaded the needed azmet data It's stored
            # by year, so we loop through the needed years for this season and
            # see if we have it locally.  If not, we DL it.  Then, we read it
            # into a df and add it to our temp_df_lists

            for key, filename in azmet_filenames.items():
                filepath = os.path.join(azmet_data_dir, filename)
                if not os.path.isfile(filepath):
                    print(f"Downloading azmet data to {filepath}")
                    os.makedirs(azmet_data_dir, exist_ok=True)
                    urllib.request.urlretrieve(f'https://cals.arizona.edu/azmet/data/{filename}', filepath)
                # Reference Evapotranspiration  (ETo) 
                if key == "et":
                    print(f"reading: {filepath}")
                    _df = pd.read_fwf(filepath, names=self.eto_columns, skiprows=17, skipfooter=7)
                    _df['date'] = pd.to_datetime([f"{y} {x.doy}" for i,x in _df.iterrows()], format='%Y %j')
                    temp_df_lists[key].append(_df[_df['date'].dt.date.between(self.start_date, self.end_date)])
                # Heat Units 
                elif key == "hu":
                    print(f"reading: {filepath}")
                    _df = pd.read_fwf(filepath, names=self.hu_columns, skiprows=18, skipfooter=6)
                    if type(_df.index) is pd.core.indexes.multi.MultiIndex:
                        _df = pd.read_csv(filepath, names=self.hu_columns_post_2020, skiprows=18, skipfooter=6, delim_whitespace=True)[self.hu_columns] # lets ignore new column for now.
                    _df['date'] = pd.to_datetime([f"{y} {x.doy}" for i,x in _df.iterrows()], format='%Y %j')
                    #temp_df_lists[key].append(_df)
                    temp_df_lists[key].append(_df[_df['date'].dt.date.between(self.start_date, self.end_date)])
                elif key == "rd":
                    print(f"reading: {filepath}")
                    _df = pd.read_csv(filepath, names=self.raw_daily_columns)
                    _df['date'] = pd.to_datetime([f"{int(x.year)} {int(x.doy)}" for i,x in _df.iterrows()], format='%Y %j')
                    #temp_df_lists[key].append(_df)
                    temp_df_lists[key].append(_df[_df['date'].dt.date.between(self.start_date, self.end_date)])
                elif key == "rh":
                    print(f"reading: {filepath}")
                    _df = pd.read_csv(filepath, names=self.raw_hourly_columns)
                    _df['date'] = pd.to_datetime([f"{int(x.year)} {int(x.doy)} {int(x.hour)-1}" for i,x in _df.iterrows()], format='%Y %j %H')
                    #temp_df_lists[key].append(_df)
                    temp_df_lists[key].append(_df[_df['date'].dt.date.between(self.start_date, self.end_date)])


        self.eto_df = pd.concat(temp_df_lists['et'], axis=0, ignore_index=True).set_index('date')
        self.hu_df = pd.concat(temp_df_lists['hu'], axis=0, ignore_index=True).set_index('date')
        self.daily_df = pd.concat(temp_df_lists['rd'], axis=0, ignore_index=True).set_index('date')
        self.hourly_df = pd.concat(temp_df_lists['rh'], axis=0, ignore_index=True).set_index('date')

        # Useful debugging things...
        #self.temp_df_lists = temp_df_lists          # Useful for debugging.

