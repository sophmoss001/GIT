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
ds_all = xarray.load_dataset('download_chilbolt.nc', engine="netcdf4")

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

n_a = 5

mean_cloud = np.mean(total_clouds2.reshape(-1,n_a), axis =1)
mean_wv = np.mean(total_column_w2.reshape(-1,n_a), axis =1)
mean_low = np.mean(low_clouds2.reshape(-1,n_a), axis =1)
mean_high = np.mean(high_clouds2.reshape(-1,n_a), axis =1)

# mean_time = np.mean(timew2.reshape(-1,n_a), axis =1)

fig4, ax4 = plt.subplots(figsize=(12, 8))

ax4.set_title('Rain 2022')
ax4.set_ylabel('cloud cover')

print(len(timew)/n_a)
new_time=timew[::n_a]

ax4.bar(new_time, mean_low,color='teal', label='low cloud cover', width=1.0)
ax4.bar(new_time, mean_high, color='salmon', label='high cloud cover', width=1.0 )

plt.legend()
ax4.legend(loc='upper left')
date_form = DateFormatter("%m-%d")
ax4.xaxis.set_major_formatter(date_form)
ax4.xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))
plt.savefig('high_low_chil_clouds_NEW.png')

print('booya')
# hea