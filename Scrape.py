import aiohttp
import asyncio
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s:%(message)s')

CONCURRENCY=5
semaphore=asyncio.Semaphore(CONCURRENCY)

async def scrape_api(url,session:aiohttp.ClientSession,retries=5):
    for retry in range(retries):
        async with semaphore:
            try:
                if 'catalog' in url:
                    logging.info(f'正在爬取{url}')
                else:
                    logging.info(f'正在爬取{url},尝试第{retry+1}/{retries}次')
                await asyncio.sleep(2)
                async with session.get(url,timeout=aiohttp.ClientTimeout(total=45)) as response:
                    if response.status==200:
                        return await response.text()
                    elif response.status in (403,429):
                        wait_time=10
                        logging.info(f'{url}请求被拒绝,状态码{response.status}')
                        if 'catalog' in url:
                            logging.info('请使用手动输入目录的html')
                            return
                        await asyncio.sleep(wait_time)
                        continue
                    elif response.status==404:
                        logging.info(f'{response.status} No Found {url}')
                        return None
                    else:
                        if retries>=3:
                            await asyncio.sleep(5)
                        else:
                            await asyncio.sleep(3)
                        continue
            except aiohttp.ClientError:
                logging.error(f'在爬取{url}时出错了',exc_info=True)
    logging.error(f'达到最大重试次数，放弃爬取{url}')