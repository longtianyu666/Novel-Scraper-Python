import re
import Website as web
def extract_chapter_id(website,url):
    if website==web.Website.liNovelLib:
        match = re.search(r'/novel/\d+/(?P<chapter_id>\d+)[_.]', url) 
        if match:
            return match.group('chapter_id')
        
        match = re.search(r'/novel/\d+/(?P<chapter_id>\d+)\.html', url)
        if match:
            return match.group('chapter_id')
    # elif website==Website.wenKu8:
        # match=re.search('(.*?).htm',url)
    return None