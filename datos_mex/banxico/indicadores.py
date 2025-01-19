'''
Autor: Luis Manuel Rojas Patiño
Title: Consultor del Api del Banco de México 
'''
import pandas as pd 
import json
import requests
import textwrap 

class sie:
    '''
    Conusltor del Api del Banco de México
    '''        
    root_url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/'
    
    def __init__(self, api_token = None):
        '''
        Parametros
        ___________________________________________________________________________

        api_token: str
            Se tiene que ingresar el API de 
        '''    
        self.api_token = None
        if api_token is not None:
            self.api_token = api_token 
            self.url_token = '?token=' + self.api_token
            
        else: 
            raise ValueError(
                textwrap.dedent( '''Falta el Token, si no tiene uno pude consiguirlo en \n https://www.banxico.org.mx/SieAPIRest/service/v1/token''' ))
            
    #* Numero de variables
    def __n_vars(self, var ):
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
        del Banxico unicamente hacepta un maximo de 20 indicadores. 
        '''          
        var_list = var.split(',')
        n = len(var_list)
        if n<=20:
            return n
        else:
            raise ValueError('''Numero de variables no aceptadas''' )
    
    #* Consulta del API
    def __response (self):
        ''' 
        Codijo 200 te da la consulta
        
        Parameters 
        ___________________________________________________________________________
        - url: str 
        
        Returns 
        ___________________________________________________________________________
        - content: dict
        '''
        #Url del API de consulta 
        url = self.root_url + self.var + '/datos/' + self.start + '/' + self.end + self.url_token
        # Solitud del API
        response = requests.get(url)
        if response.status_code == 200:
            content = json.loads(response.content)
        return content 
    
    #*  Pasar de Diccionario a data frame
    def __from_dict_to_df(self, content, n):
        ''' 
        De dict a data frame 
        
        Parameters 
        ___________________________________________________________________________
        - n: int, number of varibles
        - content: dict, Consulta en bruto
        
        Returns  
        ___________________________________________________________________________
        - data: Dataframe
        
        Notes
        ___________________________________________________________________________
        Los datos tiene diferentes periodicadad entonces, las variables con un 
        menor rango van a tener nan en las ultimas observaciones
        
        '''
        # Bucle para pasar de un diccionario a Data Frame
        for x in range(0,n,1):
            
            # Nombre de la variable
            id_serie= content['bmx']['series'][x]['titulo']
            if x == 0 :
                series = content['bmx']['series'][x]['datos']
                data = pd.DataFrame(series, columns=['fecha', 'dato'])
                data = data.rename(columns= {data.columns[x+1]: str(id_serie)})
            else:
                series = content['bmx']['series'][x]['datos']
                data[str(x)] = pd.DataFrame(series, columns=['dato'])
                data = data.rename(columns={data.columns[x+1]:str(id_serie)})
        return data   

    #* Formato del Dataframe
    def __format_df ( self, data):
        '''
        Le da formato a los datos, en donde, a las observaciones de los indicadores
        se pasan de str a valores numericos.
        
        Parameters
        ___________________________________________________________________________

        Data: Data Frame
            Los datos en bruto de la cosnulta realizada

        Return
        ___________________________________________________________________________

        dta: Data Frame
        '''       
        data['fecha'] = pd.to_datetime(data['fecha'],format='%d/%m/%Y')
        
        columns = data.columns[1:]  
        for var in columns:
            data[var] = pd.to_numeric(data[var].str.replace(',', ''), errors='coerce')
        return data

    # TODO: Consultor 
    def request ( self,  var = 'str', start = None, end = None):
        
        """
        Consultor de API del Banco de Mexico    

        Parametros
        ___________________________________________________________________________
        - var: str | Ejemplo: 'SP68257,SF43718'
        - start (optional): YYYY-MM-DD | Year-Month-Day
        - end (optional): YYYY-MM-DD | Year-Month-Day
        
        Returns
        ___________________________________________________________________________
        data: DataFrame
            Regresa el data frame de la consulta realizada 
        
        Notes
        ___________________________________________________________________________
            - El API del Banco de Mexico tiene un máximo de 20 variables a consultar
            - No es necesario renombrar la id de los indicadores ya que el diccionario
            que te de vuelve al hacer la consulta ya contiene el titulo de la variable
        """
        # Informacion
        self.var = var
        self.start = start
        self.end = end
        
        if start is None: 
            self.start = '1950-1-1' 
        if  end is None: 
            self.end = '9999-12-31'
        # Uso de las definiciones
        n = self.__n_vars(self.var)
        content = self.__response()
        data = self.__from_dict_to_df(content, n)
        data = self.__format_df( data)
        return data 