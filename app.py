import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Rakshitha\Downloads\API_SP.POP.TOTL_DS2_en_csv_v2_571486\API_SP.POP.TOTL_DS2_en_csv_v2_571486.csv", skiprows=4)
    return df

data = load_data()

st.title("World Population Analysis")

# Sidebar for inputs
st.sidebar.header("Filter Options")

# Select country in sidebar
countries = data['Country Name'].unique()
selected_country = st.sidebar.selectbox('Select a country:', countries)

# Select year range in sidebar
start_year, end_year = st.sidebar.slider(
    'Select Year Range',
    min_value=1960,
    max_value=2024,
    value=(1960, 2024),
    step=1
)

# Filter data for selected country and years
country_data = data[data['Country Name'] == selected_country]

selected_years = list(range(start_year, end_year + 1))
populations = country_data.loc[:, str(start_year):str(end_year)].values.flatten()
df_pop = pd.DataFrame({'Year': selected_years, 'Population': populations}).set_index('Year')

# Calculate growth rates per decade within selection (only full decades)
growth_rates = []
decades = []
decade_start = (start_year // 10) * 10
decade_end = (end_year // 10) * 10
for year in range(decade_start, decade_end, 10):
    if year >= start_year and (year + 10) <= end_year:
        start_pop = country_data[str(year)].values[0]
        end_pop = country_data[str(year + 10)].values[0]
        growth_rate = ((end_pop - start_pop) / start_pop) * 100 if start_pop > 0 else 0
        growth_rates.append(growth_rate)
        decades.append(f'{year}-{year+10}')

# Cumulative growth
cumulative_pop = np.cumsum(np.maximum(populations - populations[0], 0))
df_cum = pd.DataFrame({'Year': selected_years, 'Cumulative Growth': cumulative_pop}).set_index('Year')

# Display charts and table stacked in main page
st.subheader(f'Population Trend for {selected_country}')
st.line_chart(df_pop)

if growth_rates and decades:
    st.subheader(f'Population Growth Rate per Decade (%) for {selected_country}')
    fig2, ax2 = plt.subplots()
    ax2.bar(decades, growth_rates, color='skyblue')
    ax2.set_ylabel('Growth Rate (%)')
    ax2.set_xlabel('Decade')
    ax2.set_title(f'Population Growth Rate (Decade) in {selected_country}')
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)

st.subheader(f'Cumulative Population Growth Since {start_year} for {selected_country}')
st.area_chart(df_cum)

st.subheader('Population Data Sample')
df_display = pd.DataFrame({'Year': selected_years, 'Population': populations})
st.dataframe(df_display.head(10))
