'''
Autor: Luis Manuel Rojas Patiño
Title: Consultor del Api del Banco de México 
Created: 2024
'''
import pandas as pd 
import requests
import json
import textwrap

#* Clase API INEGI
class banco_de_indicadores: 
    '''
    Pide el Token del INEGI
    
    Parameters
    ___________________________________________________________________________
    Api token: str 
    - If you don't have the api key you can get in this url
    https://www.inegi.org.mx/app/desarrolladores/generatoken/Usuarios/token_Verify
    '''
    root_url='https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/'
    
    #* Token Cheking
    def __init__(self, api_token = None):
        self.api_token = None
        if api_token is not None: 
            self.api_token = api_token
            
        else: 
            raise ValueError(
                textwrap.dedent( '''The api key is missing if you don't have you get in  \n https://www.inegi.org.mx/app/desarrolladores/generatoken/Usuarios/token_Verify''' ))
 

    #* Numero de variables
    def __n_var(self, var): 
        '''
        Numero de variables 
        
        Parameters 
        ___________________________________________________________________________
        - Var: Varibles
        
        Returns 
        ___________________________________________________________________________
        - n: Number of variables
        
        Notes
        ___________________________________________________________________________
        Del str de las variables, las divide para contar cuantas son ya que el API
        del INEGI unicamente hacepta un maximo de 10 indicadores. 
        '''
        var_list = var.split(',')
        n = len( var_list)
        if n<= 10:
            return n
        else:
            
            raise ValueError('''Numero de variables no aceptadas''' ) 


    #* Consulta del API
    def __response(self, url): 
        ''' 
        Codijo 200 te da la consulta
        
        Parameters 
        ___________________________________________________________________________
        - url: str 
        
        Returns 
        ___________________________________________________________________________
        - content: dict
        '''
        # Solitud del API
        response = requests.get(url)
        if response.status_code == 200:
            content = json.loads(response.content)
        return content
    
    #* Pasar de Diccionario a data frame
    def __from_dict_to_df( self, content, n):
        '''
        Pasa de dictionario a DataFrame
        
        Parameters 
        ___________________________________________________________________________
        - n: int, number of varibles
        - content: dict, Consulta en bruto
        
        Parameters 
        ___________________________________________________________________________
        - data: Dataframe
        
        Notes
        ___________________________________________________________________________
        Los datos tiene diferentes periodicadad entonces, las variables con un 
        menor rango van a tener nan en las ultimas observaciones
        
        '''
        for x in range(0,n,1):
            id_serie = content['Series'][x]['INDICADOR']
            if x == 0:
                series = content['Series'][x]['OBSERVATIONS']
                data = pd.DataFrame(series, columns=['TIME_PERIOD', 'OBS_VALUE'])
                data = data.rename(columns={data.columns[x+1]: str(id_serie) })
            else:
                series = content['Series'][x]['OBSERVATIONS']
                data[str(x)] = pd.DataFrame(series, columns=['OBS_VALUE'])
                data = data.rename(columns={data.columns[x+1]: str(id_serie) })  
        return data


    #* Darle Formato al Frame
    def __format_df(self, data):
        '''
        Le da formato al data frame
        
        Parameters 
        ___________________________________________________________________________
        - data: Dataframe 
        
        Returns
        ___________________________________________________________________________
        - data: Dataframe
        
        Notes
        ___________________________________________________________________________
        A las variables las vuelve numericas, las ordena de inicio a fin y los valores
        tiempo los pasa a datetime, por la gran diversidad en la que se mide la 
        temporalidad puede salir error al tranformar los datos pero time period 
        sigue manteninde el formato de datetime.
        '''
        data1 = data.iloc[:,:1]
        data2 = data.iloc[:, 1:].apply(pd.to_numeric)
        data = data1.join(data2)
        data = data.sort_values(by='TIME_PERIOD').reset_index(drop = True) 
        
        data['TIME_PERIOD'] = pd.to_datetime(data['TIME_PERIOD'])
        return data

    #* Renombra las variables
    def __rename(self, name, data):
        ''' 
        Renombra las variables 
        
        Parameters 
        ___________________________________________________________________________
        - name: List de las variables a renombrar 
        - data: Dataframe
        
        Returns
        ___________________________________________________________________________
        - data: dataframe
        '''
        lt1 = ['fecha']
        lt1.extend(name)

        # verificador de que el nombres igual a varibles consultados
        if len(lt1) != len(data.columns):
            raise ValueError("Los nombres son diferentes al total de las variables")

        # Cambio de las columnas
        data.columns = lt1[:len(data.columns)] 
        return data
    
    #* Filtrar los datos
    def __filter_time(self, data, end= None, start = None):
        ''' 
        Filtra la consulta histórica según los parámetros de start y end  
        
        Parameters
        ___________________________________________________________________________
        - Data: Dataframe 
        - start: rango superior de la conuslta
        - End: rango superior de la conuslta
        
        Returns
        ___________________________________________________________________________
        - Data: Filter Data by time
        '''
        if start is not None:
            data = data.loc[(data['TIME_PERIOD'] >= start)].reset_index(drop=True)
        if end is not None:
            data = data.loc[(data['TIME_PERIOD'] <= end)]
        return data
    
    # TODO: Consultor 
    def request (self, var = 'str', bank ='BIE|BISE',  name = None, start =None,
                 end = None):
        '''
        El script te saca las variables a nivel historico, normalmente empieza en 1993. 
        
        Parameters
        ___________________________________________________________________________
        - var: str, son las cadenas de numeros que te saca el buscador del INEGI
        - Banco: str: BIE (Banco de indicadores economico) |BISE (Banco de Indicadores)
        - start: None,(opcional) YYYY-MM-DD fecha de inicio del perido consulta
        - end: None, (opcional) YYYY-MM-DD fecha de final del perido consulta
        - name: None, (opcional) Nombre de las variables
        
        Returns
        ___________________________________________________________________________
        data: DataFrame de las variables consutladas
        
        Notes
        ___________________________________________________________________________
        - El script hace consultas de nivel nacional 
        - Consulta a nivel historico 
        - El numero maximo de variables es 10 
        '''
        
        #Variables
        self.var = var
        self.bank = bank
        self.name = name
        self.end = end 
        self.start = start 

        # Url de consulta
        url = self.root_url + self.var + '/es/0700/false/'+self.bank +'/2.0/'+self.api_token+'?type=json'
        
        # Uso de las definciones
        n = self.__n_var(self.var)
        content = self.__response(url)
        data = self.__from_dict_to_df(content, n) 
        data = self.__format_df( data )
        data = self.__filter_time(data, self.end, self.start)
        if name is not None:
            data = self.__rename(self.name, data) 
        return data