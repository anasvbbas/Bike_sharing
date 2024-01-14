import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Memuat data
hour_df = pd.read_csv("hour.csv")
day_df = pd.read_csv("day.csv")
min_date = pd.to_datetime(day_df["dteday"].min())
max_date = pd.to_datetime(day_df["dteday"].max())
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang waktu yang dipilih
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date))]

day_df['total_rent'] = day_df['casual'] + day_df['registered']
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Melakukan pengelompokan dan perhitungan total_rent per bulan
monthly_rent = day_df.groupby(day_df['dteday'].dt.to_period('M'))['total_rent'].sum().reset_index()
monthly_rent['dteday'] = monthly_rent['dteday'].astype(str)
main_df['total_rent'] = main_df['casual'] + main_df['registered']

# Fungsi untuk melakukan plot
def plot_monthly_rent(monthly_rent, start_date, end_date):
    filtered_data = monthly_rent[
        (monthly_rent["dteday"] >= start_date) & (monthly_rent["dteday"] <= end_date)
    ]

    plt.figure(figsize=(10, 5))
    plt.plot(
        filtered_data["dteday"],
        filtered_data["total_rent"],
        marker='o',
        linewidth=2,
        color="#72BCD4"
    )
    plt.title("Total Rent per Month", loc="center", fontsize=20)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Total Rent", fontsize=12)
    plt.xticks(fontsize=10, rotation=45)
    plt.yticks(fontsize=10)
    plt.grid(True)
    
    # Simpan plot sebagai gambar
    plt.savefig("monthly_rent_plot.png")
    
    return plt

# Menampilkan grafik di Streamlit
st.title('Total Rent per Month')
filtered_monthly_rent = day_df.groupby(day_df['dteday'].dt.to_period('M'))['total_rent'].sum().reset_index()
filtered_monthly_rent['dteday'] = filtered_monthly_rent['dteday'].astype(str)
filtered_plot = plot_monthly_rent(filtered_monthly_rent, str(start_date), str(end_date))
st.image("monthly_rent_plot.png")

# Fungsi untuk membuat plot jumlah pelanggan berdasarkan musim
# Fungsi untuk membuat plot jumlah pelanggan berdasarkan musim
def plot_season_rent(day_df):
    day_df["season"] = day_df.season.apply(
        lambda x: "Spring" if x == 1 else ("Summer" if x == 2 else ("Fall" if x == 3 else ("Winter" if x == 4 else "Unknown")))
    )
    season = day_df.groupby(by="season")["total_rent"].sum().reset_index()

    plt.figure(figsize=(10, 5))
    colors = ['#72BCD4', '#FFA07A', '#90EE90', '#FFD700']  # Atur warna untuk setiap musim
    sns.barplot(
        x="season",
        y="total_rent",
        data=season.sort_values(by="total_rent", ascending=False),
        palette=colors
    )
    plt.title("Total Rent by Season", loc="center", fontsize=15)
    plt.xlabel("Season")
    plt.ylabel("Total Rent")
    plt.xticks(rotation=45)
    plt.grid(True)
    
    # Simpan plot sebagai gambar
    plt.savefig("season_plot.png")
    
    return plt

# Menampilkan grafik di Streamlit
st.title('Total Rent by Season')
filtered_season_plot = plot_season_rent(main_df)
st.image("season_plot.png")


# Fungsi untuk membuat plot jumlah pelanggan berdasarkan hari kerja/libur
def plot_workingday_rent(day_df):
    day_df["workingday"] = day_df.workingday.apply(
        lambda x: "Working Day" if x == 1 else ("Holiday" if x == 0 else "Unidentified")
    )
    workingday = day_df.groupby(by="workingday")["total_rent"].sum().reset_index()

    plt.figure(figsize=(10, 5))
    colors = ['#72BCD4', '#FFA07A', '#90EE90', '#FFD700']  # Atur warna untuk setiap hari
    sns.barplot(
        x="workingday",
        y="total_rent",
        data=workingday.sort_values(by="total_rent", ascending=False),
        palette=colors
    )
    plt.title("Total Rent by Working Day/Holiday", loc="center", fontsize=15)
    plt.xlabel("Day")
    plt.ylabel("Total Rent")
    plt.grid(True)
    
    # Simpan plot sebagai gambar
    plt.savefig("workingday_plot.png")
    
    return plt

# Menampilkan grafik di Streamlit
st.title('Total Rent by Working Day/Holiday')
filtered_workingday_plot = plot_workingday_rent(main_df)
st.image("workingday_plot.png")

filtered_df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]

# Assign temperature categories based on temperature values
filtered_df["temp"] = filtered_df["temp"]*41 
filtered_df["temp_category"] = filtered_df["temp"].apply(
    lambda x: "Cold" if x <= 15 else ("Moderate" if x <= 25 else ("Hot" if x <= 41 else "Extreme")))
  
# Group by temperature categories and calculate total rent
temp = filtered_df.groupby(by="temp_category")["total_rent"].sum().reset_index()

# Create bar chart
st.title('Total Rent by Temperature')
plt.figure(figsize=(10, 5))
colors = ['#72BCD4', '#FFA07A', '#90EE90', '#FFD700']
sns.barplot(
    x="temp_category",
    y="total_rent",
    data=temp.sort_values(by="total_rent", ascending=False),
    palette=colors
)
plt.title("Total Rent by Temperature", loc="center", fontsize=15)
plt.xlabel("Temperature")
plt.ylabel("Total Rent")

# Display the plot in Streamlit
st.pyplot()
# Menampilkan grafik di Streamlit
st.title('Total rent by hour')
if 'total_rent' not in hour_df.columns:
    hour_df['total_rent'] = hour_df['casual'] + hour_df['registered']


# Fungsi untuk melakukan plot
def plot_hourly_rent(hour_df):
    plt.figure(figsize=(10, 6))

    sns.barplot(x="hr", y="total_rent", data=hour_df, palette='tab10')
    plt.ylabel("Total Rent")
    plt.xlabel("Hour")
    plt.title("Total Rent by Hour", loc="center", fontsize=15)
    plt.xticks(rotation=45)  # Memutar label sumbu x untuk memudahkan pembacaan jam

    return plt

# Menampilkan grafik di Streamlit
st.pyplot(plot_hourly_rent(hour_df))