import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Crisis Dashboard",
    page_icon="🌍",
    layout="wide",
)


st.image("Crisis.webp",width=700)

# Example dataset with random data
@st.cache_data
def get_data():
    '''data = {
        'date': pd.date_range(start='2023-04-10', periods=100, freq='D'),
        'time': pd.date_range(start='2023-04-10', periods=100, freq='H').time,
        'location': np.random.choice(['London', 'Russia', 'Ukraine'], size=100),
        'category': np.random.choice(['Earthquake', 'Flood', 'Fire'], size=100),
        'text': np.random.choice(['boy', 'word', 'choice'], size=100)
    }

    df = pd.DataFrame(data)'''
    df = pd.read_csv("C:\\Users\\Salami\\Documents\\final_data.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date
    return df

df = get_data()

# dashboard title
st.title("Crisis Dashboard")

# top-level filters
#default_date = pd.to_datetime('2023-04-10').date()


st.sidebar.header("Please Filter here: ")

min_date = min(df['date'])
max_date = max(df['date'])
default_date = min_date + (max_date - min_date) // 2 

selected_date = st.sidebar.date_input("Select Date", min_value=min_date, max_value=max_date, value=default_date)

# Use a slider for selecting time
df['time'] = pd.to_datetime(df['time']).dt.time



unique_times = df['time'].unique()
min_time, max_time = min(unique_times), max(unique_times)
selected_time = st.sidebar.slider("Select Time", min_value=min_time, max_value=max_time)

# Filter the data based on selected date and time
df_selection=df.query("date==@selected_date & time==@selected_time")
st.dataframe(df_selection)


# Fill in the second column with the world map
fig = px.scatter_geo(df_selection, locationmode="country names", locations="country", text=None,
                     color="categories", color_continuous_scale="RdYlGn",
                     title=f"World Map of crisis occurences on {selected_date} at {selected_time}")

#
# Update existing traces on the map
fig.update_traces(marker=dict(size=10))
fig.update_geos(projection_type="natural earth")
st.plotly_chart(fig)
#use_container_width=True

# display detailed data view
st.markdown("### Detailed Data View")
st.dataframe(df)
