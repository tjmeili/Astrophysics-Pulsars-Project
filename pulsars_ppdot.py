import matplotlib.pyplot as plt
import numpy as np
import atnfparser


def pulsarLifeCyclePlot():
    # variables
    npoints = 100000
    p = np.zeros(npoints)
    p[0] = 33.5 * 10 ** -3
    pdot = [10 ** (-13 - (3 * i / npoints)) for i in range(npoints)]
    dt = [10 ** (8.2 + (3 * i / npoints)) for i in range(npoints)]

    for i in range(1, npoints):
        p[i] = p[i - 1] + pdot[i] * dt[i]
        print(p[i], "\t", pdot[i])
    ax[1].plot(p, pdot, linewidth=3, color='orange', label='Pulsar Life')

xlo = 1.0e-3
xhi = 30.0
ylo = 1.0e-22
yhi = 1.0e-8

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
pulsarLifeCyclePlot()

# load pulsar data from json file
plsr = atnfparser.load_atnf_data()

x=[]
y=[]
xbin=[[],[],[],[],[],[]]
ybin=[[],[],[],[],[],[]]

# sift through pulsars and sort them while creating the x and y axis lists to graph
for i in range(0, len(plsr)):
    # print(plsr[i]['P0'], '\t', plsr[i]['P1'], '\t', plsr[i]['BINARY'], '\t', plsr[i]['BINCOMP'])
    if plsr[i]['P0'] != None and plsr[i]['P1'] != None:
        if plsr[i]['BINCOMP']:
            if plsr[i]['BINCOMP'] == 'MS':
                xbin[0].append(float(plsr[i]['P0']))
                ybin[0].append(float(plsr[i]['P1']))
            elif plsr[i]['BINCOMP'] == 'NS':
                xbin[1].append(float(plsr[i]['P0']))
                ybin[1].append(float(plsr[i]['P1']))
            elif plsr[i]['BINCOMP'] == 'CO':
                xbin[2].append(float(plsr[i]['P0']))
                ybin[2].append(float(plsr[i]['P1']))
            elif plsr[i]['BINCOMP'] == 'HE':
                xbin[3].append(float(plsr[i]['P0']))
                ybin[3].append(float(plsr[i]['P1']))
            elif plsr[i]['BINCOMP'] == 'UL':
                xbin[4].append(float(plsr[i]['P0']))
                ybin[4].append(float(plsr[i]['P1']))
            else:
                xbin[5].append(float(plsr[i]['P0']))
                ybin[5].append(float(plsr[i]['P1']))
        else:
            x.append(float(plsr[i]['P0']))
            y.append(float(plsr[i]['P1']))


ax[0].scatter(x, y, marker='.', color='black', label="Pulsar")
ax[0].scatter(xbin[0], ybin[0], marker='o', color='green', label="Bin-MS")
ax[0].scatter(xbin[1], ybin[1], marker='v', color='red', label="Bin-NS")
ax[0].scatter(xbin[2], ybin[2], marker='*', color='blue', label="Bin-CO")
ax[0].scatter(xbin[3], ybin[3], marker='^', color='orange', label="Bin-HE")
ax[0].scatter(xbin[4], ybin[4], marker='<', color='firebrick', label="Bin-UL")
ax[0].scatter(xbin[5], ybin[5], marker='x', color='purple', label="Bin-Other")

def makeDetailLines(plt):
    # magnetic field lines
    for logB in range(8, 16):
        xright = 100.0
        yleft = (10.0**logB/3.3e19)**2.0/xlo
        plt.plot([xlo, xright], [yleft, (10.0 ** logB / 3.3e19) ** 2.0 / xright], ls=':', color='black')
        if 8 < logB < 13:
            plt.text(1.1e-3, yleft * 0.78, '$ 10^{' + str(logB) + '}~\mathrm{G} $', fontsize=12)
        elif logB==13:
            plt.text(1.1e-3, yleft * 0.78, '$ B=10^{' + str(logB) + '}~\mathrm{G} $', fontsize=12)
        elif logB==14:
            plt.text(1.5e-2, 1.0e-9, '$ 10^{' + str(logB) + '}~\mathrm{G} $', fontsize=12)
        elif logB==15:
            plt.text(1.05, 1.0e-9, '$ 10^{' + str(logB) + '}~\mathrm{G} $', fontsize=12)

    # age lines
    for age in range(2, 12):
        line_left = xlo
        text_x = 14.0

        yright = 0.5 / (10.0 ** age * 31556926) * xhi
        plt.plot([line_left, xhi], [0.5 / (10.0 ** age * 31556926) * line_left, yright], ls=':', color='blue')
        if age == 10:
            plt.text(text_x * 0.85, yright * 0.9, '$ 10^{' + str(age) + '} $', fontsize=12, color='blue')
        elif age > 3:
            plt.text(text_x, yright * 0.9, '$ 10^{' + str(age) + '} $', fontsize=12, color='blue')
        elif age > 2:
            plt.text(text_x * 0.85, yright * 1.0, '$ 10^{' + str(age) + '}~\mathrm{yr} $', fontsize=12, color='blue')

    # graveyard line
    y_grave = [10 ** (2.0 * (-3.0) - 16.52), 10 ** (2.0 * np.log10(xhi) - 16.52)]
    plt.plot([xlo, xhi], y_grave, color='grey')
    plt.fill_between([xlo, xhi], y_grave, color='grey', alpha=0.3)
    plt.text(0.3, 3e-20, 'Graveyard', fontsize=14.0, fontweight='bold', color='grey')

makeDetailLines(ax[0])
makeDetailLines(ax[1])

ax[0].set_xscale('log')
ax[0].set_yscale('log')
ax[0].set_xlim([xlo, xhi])
ax[0].set_ylim([ylo, yhi])
ax[0].set_xlabel('$ P~(\mathrm{s}) $', fontsize=16)
ax[0].set_ylabel('$ \dot{P} $', fontsize=16)
ax[0].legend(loc="lower right")
ax[0].set_title("PPdot of Known Pulsars", fontsize=16)

plt.xscale('log')
plt.yscale('log')
plt.xlim([xlo, xhi])
plt.ylim([ylo, yhi])
plt.xlabel('$ P~(\mathrm{s}) $', fontsize=16)
plt.ylabel('$ \dot{P} $', fontsize=16)
plt.legend(loc="lower right")
plt.title("PPdot of Typical (Crab) Pulsar Life", fontsize=16)
plt.savefig('pulsars_ppdot.jpg')
plt.show()
