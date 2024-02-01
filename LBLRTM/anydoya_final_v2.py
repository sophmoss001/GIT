
import pandas as pd
import pyreadstat
from os.path import dirname, join as pjoin
import scipy.io as sio
from scipy.io import readsav
import numpy as np
from matplotlib import pyplot as plt
import xarray as xr
import tkinter

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
# Andoya file
# sav_fname = "/disk1/Andoya/jon/calibrated_radiances/20230308/20230308_0723_to_0901_calibrated_radiancesv1_1.sav"

# File from Jon's publication
sav_fname = "/users/jon/data_sets_for_pub_20220323.sav"
data_sav = readsav(sav_fname, verbose=True)
print('data sav worked')
# times = (data_sav['scan_times'])
# lucas_type = np.unravel_index((np.abs(times-3600*8)).argmax(), times.shape)

wv = (data_sav['wv'])
rad = (data_sav['zen'])
# rad = (data_sav['radiance'])

path = "/disk1/sm4219/LBLRTM_FOR_SOPHIE/LBLRTM_SIMGA_BOUNDS_40/"
path2 = "/disk1/sm4219/LBLRTM_FOR_SOPHIE/LBLRTM_SIMGA_BOUNDS_40/"

wn,spectrum = np.loadtxt(path+"apodised_spectra_126_22.txt", unpack = True, dtype=np.float64) #137
wn2,spectrum2 = np.loadtxt(path2+"apodised_spectra_36_01_12.txt", unpack = True , dtype=np.float64) #40

print('found both spectra')
# wn,spectrum = np.loadtxt(path+'apodised_spectra_126_22.txt', unpack = True, dtype=np.float64)
# wn2,spectrum2 = np.loadtxt(path2+'apodised_spectra_36_og.txt', unpack = True , dtype=np.float64) #37 LAUYERS

# Scale spectra
spectrum_new = spectrum * 10000
spectrum_new2 = spectrum2 * 10000
"""
da = xr.DataArray(
    data=spectrum_new,
    dims=["wn"],
    coords=dict(
        wn = np.linspace(300,1600,5201870),
        # chanigng wavenumber ot be more accurate
    ),)

da2 = xr.DataArray(
    data=spectrum_new2,
    dims=["wn_2"],
    coords=dict(
        wn_2 = np.linspace(300,1600,5103796),
    ),)

# interpolating so that wavenumber scales match up
# da_new = (da.interp(wn=wv, method="linear", kwargs={"fill_value": "extrapolate"}))
# da_new2 = (da2.interp(wn_2=wv, method="linear", kwargs={"fill_value": "extrapolate"}))

# spec = da_new.data
# spec2 = da_new2.data
# print(len(spec2), da_new2)

# subtraction
sub = []
for i in range(0,12500):
    diff = rad[i:i+1,21, 1, 39] - spec[i]
    sub.append(diff)

sub2 = []
for j in range(0,12500):
    diff2 = rad[j:j+1,21, 1, 39] - spec2[j]
    sub2.append(diff2)
"""

# subtraction plots
# plt.plot(wv, sub,label ='andoya-36layers', lw=0.5, color='red')
# plt.plot(wv, sub2,label ='andoya-126layers', lw=0.5, color='green', alpha=0.8)
# plt.axhline(y=0, linestyle='--', color='black')

# usual plots
# plt.plot(wn2, spectrum_new2, label='36 layers', alpha=0.6, lw=0.7, color='darkblue' )
# plt.plot(wn, spectrum_new, label='126 layers', alpha=0.6, lw=0.7, color='darkgreen')
# plt.plot(wv,rad[0:12500,21, 1, 39], label='data pub', alpha=0.6, lw=0.7, color='red')

# Download Jons data SIMULATION HIS TAPE 5 MY APODISATION
path3 = "/disk1/sm4219/LBLRTM_FOR_SOPHIE/LBLRTM_SIMGA_BOUNDS_40/"
wn3,spectrum3 = np.loadtxt(path2+"apodised_spectra_NEW_SOPH.txt", unpack = True , dtype=np.float64) #jons file
spectrum_new3 = spectrum3 * 10000

# wn3,spectrum3 = np.loadtxt(path2+"apodised_spectra_NEW_old.txt.txt", unpack = True , dtype=np.float64) #jons file
# np.savetxt(path+'/apodised_spectra_NEW_NEW.txt',np.vstack([apodised_wn, apodised_spectrum]).T)
#np.savetxt(path+'/apodised_spectra_NEW_old.txt',np.vstack([wn,apodised_interp]).T)

# TRYING WITH JONS OWN APODISATION
# File from Jon's publication
sav_fname = "/disk1/sm4219/GIT/LBLRTM/example_spe.sav"
data_sav_jon = readsav(sav_fname, verbose=True)
# print('data sav 2 worked')
# times = (data_sav['scan_times'])
# lucas_type = np.unravel_index((np.abs(times-3600*8)).argmax(), times.shape)
wv_jon = (data_sav_jon['conv_wv'])
rad_jon = (data_sav_jon['con_spe'])
spe_jon = (data_sav_jon['spe'])
# print(spe_jon)

# da3 is the rad which is from dataset pub observationse
da3 = xr.DataArray(
    data=rad[0:12500,31],
    dims=["wv3"],
    coords=dict(
        wv3 = np.concatenate(wv, axis=0)
        # chanigng wavenumber ot be more accurate
    ),)


# apply this to obseravations stretch
stretch_factor = 1.00016
wn_stretch = (da3.wv3.values)*stretch_factor
stretched_obvs = da3.interp(wv3=wn_stretch)

# print(stretched_obvs)

da4 = xr.DataArray(
    data=spectrum_new3,
    dims=["wv4"],
    coords=dict(
	wv4 = np.linspace(300,2000,8499),
        # chanigng wavenumber ot be more accurate
    ))

wn_refined = np.linspace(400,1600,120000)
# wn_refined = np.linspace(400,2000,120000)

da_new4 = (da4.interp(wv4=wn_refined))
da_new5 = (da_new4.interp(wv4=wn_stretch))
spec4 = da_new5.data


plt.figure()
# plt.plot(wn_stretch, ((stretched_obvs*10000)/10), label='rad from datasetforpub', alpha=0.9, lw=0.6, color='red')
# plt.plot(wn_stretch, (spec4/10), label='spec thru soph layers', alpha=0.6, lw=0.7, color='green')
# plt.plot(wv_jon, (rad_jon)*1000, label='Jons layers 11', alpha=0.6, lw=0.7, color='blue')

da6 = xr.DataArray(
    data=rad_jon,
    dims=["wv6"],
    coords=dict(
	wv6 = np.linspace(300,2000,8500),
        # chanigng wavenumber ot be more accurate
    ))

da_new6 = (da6.interp(wv6=wn_refined))
da_new7 = (da_new6.interp(wv6=wn_stretch))
spec6 = da_new7.data

print(len(spec4))

# plt.plot(wn_stretch, (spec6)*1000, label='jon rad my strecth ', alpha=0.6, lw=0.7, color='darkblue')

# plt.plot(wn_stretch, (stretched_obvs*10000)/10, label='rad from datasetforpub', alpha=0.9, lw=0.6, color='red')
# plt.plot(wn_stretch, (spec4)/10, label='soph layers', alpha=0.6, lw=0.9, color='green')

# plt.plot(wn_stretch , spec4*1000, label='apodised spec', alpha=0.9, lw=0.6, color='teal')
# plt.plot(wn_stretch, stretched_obvs*1000, label='rad from datasetforpub', alpha=0.9, lw=0.6, color='red')

# plt.plot(wv_jon, (rad_jon)*10000, label='Jons layers 11', alpha=0.6, lw=0.7, color='blue')
# plt.plot(wv[0:12500,0], rad[0:12500,31], label='rad from datasetforpub', alpha=0.6, lw=0.7, color='red')
# plt.plot(wn3, spectrum_new3, label='raw sophiejon', alpha=0.6, lw=0.7, color='green')
# plt.plot(wv_jon, spe_jon*10000, color='red', lw=0.5, alpha=0.6)

plt.xlim(400,1600)
plt.ylim(-8,8)


stretch_new = stretched_obvs[2000:10500]
print(stretch_new)

print(len(wn_stretch))
print(wn_stretch[2000:])
# DIFFERENCE CALCULATIONS AND PLOTS
sub3 = ((stretch_new*10000)/10) - (spec4/10)[2000:10500]
plt.plot(wn_stretch[2000:10500],sub3, label='Difference pub - jons layers', alpha=0.8, lw=0.4, color='pink',)

# plt.plot(wn_stretch[2000:10500],(stretch_new*10000)/10, label='stretchnew', lw=0.6)

# plt.plot(wn_stretch[2000:10500], (spec4/10)[2000:10500], label='jonlayers', lw=0.6)


# plt.plot(wv_jon,(spec4)*1000, color='blue')


# sub5 = ((stretch_new*10000)/10) - (rad_jon)*1000
# plt.plot(wv_jon, sub5, label='Difference pub - jons layers', alpha=0.8, lw=0.4, color='teal')

# The variable zen is a floating point array fltarr(72,12500) 
# index 31 (of the index ranging from 0-71) is the 11:00 1 minute average for 11:00

plt.legend()
plt.xlabel('Wavenumber / cm-1')
plt.ylabel('Radiance / [mW m-2 sr-1 / cm-1]')
plt.savefig(path+'jon_andoya_vs_lblrtm_APODISED_NEW.png')

"""
ax1.plot(wv, rad[0:12500,0,0,0])
ax1.set_xlim(400,1500)
ax1.set_ylim(0,0.12)
ax1.set_title('Downwelling Spectrum')
ax1.set_xlabel('Wavenumber / cm-1')
ax1.set_ylabel('Radiance / [W m-2 sr-1 / cm-1]')
ax2.plot(dum_new_fre, diff_dum, lw=0.8, color = 'purple', label='36-126')
ax2.set_title('Difference')
ax2.set_xlabel('Wavenumber / cm-1')
ax2.set_ylabel('Radiance / [W m-2 sr-1 / cm-1]')
"""

