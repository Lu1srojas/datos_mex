# Datos Mex

`datos_mex` es una librería construida en Python con la finalidad de consultar datos públicos de México, para el Api del Banco de México ([Banxico](https://www.banxico.org.mx/SieAPIRest/service/v1/)) y el Instituto Nacional de Estadística  y Geografía ([INEGI](https://www.inegi.org.mx/servicios/api_indicadores.html)) . Estas dos instituciones publican información de la economía real como financiera.

`datos_mex` esta construida a partir de `pandas` por lo que las consultas retornadas son `pd.Dataframe()`, teniendo asi integración con otras librerías como `Matplotlib`, `Seaborn` o `Statsmodels`.

## Tabla de contenidos

* [Banco de México](#api-banco-de-méxico)
  * [SIE](#sistema-de-información-económica-sie): Sistema de Información Económica
* [INEGI](#api-inegi): Instituto Nacional de Estadistica, Geografia e Informatica
  * [BIE](#banco-de-indicadores-bise): Banco de Información Económica
  * [BISE](#banco-de-indicadores-bise): Banco de Indicadores
* [Otras Funciones](#otras-funciones)  
  * [Rename](#rename): Renombra las variables
  * [Group by time](#group_by_time): Agrupa los datos según el año o mes

## API INEGI

Puedes obtener un Token en la siguiente [URL](https://www.inegi.org.mx/app/api/denue/v1/tokenVerify.aspx), mientras que los indicadores los puedes consultar en [API](https://www.inegi.org.mx/servicios/api_indicadores.html), en la misma página se consultan tanto el BIE y BISE.

### Banco de Información Económica (BIE)

En el BIE se encuentra información del PIB por el lado de la demanda y de la oferta, Índices de precios, Cuentas nacionales, Tasas de ocupación y desocupación, así como Encuestas periódicas que realiza esta institución como la ENOE, EMOE, EMIM, ENEC, entre otros.

#### Ejemplo PIB y sectores económicos  

##### Consulta parámetros obligatorios

Indicadores:

* Producto Interno Bruto: 735879
* Actividades primarias: 735882
* Actividades secundarias: 735883
* Actividades terciarias: 735888

```python
from datos_mex.inegi import banco_de_indicadores

# Parametros 
token= 'tu token'
indbie = '735879,735882,735883,735888'

# Consulta 
inegi = banco_de_indicadores(token)
bie1 = inegi.request(var=indbie, bank='BIE')
bie1.head()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TIME_PERIOD</th>
      <th>735879</th>
      <th>735882</th>
      <th>735883</th>
      <th>735888</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1980-01-01</td>
      <td>1.040137e+07</td>
      <td>419192.590</td>
      <td>4014172.291</td>
      <td>5383811.941</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1980-02-01</td>
      <td>1.034235e+07</td>
      <td>386092.639</td>
      <td>4003454.651</td>
      <td>5369491.411</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1980-03-01</td>
      <td>1.039273e+07</td>
      <td>424698.389</td>
      <td>4131481.268</td>
      <td>5257710.872</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1980-04-01</td>
      <td>1.092767e+07</td>
      <td>412868.415</td>
      <td>4149062.192</td>
      <td>5745881.173</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1981-01-01</td>
      <td>1.134585e+07</td>
      <td>438850.326</td>
      <td>4412239.779</td>
      <td>5856656.820</td>
    </tr>
  </tbody>
</table>

##### Consulta no parámetros obligatorios

```python
# Parametros 
name = ['pib', 'act_1', 'act_2', 'act_3']
inicio = '2018-04-01' 
fin = '2022-01-01' 

# Consulta 
bie2 = banco_de_indicadores(token).request(var=indbie, bank='BIE', name=name, start = inicio, end = fin)
bie2.head()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fecha</th>
      <th>pib</th>
      <th>act_1</th>
      <th>act_2</th>
      <th>act_3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>9</th>
      <td>2021-01-01</td>
      <td>2.284084e+07</td>
      <td>758035.123</td>
      <td>7265140.515</td>
      <td>1.360932e+07</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2021-02-01</td>
      <td>2.362332e+07</td>
      <td>872394.447</td>
      <td>7396306.801</td>
      <td>1.406373e+07</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2021-03-01</td>
      <td>2.320473e+07</td>
      <td>720485.108</td>
      <td>7417864.609</td>
      <td>1.381038e+07</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2021-04-01</td>
      <td>2.395044e+07</td>
      <td>957920.499</td>
      <td>7449600.892</td>
      <td>1.427720e+07</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2022-01-01</td>
      <td>2.344404e+07</td>
      <td>762523.258</td>
      <td>7576903.255</td>
      <td>1.381633e+07</td>
    </tr>
  </tbody>
</table>

### Banco de indicadores (BISE)

En el BISE resume los indicadores más importantes de las encuestas recabadas por el INEGI como, por ejemplo:

* ENIGH (Encuesta de Ingreso y Gasto de los Hogares) el ingreso promedio trimestral por hogar según el decil.
* Censos de población destaca población total, por género o rango de edades.

También hay variables cualitativas de Educación, Economía, Geografía, Gobierno y Salud.

#### Ejemplo: Población

**Indicadores:**

* Población total: 1002000001

```python
# Parametros
indbise = '1002000001' 
name = ['pop_tot']

# Consulta 
bise = inegi.request(var=indbise, bank='BISE', name=name)
bise.tail()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fecha</th>
      <th>pop_tot</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10</th>
      <td>2000-01-01</td>
      <td>97483412.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2005-01-01</td>
      <td>103263388.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2010-01-01</td>
      <td>112336538.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2015-01-01</td>
      <td>119938473.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2020-01-01</td>
      <td>126014024.0</td>
    </tr>
  </tbody>
</table>

## API Banco de México

Puedes obtener un Token en la siguiente [URL](https://www.banxico.org.mx/SieAPIRest/service/v1/token), mientras que los indicadores los puedes consultar en [API](https://www.banxico.org.mx/SieAPIRest/service/v1/)

### Sistema de información Económica (SIE)

En el SIE principalmente se puede encontrar información financiera como Tasas de interés, UDIS, Base Monetaria, Tipo de Cambio, Subastas de Valores o Encuestas realizadas por esta institución, así como el índice de precios, PIB o Indicadores laborales que son elaborados por otras instituciones.

#### Ejemplo: Consulta de la Base Monetaria, Crédito Interno y Activos Internacionales

**Indicadores:**

* Base Monetaria (BM): SF43703
* Activos Internacionales (AIC): SF43704
* Crédito Interno (CIN): SF43706

```python
### Token
from datos_mex.banxico import sie
tokenbm = 'tu token'

# A partir de esta se realiza la consulta 
banxico = sie(tokenbm)

# Indicadores 
var = 'SF43703,SF43704,SF43706'

# Consulta 
bm = banxico.request(var= var)
bm.tail()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fecha</th>
      <th>Crédito Interno Neto</th>
      <th>Base Monetaria</th>
      <th>Activos Internacionales Netos</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1512</th>
      <td>2024-12-13</td>
      <td>-1455509.3</td>
      <td>3223066.4</td>
      <td>4678575.7</td>
    </tr>
    <tr>
      <th>1513</th>
      <td>2024-12-20</td>
      <td>-1399500.7</td>
      <td>3254478.2</td>
      <td>4653978.9</td>
    </tr>
    <tr>
      <th>1514</th>
      <td>2024-12-27</td>
      <td>-1403433.5</td>
      <td>3294743.7</td>
      <td>4698177.2</td>
    </tr>
    <tr>
      <th>1515</th>
      <td>2025-01-03</td>
      <td>-1493095.0</td>
      <td>3304980.1</td>
      <td>4798075.1</td>
    </tr>
    <tr>
      <th>1516</th>
      <td>2025-01-10</td>
      <td>-1497493.5</td>
      <td>3298100.4</td>
      <td>4795593.9</td>
    </tr>
  </tbody>
</table>

## Otras Funciones

Estos son una serie de códigos auxiliares que facilitan el procesamiento de las consultas.

### Rename

La función **rename** cambia los valores de los encabezados de un data frame mediante el index.

```python
### Libreria
from datos_mex.data_format import rename

### Renombrar variables 
names = ['fecha','BM', 'CIN', 'AIC']
bm = rename(bm, names)
bm.head()
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fecha</th>
      <th>BM</th>
      <th>CIN</th>
      <th>AIC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1995-12-29</td>
      <td>-264.4</td>
      <td>67073.1</td>
      <td>66808.6</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1996-01-05</td>
      <td>7304.2</td>
      <td>56069.6</td>
      <td>63373.8</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1996-01-12</td>
      <td>10199.0</td>
      <td>52025.7</td>
      <td>62224.7</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1996-01-19</td>
      <td>8593.1</td>
      <td>51371.0</td>
      <td>59964.1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1996-01-26</td>
      <td>8360.1</td>
      <td>49270.0</td>
      <td>57630.1</td>
    </tr>
  </tbody>
</table>

### Group_by_time

La función **group_by_time()** es un fork de la función pandas.DataFrame.groupby(), está únicamente funciona con consultas realizadas con esta librería. La finalidad de esta función es agrupar los datos según el mes o año.

```python
### Libreria
from datos_mex.data_format import group_by_time 

### Base Monetaria por meses 
bm_m = group_by_time(bm, False, 'mean')
bm_m.tail()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fecha</th>
      <th>BM</th>
      <th>CIN</th>
      <th>AIC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>345</th>
      <td>2024-09-01</td>
      <td>4525193.625</td>
      <td>-1453882.950</td>
      <td>3071310.675</td>
    </tr>
    <tr>
      <th>346</th>
      <td>2024-10-01</td>
      <td>4511781.675</td>
      <td>-1445313.150</td>
      <td>3066468.525</td>
    </tr>
    <tr>
      <th>347</th>
      <td>2024-11-01</td>
      <td>4664126.300</td>
      <td>-1537982.600</td>
      <td>3126143.700</td>
    </tr>
    <tr>
      <th>348</th>
      <td>2024-12-01</td>
      <td>4683622.925</td>
      <td>-1441827.175</td>
      <td>3241795.750</td>
    </tr>
    <tr>
      <th>349</th>
      <td>2025-01-01</td>
      <td>4796834.500</td>
      <td>-1495294.250</td>
      <td>3301540.250</td>
    </tr>
  </tbody>
</table>

**Nota:** Esta librería no asociada con el Banco de México o el Instituto Nacional de Estadística y Geografía.  
