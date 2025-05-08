from typing import Final
import matplotlib.pyplot as plt
import numpy as np

from utils.signals.frequencies import DELTA_FREQ_GLO_L1_MHZ, DELTA_FREQ_GLO_L2_MHZ, FREQ_BDS_B1A_MHZ, FREQ_BDS_B1C_MHZ, FREQ_BDS_B1I_MHZ, FREQ_BDS_B2I_MHZ, FREQ_BDS_B3A_MHZ, FREQ_BDS_B3I_MHZ, FREQ_GAL_E1_MHZ, FREQ_GAL_E5_MHZ, FREQ_GAL_E6_MHZ, FREQ_GLO_L1_MHZ, FREQ_GLO_L1OC_MHZ, FREQ_GLO_L2_MHZ, FREQ_GLO_L2OC_MHZ, FREQ_GLO_L3OC_MHZ, FREQ_GPS_L1_MHZ, FREQ_GPS_L2_MHZ, FREQ_GPS_L5_MHZ, FREQ_NAVIC_L5, FREQ_QZS_L1, FREQ_QZS_L2, FREQ_QZS_L5, FREQ_QZS_L6, FREQ_GAL_E5a_MHZ, FREQ_GAL_E5b_MHZ
from utils.signals.psd import phi_AltBOC, phi_BOCc, phi_BOCs, phi_BPSK

plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

ALPHA_VAL: Final[float] = .7
THETA_VAL: Final = 5*np.pi/180
f0: Final[float] = 1.023e6
PLOT_NUM_POINTS: Final[int] = 1000

PSD_OFFSET: int = 110
VERT_SEPARATION: int = 100
HZ_IN_MHZ: float = 1.e6

fig, ax = plt.subplots(dpi=300, figsize=(18, 10.5))

def fill_vertical(x, y, opts='b', yoffset=0, color=''):
    y[y<0] = 0
    ax.fill_between(x, yoffset, y+yoffset, alpha=ALPHA_VAL, facecolor=color)

def plot_vertical(x, y, opts='b', yoffset=0, color=''):
    y[y<0] = np.nan
    ax.plot(x, y+yoffset, opts, alpha=ALPHA_VAL, color=color)

def fill_horizontal(x,y, opts='r', yoffset=0, color=''):
    y[y<0] = 0
    y[0] = 0
    y[-1] = 0
    
    x_ = x-y*np.sin(THETA_VAL)
    y_ = -y*np.cos(THETA_VAL)*.8

    ax.fill_between(x_, yoffset, y_+yoffset, alpha=ALPHA_VAL, facecolor=color)

def plot_horizontal(x,y, opts='r', yoffset=0, color=''):
    y[y<0] = np.nan

    x_ = x-y*np.sin(THETA_VAL)
    y_ = -y*np.cos(THETA_VAL)*.8

    ax.plot(x_, y_+yoffset, opts, alpha=ALPHA_VAL, color=color)

yoffset: int = 0

# GPS L1
f: np.ndarray = np.linspace(-20*f0/HZ_IN_MHZ, 20*f0/HZ_IN_MHZ, PLOT_NUM_POINTS)
fill_vertical(f+FREQ_GPS_L1_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET, color='#dbc51f')
fill_vertical(f+FREQ_GPS_L1_MHZ, 10*np.log10(phi_BOCs(f*HZ_IN_MHZ, f0, 10, 5))+PSD_OFFSET, color='red')
fill_vertical(f+FREQ_GPS_L1_MHZ,  10*np.log10(phi_BOCs(f*HZ_IN_MHZ, f0, 1, 1))+PSD_OFFSET, color='green')
fill_horizontal(f+FREQ_GPS_L1_MHZ, 10*np.log10(np.sqrt(29/33)*phi_BOCs(f*HZ_IN_MHZ, f0, 1, 1)+np.sqrt(4/33)*phi_BOCs(f*HZ_IN_MHZ, f0, 6, 1))+PSD_OFFSET, color='green')
fill_horizontal(f+FREQ_GPS_L1_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 1))+PSD_OFFSET, color='cyan')
ax.text(1578.35, 42.52, 'L1P', horizontalalignment='center', fontsize=9, color='#dbc51f', clip_on=True)
ax.text(FREQ_GPS_L1_MHZ, 50.8, 'L1C-I', horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='green', clip_on=True)
ax.text(1585.22, 42.52, 'L1M', horizontalalignment='center', fontsize=9, color='red', clip_on=True)
ax.text(1577.57, -41.53, 'L1C-Q', horizontalalignment='center', va='top',fontsize=9, color='green', clip_on=True)
ax.text(1570.7, -41.53, 'L1C/A', horizontalalignment='center', va='top',fontsize=9, color='cyan', clip_on=True)

# GPS L2
fill_vertical(f+FREQ_GPS_L2_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET, color='#dbc51f')
fill_vertical(f+FREQ_GPS_L2_MHZ, 10*np.log10(phi_BOCs(f*HZ_IN_MHZ, f0, 10, 5))+PSD_OFFSET, color='red')
fill_horizontal(f+FREQ_GPS_L2_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 1))+PSD_OFFSET, color='green')
ax.text(FREQ_GPS_L2_MHZ, 43.82, 'L2P', horizontalalignment='center', va='bottom',fontsize=9, color='#dbc51f', clip_on=True)
ax.text(1237.3, 43.06, 'L2M', horizontalalignment='center', va='bottom',fontsize=9, color='red', clip_on=True)
ax.text(1225.6,-36.7, 'L2C', horizontalalignment='left', va='top',fontsize=9, color='green', clip_on=True)

# GPS L5
fill_vertical(f+FREQ_GPS_L5_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET, color='green')
fill_horizontal(f+FREQ_GPS_L5_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET, color='#2d8124')
ax.text(FREQ_GPS_L5_MHZ, 45.34, 'L5-I', horizontalalignment='center', va='bottom',fontsize=9, color='green', clip_on=True)
ax.text(FREQ_GPS_L5_MHZ-55*np.sin(THETA_VAL), yoffset-55*np.cos(THETA_VAL)*.8, 'L5-Q', horizontalalignment='center', verticalalignment='center', fontsize=9, color='#2d8124', clip_on=True)


yoffset-=VERT_SEPARATION
# GLO FDMA L1
f = np.linspace(-1.023*5.11, 1.023*5.11, PLOT_NUM_POINTS)
for k in range(-7,8):
    plot_vertical(f+k*DELTA_FREQ_GLO_L1_MHZ+FREQ_GLO_L1_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 5.11))+PSD_OFFSET, yoffset=yoffset, color='r')
f = np.linspace(-1.023*0.511, 1.023*0.511, PLOT_NUM_POINTS)
for k in range(-7,8):
    plot_horizontal(f+k*DELTA_FREQ_GLO_L1_MHZ+FREQ_GLO_L1_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 0.511))+PSD_OFFSET, yoffset=yoffset, color='g')
ax.text(1602.34,yoffset+47.34, 'L1P', horizontalalignment='center', va='bottom',fontsize=9, color='red', clip_on=True)
ax.text(1595,yoffset-10.8, 'L1C/A', horizontalalignment='right', va='top',fontsize=9, color='green', clip_on=True)

# # GLO FDMA L2
f = np.linspace(-1.023*5.11, 1.023*5.11, PLOT_NUM_POINTS)
for k in range(-7,8):
    plot_vertical(f+FREQ_GLO_L2_MHZ+k*DELTA_FREQ_GLO_L2_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 5.11))+PSD_OFFSET, yoffset=yoffset, color='r')
f = np.linspace(-1.023*0.511, 1.023*0.511, PLOT_NUM_POINTS)
for k in range(-7,8):
    plot_horizontal(f+FREQ_GLO_L2_MHZ+k*DELTA_FREQ_GLO_L2_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 0.511))+PSD_OFFSET, yoffset=yoffset, color='g')
ax.text(FREQ_GLO_L2_MHZ, yoffset+47.22, 'L2P', horizontalalignment='center', va='bottom',fontsize=9, color='red', clip_on=True)
ax.text(1248.8, yoffset-19.63, 'L2C/A', horizontalalignment='left', va='top',fontsize=9, color='green', clip_on=True)


yoffset-=VERT_SEPARATION

# GLO CDMA L1
f = np.linspace(-20*f0/HZ_IN_MHZ, 20*f0/HZ_IN_MHZ, PLOT_NUM_POINTS)
fill_vertical(f+FREQ_GLO_L1OC_MHZ, 10*np.log10(phi_BOCs(f*HZ_IN_MHZ, f0, 1, 1))+PSD_OFFSET, yoffset=yoffset, color='green')
fill_horizontal(f+FREQ_GLO_L1OC_MHZ, 10*np.log10(phi_BOCs(f*HZ_IN_MHZ, f0, 5, 2.5))+PSD_OFFSET, yoffset=yoffset, color='red')
ax.text(1607, yoffset-22.5, 'L1SC', horizontalalignment='left', verticalalignment='top', fontsize=9, color='red', clip_on=True)
ax.text(1614.5,yoffset+30.4, 'L1OC', horizontalalignment='left', verticalalignment='bottom', fontsize=9, color='green', clip_on=True)

# GLO CDMA L2
fill_vertical(f+FREQ_GLO_L2OC_MHZ, 10*np.log10(phi_BOCs(f*HZ_IN_MHZ, f0, 1, 1))+PSD_OFFSET, yoffset=yoffset, color='green')
fill_horizontal(f+FREQ_GLO_L2OC_MHZ, 10*np.log10(phi_BOCs(f*HZ_IN_MHZ, f0, 5, 2.5))+PSD_OFFSET, yoffset=yoffset, color='red')
ax.text(1254.54, yoffset-22.5, 'L2SC', horizontalalignment='left', verticalalignment='top', fontsize=9, color='red', clip_on=True)
ax.text(1263,yoffset+30.4, 'L2OC', horizontalalignment='left', verticalalignment='bottom', fontsize=9, color='green', clip_on=True)

# GLO CDMA L3
fill_vertical(f+FREQ_GLO_L3OC_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET, yoffset=yoffset, color='green')
fill_horizontal(f+FREQ_GLO_L3OC_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET, yoffset=yoffset, color='#2d8124')
ax.text(FREQ_GLO_L3OC_MHZ, yoffset+45, 'L3-I', horizontalalignment='center', va='bottom',fontsize=9, color='green', clip_on=True)
ax.text(FREQ_GLO_L3OC_MHZ-55*np.sin(THETA_VAL), yoffset-55*np.cos(THETA_VAL)*.8, 'L3-Q', horizontalalignment='center', verticalalignment='center', fontsize=9, color='#2d8124', clip_on=True)

yoffset-=VERT_SEPARATION

# GAL E1
f = np.linspace(-20*f0/HZ_IN_MHZ, 20*f0/HZ_IN_MHZ, PLOT_NUM_POINTS)
fill_vertical(f+FREQ_GAL_E1_MHZ, 10*np.log10(np.sqrt(10/11)*phi_BOCs(f*HZ_IN_MHZ, f0, 1, 1)+np.sqrt(1/11)*phi_BOCs(f*HZ_IN_MHZ, f0, 6, 1))+PSD_OFFSET, yoffset=yoffset, color='green')
fill_horizontal(f+FREQ_GAL_E1_MHZ, 10*np.log10(phi_BOCc(f*HZ_IN_MHZ, f0, 15, 2.5))+PSD_OFFSET, yoffset=yoffset, color='red')
ax.text(FREQ_GAL_E1_MHZ, yoffset+60, 'E1$_B$ E1$_C$', horizontalalignment='center', verticalalignment='center', fontsize=9, color='green', clip_on=True)
ax.text(FREQ_GAL_E1_MHZ-30*np.sin(THETA_VAL), yoffset-30*np.cos(THETA_VAL)*.8, 'E1$_A$', horizontalalignment='center', verticalalignment='center', fontsize=9, color='red', clip_on=True)

# GAL E6
fill_vertical(f+FREQ_GAL_E6_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 5))+PSD_OFFSET, yoffset=yoffset, color='green')
fill_horizontal(f+FREQ_GAL_E6_MHZ, 10*np.log10(phi_BOCc(f*HZ_IN_MHZ, f0, 10, 5))+PSD_OFFSET, yoffset=yoffset, color='red')
ax.text(FREQ_GAL_E6_MHZ, yoffset+50, 'E6$_B$ E6$_C$', horizontalalignment='center', verticalalignment='center', fontsize=9, color='green', clip_on=True)
ax.text(FREQ_GAL_E6_MHZ-10*np.sin(THETA_VAL), yoffset-30*np.cos(THETA_VAL)*.8, 'E6$_A$', horizontalalignment='center', verticalalignment='center', fontsize=9, color='red', clip_on=True)

# GAL E5
f = np.linspace(-35*f0/HZ_IN_MHZ, 35*f0/HZ_IN_MHZ, PLOT_NUM_POINTS)
fill_vertical(f+FREQ_GAL_E5_MHZ, 10*np.log10(phi_AltBOC(f*HZ_IN_MHZ, f0, 15, 10))+PSD_OFFSET, yoffset=yoffset, color='#3399ff')
fill_horizontal(f+FREQ_GAL_E5_MHZ, 10*np.log10(phi_AltBOC(f*HZ_IN_MHZ, f0, 15, 10))+PSD_OFFSET, yoffset=yoffset, color='#2879c9')
ax.text(FREQ_GAL_E5a_MHZ, yoffset+55, 'E5a-I', horizontalalignment='center', verticalalignment='center', fontsize=9, color='#3399ff', clip_on=True)
ax.text(FREQ_GAL_E5b_MHZ, yoffset+55, 'E5b-I', horizontalalignment='center', verticalalignment='center', fontsize=9, color='#3399ff', clip_on=True)
ax.text(FREQ_GAL_E5a_MHZ-60*np.sin(THETA_VAL), yoffset-60*np.cos(THETA_VAL)*.8, 'E5a-Q', horizontalalignment='center', verticalalignment='center', fontsize=9, color='#2879c9', clip_on=True)
ax.text(FREQ_GAL_E5b_MHZ-60*np.sin(THETA_VAL), yoffset-60*np.cos(THETA_VAL)*.8, 'E5b-Q', horizontalalignment='center', verticalalignment='center', fontsize=9, color='#2879c9', clip_on=True)

yoffset-=VERT_SEPARATION

# BDS-2 B1
f = np.linspace(-20*f0/HZ_IN_MHZ, 20*f0/HZ_IN_MHZ, PLOT_NUM_POINTS)
fill_vertical(f+FREQ_BDS_B1I_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 2))+PSD_OFFSET, yoffset=yoffset, color='green')
fill_horizontal(f+FREQ_BDS_B1I_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 2))+PSD_OFFSET, yoffset=yoffset, color='red')
ax.text(1564,yoffset+37.237, 'B1I', horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='green', clip_on=True)
ax.text(1551.34,yoffset-25.355, 'B1Q', horizontalalignment='center', verticalalignment='top', fontsize=9, color='red', clip_on=True)

# BDS-2 B3
fill_vertical(f+FREQ_BDS_B3I_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET, yoffset=yoffset, color='green') # B3I
fill_horizontal(f+FREQ_BDS_B3I_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET, yoffset=yoffset, color='red') # B3Q
ax.text(1283.37, yoffset+30, 'B3I', horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='green', clip_on=True)
ax.text(1287.8, yoffset-11.71, 'B3Q', horizontalalignment='left', verticalalignment='top', fontsize=9, color='red', clip_on=True)


# BDS-2 B2I
fill_vertical(f+FREQ_BDS_B2I_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 2))+PSD_OFFSET, yoffset=yoffset, color='green')
ax.text(1209.68, yoffset+38.72, 'B2I', horizontalalignment='left', verticalalignment='bottom', fontsize=9, color='green', clip_on=True)

# BDS-2 B2Q
fill_horizontal(f+FREQ_BDS_B2I_MHZ, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET, yoffset=yoffset, color='red')
ax.text(1226.11, yoffset-12.8, 'B2Q', horizontalalignment='left', verticalalignment='top', fontsize=9, color='red', clip_on=True)


yoffset-=VERT_SEPARATION

# BDS-3 B1A
fill_vertical(f+FREQ_BDS_B1A_MHZ, 10*np.log10(phi_BOCs(f*HZ_IN_MHZ, f0, 14, 2))+PSD_OFFSET, yoffset=yoffset, color='red')
fill_horizontal(f+FREQ_BDS_B1A_MHZ, 10*np.log10(phi_BOCs(f*HZ_IN_MHZ, f0, 14, 2))+PSD_OFFSET, yoffset=yoffset, color='red')
ax.text(1589.6, yoffset+46.4, 'B1A', horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='red', clip_on=True)

# BDS-3 B1C
fill_vertical(f+FREQ_BDS_B1C_MHZ, 10*np.log10(phi_BOCs(f*HZ_IN_MHZ, f0, 1, 1))+PSD_OFFSET, yoffset=yoffset, color='green') # Data
fill_horizontal(f+FREQ_BDS_B1C_MHZ, 10*np.log10(np.sqrt(29/33)*phi_BOCs(f*HZ_IN_MHZ, f0, 1, 1)+np.sqrt(4/33)*phi_BOCs(f*HZ_IN_MHZ, f0, 6, 1))+PSD_OFFSET, yoffset=yoffset, color='green') # Pilot
ax.text(1582.38, yoffset+34.5, 'B1C$_D$', horizontalalignment='left', verticalalignment='bottom', fontsize=9, color='green', clip_on=True)
ax.text(1580, yoffset-30, 'B1C$_P$', horizontalalignment='left', verticalalignment='top', fontsize=9, color='green', clip_on=True)


# BDS-3 B3A
fill_vertical(f+FREQ_BDS_B3A_MHZ, 10*np.log10(phi_BOCs(f*HZ_IN_MHZ, f0, 15, 2.5))+PSD_OFFSET, yoffset=yoffset, color='red')
ax.text(FREQ_BDS_B3A_MHZ, yoffset+31.2, 'B3$_A$', horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='red', clip_on=True)

# BDS-3 B2a/B2b
f = np.linspace(-35*f0/HZ_IN_MHZ, 35*f0/HZ_IN_MHZ, PLOT_NUM_POINTS)
fill_vertical(f+FREQ_GAL_E5_MHZ, 10*np.log10(phi_AltBOC(f*HZ_IN_MHZ, f0, 15, 10))+PSD_OFFSET, yoffset=yoffset, color='#3399ff')
fill_horizontal(f+FREQ_GAL_E5_MHZ, 10*np.log10(phi_AltBOC(f*HZ_IN_MHZ, f0, 15, 10))+PSD_OFFSET, yoffset=yoffset, color='#2879c9')
ax.text(FREQ_GAL_E5a_MHZ, yoffset+55, 'B2a-I', horizontalalignment='center', verticalalignment='center', fontsize=9, color='#3399ff', clip_on=True)
ax.text(FREQ_GAL_E5b_MHZ, yoffset+55, 'B2b-I', horizontalalignment='center', verticalalignment='center', fontsize=9, color='#3399ff', clip_on=True)
ax.text(FREQ_GAL_E5a_MHZ-60*np.sin(THETA_VAL), yoffset-60*np.cos(THETA_VAL)*.8, 'B2a-Q', horizontalalignment='center', verticalalignment='center', fontsize=9, color='#2879c9', clip_on=True)
ax.text(FREQ_GAL_E5b_MHZ-60*np.sin(THETA_VAL), yoffset-60*np.cos(THETA_VAL)*.8, 'B2b-Q', horizontalalignment='center', verticalalignment='center', fontsize=9, color='#2879c9', clip_on=True)


yoffset-=VERT_SEPARATION


f = np.linspace(-20*f0/HZ_IN_MHZ, 20*f0/HZ_IN_MHZ, PLOT_NUM_POINTS)
# QZSS L1
fill_horizontal(f+FREQ_QZS_L1, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 1))+PSD_OFFSET, yoffset=yoffset, color='green') # L1C/A
fill_vertical(f+FREQ_QZS_L1, 10*np.log10(phi_BOCs(f*HZ_IN_MHZ, f0, 1, 1))+PSD_OFFSET, yoffset=yoffset, color='green') # L1CD
fill_vertical(f+FREQ_QZS_L1, 10*np.log10(np.sqrt(10/11)*phi_BOCs(f*HZ_IN_MHZ, f0, 1, 1)+np.sqrt(1/11)*phi_BOCs(f*HZ_IN_MHZ, f0, 6, 1))+PSD_OFFSET, yoffset=yoffset, color='cyan') # L1CP
fill_vertical(f+FREQ_QZS_L1, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 1))+PSD_OFFSET, yoffset=yoffset, color='#3399ff') # L1S

ax.text(1570.66, yoffset-45.76, 'L1C/A', horizontalalignment='center', verticalalignment='top', fontsize=9, color='green', clip_on=True)
ax.text(FREQ_QZS_L1, yoffset+51, 'L1S', horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='#3399ff', clip_on=True)
ax.text(1578.32, yoffset+39.4, 'L1C$_D$', horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='green', clip_on=True)
ax.text(1593.64, yoffset+36, 'L1C$_P$', horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='cyan', clip_on=True)


# QZSS L2
fill_vertical(f+FREQ_QZS_L2, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 1))+PSD_OFFSET, yoffset=yoffset, color='green') # L2C
ax.text(FREQ_QZS_L2, yoffset+55.32, 'L2', horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='green', clip_on=True)

# QZSS L5
fill_vertical(f+FREQ_QZS_L5, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET, yoffset=yoffset, color='green') 
fill_horizontal(f+FREQ_QZS_L5, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET, yoffset=yoffset, color='#2d8124')
fill_vertical(f+FREQ_QZS_L5, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET-5, yoffset=yoffset, color='#3399ff') # L5S-I
fill_horizontal(f+FREQ_QZS_L5, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 10))+PSD_OFFSET-5, yoffset=yoffset, color='#2879c9') # L5S-I
ax.text(FREQ_QZS_L5, yoffset+43.34, 'L5-I', horizontalalignment='center', va='bottom',fontsize=9, color='green', clip_on=True)
ax.text(FREQ_QZS_L5-55*np.sin(THETA_VAL), yoffset-55*np.cos(THETA_VAL)*.8, 'L5-Q', horizontalalignment='center', verticalalignment='center', fontsize=9, color='#2d8124', clip_on=True)
ax.text(1191.23, yoffset+33.73, 'L5S-I', horizontalalignment='center', va='bottom',fontsize=9, color='#3399ff', clip_on=True)
ax.text(1191.23-33.73*np.sin(THETA_VAL), yoffset-33.73*np.cos(THETA_VAL), 'L5S-Q', horizontalalignment='center', verticalalignment='center', fontsize=9, color='#2879c9', clip_on=True)

# QZSS L6
fill_vertical(f+FREQ_QZS_L6, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 5))+PSD_OFFSET, yoffset=yoffset, color='green') 
ax.text(FREQ_QZS_L6, yoffset+47.27, 'L6', horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='green', clip_on=True)

yoffset-=VERT_SEPARATION

# NavIC L5
fill_vertical(f+FREQ_NAVIC_L5, 10*np.log10(phi_BPSK(f*HZ_IN_MHZ, f0, 1))+PSD_OFFSET, yoffset=yoffset, color='green') 
fill_horizontal(f+FREQ_NAVIC_L5, 10*np.log10(phi_BOCc(f*HZ_IN_MHZ, f0, 5, 2))+PSD_OFFSET, yoffset=yoffset, color='red') 
ax.text(1179.13, yoffset+38.276, 'L5$_{SPS}$', horizontalalignment='left', verticalalignment='bottom', fontsize=9, color='green', clip_on=True)
ax.text(1173.8,yoffset-33.6, 'L5$_{RS}$', horizontalalignment='center', verticalalignment='top', fontsize=9, color='red', clip_on=True)

ax.plot([FREQ_GPS_L1_MHZ, FREQ_GPS_L1_MHZ], [yoffset-75,75], 'k--', alpha=.1)
ax.plot([FREQ_GPS_L5_MHZ, FREQ_GPS_L5_MHZ], [yoffset-75,75], 'k--', alpha=.1)
ax.plot([FREQ_GPS_L2_MHZ, FREQ_GPS_L2_MHZ], [yoffset-75,75], 'k--', alpha=.1)
ax.plot([FREQ_GAL_E6_MHZ, FREQ_GAL_E6_MHZ], [yoffset-75,75], 'k--', alpha=.1)
ax.plot([FREQ_GAL_E5b_MHZ, FREQ_GAL_E5b_MHZ], [yoffset-75,75], 'k--', alpha=.1)
ax.plot([1150,1650], [0,0], 'k--', alpha=.1)
ax.plot([1150,1650], [-1*VERT_SEPARATION, -1*VERT_SEPARATION], 'k--', alpha=.1)
ax.plot([1150,1650], [-2*VERT_SEPARATION, -2*VERT_SEPARATION], 'k--', alpha=.1)
ax.plot([1150,1650], [-3*VERT_SEPARATION, -3*VERT_SEPARATION], 'k--', alpha=.1)
ax.plot([1150,1650], [-4*VERT_SEPARATION, -4*VERT_SEPARATION], 'k--', alpha=.1)
ax.plot([1150,1650], [-5*VERT_SEPARATION, -5*VERT_SEPARATION], 'k--', alpha=.1)
ax.plot([1150,1650], [-6*VERT_SEPARATION, -6*VERT_SEPARATION], 'k--', alpha=.1)
ax.plot([1150,1650], [-7*VERT_SEPARATION, -7*VERT_SEPARATION], 'k--', alpha=.1)

ax.text(FREQ_GPS_L1_MHZ, yoffset-75, str(FREQ_GPS_L1_MHZ), horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='black', clip_on=True)
ax.text(FREQ_GPS_L2_MHZ, yoffset-75, str(FREQ_GPS_L2_MHZ), horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='black', clip_on=True)
ax.text(FREQ_GPS_L5_MHZ, yoffset-75, str(FREQ_GPS_L5_MHZ), horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='black', clip_on=True)
ax.text(FREQ_GAL_E6_MHZ, yoffset-75, str(FREQ_GAL_E6_MHZ), horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='black', clip_on=True)
ax.text(FREQ_GAL_E5b_MHZ, yoffset-75, str(FREQ_GAL_E5b_MHZ), horizontalalignment='center', verticalalignment='bottom', fontsize=9, color='black', clip_on=True)

ax.plot([FREQ_GLO_L1_MHZ, FREQ_GLO_L1_MHZ], [-0.15*VERT_SEPARATION,-1.5*VERT_SEPARATION], 'k--', alpha=.1)
ax.text(FREQ_GLO_L1_MHZ, -0.15*VERT_SEPARATION, str(FREQ_GLO_L1_MHZ), horizontalalignment='center', verticalalignment='center', fontsize=9, color='black', clip_on=True)

ax.plot([FREQ_GLO_L1OC_MHZ, FREQ_GLO_L1OC_MHZ], [-1.5*VERT_SEPARATION,-2.5*VERT_SEPARATION], 'k--', alpha=.1)
ax.text(FREQ_GLO_L1OC_MHZ, -2.5*VERT_SEPARATION, str(FREQ_GLO_L1OC_MHZ), horizontalalignment='center', verticalalignment='center', fontsize=9, color='black', clip_on=True)

ax.plot([FREQ_BDS_B1I_MHZ, FREQ_BDS_B1I_MHZ], [-3.4*VERT_SEPARATION,-4.5*VERT_SEPARATION], 'k--', alpha=.1)
ax.text(FREQ_BDS_B1I_MHZ, -3.4*VERT_SEPARATION, str(FREQ_BDS_B1I_MHZ), horizontalalignment='center', verticalalignment='center', fontsize=9, color='black', clip_on=True)

ax.plot([FREQ_GLO_L2OC_MHZ, FREQ_GLO_L2OC_MHZ], [-3*VERT_SEPARATION,-1.5*VERT_SEPARATION], 'k--', alpha=.1)
ax.text(FREQ_GLO_L2OC_MHZ, -3*VERT_SEPARATION, str(FREQ_GLO_L2OC_MHZ), horizontalalignment='center', verticalalignment='center', fontsize=9, color='black', clip_on=True)

ax.plot([FREQ_GLO_L2_MHZ, FREQ_GLO_L2_MHZ], [-2.5*VERT_SEPARATION,-0.5*VERT_SEPARATION], 'k--', alpha=.1)
ax.text(FREQ_GLO_L2_MHZ, -2.5*VERT_SEPARATION, str(FREQ_GLO_L2_MHZ), horizontalalignment='center', verticalalignment='center', fontsize=9, color='black', clip_on=True)

ax.plot([FREQ_BDS_B3A_MHZ, FREQ_BDS_B3A_MHZ], [-5.5*VERT_SEPARATION,-3.5*VERT_SEPARATION], 'k--', alpha=.1)
ax.text(FREQ_BDS_B3A_MHZ, -5.5*VERT_SEPARATION, str(FREQ_BDS_B3A_MHZ), horizontalalignment='center', verticalalignment='center', fontsize=9, color='black', clip_on=True)

ax.plot([FREQ_GLO_L3OC_MHZ, FREQ_GLO_L3OC_MHZ], [-2.5*VERT_SEPARATION,-1*VERT_SEPARATION], 'k--', alpha=.1)
ax.text(FREQ_GLO_L3OC_MHZ, -1*VERT_SEPARATION, str(FREQ_GLO_L3OC_MHZ), horizontalalignment='center', verticalalignment='center', fontsize=9, color='black', clip_on=True)


ax.set_yticks([0,-VERT_SEPARATION,-VERT_SEPARATION*2, -VERT_SEPARATION*3, -VERT_SEPARATION*4, -VERT_SEPARATION*5, -VERT_SEPARATION*6, -VERT_SEPARATION*7],\
    ['GPS', 'GLO FDMA', 'GLO CDMA', 'GAL', 'BDS-2', 'BDS-3','QZSS','NavIC'], rotation=90)

ax.set_xlabel('Frequency [MHz]')
ax.set_ylim((yoffset-75,75))

ax.set_xlim((1530., 1630.))
fig.set_size_inches(37/3, 10.5)
fig.tight_layout()
fig.savefig('upper_L_band.svg', dpi=250)

ax.set_xlim((1150., 1300.))
fig.set_size_inches(18, 10.5)
fig.tight_layout()
fig.savefig('lower_L_band.svg', dpi=250)