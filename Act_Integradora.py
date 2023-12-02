# UF-6 Actividad Integradora M6
# Luis Javier González Romero - A01702728

# Librerías
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Formato de página
st.title(':red[Police Incident Reports from 2018 to 2020 in San Francisco]')
st.markdown('The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.')

# Cargar datos
df = pd.read_csv('Police.csv')

# Filtrar datos relevantes y eliminar datos nulos
mapa = df[['Incident Date', 'Incident Day of Week', 'Police District', 'Analysis Neighborhood', 'Incident Category', 'Incident Subcategory', 'Resolution', 'Latitude', 'Longitude']]
mapa.columns = ['Date','Day','Police District','Neighborhood','Incident Category',
                'Incident Subcategory','Resolution','lat','lon']
mapa = mapa.dropna()

subset_data = mapa

# Siderbar para seleccionar filtros
st.sidebar.title(':red[Filters]')
police_district_input = st.sidebar.multiselect('Police District', subset_data['Police District'].unique())
neighborhood_input = st.sidebar.multiselect('Neighborhood', subset_data['Neighborhood'].unique())
incident_input = st.sidebar.multiselect('Incident Category', subset_data['Incident Category'].unique())
incident_sub_input = st.sidebar.multiselect('Incident Subcategory', subset_data['Incident Subcategory'].unique())
resolution_input = st.sidebar.multiselect('Resolution', subset_data['Resolution'].unique())

# Aplicar filtros a DataFrame
if police_district_input:
    subset_data = subset_data[subset_data['Police District'].isin(police_district_input)]
if neighborhood_input:
    subset_data = subset_data[subset_data['Neighborhood'].isin(neighborhood_input)]
if incident_input:
    subset_data = subset_data[subset_data['Incident Category'].isin(incident_input)]
if incident_sub_input:
    subset_data = subset_data[subset_data['Incident Subcategory'].isin(incident_sub_input)]
if resolution_input:
    subset_data = subset_data[subset_data['Resolution'].isin(resolution_input)]

# Ordenar los días de la semana (Al graficar aparecen en orden)
days_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
subset_data['Day'] = pd.Categorical(subset_data['Day'], categories=days_order, ordered=True)

# Mostrar los datos filtrados
st.title(':red[Filtered Incidents Data]')
subset_data

# Gráfico tipo mapa de los incidentes
st.title(':red[Map of Police Incidents]')
fig = px.scatter_mapbox(subset_data, lat='lat', lon='lon', hover_name='Incident Category', hover_data=['Incident Subcategory', 'Resolution'],
                        color='Police District', zoom=10)
fig.update_layout(mapbox_style='carto-positron')
st.plotly_chart(fig)

# Gráfico de barras de incidentes por distrito policial
st.title(':red[Incidents by Police District]')
fig_police_district = px.bar(subset_data, x='Police District', color='Resolution')
st.plotly_chart(fig_police_district)

# Gráfico de barras de incidentes por día de la semana
st.title(':red[Incidents by Day of the Week]')
fig_day_of_week = px.bar(subset_data.sort_values('Day'),x='Day',color='Police District', labels={'Day': 'Day of Week'})
st.plotly_chart(fig_day_of_week)

# Gráfico de barras de tipos de incidentes
st.title(':red[Total Incidents by Category]')
fig_incident_type = px.bar(subset_data, x='Incident Category')
st.plotly_chart(fig_incident_type)

# Gráfico tipo pie de resoluciones de incidentes
st.title(':red[Incidents by Resolutions]')
labels = subset_data['Resolution'].unique()
values = subset_data['Resolution'].value_counts()
fig_resolution = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.6)])
st.plotly_chart(fig_resolution)






