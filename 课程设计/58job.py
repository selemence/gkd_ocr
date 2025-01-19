import matplotlib.pyplot as plt

# 创建流程图
plt.figure(figsize=(10, 8))

# 定义节点和描述
nodes = [
    ('开始', '程序开始运行'),
    ('读取数据', '从 cleaned_shop_listings.xlsx 文件中读取数据'),
    ('数据清洗', '删除缺失值\n过滤 Rent 和 Area 列中大于0的值'),
    ('特征工程', '标准化 Area, Rent, Latitude, Longitude 列'),
    ('聚类分析', '使用 KMeans 算法聚类数据'),
    ('聚类结果评估', '计算轮廓系数评估聚类效果'),
    ('结果可视化', '生成Pairplot、箱线图、条形图和地理散点图'),
    ('保存图像', '将生成的图像保存为文件'),
    ('结束', '程序执行完毕')
]

# 定义节点位置
pos = {
    '开始': (1, 8),
    '读取数据': (1, 7),
    '数据清洗': (1, 6),
    '特征工程': (1, 5),
    '聚类分析': (1, 4),
    '聚类结果评估': (1, 3),
    '结果可视化': (1, 2),
    '保存图像': (1, 1),
    '结束': (1, 0)
}

# 绘制节点和描述文本
for node, desc in nodes:
    # 绘制节点
    plt.text(pos[node][0], pos[node][1], node, ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='black'))

    # 绘制描述文本
    desc_lines = desc.split('\n')
    for i, line in enumerate(desc_lines):
        plt.text(pos[node][0] + 0.5, pos[node][1] - 0.2 * i,
                 line, ha='left', va='center', wrap=True, fontsize=10)

# 绘制箭头表示流程
for i in range(len(nodes) - 1):
    start_node = nodes[i][0]
    end_node = nodes[i + 1][0]
    plt.annotate('', xy=pos[end_node], xytext=pos[start_node],
                 arrowprops=dict(facecolor='black', arrowstyle='->'))

# 设置图形属性
plt.xlim(0, 2)
plt.ylim(-0.5, 8.5)
plt.axis('off')
plt.title('数据分析流程图', fontsize=15)
plt.tight_layout()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.show()
