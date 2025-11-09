""" 
实现功能
1.图形化界面 √
2.搜索小说，选择模式 
3.爬取已经完结的轻小说 √
4.每日启动电脑时进行访问网站查看是否更新 
5.两个网站的切换 （不需要了）
6.使用epub进行存储 √
"""
import aiohttp
import os
import asyncio
import random
import logging
import time
import json


from lxml import etree

import download_image
import Scrape as Scrape
import Website as web
import Save_data
import extract_chapter_id as ex
import unscramble_paragraph as us

start_time=time.time()

session=None

liNovelLib_catalog_url='https://www.linovelib.com/novel/{lib_novel_id}/catalog'
# wenKu8_catalog_url='https://www.wenku8.net/novel/{first_number_wenku_novel_id}/{wenku_novel_id}/index.htm'

async def scrape_catalog(website,id):
    # 获取目录html的url
    if website==web.Website.liNovelLib:
        Current_url=liNovelLib_catalog_url.format(lib_novel_id=id)
    """ elif website==web.Website.wenKu8:
        if id<1000:
            first_number=0
        else:
            first_number=id//1000
        Current_url=wenKu8_catalog_url.format(first_number_wenku_novel_id=first_number,wenku_novel_id=id) """
    
    return await Scrape.scrape_api(Current_url,session)

async def safe_scrape_catalog(website,id):
    # 获取目录html
    logging.info(f"尝试爬取目录 (ID: {id})")
    
    catalog_html =await scrape_catalog(website=website, id=id)
    
    if catalog_html:
        root = etree.HTML(catalog_html)
        title_list = root.xpath('.//div[@class="book-meta"]/h1/text()')
        
        if title_list:
            logging.info(f"目录 HTML 成功获取并验证通过 (ID: {id})。")
            return catalog_html
        else:
            logging.warning(f"获取目录 HTML 成功，但内容不完整 (缺少标题)，请重启程序。")
            return
    else:
        logging.warning(f"目录请求失败或返回空内容，进行重试。")

    logging.error(f"最终失败 (ID: {id})，请手动输入html。")
    return None

async def scrape_chapter_content(website,chapter_data):
    # 爬取章节内容
    start_url=chapter_data['url']
    chapter_id=ex.extract_chapter_id(website,start_url)
    if not chapter_id:
        logging.error(f'在提取{start_url}时无法爬取章节ID')
        return
    if website==web.Website.liNovelLib:
        URL='https://www.linovelib.com{url}'
        page_content=[]
        current_url=URL.format(url=start_url)
        
        next_image_index=0
        logging.info(f'开始爬取{current_url}')
        while current_url:
            html=await Scrape.scrape_api(current_url,session)
            if not html:
                logging.info(f'爬取{current_url}时html为空')
                break
            # 获取内容
            root=etree.HTML(html)
            text_content=root.xpath('//div[@id="TextContent"]')
            # 处理图片
            if text_content:
                content_container=text_content[0]
                image_holder,next_image_index=download_image.get_image(content_container,chapter_id,index=next_image_index)
                chapter_data['img'].extend(image_holder)
                
                original_paragraph=[]
                paragraph_nodes=content_container.xpath('.//p|.//img')
                cleared_paragraph=content_container.xpath('.//p')
                
                for p_node in paragraph_nodes:
                    full_text=""
                    if p_node.tag=='img' and p_node.text.startswith('--IMAGE-PLACEHOLDER-<') and p_node.text:
                        full_text=p_node.text.strip()
                    else:
                        full_text=p_node.xpath('string(.)').strip()
                        
                    if full_text:
                        original_paragraph.append(full_text)

                cleared_paragraph_nodes=[]
                for nodes in cleared_paragraph:
                    cleared_paragraph_nodes.append(nodes.xpath('string(.)').strip())
                # 解密
                if cleared_paragraph_nodes:
                    try:
                        correctly_ordered_paragraph=us.unscramble_paragraph_final(cleared_paragraph_nodes,chapter_id)
                    except Exception as e:
                        logging.error(f"章节{chapter_id} 解密失败:{e}.使用原始乱序内容。")
                        correctly_ordered_paragraph=cleared_paragraph_nodes
                else:
                    correctly_ordered_paragraph=[]
                
                text_index=0
                # 处理乱序
                for i in range(len(original_paragraph)):
                    if original_paragraph[i].startswith('--IMAGE-PLACEHOLDER-<'):
                        continue
                    original_paragraph[i]=correctly_ordered_paragraph[text_index]
                    text_index+=1
                
                page_string='\n\n'.join(original_paragraph)
                page_content.append(page_string)
            else:
                logging.error(f'无法找到内容{current_url}')
            next_href_url=root.xpath('//div[@class="mlfy_page"]/a[text()="下一页"]/@href')
            # 获取分页
            if next_href_url:
                next_url=next_href_url[0]
                if f'/{chapter_id}_' in next_url:
                    current_url=URL.format(url=next_url)
                else:
                    current_url=None
            else:
                logging.info(f"章节 {chapter_data['title']} 结束，未找到分页或下一章链接。")
                current_url=None
        # 获取分页
        final_content="\n\n".join(page_content)
        chapter_data['content']=final_content
        chapter_data['content']=chapter_data['content'].replace('style_tp();','')
        
        

        logging.info(f"章节合并完成 {chapter_data['title']} (共{len(page_content)}页)")
        
        novel_title=chapter_data.get('novel_title')
        base_save_data=os.path.join(r'.\downloads',novel_title)
        os.makedirs(base_save_data,exist_ok=True)
        logging.info(f"图片将保存到：{base_save_data}")
        await download_image.download_all_img(chapter_data['img'],base_save_data,session)
        return
async def incremental_update(novel_title, novel_id, novel_volumes, novel_author):
    # 增量更新

    old_volumes = Save_data.load_data(novel_title)
    old_chapter_map = {}
    # 将已下载章节内容保存到字典中
    for vol in old_volumes:
        for chapter in vol.get('chapters', []): 
            if chapter.get('content') and chapter.get('url'):
                old_chapter_map[chapter['url']] = {
                    'content': chapter['content'],
                    'img': chapter.get('img', [])
                }
                
    logging.info(f'已加载 {len(old_chapter_map)} 个已下载章节内容作为基准。')
    # 获取目录
    if not novel_volumes and novel_id:
        raw_root=await scrape_catalog(web.Website.liNovelLib,novel_id)
        if not raw_root:
            root=etree.HTML(raw_root)
            volumes_titles=root.xpath('//div[@class="volume-info"]')
            novel_title=(root.xpath('.//div[@class="book-meta"]/h1/text()'))[0].strip()
            novel_author=(root.xpath('.//span[text()="作者："]/a/text()'))[0].strip()
            if volumes_titles:
                for title in volumes_titles:
                    title_list=title.xpath('./h2[@class="v-line"]/text()')
                    volume_title=title_list[0].strip() if title_list else "未知卷名"
                    current_volume={
                        'title':volume_title,
                        'chapters':[]
                    }
                    novel_volumes.append(current_volume)
                    chapter_list_ul=title.xpath('following-sibling::ul[@class="chapter-list clearfix"]')[0]
                    chapter_links=chapter_list_ul.xpath('./li/a')
                    for link_element in chapter_links:
                        chapter_title=link_element.text.strip()
                        chapter_url=link_element.get('href')
                        current_volume['chapters'].append({
                            'title':chapter_title,
                            'url':chapter_url,
                            'content':'',
                            'img':[]
                        })
        else:
            return '失败'

    if not novel_volumes:
        logging.warning("解析或网络获取失败，增量更新终止。")
        return "增量更新失败：未能获取或解析出任何章节目录信息。"
        
    tasks = []
    new_chapters_count = 0
    # 遍历目录
    for new_vol in novel_volumes:
        for new_chapter in new_vol.get('chapters', []): 
            chapter_url = new_chapter.get('url')
            
            if chapter_url in old_chapter_map:
                old_data = old_chapter_map[chapter_url]
                new_chapter['content'] = old_data['content']
                new_chapter['img'] = old_data['img']
                logging.debug(f'该章节已存在,跳过爬取:{new_chapter["title"]}')
            else:
                new_chapter['novel_title'] = new_vol['title']
                tasks.append(scrape_chapter_content(web.Website.liNovelLib, new_chapter))
                new_chapters_count += 1
                logging.info(f'发现新章节,待爬取:{new_chapter["title"]}')
                
    if tasks:
        logging.info(f'开始并发下载 {len(tasks)} 个新章节内容...')
        await asyncio.gather(*tasks, return_exceptions=True)
    else:
        logging.info('目录中未发现新章节，无需爬取新内容。')
        
    logging.info("所有新章节处理完毕。开始保存数据并重建 EPUB 文件...")
    Save_data.save_data_as_json(novel_volumes, novel_title) # 你的函数名可能是 save_data
    Save_data.save_data_as_epub(novel_volumes, novel_title, novel_author)
    logging.info(f"EPUB 文件（含所有章节）已更新成功！")
    
    return f'增量更新完成！发现 {new_chapters_count} 个新章节。'
async def scrape_liNovelLib(id,catalog,is_incremental):
    # 轻小说爬虫
    global session
    USER_AGENTS = [
        # Windows 10 - Chrome (桌面端主流)
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6535.100 Safari/537.36',
        # Windows 10 - Firefox
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
        # Windows 10 - Edge
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Edge/129.0.0.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.2764.100',
        # macOS - Safari
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
        # Linux - Chrome
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        # Mobile - iPhone/Safari (模拟移动端访问，有时会绕过桌面端限制)
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        # Mobile - Android/Chrome
        'Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36',
    ]
    
    header={
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://www.linovelib.com/', 
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    session=aiohttp.ClientSession(
        headers=header,
        timeout=aiohttp.ClientTimeout(total=45)
    )
    # id=3805
    
    if not catalog and id:
        catalog=await safe_scrape_catalog(website=web.Website.liNovelLib,id=id)
    if not catalog:
        return '无法爬取到html,请手动输入html'
    root=etree.HTML(catalog)
    # 目录
    novel_volumes=[]
    current_volume=None
    volumes_titles=root.xpath('//div[@class="volume-info"]')
    novel_title=(root.xpath('.//div[@class="book-meta"]/h1/text()'))[0].strip()
    novel_author=(root.xpath('.//span[text()="作者："]/a/text()'))[0].strip()
    if volumes_titles:
        for title in volumes_titles:
            title_list=title.xpath('./h2[@class="v-line"]/text()')
            volume_title=title_list[0].strip() if title_list else "未知卷名"
            current_volume={
                'title':volume_title,
                'chapters':[]
            }
            novel_volumes.append(current_volume)
            chapter_list_ul=title.xpath('following-sibling::ul[@class="chapter-list clearfix"]')[0]
            chapter_links=chapter_list_ul.xpath('./li/a')
            for link_element in chapter_links:
                chapter_title=link_element.text.strip()
                chapter_url=link_element.get('href')
                current_volume['chapters'].append({
                    'title':chapter_title,
                    'url':chapter_url,
                    'content':'',
                    'img':[]
                })
        if is_incremental:
            # 增量更新
            await incremental_update(novel_title,id,novel_volumes,novel_author)
            return 
        tasks=[]
        for vol in novel_volumes:
            for chapter_data in vol['chapters']:
                chapter_data['novel_title']=vol['title']
                tasks.append(scrape_chapter_content(web.Website.liNovelLib,chapter_data))
        await asyncio.gather(*tasks,return_exceptions=True)
        await session.close()
        
        Save_data.save_data_as_json(novel_volumes,novel_title)
        Save_data.save_data_as_epub(novel_volumes,novel_title,novel_author)
    
    end_time=time.time()
    logging.info(f'用时{end_time-start_time}s')
    return '已完成'

""" if __name__=='__main__':
    asyncio.run(main()) """
    
def start_scrape(novel_id,catalog_html,flag):
    message=asyncio.run(scrape_liNovelLib(novel_id,catalog_html,flag))
    if not flag:
        return message
    else:
        return '小说已更新'
