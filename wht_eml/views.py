from django.shortcuts import render
import gspread
import pywhatkit
from django.core.mail import EmailMessage

# Create your views here.

def index(request):
    return render(request , 'index.html')

def whtsapp(request):
    if request.method =='POST':
        wksht = request.POST.get('sheetName')
        gc = gspread.service_account(filename='sheetAuth2.json')

        wks = gc.open('PRIVATE OPD DATA').worksheet(f'{wksht}')
        li = []
        ln =[]
        for i in wks.get_all_records():
            if i['Contact No'] != '':
                try:
                    pywhatkit.sendwhatmsg_instantly(phone_no=f"+91{i['Contact No']}", message=i.get('Message'),tab_close=True)
                    li.append(i["Doctor's Name"])
                except Exception as e:
                    print(e)
                    ln.append(i["Doctor's Name"])
                    print(f'''whtsapp has not sent to {i["Doctor's Name"]}''')     
            elif i['Contact No'] == '':
                break
        print(ln)
        context = {'li':li , 'ln':ln}
        return render (request, 'sentt_whts.html' , context )
    else :
        return render(request , 'sentt_whts.html')

def emaill(request):
    if request.method =='POST':
        wksht = request.POST.get('sheetName')
        gc = gspread.service_account(filename='sheetAuth2.json')

        wks = gc.open('PRIVATE OPD DATA').worksheet(f'{wksht}')
        li = []
        ln = []
        for i in wks.get_all_records():
            if i['Email Id'] != '': 
                msg =  i.get('Message')
                try:
                    email = EmailMessage(body= msg , from_email= 'nancy.choudhary@cmcludhiana.in' , to= [i['Email Id']])
                    email.send()
                    li.append(i['Email Id'])
                    print(f'mail has been send to {i["Email Id"]}')
                except Exception as e:
                    ln.append(i['Email Id'])
                    print(f"maillllll has not sent to {i['Email Id']}")
            elif i['Email Id'] == '':
                break
        context = {'li':li , 'ln':ln}
        return render (request, 'sentt_email.html' , context )

    else :
        return render(request , 'sentt_email.html')