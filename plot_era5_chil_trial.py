#importing packagess
import xarray
import numpy  as np
import scipy
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from netCDF4 import Dataset
from matplotlib.dates import DateFormatter
import matplotlib as mpl
from datetime import datetime
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap


# importing data set
ds_1part = xarray.load_dataset('/home/sm4219/download_new_23_lateryears.nc', engine="netcdf4")

ds_2part = xarray.load_dataset('/home/sm4219/download_new_23.nc', engine="netcdf4")

updated_ds_1 = ds_1part.sel(latitude = 51.145 , longitude = -1.44, method = 'nearest')
updated_ds_2 = ds_2part.sel(latitude = 51.145 , longitude = -1.44, method = 'nearest')

ds_grid = [updated_ds_1 ,updated_ds_2]
updated_ds = xarray.combine_by_coords(ds_grid, combine_attrs='override')

print(updated_ds['time'])

# total_clouds = (updated_ds.variables['tcc'])
total_column_w = (updated_ds.variables['tcwv'])
low_clouds = (updated_ds.variables['lcc'])
high_clouds = (updated_ds.variables['hcc'])
timew = (updated_ds.variables['time'])
# raise Exception('HOLD YOUR HORSES')
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
# total_clouds2 = np.array(total_clouds)

timew2 = np.array(timew)
low_clouds2 = np.array(low_clouds)
high_clouds2 = np.array(high_clouds)

months = []

for i in range(len(timew2)):
    months.append(int(np.datetime_as_string(timew2[i], unit='M').split('-')[1]))

years = []
for j in range(len(timew2)):
    years.append(int(np.datetime_as_string(timew2[j], unit='Y').split('-')[0]))

# ax4.set_title('2012 to 2012')
# ax4.set_ylabel('cloud cover')
# ax4.set_xlabel('tcwv')

# # Create xarray Dataset
ds = xarray.Dataset({
    'total_column_w': ('time', total_column_w),
    'high_cloud': ('time', high_clouds),
    # 'total_clouds': ('time', total_clouds),
    'low_cloud': ('time', low_clouds),
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

# cmap = plt.get_cmap('Paired', 12)
# cmap.set_under('gray')

"12 SUBPLOT START HERE"

# Create 12 subplots
fig, axs = plt.subplots(3, 4, figsize=(22, 18), sharex=True, sharey=True)

# Flatten the 2D array of subplots to make indexing easier
axs = axs.flatten()

# Define a list of distinct colors
distinct_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                   '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                   '#ff0000', '#00ff00']  # Add or modify colors as needed

# Create a custom ListedColormap with the distinct colors
color_map = ListedColormap(distinct_colors)

# Corrected list with distinct colors
distinct_colors = ['#ff0000', '#ff9900', '#ffff00', '#00ff00', '#00ccff',
                   '#3300cc', '#9900ff', '#ff00cc', '#006400', '#ff6699',
                   '#666666', '#996633']  # Dark green: '#006400', Light pink: '#ffc0cb'


# Create a custom ListedColormap with the different distinct colors
color_map2  = ListedColormap(distinct_colors )

# Create year_month variable in the original dataset
ds['year_month'] = ds['years'] * 100 + ds['months']

print(ds['years'].values)

# Iterate over each month
months_range = range(1, 13)

for i, month in enumerate(months_range):
    # Select data for the current month
    # monthly_data = ds.where(ds['months'] == month, drop=True)3
    # print(i, monthly_data)
    # Group by year_month and calculate the mean
    # grouped_data2 = ds.groupby('year_month').mean(dim='time')

    # Select data for the current month
    monthly_data = ds.where(ds['months'] == month, drop=True)

    grouped_data = monthly_data.groupby('year_month').mean(dim='time')


    # Normalize 'months' values to be between 0 and 1
    normalized_months = (grouped_data['months'] - grouped_data['months'].min()) / (grouped_data['months'].max() - grouped_data['months'].min())


    # Filter data based on conditions
    grouped_data = grouped_data.where((grouped_data['low_cloud'] < 0.4) & (grouped_data['total_column_w'] < 20))

    # Scatter plot, c=color_map(i/12))
    axs[i].scatter(grouped_data['total_column_w'], grouped_data['high_cloud'], s=220, c=distinct_colors[i], alpha=0.8 )
    axs[i].scatter(grouped_data['total_column_w'], grouped_data['low_cloud'], s=220, marker='^', c=distinct_colors[i], alpha=0.8)

    # Set subplot title with month names
    month_name = datetime.strptime(str(month), "%m").strftime("%b")
    axs[i].set_title(month_name, fontsize=26)

     # Increase the size of axis labels and tick labels
    axs[i].tick_params(axis='both', which='both', labelsize=16)

    
    
# Set common labels and title
fig.suptitle('Total Column Water vs Total Clouds for Each Month')
fig.text(0.5, 0.04, 'Total Column Water', ha='center', va='center')
fig.text(0.07, 0.5, 'Total Clouds', ha='center', va='center', rotation='vertical')


# Create custom legend with markers
legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map(0), markersize=10, label='High Clouds'),
                    Line2D([0], [0], marker='^', color='w', markerfacecolor=color_map2(0), markersize=10, label='Low Clouds')]

# Add the custom legend to the figure
fig.legend(handles=legend_elements, loc='upper right', title='Cloud Types')

# Create a colorbar axis on the right side of the figure
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  # Adjust position and size as needed

# Add a colorbar
cbar = fig.colorbar(axs[0].scatter([], [], c=[], cmap=color_map2, vmin=1, vmax=12), cax=cbar_ax, label='Month')

# Create a colorbar axis on the right side of the figure
# cbar_ax2 = fig.add_axes([0.96, 0.15, 0.02, 0.7])  # Adjust position and size as needed

# Add a colorbar
# cbar2 = fig.colorbar(axs[0].scatter([], [], c=[], cmap=color_map, vmin=1, vmax=12), cax=cbar_ax2, label='Month')


# Customize colorbar ticks and tick labels to represent months
cbar.set_ticks(months_range)
cbar.set_ticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.savefig('/home/sm4219/twelveplots_newjan.png')

# Adjust layout
# plt.tight_layout(rect=[0, 0.03, 1, 0.95])

"END HERE"
# create a second axes for the colorbar
# Create a scatter plot with color based on months
# plt.scatter(grouped_data['total_column_w'], grouped_data['high_cloud'], c=grouped_data['months'], 
#             cmap='spring',
#             alpha=0.7,
#             s = 150)
# plt.colorbar(label='Month')

# plt.scatter(grouped_data['total_column_w'], grouped_data['total_clouds'], c=grouped_data['months'], 
#             alpha=0.7,
#             s = 300,
#             cmap=cmap)

# hist = ax4.hist2d(mean_wv, mean_cloud)
# fig4.colorbar(hist[3], ax=ax4)
# print(len(grouped_data['total_column_w']))
# plt.colorbar(label='Month')
# # plt.grid()
# plt.ylim(0.35,0.6)
# plt.xlim(9.0,16.0)

# ax4.bar(new_time, mean_low,color='teal', label='low cloud cover', width=1.0)
# ax4.bar(new_time, mean_high, color='salmon', label='high cloud cover', width=1.0 
# plt.legend()
# ax4.legend(loc='upper left')

# date_form = DateFormatter("%d-%m-%y")
# ax4.xaxis.set_major_formatter(date_form)
# ax4.xaxis.set_major_locator(mdates.WeekdayLocator(interval=50))
# plt.xlabel('Day-Month-Year')


print('booya')
# hea

"""

# Iterate over each month
for i, month in enumerate(range(1, 13)):
    # Select data for the current month
    monthly_data = ds.where(ds['months'] == month, drop=True)
    
    # Group by year_month and calculate the mean
    grouped_data = monthly_data.groupby('year_month').mean(dim='time')
    

    # Scatter plot
    axs[i].scatter(grouped_data['total_column_w'], grouped_data['high_cloud'], s=50, c=color_map(i/12))
    axs[i].scatter(grouped_data['total_column_w'], grouped_data['low_cloud'], s=50, marker='^', c=color_map2(i/12))
    # Set subplot title with month names
    month_name = datetime.strptime(str(month), "%m").strftime("%b")
    axs[i].set_title(month_name)

"""