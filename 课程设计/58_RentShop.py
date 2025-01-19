import asyncio
from pyppeteer import launch
from openpyxl import Workbook
from openpyxl.utils.exceptions import InvalidFileException

async def wait_for_multiple_xpaths(page, xpaths, timeout=3000):
    elements = []
    for xpath in xpaths:
        try:
            element = await page.waitForXPath(xpath, {'timeout': timeout})
            elements.append(element)
        except Exception as e:
            print(f"XPath not found: {xpath} with error {e}")
            elements.append(None)
    return elements

# 爬取单个页面的商铺信息并写入Excel
async def crawl_page(page, sheet, row_num):
    for i in range(1, 51):  # 假设每页有50个商铺信息
        try:
            xpaths = [
                f"/html/body/div[5]/div[5]/div[1]/ul/li[{i}]/a/div[2]/p[1]/span[1]",  # 商铺位置
                f"/html/body/div[5]/div[5]/div[1]/ul/li[{i}]/a/div[4]/p[1]/span[1]",  # 商铺面积
                f"/html/body/div[5]/div[5]/div[1]/ul/li[{i}]/a/div[3]/p[2]",  # 商铺租金
                f"/html/body/div[5]/div[5]/div[1]/ul/li[{i}]/a/div[5]"  # 发布时间
            ]
            elements = await wait_for_multiple_xpaths(page, xpaths, timeout=3000)

            # 处理抓取到的元素数据
            data = []
            for element in elements:
                if element is not None:
                    text = await page.evaluate('(element) => element.textContent', element)
                    data.append(text.strip())
                else:
                    data.append("无数据")

            for col_num, cell_value in enumerate(data, start=1):
                sheet.cell(row=row_num, column=col_num, value=cell_value)
            print(f"已获取并写入第{row_num - 1}行数据")
            row_num += 1
            
            # 每次请求之间添加延迟
            await asyncio.sleep(1)
        except Exception as e:
            print(f"获取数据时出现错误: {e}")
            continue

    return row_num

# 爬取多页的商铺信息并写入Excel
async def crawl_multiple_pages(base_url, num_pages, sheet, workbook):
    row_num = 2  # 从第二行开始写入
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    
    for page_num in range(1, num_pages + 1):
        url = f"{base_url}pn{page_num}/"
        try:
            await page.goto(url, {'waitUntil': 'domcontentloaded', 'timeout': 60000})
            row_num = await crawl_page(page, sheet, row_num)
            # 每页爬取后立即保存文件
            workbook.save('shop_listings.xlsx')
            
            # 每页请求之间添加延迟
            await asyncio.sleep(5)
        except Exception as e:
            print(f"导航到页面 {url} 时出错: {e}")
            # 保存已获取的数据
            workbook.save('shop_listings.xlsx')
            continue
    
    await browser.close()

# 保存数据到Excel
def save_to_excel(filename):
    try:
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = 'Shop Listings'
        headers = ['Location', 'Area', 'Rent', 'Date']
        sheet.append(headers)
        return workbook, sheet
    except InvalidFileException as e:
        print(f"Error creating Excel file: {e}")
        return None, None

# 主函数
async def main():
    # 从控制台获取关键词和页数
    try:
        num_pages = int(input("请输入要爬取的页数: ").strip())
    except ValueError:
        print("请输入有效的数字页数")
        return

    base_url = 'https://tj.58.com/shangpu/'

    # 创建Excel工作簿和工作表
    workbook, sheet = save_to_excel('shop_listings.xlsx')
    if not workbook or not sheet:
        return

    # 爬取数据并写入Excel
    try:
        await crawl_multiple_pages(base_url, num_pages, sheet, workbook)
    except Exception as e:
        print(f"运行过程中出错: {e}")
        # 保存已获取的数据
        workbook.save('shop_listings.xlsx')

    # 最终保存Excel文件
    workbook.save('shop_listings.xlsx')
    print(f"数据已保存到 shop_listings.xlsx")

# 运行主函数
asyncio.get_event_loop().run_until_complete(main())
