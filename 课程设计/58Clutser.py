import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# 读取数据
data = pd.read_excel('data/cleaned_shop_listings_with_coordinates.xlsx')

# 数据清洗
data = data.dropna()
data = data[(data['Rent'] > 0) & (data['Area'] > 0)]

# 特征工程
features = ['Area', 'Rent', 'Latitude', 'Longitude']
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[features])

# 聚类分析
k = 4  # 示例聚类数目
kmeans = KMeans(n_clusters=k, random_state=0, n_init=10)  # 显式设置 n_init 参数
clusters = kmeans.fit_predict(data_scaled)
data['Cluster'] = clusters

# 聚类结果评估
silhouette_avg = silhouette_score(data_scaled, clusters)
print(f'For n_clusters = {k}, the average silhouette_score is : {silhouette_avg}')

# 1. Pairplot
sns.pairplot(data, vars=features, hue='Cluster', palette='viridis')
plt.suptitle('Pairplot of 58.com Housing Data Clusters', y=1.02)
plt.savefig("data/Pairplot.png", dpi=600)
plt.show()

# 2. 箱线图
plt.figure(figsize=(16, 8))
for i, feature in enumerate(features):
    plt.subplot(2, 2, i+1)
    sns.boxplot(x='Cluster', y=feature, data=data, palette='viridis')
    plt.title(f'Boxplot of {feature}')
plt.tight_layout()
plt.savefig("data/box.png", dpi=600)
plt.show()

# 3. 条形图
cluster_means = data.groupby('Cluster').mean().reset_index()
plt.figure(figsize=(16, 8))
for i, feature in enumerate(features):
    plt.subplot(2, 2, i+1)
    sns.barplot(x='Cluster', y=feature, data=cluster_means, palette='viridis')
    plt.title(f'Mean {feature} by Cluster')
plt.tight_layout()
plt.savefig("data/line.png", dpi=600)
plt.show()

# 4. 地理散点图
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Longitude', y='Latitude', hue='Cluster', data=data, palette='viridis')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Geographical Scatter Plot of 58.com Housing Clusters')
plt.savefig("data/geo.png", dpi=600)
plt.show()

# 5. 三维散点图
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(data['Longitude'], data['Latitude'], data['Rent'], c=data['Cluster'], cmap='viridis')

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Rent')
ax.set_title('3D Scatter Plot of 58.com Housing Clusters')

# 添加颜色条
legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
ax.add_artist(legend1)

plt.savefig("data/3d_scatter.png", dpi=600)
plt.show()

