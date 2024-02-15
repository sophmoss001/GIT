"comparision of TAPE12_1100 FROM JON and SOPHIE"
import pandas as pd
import pyreadstat
from os.path import dirname, join as pjoin
import scipy.io as sio
from scipy.io import readsav
import numpy as np
from matplotlib import pyplot as plt
import xarray as xr
import tkinter
# JONS DATA

sav_fname = "/disk1/sm4219/GIT/LBLRTM/apodised_spectra_TAPE12_1100.sav"
data_sav = readsav(sav_fname, verbose=True)
all_d = (data_sav['apodised_spectra'])
wv_jon = all_d[:, 0]
rad_jon = all_d[:, 1]

# SOPHIES DATA
# wn_raw,spectrum = np.loadtxt("/disk1/sm4219/LBLRTM_FOR_SOPHIE/LBLRTM_SIMGA_BOUNDS_40/apodised_spectra_TOPHAT_APODISED_DONE.txt", unpack = True, dtype=np.float64)
# spectrum = np.loadtxt('/disk1/sm4219/GIT/LBLRTM/apodized_spectrum_TOPHAT_SOPH.txt', unpack=True)
# spectrum = np.loadtxt("/disk1/sm4219/GIT/LBLRTM/apodized_spectrum_TOPHAT_python.txt", delimiter=',')
# print(spectrum, 'spec')

spectrum = np.loadtxt("/disk1/sm4219/GIT/LBLRTM/apodized_spectrum_RAD.txt")
wn = np.loadtxt("/disk1/sm4219/GIT/LBLRTM/apodized_spectrum_wn.txt")

start_fre=np.array([400,450,560,630,730,850,950,1050,1150,1250,1360,1450,1550,1650,1750,1800,1900])
end_fre=np.array([450,560,630,730,850,950,1050,1150,1250,1360,1450,1550,1650,1750,1800,1900,1950])
 
# wn_raw = np.linspace(start_fre[0],1950,np.shape(spectrum)[0])    
# start = 300
# stop = 2000
# step = 0.2
# wn_n = np.arange(start, stop + step, step)   
# print(wv_jon, wn_raw)
# df2.set_index(wn_raw, append=False, inplace=False)
# df = xr.DataArray(data=spectrum, dims=['wn'], coords=dict(wn=wn_raw))
# Initialize an empty array to store the nearest indices
# nearest_indices = np.zeros_like(unique_wn_rounded, dtype=int)
# Iterate over unique values in wn_rounded and find the nearest index in wn_raw
# for i, val in enumerate(unique_wn_rounded):
#     nearest_indices[i] = np.abs(wn_raw - val).argmin()
# # Extract corresponding values from spectrum
# matched_spectrum = spectrum[nearest_indices]
# df = xr.DataArray(data=spec_small, dims=['wn'], coords=dict(wn=wn_unique[0:694999]))
# df = pd.DataFrame(data=spectrum, columns=wn_raw)
# print(df)
# apodised_interp = df.interp(wn=new_wn, method='linear', kwargs={'fill_value': 'extrapolate'})
# raise Exception("x should not be greater than 5")

# wn_values = apodised_interp.coords['wn']
# spectrum_values = apodised_interp.values
# print(spectrum_values)

colours = ['darkblue', 'darkblue', 'red', 'darkblue', 'darkblue']

plt.figure()
lima = 502
lima2 = 602

for i in range(-2,2):
    limb = lima - i
    limb2 = lima2 - i
    sub = spectrum[lima:lima2] - rad_jon[limb:limb2]
    # plt.plot(wv_jon[lima:lima2], sub, color='darkblue', label='sophie502- jon500', lw=0.5, alpha=0.6)

sub = spectrum*1E7 - rad_jon[0:6500]*1E7
print(wv_jon[6499], wn[6499])
# plt.plot(wn, sub, color='red', label='00', lw=0.3, alpha=0.6)

spec_new, wn = np.loadtxt("/net/sirocco/disk1/sm4219/LBLRTM_FOR_SOPHIE/LBLRTM_SIMGA_BOUNDS_40/apodised_spectra_APODISED_AFTERHAT.txt", unpack=True)

plt.plot(wn,spec_new*1E7, label='sophie', alpha=0.6, lw=0.7, color='red')
# plt.plot(wv_jon, rad_jon*1E7, color='green', label='jon', lw=0.7, alpha=0.6)
# plt.plot(wn,spectrum, label='sophie_new', alpha=0.6, lw=0.7, color='blue')
plt.xlim(400,1600)
# plt.ylim(-0.5,0.5)

# print(spectrum)
# lima = 500
# lima2 = 600
# limb = lima + 2
# limb2 = lima2 + 2
# sub2 = spectrum_values[lima:lima2] - rad_jon[limb:limb2]
# plt.plot(wv_jon[lima:lima2], sub2, color='red', label='sophie500 - jon502', lw=0.5, alpha=0.6)
plt.legend()
# plt.xlim(400,1600)
plt.ylabel('Radiance (mW m-2 sr-1 / cm -1)')
plt.xlabel('Wavenumber / cm -1')
plt.savefig('/disk1/sm4219/GIT/LBLRTM/compare_tape12.png')
