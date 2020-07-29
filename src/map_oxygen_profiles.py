#!/usr/bin/python

from pathlib import Path

import numpy as np

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
import colorcet as cc
import cmocean.cm as cmo

import bgcArgo as bgc

bp = bgc.get_index()
bp = bp[bp.parameters.notna()]
index = ['DOXY' in parameter_list for parameter_list in bp.parameters]
doxy = bp[index]

lat_bin_size = 5
lon_bin_size = 10
vmax = 4000

lat_bins = np.arange(-90, 90+lat_bin_size, lat_bin_size)
lon_bins = np.arange(-180, 180+lon_bin_size, lon_bin_size)

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson(central_longitude=180))

h = ax.hist2d(doxy.longitude, doxy.latitude, bins=[lon_bins, lat_bins], cmap=cmo.amp, transform=ccrs.PlateCarree(), vmax=vmax)

ax.set_global()
ax.coastlines()
ax.add_feature(cfeature.LAND, zorder=100, edgecolor='k')
ax.add_feature(cfeature.BORDERS, zorder=101)

plt.colorbar(h[-1], ax=ax, orientation='horizontal', extend='max', shrink=0.5, pad=0.05, label='$N_{profile}$')

ax.set_title('Number of Oxygen Profiles in each {:d}{}x{:d}{} box'.format(lat_bin_size, chr(176), lon_bin_size, chr(176)))

plt.savefig(Path('figures/argo_oxygen_profiles_{:d}x{:d}.png'.format(lat_bin_size, lon_bin_size)), dpi=350, bbox_inches='tight')
