from  scrapy.cmdline import  execute

import  sys
import  os
import  time
ppath=os.path.dirname(os.path.abspath(__file__))
print(ppath)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#execute(['cd',ppath])
execute(['scrapy','crawl','xzquhua'])
