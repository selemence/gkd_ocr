import asyncio
from pyppeteer import launch
from openpyxl import Workbook

async def wait_for_multiple_xpaths(page, xpaths, timeout=3000):
    elements = []
    for xpath in xpaths:
        try:
            element = await page.waitForXPath(xpath, {'timeout': timeout})
            elements.append(element)
        except:
            elements.append(None)
    return elements

# 爬取单个页面的岗位信息并写入Excel
async def crawl_page(url, sheet, row_num):
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'domcontentloaded'})

    for i in range(1, 5):  # 假设每页有27个岗位信息
        try:
            xpaths = [
                f"/html/body/div[3]/div[4]/div[{i}]/ul/li[1]/div[1]/div[1]/a/text()",
                f"/html/body/div[3]/div[4]/div[1]/ul/li[{i}]/div[2]/div/a",
                f"/html/body/div[3]/div[4]/div[1]/ul/li[{i}]/div[1]/p/text()",
                f"/html/body/div[3]/div[4]/div[1]/ul/li[{i}]/span"
                
            ]
            elements = await wait_for_multiple_xpaths(page, xpaths, timeout=1000)

            # 处理抓取到的元素数据
            data = []
            for element in elements:
                if element is not None:
                    text = await page.evaluate('(element) => element.textContent', element)
                    data.append(text.strip())
                else:
                    print("无数据")

            for col_num, cell_value in enumerate(data, start=1):
                sheet.cell(row=row_num, column=col_num, value=cell_value)
            print(f"已获取并写入第{row_num - 1}行数据")
            row_num += 1
        except Exception as e:
            print(f"获取数据时出现错误: {e}")
            continue

    await browser.close()
    return row_num

# 爬取多页的岗位信息并写入Excel
async def crawl_multiple_pages(base_url, num_pages, sheet):
    row_num = 2  # 从第二行开始写入
    for page_num in range(1, num_pages + 1):
        url = f"{base_url}pn{page_num}/"
        row_num = await crawl_page(url, sheet, row_num)

# 保存数据到Excel
def save_to_excel(filename):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Job Listings'

    headers = ['Title', 'Company', 'Salary', 'Date']
    sheet.append(headers)

    return workbook, sheet

# 主函数
async def main():
    # 从控制台获取岗位关键词
    keyword = input("请输入要搜索的岗位关键词: ")
    base_url = f'https://sz.58.com/job/?key={keyword}&'
    num_pages = 1  # 假设爬取前5页********************************************************************************

    # 创建Excel工作簿和工作表
    workbook, sheet = save_to_excel('job_listings.xlsx')

    # 爬取数据并写入Excel
    await crawl_multiple_pages(base_url, num_pages, sheet)

    # 保存Excel文件
    workbook.save('job_listings.xlsx')
    print(f"数据已保存到 job_listings.xlsx")

# 运行主函数
asyncio.get_event_loop().run_until_complete(main())
