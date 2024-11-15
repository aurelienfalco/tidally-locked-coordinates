#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

from TL_coordinates import get_GCM_data
from TL_coordinates import transform_to_TL_coordinates

# ### Get GCM output data.
filename = "diagfi.nc"

var="temp"
output = { 'tsurf':'tsurf',var:var,'u':'u','v':'v'
          }
grid = { "t":"Time",
       "lat":"latitude",
       "lon":"longitude",
       "p":"p",
       "alt":"altitude"
}
grid.update(output)
state = get_GCM_data.get_GCM("./", [filename], vars_list=grid)

# ### Now convert to TL coords.
# ### Pick Nlat/Nlon to match GCM's resolution in Earth-like coordinates, otherwise can get different global means!

nlat_tl = state.lat.size  # what resolution desired for interp into TL coords?
nlon_tl = state.lon.size  #
lon_ss = 180. # at which lon is the substellar point?
state_TL = transform_to_TL_coordinates.transform_state(state,output,(nlat_tl,nlon_tl),lon_ss=lon_ss,do_vel=True)


# note: in this case the time coord only has one entry.
#   get rid of singleton dims with np.squeeze()
for s in [state,state_TL]:
    for v in output:
        x0 = getattr(s,v)
        if x0.shape[0] == getattr(s,"t").shape[0]:
            start_t=-10
            x0 = np.mean(x0[start_t:],0)
            # alt=10 # in m
            # ind = np.where(getattr(s,"alt") == alt)[0]
            # ind = 10
            # if x0.shape[0] == getattr(s,"alt").shape[0]:
            #     ind = 0
            #     x0 = x0[ind]
        x1 = np.squeeze(x0)
        setattr(s,v,x1)


# ### Check global means.
print("global mean Ts in Earth coords = %.3f K" % np.average(np.average(state.tsurf,axis=-1) * state.weights,axis=-1))
print("global mean Ts in TL coords = %.3f K" % np.nanmean(np.nanmean(state_TL.tsurf,axis=-1) * state_TL.weights,axis=-1))


# ### add diagnostics to help plot the exact coordinate points
degtorad = np.pi/180.
lat_in_tl,lon_in_tl = transform_to_TL_coordinates.transform_latlon_to_TL(state.lat*degtorad,state.lon*degtorad,lon_ss=lon_ss)
lat_in_tl = lat_in_tl/degtorad
lon_in_tl = lon_in_tl/degtorad

lat_2d,lon_2d = np.meshgrid(state.lat,state.lon)

# # ----------------
# ### Make a plot of surface temperature in both coordinate systems, show the original lat/lon points
cmap = 'RdBu_r'

def plot_var(var="tsurf", ind_p = -1, n = 2, units="K"):
    # ind_p : desired index in vertical, e.g., mid-troposphere or near surface
    # n : how dense to plot wind vectors?
    try:
        alt = state.alt[ind_p]
    except:
        alt=None

    fig, ax = plt.subplots(1,2,figsize=[10,3.])
    CS = ax[0].pcolormesh(state.lon,state.lat,getattr(state,var),cmap=cmap)
    ax[0].scatter(lon_2d[::n,::n],lat_2d[::n,::n],s=4,c="k")
    plt.colorbar(CS)
    ax[0].set_ylim(-90,90)
    ax[0].set_title(f'{var}, Earth coordinates')

    CS = ax[1].pcolormesh(state_TL.lon,state_TL.lat,getattr(state_TL,var),cmap=cmap)
    ax[1].scatter(lon_in_tl[::n,::n],lat_in_tl[::n,::n],s=4,c="k")
    plt.colorbar(CS)
    # ax[1].set_xlim(state_TL.lon.min(),state_TL.lon.max())
    ax[1].set_ylim(-90,90)
    ax[1].set_title(f"{var}, TL coordinates")

    plt.savefig(f"{var}_TL_{alt:.2f}.pdf",format='pdf')


# ### Make a plot of surface temp, overlay surface winds
def plot_winds(var="tsurf", ind_p = -1, n = 4, units="K"):
    # ind_p : desired index in vertical, e.g., mid-troposphere or near surface
    # n : how dense to plot wind vectors?
    try:
        alt = state.alt[ind_p]
    except:
        alt=None

    plt.figure(figsize=[12,4])
    plt.subplot(1,2,1)
    CS = plt.pcolormesh(state.lon,state.lat,getattr(state,var),cmap=cmap)
    Q = plt.quiver(state.lon[::n],state.lat[::n],state.u[ind_p,::n,::n],state.v[ind_p,::n,::n],pivot='mid')
    qk = plt.quiverkey(Q, 0.45, 0.92, 10, r'$10 \frac{m}{s}$', labelpos='E',
                    coordinates='figure')
    plt.colorbar(CS,label=units)
    plt.xlim(state.lon.min(),state.lon.max())
    plt.ylim(-90,90)
    plt.title(f"{var}+wind,Earth coordinates")

    plt.subplot(1,2,2)
    CS = plt.pcolormesh(state_TL.lon,state_TL.lat,getattr(state_TL,var),cmap=cmap)
    Q = plt.quiver(state_TL.lon[::n],state_TL.lat[::n],state_TL.u[ind_p,::n,::n],state_TL.v[ind_p,::n,::n],pivot='mid')
    qk = plt.quiverkey(Q, 0.85, 0.92, 10, r'$10 \frac{m}{s}$', labelpos='E',
                    coordinates='figure')
    plt.colorbar(CS,label=units)
    plt.xlim(state_TL.lon.min(),state_TL.lon.max())
    plt.ylim(-90,90)
    plt.title(f"{var}+wind,TL coordinates")
    plt.tight_layout()
    plt.savefig(f"tsurf_wind_TL_{alt:.2f}.pdf",format='pdf')

plot_var(ind_p=-1)
plot_winds(ind_p=-1)
plot_winds(ind_p=20)