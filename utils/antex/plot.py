import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D  # Explicit import for 3D plotting
from utils.antex.types import AntennaInfo, FrequencyInfo

plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

def plot_PCV_surface(
    antenna_info: AntennaInfo,
    idx: int = 0,
):
    freq_info: FrequencyInfo = antenna_info.frequency_data[idx]
    
    X, Y = np.meshgrid(antenna_info.elevs, antenna_info.azs)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    ax.plot_surface(X, Y, freq_info.pcv_values, cmap=cm.get_cmap("viridis"))
    ax.zaxis.set_rotate_label(False)
    ax.set_zlabel("PCV [mm]", rotation=90)
    ax.view_init(elev=23.0, azim=29)
    ax.set_ylabel("Azimuth [deg]")
    ax.set_xlabel("Elevation [deg]")

    fig.suptitle(
        f"{freq_info.frequency} {antenna_info.antenna_type}\nPCO N/E/U: {freq_info.pco_n}, {freq_info.pco_e}, {freq_info.pco_u} [mm]"
    )

    return fig

def plot_PCV_polar(
    antenna_info: AntennaInfo,
    idx: int = 0,
):
    freq_info: FrequencyInfo = antenna_info.frequency_data[idx]
    rmesh, thetamesh = np.meshgrid(antenna_info.elevs, np.radians(antenna_info.azs))   
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    # ax.set_yticklabels(['','','','','','','','','$\\theta$=0°'])
    ax.set_yticks([10,20,30,40,50,60,70,80,90])
    pos = ax.contourf(thetamesh, rmesh, -freq_info.pcv_values)
    cbar = fig.colorbar(pos, ax=ax, location='left')
    cbar.ax.set_ylabel('Bias [mm]')

    ax.set_title(f"{antenna_info.antenna_type}; Freq: {freq_info.frequency}")

    return fig
