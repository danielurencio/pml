import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.oracle import NVARCHAR2, DATE, NUMBER, FLOAT
import sys

filename = sys.argv[1]
lines = open(filename).read().split('\n')

lines = list(filter(lambda x: x != '',lines))
header = list(filter(lambda x:x,[ i if not re.match('^[1-9]',d) else None for i,d in enumerate(lines) ]))
cols = lines[header[-1]].split(',')
rows = np.array(list(map(lambda x:x.split(','),lines[header[-1] + 1:])))

df = pd.DataFrame(rows,columns=cols)
