"""
Downloading data from ERA5  
"""

import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': [
            'high_cloud_cover', 'low_cloud_cover',
            'total_cloud_cover', 'total_column_water_vapour',
        ],
        'year': [ '2019', '2020','2021', '2022'
        ],

        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],

        'day': [
            '01', '02', '03','04',
            '05',
            '07', '09', '10',
            '11','12',
            '13','14', '15','16','17',
            '18','19',
            '21','22',
            '23', '24',
            '25','26', '27','28',
            '29'
        ],

        'time': [
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00'
        ],
        'area': [
            53, -1.4, 52,
            1,
        ],
        'format': 'netcdf',
    },
    'download_new_23_lateryears.nc')
    


    # '2019', '2020',
        #    '2019', '2020',
          