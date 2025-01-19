'''
Autor: Luis Manuel Rojas Patiño
Title: Códigos auxiliares 
'''
# Codijos Auxiliares

import pandas as pd
import webbrowser

def group_by_time(data, year=True, operation = str):
    """ 
    Agrupa los valores según la periodicidad y la operacion
    
    Parameters
    ___________________________________________________________________________
    - data: DataFrame de la consulta del API del INEGI o Banxico
    - year: bool, True para agrupar por año, False para agrupar por mes
    - operation: str, tipo de operación a realizar: 'sum', 'mean', 'median'
               
    Returns
    ___________________________________________________________________________
    DataFrame agrupado según la operación solicitada       
    """
    
    # Date 
    if year:
        data['date'] = pd.DatetimeIndex(data['fecha']).year
        data = data.drop(columns=['fecha'])
        grouped_data = data.groupby(by='date') 

    else:
        data['year'] = pd.DatetimeIndex(data['fecha']).year
        data['month'] = pd.DatetimeIndex(data['fecha']).month
        data['date'] = data['year'].astype(str) + '-' + data['month'].map(str).str.zfill(2)
        data = data.drop(columns=['fecha', 'month', 'year'])
        grouped_data = data.groupby(by='date')
        
    # Operaciones
    operations = {
        'sum': lambda x: x.sum(),
        'mean': lambda x: x.mean(),
        'median': lambda x: x.median(),
    }

    if operation in operations:
        data = operations[operation](grouped_data)
        data = data.reset_index()
        data['date'] = pd.to_datetime(data['date'])
    
    data = data.rename(columns= {'date':'fecha'})
        
    return data


def rename(data,  col): 
    '''
    Renombra las variables del dataframe
    
    Parameters
    ___________________________________________________________________________
    - data: dataframe
    - names: list de las variables de las a renombrar
    
    Returns
    ___________________________________________________________________________
    dataframe
    '''
    # verificador de que el nombres igual a varibles consultados
    if len(col) != len(data.columns):
        raise ValueError("Las variables no coinciden con el total de columnas")

    # Cambio de las columnas
    data.columns = col[:len(data.columns)] 
    return data

def url_api(API =str):
    '''
    Abre la pagina web del API del INEGI o Banxico
    
    Parameters
    ___________________________________________________________________________
    API: banxico|inegi
    
    Returns
    ___________________________________________________________________________
    Abre la pagina web
    '''
    if API== 'inegi':
       url = 'https://www.inegi.org.mx/servicios/api_indicadores.html'
    elif API == 'banxico':
        url ='https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries'
    else:
        raise ValueError('Codijo no identificado')
        
    return(webbrowser.open(url= url))

