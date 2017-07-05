'''
数据操作类
'''
from  shanxidaily.models import   customer,Vouchs,Comdartment,dailyinfo,susDep,User
import  xlrd
import  sys
import  os
from  datetime import  datetime
from  shanxidaily.models import SelectForm
from  django.core import  serializers
from  django.db.models import  Aggregate,Sum
from  django.db import  connections
import  math
import  xlwt
from  io import  StringIO,BytesIO

'''
从EXCEL表数据导入数据库'''
def insertDataFromxlsheet():
    ddpath=os.path.dirname(os.path.abspath(__file__))+'/faxin.xls'
    print(ddpath)

    workbook=xlrd.open_workbook(ddpath)
    sheet=workbook.sheet_by_index(0)
    sigongfei=(lambda  x:1 if (x=='公费') else 0)

    for row in range(30277,sheet.nrows-1):
        flileter = customer.objects.filter(code=sheet.cell(row, 59).value.encode('utf-8').decode()).count()
        if flileter==0:
            C=customer()
            C.name=sheet.cell(row,14).value.encode('utf-8').decode()
            C.departmentname=sheet.cell(row,15).value.encode('utf-8').decode()
            C.address=sheet.cell(row,16).value.encode('utf-8').decode()
            C.phone=sheet.cell(row,17).value.encode('utf-8').decode()
            C.compartmentcode=sheet.cell(row,22).value.encode('utf-8').decode()
            C.code=sheet.cell(row,59).value.encode('utf-8').decode()
            C.compatment_id=sheet.cell(row,22).value.encode('utf-8').decode()+'000000'
            C.isstateexprence=sigongfei(sheet.cell(row,11).value.encode('utf-8').decode())
            C.save()
            print('save',str(row))
        else:
            print(row)
#下载数据文件为EXCEL格式



def insertVouchDataFromSheet():
    ddpath = os.path.dirname(os.path.abspath(__file__)) + '/faxin.xls'
    print(ddpath)
    workbook = xlrd.open_workbook(ddpath)
    sheet = workbook.sheet_by_index(0)
    sigongfei = (lambda x: 1 if (x == '大宗') else 0)
    Value=lambda x:x.value.encode('utf-8').decode()
    for row in range(8622, sheet.nrows - 1):
        v=Vouchs()
        c=customer.objects.filter(code=sheet.cell(row,59).value.encode('utf-8').decode())[0]
        v.code=Value(sheet.cell(row,0))
        v.begindate=datetime.strptime(Value(sheet.cell(row,1))+Value(sheet.cell(row,27)),'%Y%m%d')
        v.enddate=datetime.strptime(Value(sheet.cell(row,1))+Value(sheet.cell(row,28)),'%Y%m%d')
        v.sdate=datetime.strptime(Value(sheet.cell(row,9))[0:8],'%Y%m%d')
        v.big=sigongfei(Value(sheet.cell(row,12)))
        v.count=Value(sheet.cell(row,26))
        v.customer=c
        v.fee=Value(sheet.cell(row,33))
        v.save()
        print('save',row)
'''
报纸信息汇总表'''
def GetSumByDecument():
    connectcusor=connections["default"].cursor()


    sumlist=connectcusor.execute("select susdep.susdepname,sum(vouchs.count)  from vouchs left join customer on  vouchs.customer_id=customer.`code` left JOIN susdep on customer.compatment_id=susdep.susdepcode GROUP BY susdep.susdepname ORDER BY susdepcode")
    listsum=[]
    for data in connectcusor.fetchall():
        listsum.append({'depname':data[0],'count':data[1]})
    return  listsum


def GetDailYInfo(para,pageindex=0,pagecount=100):
     index=int(pageindex)
     count=int(pagecount)
     kwags={}
     if para['beginDate']!='':
         kwags['begindate__gte']=para['beginDate']
     if para['endDate']!='':
         kwags['enddate__lte']=para['enddate']
     if para['isBig']:
         kwags['big']=para['isBig']
     if para['isState']:
         kwags['customer__isstateexprence'] = para['isState']
     if para['customername']!='':
         kwags['customer__name__icontains']=para['customername']
     if para['customeradd']!='':
         kwags['customer__address__icontains']=para['customeradd']
     if para['customerdep']!='':
         kwags['customer__departmentname__icontains']=para['customerdep']
     if para['customermobile']!='':
         kwags['customer__phone']=para['customerphone']
     if para['susdep']!='':
         kwags['customer__compatment_id']=para['susdep']
     #d=Vouchs.objects.filter(**kwags)
     dataresult=Vouchs.objects.all().filter(**kwags)
     resultdata=dataresult[count*index:count*index+count]
     dataheader = {'col1': '编码', 'col2': '客户姓名',  'col3': '客户部门','col4': '客户地址', 'col5': '客户电话', 'col6': '行政区划', 'col7': '数量',
                   'col8': '大宗/零星', 'col9': '公费/私费'
                   }

     result=[]

     result=[{'col1':v.code,'col7':v.count,'col2':v.customer.name,'col4':v.customer.address
       ,'col3':v.customer.departmentname,'col5':v.customer.phone,'col6':v.customer.compatment.susdepname
       ,'col8':( '大宗' if v.big else '零星' ),'col9':('公费' if v.customer.isstateexprence else '公费')} for v in resultdata]

     returnresult={'datalength':int(round(len(dataresult)/count)),'datalist':result,'datahead':dataheader}
     return  returnresult
#报纸信息查询

def crateuser(para):
    User.objects.create(username=para['username'],password=para['password'])
    User.save()
def islogin(para):
    return User.objects.filter(username__exact=para['username'],userpassword__exact=para['password'])

def GetDailyinfo(para):
    kwargs={}
    if para['begindate']!='':
        kwargs['date__gte']=para['begindate']
    if para['enddate']!='':
        kwargs['date__lte']=para['enddate']
    if para['content']!='':
        kwargs['content__contains']=para['content']
    if para['susdep']!='':
        kwargs['info__contains']=para['susdep']
    daiinfo=dailyinfo.objects.filter(**kwargs)
    datahead={'col1':'题目','col2':'日期','col3':'版面','col4':'作者','col5':'区域'}
    result=[{'col1':v.title,'content':v.content,'id':v.id,'col4':v.auth,'img':'/'.join([v.url,v.image]),'col5':v.info,'col2':v.date,'col3':v.banshu} for v in daiinfo]
    return  {'datahead':datahead,'datalist':result}
def GetRegion(suscode):
    datavlues=susDep.objects.filter(susdepcode__startswith=suscode,susdepcode__endswith='000000')
    result=[]
    for d in datavlues:
        result.append({'code':d.susdepcode,'value':d.susdepname})
#将数据格式化写入EXCEL
import  re
def insertDataToExcel(data):
    #定义一个数据表

    valuedata=eval(data['data'])
    print(valuedata)



    dataworkbook=xlwt.Workbook("encoding='utf-8'")
    datasheet=dataworkbook.add_sheet('datasheet')
    style_heading=xlwt.easyxf("""
    font:
        name Arial,
        colour_index white,
        bold on,
        height 0XA0;
    align:
        wrap off,
        vert center,
        horiz center;
    pattern:
        pattern solid,
        fore-colour 0X19;
    borders:
        left THIN,
        right THIN,
        top THIN,
        bottom THIN

    """)
    stylebody=xlwt.easyxf("""
    font:
        name Arial,
        colour_index black,
        bold on,
        height 0XA0;
    align:
        wrap off,
        vert center,
        horiz center;
    borders:
        left THIN,
        right THIN,
        top THIN,
        bottom THIN

    """)
    datahaead = [v for  v in valuedata['datahead']]

    colindex=0
    #写入表头
    for col in range(1,len(datahaead)+1):
        datasheet.write(0,col-1,valuedata["datahead"]["col"+repr(col)])

    rowindex=1
    collength=len(datahaead)
    datalist=valuedata['datalist']
    rowscount=len(datalist)

    for row in datalist:
        colindex=0
        for colname in range(1,len(datahaead)+1):
            datasheet.write(rowindex, colname-1, row['col'+repr(colname)])
        rowindex=rowindex+1


    #写入数据

    #res=BytesIO()
    #dataworkbook.save(res)
    return  dataworkbook


if __name__ == '__main__':
    data={
        'head':{'col1':'部门','col2':'人员','col3':'成绩'},
        'data':[
            {'col1':'财务部','col2':'谢志刚','col3':100},
            {'col1':'技术部','col2':'张小峰','col3':100}

        ]
    }
    insertDataToExcel(data)



















    




