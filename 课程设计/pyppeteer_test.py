import asyncio
from pyppeteer import launch
import openpyxl

async def wait_for_multiple_xpaths(page, xpaths, timeout=3000):
    elements = []
    for xpath in xpaths:
        try:
            element = await page.waitForXPath(xpath, timeout=timeout)
            elements.append(element)
        except Exception as e:
            print(f"Error finding element for xpath {xpath}: {e}")
            elements.append(None)
    return elements

async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('https://me.pharnexcloud.com/login/signin?redirect=https%3A%2F%2Fdata.pharnexcloud.com%2F4%2Ftable%2F243&type=11')
    await asyncio.sleep(10)  # 等待登录页加载
    await page.goto('https://data.pharnexcloud.com/4/table/243')
    button_selector = 'button[type="button"].btn-next'
    page_count = 1

    # 创建Excel工作簿和工作表
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Scraped Data'
    row_num = 1

    async def get_page_data():
        nonlocal row_num
        for i in range(1, 11):
            try:
                xpaths = [
                    f"/html/body/div/div[3]/div/div/div/div/div[3]/div[2]/div[2]/div/div[4]/div[2]/table/tbody/tr[{i}]/td[1]",
                    f"/html/body/div/div[3]/div/div/div/div/div[3]/div[2]/div[2]/div/div[3]/table/tbody/tr[{i}]/td[3]",
                    f"/html/body/div/div[3]/div/div/div/div/div[3]/div[2]/div[2]/div/div[4]/div[2]/table/tbody/tr[{i}]/td[4]",
                    f"/html/body/div/div[3]/div/div/div/div/div[3]/div[2]/div[2]/div/div[4]/div[2]/table/tbody/tr[{i}]/td[5]",
                    f"/html/body/div/div[3]/div/div/div/div/div[3]/div[2]/div[2]/div/div[4]/div[2]/table/tbody/tr[{i}]/td[6]"
                ]
                elements = await wait_for_multiple_xpaths(page, xpaths, timeout=3000)

                # 处理抓取到的元素数据
                data = []
                for element in elements:
                    if element is not None:
                        text = await page.evaluate('(element) => element.textContent', element)
                        data.append(text.strip())
                    else:
                        data.append('')  # 如果没有找到元素，填充空字符串

                for col_num, cell_value in enumerate(data, start=1):
                    sheet.cell(row=row_num, column=col_num, value=cell_value)
                print(f"已获取并写入第{page_count}页第{i}行数据")
                row_num += 1
            except Exception as e:
                print(f"获取数据时出现错误: {e}")
                continue

    await get_page_data()

    while page_count < 10:
        try:
            next_button = await page.waitForSelector(button_selector, timeout=60000)
            
            if next_button:
                is_visible = await page.evaluate('(element) => window.getComputedStyle(element).display !== "none" && window.getComputedStyle(element).visibility !== "hidden"', next_button)
                if is_visible:
                    await next_button.click()
                    
                    # 等待一段时间，确保页面局部更新完成
                    await asyncio.sleep(5)
                    
                    # 检查是否需要等待特定元素加载，而不是整个页面导航
                    await page.waitForSelector('table tbody tr', timeout=60000)
                    
                    page_count += 1
                    await get_page_data()
                    print(f"已翻到第 {page_count} 页")
                else:
                    print("下一页按钮不可见")
                    break
            else:
                print("已到最后一页")
                break
        except Exception as e:
            print(f"翻页时出现错误: {e}")
            break

    # 保存Excel文件
    workbook.save('D:\\VsCodeProject\\hospital.xlsx')
    print('数据已保存到 hospital.xlsx')

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())