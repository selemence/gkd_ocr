import schedule
import time
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_shareCrawler():
    logging.info('crawler1任务开始')
    import shareCralwer
    shareCralwer.main()
    logging.info('crawler1任务结束')

def run_ShareKlineCrawler():
    logging.info('crawler2任务开始')
    import ShareKlineCrawler
    ShareKlineCrawler.py.main()
    logging.info('crawler2任务结束')

# 定义每天0点运行crawler1任务
schedule.every().day.at("00:00").do(run_shareCrawler)

# 定义每天1点运行crawler2任务
schedule.every().day.at("01:00").do(run_ShareKlineCrawler)

logging.info('爬虫任务调度器已启动')

while True:
    schedule.run_pending()
    time.sleep(1)
