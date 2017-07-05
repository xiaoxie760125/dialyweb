
import  os
import  xlrd
from  datetime import  datetime
ddpath = os.path.dirname(os.path.abspath(__file__)) + '/faxin.xls'
print(ddpath)

workbook = xlrd.open_workbook(ddpath)
sheet = workbook.sheet_by_index(0)
for row in range(2, sheet.nrows - 1):
    sigongfei = (lambda x: 1 if (x == '公费') else 0)
    Value = lambda x: x.value.encode('utf-8').decode()
    print(datetime.strptime(Value(sheet.cell(row,1))+Value(sheet.cell(row,27)),'%Y%m%d'))
    print(sigongfei(sheet.cell(row, 11).value.encode('utf-8').decode()))