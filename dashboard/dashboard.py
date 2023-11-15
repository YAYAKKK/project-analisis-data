import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

all_df = pd.read_csv("all_data.csv")

sns.set(style='darkgrid')
with st.sidebar:
    # Menambahkan logo agar terlihat lebih formal
    st.image("https://www.logolynx.com/images/logolynx/56/56afea50b83164e3e272d4ebeccd94fb.png")

# Membuat fungsi untuk dashboard produk terlaris dan terburuk
def best_worst_dashboard(df):
    frameCatt = df.groupby("product_category_name_english")["order_id"].count().reset_index(name="orders")

    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 12))

    colors = ["#102cd4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    # Bar plot untuk Produk Terbaik
    sns.barplot(x="orders", y="product_category_name_english", data=frameCatt.sort_values(by="orders", ascending=False).head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Produk Terbaik", loc="center", fontsize=15)
    ax[0].tick_params(axis='y', labelsize=12)

    # Bar plot untuk Produk Terburuk
    sns.barplot(x="orders", y="product_category_name_english", data=frameCatt.sort_values(by="orders", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Produk Terburuk", loc="center", fontsize=15)
    ax[1].tick_params(axis='y', labelsize=12)

    for p in ax[1].patches:
        ax[1].annotate("", (p.get_width() + 0.5, p.get_y() + p.get_height() / 2), ha='left', va='center', fontsize=12, color='black')

    plt.suptitle("PRODUK TERBAIK DAN TERBURUK", fontsize=20)

    st.pyplot(fig)

# Membuat fungsi untuk payment atau pembayaran
def payment_dashboard(df):
    payment_mean = df.groupby(by="payment_type").payment_value.mean().sort_values(ascending=False)
    order_count = df.groupby(by='payment_type').order_id.count().sort_values(ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

    # Plot pertama untuk rata-rata payment_value
    sns.barplot(x=payment_mean / payment_mean.sum() * 100, y=payment_mean.index, palette='viridis', ax=ax1)
    ax1.set_title('Rata-rata Payment Value untuk Setiap Jenis Pembayaran')
    ax1.set_xlabel('Persentase Rata-rata Payment Value')
    ax1.set_ylabel('Tipe Pembayaran')

    for i, v in enumerate(payment_mean / payment_mean.sum() * 100):
        ax1.text(v + 2, i, f'{v:.0f}%', color='black', ha='left', va='center')

    # Plot kedua untuk jumlah order
    sns.barplot(x=order_count / order_count.sum() * 100, y=order_count.index, palette='viridis', ax=ax2)
    ax2.set_title('Persentase Jumlah Order untuk Setiap Jenis Pembayaran')
    ax2.set_xlabel('Persentase Jumlah Order')
    ax2.set_ylabel('Tipe Pembayaran')

    for i, v in enumerate(order_count / order_count.sum() * 100):
        ax2.text(v + 2, i, f'{v:.0f}%', color='black', ha='left', va='center')

    plt.tight_layout()
    st.pyplot(fig)

# Membuat fungsi untuk demografi customer
def customer_dashboard(df):
    fig_state, ax_state = plt.subplots(figsize=(8, 6))
    state_counts = df.groupby(by='customer_state').customer_id.nunique().sort_values(ascending=False).head(10)
    state_counts.plot(kind='bar', color='skyblue', ax=ax_state)
    ax_state.set_title('Jumlah Pelanggan Berdasarkan State')
    ax_state.set_xlabel('State')
    ax_state.set_ylabel('Jumlah Pelanggan')
    ax_state.tick_params(axis='x', rotation=45)

    st.pyplot(fig_state)

    fig_city, ax_city = plt.subplots(figsize=(8, 6))
    city_counts = df.groupby(by='customer_city').customer_id.nunique().sort_values(ascending=False).head(10)
    city_counts.plot(kind='bar', color='lightcoral', ax=ax_city)
    ax_city.set_title('Top 10 Kota dengan Jumlah Pelanggan Terbanyak')
    ax_city.set_xlabel('Kota')
    ax_city.set_ylabel('Jumlah Pelanggan')
    ax_city.tick_params(axis='x', rotation=45)

    st.pyplot(fig_city)

st.title('E-Commerce Dashboard:sparkles')

# Sidebar navigation
page_options = ["Semua Chart", "Produk Terlaris dan Terburuk", "Rata-rata Pembayaran dan Tipe Pembayaran Terbanyak", "Customer Berdasarkan Kota dan State"]
selected_page = st.sidebar.selectbox("Pilih Dashboard", page_options)

if selected_page == "Semua Chart":
    st.subheader("Semua Chart")
    best_worst_dashboard(all_df)
    payment_dashboard(all_df)
    customer_dashboard(all_df)
elif selected_page == "Produk Terlaris dan Terburuk":
    st.subheader("Dashboard Produk Terbaik dan Terburuk")
    best_worst_dashboard(all_df)
elif selected_page == "Rata-rata Pembayaran dan Tipe Pembayaran Terbanyak":
    st.subheader("Dashboard Rata-rata Pembayaran dan Tipe Pembayaran Terbanyak")
    payment_dashboard(all_df)
elif selected_page == "Customer Berdasarkan Kota dan State":
    st.subheader("Dashboard Pelanggan Berdasarkan Kota dan State")
    customer_dashboard(all_df)

