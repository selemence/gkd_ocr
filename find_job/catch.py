from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 设置ChromeDriver路径
service = Service('/path/to/chromedriver')  # 请替换为您ChromeDriver的实际路径

# 初始化webdriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 打开目标网页
    driver.get('https://las.cnas.org.cn/LAS_FQ/publish/externalQueryL1.jsp')

    # 等待页面加载
    time.sleep(5)  # 根据需要调整等待时间

    # 获取页面内容
    page_content = driver.page_source

    # 处理页面内容
    # 例如，可以使用BeautifulSoup来解析HTML
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')

    # 示例：打印页面标题
    print(soup.title.string)

    # 在此处添加更多数据处理逻辑

finally:
    # 关闭浏览器
    driver.quit()
