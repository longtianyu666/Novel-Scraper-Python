import aiohttp
import asyncio
import logging
import os
import io
from lxml import etree
from urllib.parse import urlparse
from PIL import Image

async def download_all_img(img_info,base_save_data,session:aiohttp.ClientSession):
    if not img_info:
        return
    logging.info(f'开始并发下载{len(img_info)}张图片')
    tasks=[]
    for info in img_info:
        full_save_path=os.path.join(base_save_data,info['relative_path'])
        os.makedirs(os.path.dirname(full_save_path),exist_ok=True)
        task=download_img(session,info['url'],full_save_path)
        tasks.append(task)
    await asyncio.gather(*tasks)
    logging.info('图片下载完成')
    
""" async def download_img(session:aiohttp.ClientSession,url,full_sava_path):
    try:
        async with session.get(url,timeout=30) as response:
            if response.status==200:
                image_data=await response.read()
                with open(full_sava_path,'wb') as f:
                    f.write(image_data)
                logging.info(f"成功下载图片到{full_sava_path}")
                return full_sava_path
            else:
                logging.error(f"下载图片失败,状态码{response.status}:{url}")
                return None
    except Exception as e:
        logging.error(f"下载图片{url}时发生异常:{e}")
        return None """
async def download_img(session:aiohttp.ClientSession,url,full_sava_path):
    try:
        async with session.get(url,timeout=30) as response:
            if response.status==200:
                image_data=await response.read()
                try:
                    image_stream=io.BytesIO(image_data)
                    img=Image.open(image_stream)
                    
                    if img.mode!='RGB':
                        img=img.convert('RGB')
                    
                    img.save(full_sava_path,format=img.format or 'JPEG',quality=95)
                except Exception as e:
                    logging.warning(f"图片 {full_sava_path} 标准化失败({e})，使用原始字节保存。")
                    with open(full_sava_path,'wb') as f:
                        f.write(image_data)
    except Exception as e:
        logging.error(f"下载图片{url}时发生异常:{e}")
        return None
    
def get_image(content_container,chapter_id):
    image_holder=[]
    xpath_expression='.//img[contains(@class,"imagecontent") and (@src or @data-src or @data-original)]'
    for index,image in enumerate(content_container.xpath(xpath_expression)):
        img_src=image.get('data-src') or image.get('src')
        relative_filename=f"images/{chapter_id}_{index+1:03d}{os.path.splitext(urlparse(img_src).path)[1] or'.jpg'}"
        image_info={
            'url':img_src,
            'relative_path':relative_filename
        }
        image_holder.append(image_info)
    
        placeholder_tag = f'--IMAGE-PLACEHOLDER-<{relative_filename}>--'
        new_text_node=etree.Element('img')
        new_text_node.text=placeholder_tag
        image.getparent().replace(image,new_text_node)
    return image_holder