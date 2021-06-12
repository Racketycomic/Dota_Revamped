from counterbalancer import cbparse
from loglcs import logclear
from regexparser import regcl
import time


cb = cbparse()
lg = logclear()
rg = regcl()



while(1):
    time.sleep(40)
    rg.regfun()
    cb.parsefun()
    lg.clearlog()
