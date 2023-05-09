import pandas as pd
from sqlite3 import connect
import streamlit as st
from PIL import Image


#leer base de datos
conn = connect('ecsel_database.db')   
countries = pd.read_sql("SELECT * FROM countries",conn)
participants = pd.read_sql("SELECT * FROM participants",conn)
projects = pd.read_sql("SELECT * FROM projects",conn)

#llamar al objeto proyecto
from project import Project
ejercicio = Project(countries,participants,projects)



#create web page

#Header section
with st.container():
    image = Image.open('Imagen.png')
    st.image(image, caption='')
    st.title("Partner search tool")
    st.write("---")
    
#expander
st.header("Total Contribution per Year")
my_expander = st.expander(label="Expand me to see the Total Contribution per year")
with my_expander:    
    ejercicio.annual_grants2(ejercicio.annual_grants1(participants, projects))
    
st.write("---")

with st.container():
    st.header("Country Section")
    country_acronyms = {'Belgium': 'BE', 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany':
    'DE', 'Estonia': 'EE', 'Ireland': 'IE','Greece': 'EL', 'Spain': 'ES', 'France': 'FR', 'Croatia':
    'HR', 'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT','Luxembourg': 'LU',
    'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland': 'PL', 'Portugal':
    'PT','Romania': 'RO', 'Slovenia': 'SI', 'Slovakia': 'SK', 'Finland': 'FI', 'Sweden': 'SE'}
    keys = country_acronyms.keys()
    name_country = st.selectbox("Choose",keys)
    
    st.write('{} is the country you have chosen'.format(name_country))
    
    my_expander = st.expander(label="Expand me to see the Total Contribution of {} per year".format(name_country))
    with my_expander:    
        ejercicio.aportacion(participants, projects, name_country)

    

    #call the object contribution dataset
    ejercicio.contribution(participants, name_country)
    #call the object coordinators dataset
    ejercicio.coordinators(participants, name_country)



    #download contribution dataset
    Boton_Contribution = ejercicio.contribution(participants, name_country, a=True)
    @st.cache_data
    def convert_contribution(Boton_Contribution):
         return Boton_Contribution.to_csv().encode('utf-8')
    st.download_button(label="Download Contribution of {}".format(name_country),data=convert_contribution(Boton_Contribution), file_name='Contribution.csv', mime='text/csv',)

    #download coordinators dataset
    Boton_Coordinators = ejercicio.coordinators(participants, name_country,a=True)
    @st.cache_data  
    def convert_coordinators(Boton_Coordinators):
         return Boton_Coordinators.to_csv().encode('utf-8')
    st.download_button(label="Download Coordinators in  {}".format(name_country),data=convert_coordinators(Boton_Coordinators), file_name='Cordinators.csv', mime='text/csv',)













