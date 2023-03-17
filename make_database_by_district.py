""" 
GROUP 6
Database: Portugal Wildfires 2015
Research Question: Compare response, extinction time and cause of the wildfires, to see the influence on the burn areas for districts of Braga and Lisbon.

Qualitative variables
Distrito (Braga and Lisbon)
Causa (cause 1 and 4)
 
Quantitative variables
ResponseTime (HoraAlerta - Hora1Intervencao)
ExtinctionTime (Hora1Intervencao - HoraExtincao)
AA_Total
"""

# This file generates a new excel file using ListaIncendios2015.xlsx file 
#   with the name of the chosen district, 
#       containing the relevant columns for this project.

import pandas as pd

# outliers : tirar valores negativos

io = 'ListaIncendios_2015.xlsx'
worksheet_b = pd.read_excel(io, "2015", header=0, usecols="E,N:S,Z,AI")
worksheet_b = worksheet_b.dropna(axis = 0, how = 'any') # removing rows with null values

def newfile_filter_district(district_name):

    filename = district_name + '.xlsx'

    # filter by name of district and cause of fire
    ds_district = worksheet_b[(worksheet_b['Distrito'] == district_name) & ((worksheet_b['Causa'].between(1, 200)) | (worksheet_b['Causa'].between(400, 499)))]

    # Reformating date and time variables 
    dataAlerta = worksheet_b['DataAlerta'].str.replace('00:00:00.000','')
    ds_district['DateTimeAlerta'] = dataAlerta + '' + worksheet_b['HoraAlerta'].astype(str)

    dataInterv = worksheet_b['Data1Intervencao'].str.replace('00:00:00.000','')
    ds_district['DateTimeInterv'] = dataInterv + '' + worksheet_b['Hora1Intervencao'].astype(str)

    dataAlerta = worksheet_b['DataExtincao'].str.replace('00:00:00.000','')
    ds_district['DateTime Extincao'] = dataAlerta + '' + worksheet_b['HoraExtincao'].astype(str)

    #---Response Time Determination (in minutes)
    ds_district['InterventionTimeMin'] = pd.to_datetime(ds_district['DateTimeInterv']) - pd.to_datetime(ds_district['DateTimeAlerta'])
    ds_district['InterventionTimeMin'] = ds_district['InterventionTimeMin'] / pd.Timedelta(minutes=1)

    #---Extinction Time Determination (in minutes)
    ds_district['ExtinctionTimeMin'] = pd.to_datetime(ds_district['DateTime Extincao']) - pd.to_datetime(ds_district['DateTimeInterv'])
    ds_district['ExtinctionTimeMin'] = ds_district['ExtinctionTimeMin'] / pd.Timedelta(minutes=1)

    # removing rows that have extinction time or intervention time of less than 2 minutes. these values considered unrealistic
    ds_district.drop(ds_district[ds_district['ExtinctionTimeMin'] < 2].index, inplace=True)
    ds_district.drop(ds_district[ds_district['InterventionTimeMin'] < 2].index, inplace=True)
    
    ds_district['Cause'] = 0
    
    for n in range(0, len(ds_district)):
        if ds_district['Causa'].values[n] < 200:
            ds_district['Cause'].values[n] = 1
        else: ds_district['Cause'].values[n] = 4

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    ds_district.to_excel(writer, columns = ['Cause', 'InterventionTimeMin','ExtinctionTimeMin','AA_Total (pov+mato+agric) (ha)'] , sheet_name = district_name, index=False)
    
    # change causa name and distrubution
    # change AA name
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

#district_name = 'Santarém'
#newfile_filter_district(district_name)

district_name = ['Braga', 'Santarém']
for x in district_name:
    newfile_filter_district(x)

print('EOF.')