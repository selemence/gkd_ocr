import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1. 加载数据
# 假设你的数据保存在一个Excel文件中
data = pd.read_excel('D:\VsCodeProject\data\job_listings.xlsx')  # 请替换成你的文件路径

# 2. 数据预处理
# 处理薪资数据，将范围转换为中间值，并处理无法转换的值
def convert_salary(salary):
    if isinstance(salary, str):
        if '-' in salary:
            low, high = salary.split('-')
            return (float(low) + float(high)) / 2
        elif salary.isdigit():
            return float(salary)
    return np.nan  # 对于无法转换的值，返回NaN

data['Salary'] = data['Salary'].apply(convert_salary)

# 移除无法转换的条目
data = data.dropna(subset=['Salary'])

salaries = data['Salary'].values.reshape(-1, 1)

# 标准化数据
scaler = StandardScaler()
salaries_scaled = scaler.fit_transform(salaries)

# 3. 确定聚类数目
# 使用肘部法来确定最佳的聚类数目
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(salaries_scaled)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker='o')
plt.title('Elbow Method for Optimal Clusters')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# 4. 应用KMeans进行聚类
# 假设通过肘部法我们确定最佳聚类数目为3
optimal_clusters = 3
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
clusters = kmeans.fit_predict(salaries_scaled)

# 将聚类结果添加到原数据中
data['Cluster'] = clusters

# 5. 可视化结果
plt.figure(figsize=(10, 6))
plt.scatter(salaries_scaled, np.zeros_like(salaries_scaled), c=clusters, cmap='viridis', marker='o')
plt.title('Salary Clustering')
plt.xlabel('Scaled Salary')
plt.ylabel('Cluster')
plt.show()

# 输出聚类结果
print(data.head())
