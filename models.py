#coding:utf-8
from  django.db import  models
from  django import  forms
'''系统数据库模型'''
'''行业系统表'''
'用户表'
class User(models.Model):
    class Meta:
        db_table='user'
    username=models.CharField(max_length=50)
    userpassword=models.CharField(max_length=50)

class Comdartment(models.Model):
    class Meta:
        db_table='comdartment'
    Code=models.IntegerField(name='code')
    susdepname=models.CharField(name='susdepname',max_length=200)
    susdepcode=models.CharField(name='susdepcode',max_length=200)
'''行政区划'''
class susDep(models.Model):
    class Meta:
        db_table='susdep'
    susdepname=models.CharField(name='susdepname',max_length=200)
    susdepcode=models.CharField(name='susdepcode',max_length=20,primary_key=True)
'''客户表'''
class customer(models.Model):
    class Meta:
        db_table='customer'
    code=models.CharField(max_length=200,primary_key=True,unique=True)
    name=models.CharField(max_length=100,name='name',null=True)
    departmentname=models.CharField(max_length=400,name='departmentname',null=True)
    address=models.CharField(max_length=200,name='address',null=True)
    phone=models.CharField(max_length=100,name='phone',null=True)
    isstateexprence=models.SmallIntegerField(name='isstateexprence',default=0,null=True)
    systomcode=models.CharField(max_length=200,name='systomcode',null=True)
    compatment=models.ForeignKey(susDep)
    compartmentcode=models.CharField(max_length=200,name='compartmentcode',null=True)
'''订单表'''
class Vouchs(models.Model):
    class Meta:
        db_table='vouchs'
    code=models.CharField(max_length=200,primary_key=True,unique=True)
    sdate=models.DateField(name='sdate')
    begindate=models.DateField(name='begindate')
    enddate=models.DateField(name='enddate')
    count=models.IntegerField(name='count')
    subsdep=models.CharField(max_length=200,name='subsdep')
    big=models.SmallIntegerField(name='big',default=0)
    customer=models.ForeignKey(customer)
    #行政区划

    fee=models.FloatField(name='fee')

'''报纸信息表'''
class dailyinfo(models.Model):
    class Meta:
        db_table='dailyinfo'
    id=models.IntegerField(primary_key=True,auto_created=True,default=101)
    title=models.CharField(max_length=500,name='title')
    content=models.TextField(name='content')
    image=models.CharField(max_length=300,name='image')
    date=models.DateField(name='date')
    banshu=models.IntegerField(name='banshu')
    url=models.CharField(max_length=500,name='url')
    info=models.CharField(max_length=200,name='info')
    auth=models.CharField(max_length=200,name='auth')
class SelectForm(forms.Form):
    depchoice=susDep.objects.filter(susdepcode__startswith='610',susdepcode__endswith='000000')
    choice=[]
    for v in depchoice:
        choice.append((v.susdepcode,v.susdepname))
    customername=forms.CharField(max_length=100,label='客户名称',widget=forms.TextInput(attrs={'class':'easyui-textbox','data-options':'required:false'}),empty_value='')
    customeradd=forms.CharField(max_length=200,label='客户地址',widget=forms.TextInput(attrs={'class':'easyui-textbox','data-options':'required:false'}))
    customerdep=forms.CharField(max_length=200,label='客户部门',widget=forms.TextInput(attrs={'class':'easyui-textbox','data-options':'required:false'}))
    customermobile=forms.CharField(max_length=200,label='客户电话',widget=forms.TextInput(attrs={'class':'easyui-textbox','data-options':'required:false'}))
    beginDate=forms.DateField(label='起投日',widget=forms.DateInput(attrs={'class':'easyui-datebox','data-options':'required:false,currentText:"今天"'}))
    endDate=forms.DateField(label='截止日',widget=forms.DateInput(attrs={'class':'easyui-datebox','data-options':'required:false'}))
    susdep=forms.CharField(max_length=100,label='区域',widget=forms.Select(choices=choice,attrs={'class':'easyui-combobox'}))
    isBig=forms.BooleanField(label='大宗')
    isState=forms.BooleanField(label='公费')
class dailyForm(forms.Form):
    content=forms.CharField(max_length=300,label='内容',widget=forms.TextInput(attrs={'class':'easyui-textbox','data-options':'required:false'}),empty_value='')
    begindate = forms.DateField(label='起始日期', widget=forms.DateInput(attrs={'class': 'easyui-datebox', 'data-options': 'required:false,currentText:"今天"'}))
    enddate = forms.DateField(label='结束日期', widget=forms.DateInput(attrs={'class': 'easyui-datebox', 'data-options': 'required:false'}))
    susdep=forms.CharField(max_length=100,label='地区',widget=forms.TextInput(attrs={'class':'easyui-textbox','data-options':'required:false'}),empty_value='')















