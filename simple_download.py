from csv import DictReader
from lib import *

username = "eigenboy"
password = "quark123"

r = pyGTrends(username, password)
r.download_report(('skirt'))
d = DictReader(r.csv().split('\n'))
print d
