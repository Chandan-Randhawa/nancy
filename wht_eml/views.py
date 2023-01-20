from django.shortcuts import render
import gspread
import smtplib , ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import urllib.parse


# Create your views here.

def index(request):
    return render(request , 'index.html')

def whtsapp(request):
    if request.method =='POST':
        wksht = request.POST.get('sheetName')
        gc = gspread.service_account(filename='sheetAuth2.json')

        wks = gc.open('PRIVATE OPD DATA').worksheet(f'{wksht}')
        chrome_options = Options()
        chrome_options.add_argument('C:\chromedriver')
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 50)
        print("SCAN YOUR QR CODE FOR WHATSAPP WEB IF DISPLAYED")
        driver.get("https://web.whatsapp.com/")
        driver.maximize_window()
        print("QR CODE SCANNED")
        li = []
        ln =[]
        for i in wks.get_all_records():
            if i['Contact No'] != '':
                try:
                    # Reference : https://faq.whatsapp.com/en/android/26000030/
                    print("In send_message_to_unsavaed_contact method") 
                    params = {'phone': str(f"91{i['Contact No']}"), 'text': str(i.get('Message'))}
                    end = urllib.parse.urlencode(params)
                    final_url = 'https://web.whatsapp.com/' + 'send?' + end
                    print(final_url)
                    driver.get(final_url)
                    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[@title = "Menu"]')))
                    print("Page loaded successfully.")
                    
                    sleep(2)
                    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]')))
                    wait.until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]'))).click()
                 
                    print("Message sent successfully.")
                    sleep(4)
                    # pywhatkit.sendwhatmsg_instantly(phone_no=f"+919872968689", message=i.get('Message'),tab_close=True)
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
                msgg =  i.get('Message')
                try:
                    msg = MIMEMultipart()
                    msg['From'] = 'nancy.choudhary@cmcludhiana.in'
                    msg['To'] = i['Email Id']
                    msg['Subject'] = 'Private Opd Census'
                    msg.attach(MIMEText(msgg))
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com" , 465 , context=context) as server:
                        server.ehlo()
                        server.login(msg['From'], 'ywnnawkrtdmxutho')
                        server.sendmail(msg['From'], msg['To'], msg.as_string())
                        server.quit()
                    li.append(i['Email Id'])
                    print(f'mail has been send to {i["Email Id"]}')
                except Exception as e:
                    print(e)
                    ln.append(i['Email Id'])
                    print(f"maillllll has not sent to {i['Email Id']}")
            elif i['Email Id'] == '':
                break
        contextt = {'li':li , 'ln':ln}
        return render (request, 'sentt_email.html' , contextt )

    else :
        return render(request , 'sentt_email.html')