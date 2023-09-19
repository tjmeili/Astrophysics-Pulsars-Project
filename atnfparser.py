import numpy.ma.core
import psrqpy
import json

def get_atnf_data():
    params = ['JName', 'P0', 'P1', 'Binary', 'BinComp', 'Dist', 'Dist_DM', 'Type', 'NGlt', 'R_lum', 'Age', 'Bsurf',
              'Edot']

    # Query ATNF catalog for pulsars with params from above. Received as a table
    q = psrqpy.QueryATNF(params)
    t = q.table

    # Convert pulsars from DataFrame object to JSON (for exporting and type conflicts aka MaskedConstant)
    plsr = []
    for i in range(len(t)):
        data = {
            "JNAME": t[i]['JNAME'] if type(t[i]['JNAME']) != numpy.ma.core.MaskedConstant else None,
            "P0": t[i]['P0'] if type(t[i]['P0']) != numpy.ma.core.MaskedConstant else None,
            "P1": t[i]['P1'] if type(t[i]['P1']) != numpy.ma.core.MaskedConstant else None,
            "BINARY": t[i]['BINARY'] if type(t[i]['BINARY']) != numpy.ma.core.MaskedConstant else None,
            "BINCOMP": t[i]['BINCOMP'] if type(t[i]['BINCOMP']) != numpy.ma.core.MaskedConstant else None,
            "DIST": t[i]['DIST'] if type(t[i]['DIST']) != numpy.ma.core.MaskedConstant else None,
            "DIST_DM": t[i]['DIST_DM'] if type(t[i]['DIST_DM']) != numpy.ma.core.MaskedConstant else None,
            "TYPE": t[i]['TYPE'] if type(t[i]['TYPE']) != numpy.ma.core.MaskedConstant else None,
            "NGLT": t[i]['NGLT'] if type(t[i]['NGLT']) != numpy.ma.core.MaskedConstant else None,
            "R_LUM": t[i]['R_LUM'] if type(t[i]['R_LUM']) != numpy.ma.core.MaskedConstant else None,
            "AGE": t[i]['AGE'] if type(t[i]['AGE']) != numpy.ma.core.MaskedConstant else None,
            "BSURF": t[i]['BSURF'] if type(t[i]['BSURF']) != numpy.ma.core.MaskedConstant else None,
            "EDOT": t[i]['EDOT'] if type(t[i]['EDOT']) != numpy.ma.core.MaskedConstant else None
        }
        plsr.append(data)

    with open('atnf_pulsar_data.json', 'w') as f:
        json.dump(plsr, f)

def load_atnf_data():
    f = open('atnf_pulsar_data.json')
    plsr = json.load(f)
    f.close()
    return plsr
