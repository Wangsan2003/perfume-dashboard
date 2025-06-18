# 首先将所需要的包导入进去
# 导入数据分析常用的Python库：
# pandas: 数据处理和分析
# numpy: 数值计算
# tensorflow/keras: 深度学习框架
# sklearn: 机器学习库(虽然导入但后续未使用)
# os: 操作系统接口
import pandas as pd
import numpy as np
import os


# 导入交互式绘图库 Plotly Express
import plotly.express as px
import plotly.io as pio

# 设置默认主题为 "plotly_white"，使图表更美观
pio.templates.default = "plotly_white"

# 读取数据======这里有两个数据集，需要读取两个，使用pandas
# --- 请确保将路径 "C://Users//86175//..." 修改为您的实际文件路径 ---
try:
    men_df = pd.read_csv("perfume-dashboard/data/ebday_mens_perfume.csv")
    women_df = pd.read_csv("perfume-dashboard/data/ebday_womens_perfume.csv")
except FileNotFoundError:
    print("错误：找不到指定的CSV文件。请检查文件路径是否正确。")
    # 如果文件不在指定路径，可以退出或引导用户输入正确路径
    exit()


# 使用head()方法查看两个数据集的前5行，了解数据结构
print("男士香水数据前20行:")
print(men_df.head(20))
print("\n女士香水数据前20行:")
print(women_df.head(20))

# 使用shape属性查看两个数据集的维度(行数和列数)
print(f"\n男士香水数据维度: {men_df.shape}")
print(f"女士香水数据维度: {women_df.shape}")

# 添加数据列
men_df['sex'] = 'men'
women_df['sex'] = 'women'

# 合并两个数据集
df = pd.concat([men_df, women_df], ignore_index=True)

# 查看合并后数据的列名和前5行
print("\n合并后的数据列名:")
print(df.columns)
print("\n合并后数据的前5行:")
print(df.head())


# 检查数据中的缺失值数量
print("\n合并前缺失值统计:")
print(df.isnull().sum())

# 使用fillna()方法填充缺失值
df = df.fillna(
    {'brand': 'Unknown',
     'type': 'Unknown',
     'available': 0,
     'availableText': 'Not available',
     'sold': 0,
     'lastUpdated': 'Unknown'}
)

print("\n填充后缺失值统计:")
print(df.isnull().sum())


# 统计各品牌出现的频率
brand_counts = df['brand'].value_counts()
print("\n品牌出现频率:")
print(brand_counts)


# =================================================================
# 交互式图表部分
# =================================================================

# 1. 【交互式】绘制香水价格的直方图
# 将鼠标悬停在条形上，可以查看该价格区间的具体数量和范围
fig_hist = px.histogram(df,
                        x='price',
                        nbins=30,  # 可以调整分箱数量
                        title='<b>香水价格分布（交互式）</b>',
                        labels={'price': '价格 (USD)', 'count': '商品数量'},
                        template='plotly_white')
fig_hist.update_layout(yaxis_title='商品数量')
fig_hist.show()


# 计算价格的平均值、最大值和最小值
ac_price = df['price'].mean()
max_price = df['price'].max()
min_price = df['price'].min()
print(f'\nprice的平均价格为：${ac_price:.2f}')
print(f'price的最大价格为：${max_price:.2f}')
print(f'price的最低价格为：${min_price:.2f}')


# 计算平均可用数量和平均已售数量
available_avg = df['available'].mean()
sold_avg = df['sold'].mean()
print(f'available的平均数为：{available_avg:.2f}')
print(f'sold_avg的平均数为：{sold_avg:.2f}')


# 2. 【交互式】绘制可用数量与已售数量的散点图
# 将鼠标悬停在数据点上，可以查看具体的'available', 'sold'以及'brand'和'price'信息
fig_scatter_all = px.scatter(df,
                             x='available',
                             y='sold',
                             title='<b>可用数量 vs 已售数量（交互式）</b>',
                             labels={'available': '可用数量', 'sold': '已售数量'},
                             hover_data=['brand', 'price', 'sex']) # 添加悬停时显示的数据
fig_scatter_all.show()


# 统计商品位置的前10个最常见值
location = df['itemLocation'].value_counts().head(10)
print(f"\n商品来源地Top 10:\n{location}")


# 统计男女香水数量的对比
sex_counts = df['sex'].value_counts()
print(f"\n男女香水数量对比:\n{sex_counts}")


# 3. 【交互式】使用Plotly绘制男女香水价格的箱线图
# 将鼠标悬停在箱体上，可以查看中位数、四分位数、最大/最小值等统计信息
fig_box = px.box(df,
                 x='sex',
                 y='price',
                 color='sex', # 按性别着色
                 title='<b>男女香水价格对比（交互式）</b>',
                 labels={'sex': '性别', 'price': '价格 (USD)'},
                 points="all") # 显示所有数据点
fig_box.show()


# 将数据按性别分割为两个子数据集
men_data = df[df['sex'] == 'men']
women_data = df[df['sex'] == 'women']

# 分别计算男女香水的平均可用数量和平均已售数量
men_available = men_data['available'].mean()
women_available = women_data['available'].mean()
men_sold = men_data['sold'].mean()
women_sold = women_data['sold'].mean()
print(f'\n男士香水的平均可用数量：{men_available:.2f}')
print(f'女士香水的平均可用数量：{women_available:.2f}')
print(f'男士平均已售数量：{men_sold:.2f}')
print(f'女士平均已售数量：{women_sold:.2f}')


# 4. 【交互式】绘制男女香水可用数量与已售数量的对比散点图
# 按性别着色，悬停可查看详细信息，点击图例可筛选显示某一性别的数据
fig_scatter_gender = px.scatter(df,
                                x='available',
                                y='sold',
                                color='sex',  # 按性别进行颜色区分
                                title='<b>可用数量 vs 已售数量 (按性别对比，交互式)</b>',
                                labels={'available': '可用数量', 'sold': '已售数量'},
                                hover_data=['brand', 'price']) # 添加悬停信息
fig_scatter_gender.show()


# 分别统计男女香水的前10个最常见来源地
men_id = men_data['itemLocation'].value_counts().head(10)
women_id = women_data['itemLocation'].value_counts().head(10)
print(f'\n男士香水的前十来源地：\n{men_id}')
print(f'\n女士香水的前十来源地：\n{women_id}')
