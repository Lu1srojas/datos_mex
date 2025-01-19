from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup( 
    name='datos_mex',
    version='1.0.3',
    description='Consultor del api del Banco de México y del Instituto Nacional de Estadística y Geografía',
    author='Luis Manuel Rojas Patiño',
    author_email='luisrojaspatino5@gmail.com',
    packages=['datos_mex', 'datos_mex.banxico', 'datos_mex.inegi', 'datos_mex.data_format'],
    include_package_data=True,
    #package_dir={"":'datos_mex'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url= 'https://github.com/Lu1srojas/data_mx',

)
