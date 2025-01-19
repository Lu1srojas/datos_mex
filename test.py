'''
Autor: Luis Manuel Rojas Patiño 
Titulo: Prueba de la libreria data_mx
Fecha: 17/01/2025
'''

# Librerias 
import pandas as pd, seaborn as sns, matplotlib.pyplot as plt,numpy as np

#todo: API INEGI 

# Token 
from datos_mex.inegi import banco_de_indicadores
token= '713ad977-de9d-9fe8-1a8c-5ffb95ee93a6'
token= 'tu token'
inegi = banco_de_indicadores(token)

##* BIE
### Consulta con los parámetros obligatorios 

#### Indicadores 
indbie = '735879,735882,735883,735888'

#### Consulta 
bie1 = inegi.request(var=indbie, bank='BIE')
bie1.head()

'''
Consulta:
- Producto Interno Bruto: 735879 
- Actividades primarias: 735882
- Actividades secundarias: 735883
- Actividades terciarias: 735888

Nota: En caso de no especificar ningún uno parámetro se retorna la consulta global
'''

### Consulta con parámetros no obligatorios

#### Indicadores
name = ['pib', 'act_1', 'act_2', 'act_3']
inicio = '2018-04-01' 
fin = '2022-01-01' 

#### Consulta
bie2 = inegi.request(var=indbie, bank='BIE',name=name, start = inicio, end = fin)
bie2.tail()

#### Pequeño grafico
bie2 = pd.melt(bie2, id_vars='fecha')
sns.lineplot(bie2, x = 'fecha', y = 'value', hue='variable')

##* Banco de indicadores (BISE) 
### Consulta de la población total en los Estados Unidos Mexicanos

#### Indicadores
indbise = '1002000001' 
name = ['pop_tot']

#### Consulta 
bise = inegi.request(var=indbise, bank='BISE', name=name)
bise.tail()

#todo API Banco de Mexico
##* SIE

### Token
from datos_mex.banxico import sie
tokenbm = 'b5e3c6286b700cb562ab06fca14c02a366b3e0a215dc1c0868fbe470839b2171'
tokenbm = 'tu token'
banxico = sie(tokenbm)

### Valor de los UDIS
#### Parametros
start = '2010-1-1'
udis = 'SP68257'

#### Consulta 
udis = banxico.request(var= udis, start= start)
udis.tail()

'''
Notas: 
- Con el API del Banco de México no es necesario renombrar las consultas, debido a
que ya poseen  identificadores  
- Al momento de descargar datos desde el SIE puedes conocer el indicador de las
variables para el API, debido a que se encuentran dentro del .xlsx en la fila de fecha 
'''

#### Plot
sns.lineplot(udis, x ='fecha', y ='Valor de UDIS')

### Consulta de la  Base Monetaria, Crédito Interno y Activos Internacionales
var = 'SF43703,SF43704,SF43706'

bm = banxico.request(var= var)
bm.tail()

'''
Consulta:
- Base Monetaria: SF43703
- Activos Internacionales: SF43704
- Crédito Interno: SF43706
'''

bm = bm.melt(id_vars='fecha')
sns.lineplot(bm, x = 'fecha', y = 'value', hue='variable')


#todo: Auxiliar 

##* Renombrar

### Libreria
from datos_mex.data_format import rename

### Renombrar variables 
names = ['fecha','BM', 'CIN', 'AIC']
bm = rename(bm, names)
bm.tail()


##* Agrupar 
### Libreria
from datos_mex.data_format import group_by_time

### Base Monetaria por meses 
bm_m = group_by_time(bm, False, 'mean')
bm_m.tail()
