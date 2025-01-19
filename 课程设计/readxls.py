import pandas as pd
import requests

# 高德API的Key
API_KEY = 'fafd6896171c123c6084c5daeb341aff'

# 定义函数通过高德API将地址转换为经纬度
def get_geocode(address, api_key):
    url = f'https://restapi.amap.com/v3/geocode/geo?address={address}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        if result['geocodes']:
            location = result['geocodes'][0]['location']
            lon, lat = location.split(',')
            return float(lon), float(lat)
    return None, None

# 读取Excel文件
input_filename = 'shop_listings.xlsx'
output_filename = 'cleaned_shop_listings.xlsx'
df = pd.read_excel(input_filename)

# 数据清洗和计算
def clean_data(df):
    # 删除Rent列中非数字内容
    df['Rent'] = df['Rent'].str.extract('(\d+)').astype(float)
    df['Rent'] = pd.to_numeric(df['Rent'], errors='coerce')
    
    # 处理Area列中的非数字内容，将其转换为NaN
    df['Area'] = pd.to_numeric(df['Area'], errors='coerce')
    
    # 删除包含NaN值的行
    df = df.dropna(subset=['Rent', 'Area']).copy()
    
    # 计算新列：Rent * Area * 30
    df.loc[:, 'Computed_Value'] = df['Rent'] * df['Area'] * 30
    
    # 将Location列转换为经纬度
    df.loc[:, 'Longitude'] = df['Location'].apply(lambda x: get_geocode(x, API_KEY)[0])
    df.loc[:, 'Latitude'] = df['Location'].apply(lambda x: get_geocode(x, API_KEY)[1])
    
    return df

# 清洗数据
cleaned_df = clean_data(df)

# 保存清洗后的数据到新的Excel文件
cleaned_df.to_excel(output_filename, index=False)

print(f"数据已保存到 {output_filename}")
