#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import database
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

def out(message):
	time = datetime.now()
	database.logging(time, message)