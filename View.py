from  django.shortcuts import HttpResponse,HttpResponseRedirect,render,render_to_response
from django.http import  JsonResponse
from  shanxidaily import  DailyController,models
from  django.views.decorators.csrf import  csrf_exempt
from  django import  forms
import  json
import  xlwt
import  re
def register(request):
    if request.method=='POST':
        uf=request.POST
        DailyController.crateuser(para=uf)
        return  HttpResponse('注册成功')
    return  render_to_response('regist.html')
#登录
def GetSum(request):

    sumdata=DailyController.GetSumByDecument()
    return  JsonResponse(sumdata,safe=False)
def GetSumView(request):
    if request.method=='POST':
        sumdata = DailyController.GetSumByDecument()
        return JsonResponse(sumdata, safe=False)
    else:
        return  render_to_response('GetSumDep.html')

def login(request):
    if request.method=='POST':
        us=request.POST
        if DailyController.islogin(para=us):
            res=HttpResponseRedirect('/index/')
            res.set_cookie('username',us['username'],3600)
            return res
        else:
            return  render_to_response('login.html')
    else:
        return render_to_response('login.html')

#将数据导入到
def ExportDatatoexcel(requset):
    response=HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition']='attechment;filename=data.xls'


    data=requset.POST

    res=DailyController.insertDataToExcel(data)
    #response['Content-length']=len(res)

    res.save(response)
    return  response

def index(request):
    username=request.COOKIES.get('username','')
    print(username)
    if username=='' or  username is None:
        return  render_to_response('login.html')
    else:
        return  render_to_response('index.html',{'form':models.SelectForm(),'username':username})
def GetDaily(request):
    username = request.COOKIES.get('username', '')
    print(username)
    if username == '' or username is None:
        return render_to_response('login.html')
    else:
        return  render_to_response('Dailyinfo.html',{'form':models.dailyForm()})
def inserdatavouchs(request):
    DailyController.insertVouchDataFromSheet()
def GetDailyinfo(request):
    if request.method=='POST':
        postdata=request.POST
        paradata = {k: v[0] if len(v) == 1 else v for k, v in postdata.lists()}
        resultata=DailyController.GetDailyinfo(paradata)
        return  JsonResponse(resultata,safe=False)





def datachoice(request,pageindex,pagesize):
    if request.method=='POST':
        postdata=request.POST
        paradata={k:v[0] if len(v)==1 else v for k,v in postdata.lists()}
        paradata['isBig']=not (paradata.get('isBig') is None)
        paradata['isState']=not (paradata.get('isState') is None)

        resultdata=DailyController.GetDailYInfo(paradata,pageindex=pageindex,pagecount=pagesize)
        return JsonResponse(resultdata,safe=False)
def susdepvalue(request,suscode):

    return  JsonResponse(DailyController.GetRegion(suscode=suscode))
def ajax_list(request):
    a=range(100)
    return  JsonResponse(json.dumps(a), safe=False)
def ajax_dict(request):
    name_dict={'twz':'Love Python and Django','zqxt':'I am teaching Django'}
    return  JsonResponse(json.dumps(name_dict))
