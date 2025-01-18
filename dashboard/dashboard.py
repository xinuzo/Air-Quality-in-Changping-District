import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set seaborn style
sns.set(style='darkgrid')

# Load data
data = pd.read_csv("all_data.csv")

# Rename columns for consistency (if needed)
data.rename(columns={
    'year': 'Year',
    'month': 'Month',
    'day': 'Day',
    'hour': 'Hour',
    'O3': 'Ozone',
    'TEMP': 'Temperature'
}, inplace=True)

# Sidebar: Filter data by year
st.sidebar.header("Filter Data")
years = sorted(data['Year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

# Filter data for the selected year
filtered_data = data[data['Year'] == selected_year]

# Header
st.title("Visualisasi Data Ozone (O3) dan Temperatur")
st.subheader(f"Data Tahun {selected_year}")

# Line plot for Ozone levels
st.subheader("Level Ozone (O3) Harian")
daily_ozone = filtered_data.groupby(['Month', 'Day'])['Ozone'].mean().reset_index()
daily_ozone['Date'] = pd.to_datetime(daily_ozone[['Month', 'Day']].assign(year=selected_year))

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_ozone['Date'], daily_ozone['Ozone'], label="Ozone (O3)", color='blue')
ax.set_title("Level Ozone Harian", fontsize=16)
ax.set_xlabel("Tanggal", fontsize=12)
ax.set_ylabel("Konsentrasi Ozone (µg/m³)", fontsize=12)
ax.legend()
st.pyplot(fig)

# Line plot for Temperature
st.subheader("Temperatur Harian")
daily_temperature = filtered_data.groupby(['Month', 'Day'])['Temperature'].mean().reset_index()
daily_temperature['Date'] = pd.to_datetime(daily_temperature[['Month', 'Day']].assign(year=selected_year))

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_temperature['Date'], daily_temperature['Temperature'], label="Temperature (°C)", color='orange')
ax.set_title("Temperatur Harian", fontsize=16)
ax.set_xlabel("Tanggal", fontsize=12)
ax.set_ylabel("Temperatur (°C)", fontsize=12)
ax.legend()
st.pyplot(fig)

# Correlation heatmap between Ozone and Temperature
st.subheader("Korelasi antara Ozone dan Temperatur")
corr = filtered_data[['Ozone', 'Temperature']].corr()

fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax, fmt=".2f")
ax.set_title("Heatmap Korelasi", fontsize=16)
st.pyplot(fig)
