#importing packagess
import xarray
import numpy  as np
import scipy
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from netCDF4 import Dataset
from matplotlib.dates import DateFormatter

# importing data set
ds_all = xarray.load_dataset('download.nc', engine="netcdf4")

updated_ds = ds_all.sel(latitude = 51.145 , longitude = -1.44, method = 'nearest')
total_clouds = (updated_ds.variables['tcc'])
total_column_w = (updated_ds.variables['tcwv'])
low_clouds = (updated_ds.variables['lcc'])
high_clouds = (updated_ds.variables['hcc'])
timew = (updated_ds.variables['time'])

# print(total_clouds)
# fig, ax1 = plt.subplots(figsize=(12, 8))
# # bins = np.arange(1,10,1)
# ax2 = ax1.twinx()
# ax1.set_title('Rain 2022')
# ax1.set_ylabel('cloud cover')
# ax2.set_ylabel('total column water vapour')
# ax.set_ylabel('Total precipitation (m)/ Total column rw (kg/m2)')
# ax1.plot(timew, total_clouds, 'x', color='teal', label='cloud cover', )
# ax2.plot(timew, total_column_w,'o', color='salmon', label='total column wv',)

total_column_w2 = np.array(total_column_w)
total_clouds2 = np.array(total_clouds)
timew2 = np.array(timew)
low_clouds2 = np.array(low_clouds)
high_clouds2 = np.array(high_clouds)

# mean

n_a = 12

mean_cloud = np.mean(total_clouds2.reshape(-1,n_a), axis =1)
mean_wv = np.mean(total_column_w2.reshape(-1,n_a), axis =1)
mean_low = np.mean(low_clouds2.reshape(-1,n_a), axis =1)
mean_high = np.mean(high_clouds2.reshape(-1,n_a), axis =1)

# mean_time = np.mean(timew2.reshape(-1,n_a), axis =1)

# time_array = xarray.IndexVariable((np.array(timew)))

# months = timew2.to_series().dt.month
# months = np.datetime_as_string(timew2, unit='M').astype('int')]
months = []

for i in range(len(timew2)):
    months.append(int(np.datetime_as_string(timew2[i], unit='M').split('-')[1]))

years = []
for j in range(len(timew2)):
    years.append(int(np.datetime_as_string(timew2[j], unit='Y').split('-')[0]))

fig4, ax4 = plt.subplots(figsize=(12, 8))

ax4.set_title('2012 to 2012')
ax4.set_ylabel('cloud cover')
ax4.set_xlabel('tcwv')
# hist = ax4.hist2d(mean_wv, mean_cloud)
# fig4.colorbar(hist[3], ax=ax4)
# plt.scatter(total_column_w, total_clouds, c=months, cmap='viridis')


# # Create xarray Dataset
ds = xarray.Dataset({
    'total_column_w': ('time', total_column_w),
    'high_cloud': ('time', high_clouds),
    # 'total_clouds': ('time', total_clouds),
    'years': ('time', years),
    'months': ('time', months)
}, coords={'time': timew2})

ds2 = xarray.Dataset({
    'total_column_w': ('time', total_column_w),
    'low_cloud': ('time', low_clouds),
    # 'total_clouds': ('time', total_clouds),
    'years': ('time', years),
    'months': ('time', months)
}, coords={'time': timew2})

# Combine years and months into a single variable for grouping
ds2['year_month'] = ds2['years'] * 100 + ds2['months']
ds['year_month'] = ds['years'] * 100 + ds['months']

# Group by year_month and calculate the mean
grouped_data2 = ds2.groupby('year_month').mean(dim='time')
grouped_data = ds.groupby('year_month').mean(dim='time')

# Create a scatter plot with color based on months
plt.scatter(grouped_data['total_column_w'], grouped_data['high_cloud'], c=grouped_data['months'], 
            cmap='spring',
            alpha=0.7,
            s = 150)
plt.colorbar(label='Month')

plt.scatter(grouped_data2['total_column_w'], grouped_data2['low_cloud'], c=grouped_data2['months'], 
            cmap='winter',
            alpha=0.7,
            s = 150)

# print(len(grouped_data['total_column_w']))
plt.colorbar(label='Month')
# plt.ylim(0.35,0.6)
plt.xlim(9.0,15.5)

# ax4.bar(new_time, mean_low,color='teal', label='low cloud cover', width=1.0)
# ax4.bar(new_time, mean_high, color='salmon', label='high cloud cover', width=1.0 
# plt.legend()
# ax4.legend(loc='upper left')

# date_form = DateFormatter("%d-%m-%y")
# ax4.xaxis.set_major_formatter(date_form)
# ax4.xaxis.set_major_locator(mdates.WeekdayLocator(interval=50))
# plt.xlabel('Day-Month-Year')



plt.savefig('high_clouds_allyears.png')

print('booya')
# hea