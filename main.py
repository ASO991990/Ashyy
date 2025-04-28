from flask import Flask, request
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد مفتاح OpenAI (بدك تحط مفتاحك الشخصي هون)
openai.api_key = 'YOUR-OPENAI-API-KEY'

# إعداد الاتصال مع Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)
sheet = client.open('Ashyy Patients').sheet1

# دالة معالجة الرسائل
@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    sender = request.values.get('From', '')
    
    # إرسال الطلب لـ OpenAI عشان يرد بطريقة ذكية ومهنية
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "انت أخصائي أطراف صناعية وأجهزة مساعدة، خبير نفسي وصديق داعم، تتحدث بالعامية الفلسطينية بشكل حنون ومحترف. تحاول دائمًا فهم المريض ومساعدته بدون أن تكون رسمي جدًا."},
            {"role": "user", "content": incoming_msg}
        ]
    )
    
    reply = response['choices'][0]['message']['content'].strip()
    
    # تخزين تفاصيل المريض في Google Sheets
    row = [sender, incoming_msg, reply]
    sheet.append_row(row)

    # تجهيز الرد عالواتساب
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)
    
    return str(resp)

if __name__ == "__main__":
    app.run()
