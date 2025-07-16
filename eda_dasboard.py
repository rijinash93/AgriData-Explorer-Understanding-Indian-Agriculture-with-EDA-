import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data.csv")

# Convert 1000 units to full values
df['MILLET PRODUCTION'] = (df['PEARL MILLET PRODUCTION (1000 tons)'] + df['FINGER MILLET PRODUCTION (1000 tons)']) * 1000

# Title
st.title("📊 Agricultural Production Dashboard - India (ICRISAT Data)")

# Sidebar Navigation
options = st.sidebar.selectbox(
    "Select Visualization",
    (
        "Millet Production (Last 50 Years)",
        "Sorghum Production (Kharif vs Rabi)",
        "Top 7 Groundnut Producing States",
        "Soybean Production and Yield Efficiency",
        "Oilseed Production in Major States",
        "Impact of Area on Production",
        "Rice vs Wheat Yield Comparison",
        "Top 7 Rice Producing States",
        "Top 5 Wheat Producing States (Bar + Pie)",
        "Top 5 Oilseed Producing States",
        "Top 7 Sunflower Producing States",
        "Sugarcane Production (Last 50 Years)",
        "Rice vs Wheat Production (Last 50 Years)",
        "Rice Production by West Bengal Districts",
        "Top 10 Wheat Production Years from UP"
    )
)


# 1. Millet Production
if options == "Millet Production (Last 50 Years)":
    st.subheader("📈 Millet Production (Last 50 Years)")
    millet = df.groupby('Year')['MILLET PRODUCTION'].sum().tail(50)
    fig, ax = plt.subplots()
    millet.plot(marker='o', color='green', ax=ax)
    ax.set_ylabel("Production (Tonnes)")
    ax.set_title("Millet Production Over the Years")
    st.pyplot(fig)

# 2. Sorghum by Season
elif options == "Sorghum Production (Kharif vs Rabi)":
    st.subheader("🌾 Sorghum Production by Season and State")
    kharif = df.groupby('State Name')['KHARIF SORGHUM PRODUCTION (1000 tons)'].sum()
    rabi = df.groupby('State Name')['RABI SORGHUM PRODUCTION (1000 tons)'].sum()
    sorghum = pd.DataFrame({'KHARIF': kharif, 'RABI': rabi}) * 1000
    sorghum = sorghum.sort_values(by='KHARIF', ascending=False).head(10)
    fig, ax = plt.subplots()
    sorghum.plot(kind='bar', stacked=True, colormap='Set2', ax=ax)
    ax.set_ylabel("Production (Tonnes)")
    ax.set_title("Top 10 States - Sorghum Production")
    st.pyplot(fig)

# 3. Groundnut
elif options == "Top 7 Groundnut Producing States":
    st.subheader("🥜 Groundnut Production - Top 7 States")
    groundnut = df.groupby('State Name')['GROUNDNUT PRODUCTION (1000 tons)'].sum().sort_values(ascending=False).head(7) * 1000
    fig, ax = plt.subplots()
    groundnut.plot(kind='bar', color='saddlebrown', ax=ax)
    ax.set_ylabel("Production (Tonnes)")
    ax.set_title("Top 7 Groundnut Producing States")
    st.pyplot(fig)

# 4. Soybean
elif options == "Soybean Production and Yield Efficiency":
    st.subheader("🌱 Soybean Production and Yield")
    soybean = df.groupby('State Name')[['SOYABEAN PRODUCTION (1000 tons)', 'SOYABEAN AREA (1000 ha)']].sum()
    soybean['YIELD'] = (soybean['SOYABEAN PRODUCTION (1000 tons)'] * 1000) / (soybean['SOYABEAN AREA (1000 ha)'] * 1000)
    top5 = soybean.sort_values(by='SOYABEAN PRODUCTION (1000 tons)', ascending=False).head(5)
    
    st.write("**Production**")
    fig1, ax1 = plt.subplots()
    top5['SOYABEAN PRODUCTION (1000 tons)'].plot(kind='bar', color='orange', ax=ax1)
    ax1.set_ylabel("Production (1000 tons)")
    ax1.set_title("Top 5 Soybean Producing States")
    st.pyplot(fig1)
    
    st.write("**Yield Efficiency**")
    fig2, ax2 = plt.subplots()
    top5['YIELD'].plot(kind='bar', color='olive', ax=ax2)
    ax2.set_ylabel("Yield (Tonnes/ha)")
    ax2.set_title("Soybean Yield Efficiency")
    st.pyplot(fig2)

# 5. Oilseed
elif options == "Oilseed Production in Major States":
    st.subheader("🛢️ Oilseed Production - Top 10 States")
    oilseed = df.groupby('State Name')['OILSEEDS PRODUCTION (1000 tons)'].sum().sort_values(ascending=False).head(10) * 1000
    fig, ax = plt.subplots()
    oilseed.plot(kind='bar', color='goldenrod', ax=ax)
    ax.set_ylabel("Production (Tonnes)")
    ax.set_title("Top 10 Oilseed Producing States")
    st.pyplot(fig)

# 6. Area vs Production
elif options == "Impact of Area on Production":
    st.subheader("📐 Area Cultivated vs Production (Rice, Wheat, Maize)")
    melted = pd.DataFrame({
        'AREA': pd.concat([
            df['RICE AREA (1000 ha)'],
            df['WHEAT AREA (1000 ha)'],
            df['MAIZE AREA (1000 ha)']
        ]) * 1000,
        'PRODUCTION': pd.concat([
            df['RICE PRODUCTION (1000 tons)'],
            df['WHEAT PRODUCTION (1000 tons)'],
            df['MAIZE PRODUCTION (1000 tons)']
        ]) * 1000,
        'CROP': ['Rice'] * len(df) + ['Wheat'] * len(df) + ['Maize'] * len(df)
    })
    g = sns.lmplot(data=melted, x='AREA', y='PRODUCTION', hue='CROP', height=5, aspect=1.5)
    st.pyplot(g.figure)

# 7. Yield Comparison
elif options == "Rice vs Wheat Yield Comparison":
    st.subheader("🍚 Rice vs 🌾 Wheat Yield Across States")
    yield_df = df.groupby('State Name')[['RICE YIELD (Kg per ha)', 'WHEAT YIELD (Kg per ha)']].mean().dropna()
    fig, ax = plt.subplots(figsize=(12, 6))
    yield_df.plot(kind='bar', ax=ax)
    ax.set_ylabel("Yield (Kg/ha)")
    ax.set_title("Average Yield Comparison - Rice vs Wheat")
    plt.xticks(rotation=90)
    st.pyplot(fig)
elif options == "Top 7 Rice Producing States":
    st.subheader("🍚 Top 7 Rice Producing States")
    top7_rice = df.groupby('State Name')['RICE PRODUCTION (1000 tons)'].sum().sort_values(ascending=False).head(7) * 1000
    fig, ax = plt.subplots()
    top7_rice.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title("Top 7 Rice Producing States")
    ax.set_ylabel("Rice Production (tons)")
    st.pyplot(fig)
elif options == "Top 5 Wheat Producing States (Bar + Pie)":
    st.subheader("🌾 Top 5 Wheat Producing States")

    top5_wheat = df.groupby('State Name')['WHEAT PRODUCTION (1000 tons)'].sum().sort_values(ascending=False).head(5)
    
    # Bar Chart
    st.write("**Bar Chart**")
    fig1, ax1 = plt.subplots()
    top5_wheat.plot(kind='bar', color='peru', ax=ax1)
    ax1.set_ylabel("Wheat Production (1000 tons)")
    ax1.set_title("Top 5 Wheat Producing States")
    st.pyplot(fig1)
    
    # Pie Chart
    st.write("**Pie Chart**")
    fig2, ax2 = plt.subplots()
    ax2.pie(top5_wheat, labels=top5_wheat.index, autopct='%1.1f%%', startangle=140)
    ax2.set_title("Wheat Production Share (%)")
    st.pyplot(fig2)
elif options == "Top 5 Oilseed Producing States":
    st.subheader("🛢️ Top 5 Oilseed Producing States")
    top5_oil = df.groupby('State Name')['OILSEEDS PRODUCTION (1000 tons)'].sum().sort_values(ascending=False).head(5) * 1000
    fig, ax = plt.subplots()
    top5_oil.plot(kind='bar', color='olive', ax=ax)
    ax.set_ylabel("Production (tons)")
    ax.set_title("Top 5 Oilseed Producing States")
    st.pyplot(fig)
elif options == "Top 7 Sunflower Producing States":
    st.subheader("🌻 Top 7 Sunflower Producing States")
    top7_sun = df.groupby('State Name')['SUNFLOWER PRODUCTION (1000 tons)'].sum().sort_values(ascending=False).head(7) * 1000
    fig, ax = plt.subplots()
    top7_sun.plot(kind='bar', color='gold', ax=ax)
    ax.set_ylabel("Production (tons)")
    ax.set_title("Top 7 Sunflower Producing States")
    st.pyplot(fig)
elif options == "Sugarcane Production (Last 50 Years)":
    st.subheader("🍬 India's Sugarcane Production (Last 50 Years)")
    sugar = df.groupby('Year')['SUGARCANE PRODUCTION (1000 tons)'].sum().tail(50) * 1000
    fig, ax = plt.subplots()
    sugar.plot(marker='o', linestyle='-', color='brown', ax=ax)
    ax.set_ylabel("Production (tons)")
    ax.set_title("Sugarcane Production Over the Years")
    st.pyplot(fig)

elif options == "Rice vs Wheat Production (Last 50 Years)":
    st.subheader("🌾 Rice vs Wheat Production - Last 50 Years")
    rice = df.groupby('Year')['RICE PRODUCTION (1000 tons)'].sum().tail(50) * 1000
    wheat = df.groupby('Year')['WHEAT PRODUCTION (1000 tons)'].sum().tail(50) * 1000
    fig, ax = plt.subplots()
    rice.plot(label='Rice', color='green', ax=ax)
    wheat.plot(label='Wheat', color='orange', ax=ax)
    ax.set_title("Rice vs Wheat Production")
    ax.set_ylabel("Production (tons)")
    ax.legend()
    st.pyplot(fig)
elif options == "Rice Production by West Bengal Districts":
    st.subheader("🏞️ Rice Production - West Bengal Districts")
    wb_district = df[df['State Name'] == 'West Bengal']
    district_rice = wb_district.groupby('District Name')['RICE PRODUCTION (1000 tons)'].sum().sort_values(ascending=False) * 1000
    fig, ax = plt.subplots()
    district_rice.plot(kind='bar', color='teal', ax=ax)
    ax.set_ylabel("Rice Production (tons)")
    ax.set_title("Rice Production by District - West Bengal")
    plt.xticks(rotation=90)
    st.pyplot(fig)
elif options == "Top 10 Wheat Production Years from UP":
    st.subheader("🏅 Top 10 Wheat Production Years - Uttar Pradesh")
    up = df[df['State Name'] == 'Uttar Pradesh']
    up_yearly = up.groupby('Year')['WHEAT PRODUCTION (1000 tons)'].sum().sort_values(ascending=False).head(10) * 1000
    fig, ax = plt.subplots()
    up_yearly.plot(kind='bar', color='maroon', ax=ax)
    ax.set_ylabel("Wheat Production (tons)")
    ax.set_title("Top 10 Wheat Production Years in UP")
    st.pyplot(fig)
