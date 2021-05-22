import logging

from data.config import DEBUG

if DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=level
                    )