
import pandas as pd
import pyreadstat
from os.path import dirname, join as pjoin
import scipy.io as sio
from scipy.io import readsav
import numpy as np
from matplotlib import pyplot as plt
import xarray as xr

"""
20230308_0723_to_0901_calibrated_radiancesv1_1.sav   zenith sky views

Calibrated stored file
20230308_0723_to_0901_calibrated_radiancesv1_1.sav   zenith view measurements
************************************************ 1 cycle *********************************************
1 h
1 c
2 z
                         20230308_0723_to_0901_calibrated_radiancesv1_1
COLD_TEMP       FLOAT     = Array[23]               (C)
HOT_TEMP        FLOAT     = Array[23]               (C)    (These temperatures are an average of the front and back PRT100 sensors)
MIRROR_ANGLE    LONG      = Array[40, 2, 22]           (degrees from nadir)
RADIANCE        FLOAT     = Array[40, 2, 22, 12500]    (W m-2 sr-1 (cm-1)-1)
REP_TIMES       LONG      = Array[22]               (seconds from mid-night_
RESPONSE_FUNC   FLOAT     = Array[22, 12500]        (raw voltage (W m-2 sr-1 (cm-1)-1))
SCAN_TIMES      LONG      = Array[40, 2, 22]           (seconds from midnight)
WV              FLOAT     = Array[12500]               (cm-1)

"""

sav_fname = "/disk1/Andoya/jon/calibrated_radiances/20230308/20230308_0723_to_0901_calibrated_radiancesv1_1.sav"
data_sav = readsav(sav_fname, verbose=True)

times = (data_sav['scan_times'])
# seconds from midnightL 8am = 8 * 60 * 60

lucas_type = np.unravel_index((np.abs(times-3600*8)).argmax(), times.shape)

wv = (data_sav['wv'])
rad = (data_sav['radiance'])
# wv_important = print(len((wv.flatten())))
# print(len(wv))
print('wavenumbers here', wv)


plt.figure()
plt.title('Difference plot 20230308_8am_radiance')
# plt.plot(wv, rad[0:12500,21, 1, 39], color='red')
plt.xlabel('Wavenumber(nm)')
plt.ylabel('Radiance(W m-2 sr-1 (cm-1)-1)')
plt.plot(wv[0:12400], rad[0:12400,21, 1, 39])

# plt.savefig('wv_rad_andoyda_0803')

path = "/disk1/sm4219/LBLRTM_FOR_SOPHIE/LBLRTM_SIMGA_BOUNDS_40/"
path2 = "/disk1/sm4219/LBLRTM_FOR_SOPHIE/LBLRTM_SIMGA_BOUNDS_40/"

wn,spectrum = np.loadtxt(path+"example_spectrum_126.txt", unpack = True, dtype=np.float64) #137
wn2,spectrum2 = np.loadtxt(path2+"example_spectrum_23.txt", unpack = True , dtype=np.float64) #40

# wn,spectrum = np.loadtxt(path+'apodised_spectra_126_22.txt', unpack = True, dtype=np.float64)
# wn2,spectrum2 = np.loadtxt(path2+'apodised_spectra_36_og.txt', unpack = True , dtype=np.float64) #37 LAUYERS

# Scale spectra
spectrum_new = spectrum * 10000
spectrum_new2 = spectrum2 * 10000

# fig, (ax1, ax2) = plt.subplots(1, 2, layout='constrained')
# print((spectrum_new[::416])[156])
# sp_n = xr.DataArray([('spec', spectrum_new), ('wavenumber', wn)])

# print(len(wn)) 

# da = xr.DataArray(
#     np.arange(5201871*2).reshape(2, 5201871), 
# [("spec", [spectrum_new.tolist()]), ("wavenumber", [wn.tolist()])])

# da = xr.DataArray(
#     data=[(spectrum_new), (wn)],
#     dims=["spec", "wn"],
#     )

da = xr.DataArray(
    data=spectrum_new,
    dims=["wn"],
    coords=dict(
        wn = np.linspace(300,1600,5201871),
        # chanigng wavenumber ot be more accurate
    ),)

da2 = xr.DataArray(
    data=spectrum_new2,
    dims=["wn_2"],
    coords=dict(
        wn_2 = np.linspace(300,1600,5103797),
        # spec2 = spectrum_new2
    ),)

# interpolating so that wavenumber scales match up
# print(da.interp(wn=wv))
# da2_o = da2.interp(wn_2=wv)
# da2_new = da2_o.interpolate_na(dim="wn_2", method="linear")
# print(da2_o)

# print(wv)
"""
sub = []
for i in range(0,12500):
    diff = rad[i:i+1,21, 1, 39] - (spec[::410])[i]
    sub.append(diff)

sub2 = []
for j in range(0,12400):
    diff2 = rad[j:j+1,21, 1, 39] - (spec_2[::416])[j]
    sub2.append(diff2)

    
sub_dub = []
for kl in range(0,12400):
    diff3 = sub2[kl] - sub[kl]
    sub_dub.append(diff3)


# plt.plot(wv[0:12400], sub[0:12400],label ='andoya-36layers', lw=0.7, color='teal')
# plt.plot(wv[0:12400], sub2[0:12400],label ='andoya-126layers', lw=0.7, color='purple', alpha=0.7)
# plt.plot(wn2, spectrum_new2, label='36 layers', alpha=0.6, lw=0.7)

# plt.plot(wv[0:12400], (sub_dub),label ='(andoya-126layers) - (andoya-36layers)', lw=0.7, color='darkblue')

plt.xlim(400,1500)
plt.ylim(-0.11,0.11)
# ax1.plot(wv, rad[0:12500,0,0,0])
# ax1.set_xlim(400,1500)
# ax1.set_ylim(0,0.12)
# ax1.set_title('Downwelling Spectrum')
# ax1.set_xlabel('Wavenumber / cm-1')
# ax1.set_ylabel('Radiance / [W m-2 sr-1 / cm-1]')
# ax2.plot(dum_new_fre, diff_dum, lw=0.8, color = 'purple', label='36-126')
# ax2.set_title('Difference')
# ax2.set_xlabel('Wavenumber / cm-1')
# ax2.set_ylabel('Radiance / [W m-2 sr-1 / cm-1]')
plt.legend()
# plt.savefig(path+'andoya_vs_lblrtm.png')
# plt.savefig('wv_rad_andoyda_0803')
plt.show()
print('all is dandy')

"""