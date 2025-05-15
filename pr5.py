import geopandas as gpd
import matplotlib.pyplot as plt

# Завантаження шейп-файлу
world = gpd.read_file("C:/Users/Veronika/Downloads/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")

# Всі країни Африки
africa = world[world['REGION_UN'] == 'Africa'].copy()

# Країни Африки з населенням понад 40 млн
africa_large = africa[africa['POP_EST'] > 40_000_000]

# Малюємо всі країни
fig, ax = plt.subplots(figsize=(10, 10))
africa.plot(ax=ax, color='whitesmoke', edgecolor='black')

# Виділяємо великі країни 
africa_large.plot(ax=ax, color='pink', edgecolor='black')

# Підписи для великих країн
for idx, row in africa_large.iterrows():
    plt.annotate(
        text=row['NAME'],
        xy=(row['geometry'].centroid.x, row['geometry'].centroid.y),
        ha='center',
        fontsize=10
    )

# Оформлення
ax.set_title("Країни Африки: виділено населення понад 40 млн", fontsize=16)
ax.axis('off')
plt.tight_layout()
plt.show()








