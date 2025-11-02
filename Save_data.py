import json
import logging
import os
import html
from ebooklib import epub

def save_data_as_json(novel_volumes,novel_title):
    output_filename = f'{novel_title}.json'
    try:
        output_path=os.path.join(r'./jsons',output_filename)
        os.makedirs(os.path.dirname(output_path),exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(novel_volumes, file, ensure_ascii=False, indent=4)
        logging.info(f"所有数据已成功保存到文件: {output_path}")
    except Exception as e:
        logging.error(f"保存数据到文件时发生错误: {e}")
        
def load_data(novel_title):
    input_filename=f'{novel_title}.json'
    input_path=os.path.join(r'./jsons',input_filename)
    
    if os.path.exists(input_path):
        try:
            with open(input_path,'r',encoding='utf-8') as file:
                data=json.load(file)
                if isinstance(data,list):
                    return data
                else:
                    logging.error(f'加载旧数据文件 {input_filename} 成功，但数据类型错误 ({type(data)}).')
                    return []
        except Exception as e:
            logging.error(f'加载旧数据文件{input_filename}时发生错误:{e}')
            return []
    return []
    
def save_data_as_epub(novel_volumes,novel_title,novel_author):
    book=epub.EpubBook()
    
    EPUB_INPUT_FILE=r'./epubs'
    book.set_identifier(f'id{novel_title.replace(" ","")}')
    book.set_title(novel_title)
    book.set_language('zh')
    book.add_author(novel_author)
    book.spine=['nav']
    
    chapter_for_toc=[]
    added_image_names=set()
    
    global_chapter_names=0
    
    for vol in novel_volumes:
        logging.info(f'正在处理卷:{vol['title']}...')
        
        base_image_path=os.path.join(r'./downloads',vol['title'],'images')
        
        chapter_list=[]
        
        for i,chapter_data in enumerate(vol['chapters']):
            global_chapter_names+=1
            chapter_filename = f'chapter_{global_chapter_names:03d}.xhtml'
            c=epub.EpubHtml(
                title=chapter_data['title'],
                file_name=chapter_filename,
                lang='zh'
            )
            content_html=''
            for paragraph in chapter_data['content'].split('\n\n'):
                if paragraph.startswith('--IMAGE-PLACEHOLDER-<') and paragraph.endswith('>--'):
                    rel_path=paragraph[20:-3]
                    img_filename=os.path.basename(rel_path)
                    
                    img_file_path=os.path.join(base_image_path,img_filename)
                    logging.info(f"EPUB诊断: 章节 '{chapter_data['title']}'")
                    logging.info(f"EPUB诊断: 占位符提取的文件名: {img_filename}")
                    logging.info(f"EPUB诊断: 预期本地路径: {img_file_path}")
                    if os.path.exists(img_file_path):
                        if img_filename not in added_image_names:
                            logging.info("EPUB诊断: 文件已找到，正在导入。")
                            try:
                                with open(img_file_path,'rb') as f:
                                    f.seek(0)
                                    image_data=f.read()
                                    logging.info(f"EPUB诊断: {img_filename} 读取成功，字节大小: {len(image_data)}") 
                            except Exception as e:
                                logging.error(f"无法读取本地图片文件 {img_filename} 的数据: {e}")
                            
                            _, ext = os.path.splitext(img_filename)
                            ext=ext.lower()
                            
                            mime_map={
                                '.jpg':'image/jpeg',
                                '.jpeg':'image/jpeg',
                                '.png':'image/png',
                                '.gif':'image/gif',
                                '.webp':'image/webp',
                            }
                            media_type = mime_map.get(ext, 'image/jpeg')
                            
                            image_item=epub.EpubItem(
                                file_name=f'OEPBS/Images/{img_filename}',
                                media_type=media_type,
                                content=image_data
                            )
                            
                            book.add_item(image_item)
                            
                            added_image_names.add(img_filename)
                            content_html+=f'<p><img src="OEPBS/Images/{img_filename}" alt="{chapter_data["title"]}"></p>\n'
                    else:
                        logging.warning("EPUB诊断: 文件未找到，跳过导入！")
                        
                else:
                    content_html+=f'<p>{html.escape(paragraph)}</p>\n'
                    
            c.content=f'<h2>{chapter_data['title']}</h2>\n{content_html}'
            book.add_item(c)
            chapter_list.append(c)
            book.spine.append(c)
            
        chapter_for_toc.append((epub.Section(vol['title']),chapter_list))
    book.toc=tuple(chapter_for_toc)
    
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    style='h1 {text-align:center;} h2 {text-align: left;}'
    nav_css=epub.EpubItem(uid="style_nav",file_name="style/nav.css",media_type="text/css",content=style)
    book.add_item(nav_css)
    
    epub_filename=f'{novel_title}.epub'
    os.makedirs(EPUB_INPUT_FILE,exist_ok=True)
    
    full_path=os.path.join(EPUB_INPUT_FILE,epub_filename)
    
    epub.write_epub(full_path,book,{})
    logging.info(f'EPUB文件已创建成功:{full_path}')