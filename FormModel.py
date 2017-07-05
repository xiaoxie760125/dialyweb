from  django import  forms
from  shanxidaily.DailyController import  susDep,Vouchs
class SelectForm(forms.Form):
    depSystem=susDep.objects.filter(susDepCode__startswith='6101')
    depselect=forms.ChoiceField(choices=((d.susDepCode,d.susDepName) for d in depSystem),label='地区')
    cusomername=forms.CharField(max_length=100,label='客户名称')
    customeradd=forms.CharField(max_length=200,label='客户地址')
    customerdep=forms.CharField(max_length=200,label='客户部门')
    customermobile=forms.CharField(max_length=200,label='客户电话')