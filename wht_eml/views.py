from django.shortcuts import render
import gspread
import pywhatkit
from django.core.mail import send_mail , EmailMessage



# Create your views here.

def index(request):
    return render(request , 'index.html')

async def whtsapp(request):
    if request.method =='POST':
        wksht = request.POST.get('sheetName')
        gc = gspread.service_account(filename='sheetAuth2.json')

        wks = gc.open('PRIVATE OPD DATA').worksheet(f'{wksht}')
        li = []
        for i in wks.get_all_records():
            if i['Contact No'] != '':
                # print(i.get('Message'))
                pywhatkit.sendwhatmsg_instantly(phone_no=f"+91{i['Contact No']}", message=i.get('Message'),tab_close=True)
                li.append(['Contact No'])
            elif i['Contact No'] == '':
                break
        context = {'li':li}
        return render (request, 'sentt_email.html' , context )
    else :
        return render(request , 'index.html')

def emaill(request):
    if request.method =='POST':
        wksht = request.POST.get('sheetName')
        gc = gspread.service_account(filename='sheetAuth2.json')

        wks = gc.open('PRIVATE OPD DATA').worksheet(f'{wksht}')
        li = []
        for i in wks.get_all_records():
            if i['Email Id'] != '': 
                msg =  i.get('Message')
                email = EmailMessage( body=  msg , from_email= 'opd.coordinator@cmcludhiana.in' , to= [i['Email Id']])
                email.send()
                li.append(i['Email Id'])

            elif i['Email Id'] == '':
                break
        context = {'li':li}
        return render (request, 'sentt_email.html' , context )

    else :
        return render(request , 'index.html')