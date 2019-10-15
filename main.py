from scrapy.cmdline import execute

import sys
import os

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append( os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spiders'), 'detail_page_info.py'))

# execute(['scrapy', 'runspider', os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spiders'), 'detail_page_info.py')])
execute(['scrapy', 'crawl', 'detail_page_info'])
