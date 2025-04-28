from flask import Flask, request
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد مفتاح OpenAI
openai.api_key = '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'

# إعداد الاتصال مع Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)
sheet = client.open('Ashyy Patients').sheet1

# إنشاء محادثة ديناميكية
chat_history = {}

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From', '')
    
    if sender not in chat_history:
        chat_history[sender] = []
    
    # إضافة الرسالة للمحادثة
    chat_history[sender].append({"role": "user", "content": incoming_msg})
    
    # إنشاء الرسالة للنموذج
    system_prompt = {
        "role": "system",
        "content": "أنت Ashyy - أخصائي أطراف صناعية، مساعدات طبية، مدرب تأهيل نفسي، صديق داعم. تتحدث مع كل شخص بلغته العفوية (عربية عامية فلسطينية، عبرية، إنجليزية، ألمانية) بطريقة ذكية، حنونة، طبيعية. لا تتصرف كروبوت، بل كشخص إنساني. هدفك: فهم حالة الشخص بالكامل، دعمه عاطفيًا، إعطائه نصائح حقيقية، وجذبه لمركز ASO بدون دعاية مباشرة. اجمع معلومات عن الاسم، العمر، مكان السكن، وقت وسبب البتر، الحالة النفسية، الحاجة لطرف صناعي، واحفظها. ساعده بتحسين مستواه الحركي (AMP Level)."
    }
    
    # بناء الرسائل
    messages = [system_prompt] + chat_history[sender]
    
    # إرسال للـ GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    reply = response['choices'][0]['message']['content'].strip()
    
    # إضافة رد البوت للمحادثة
    chat_history[sender].append({"role": "assistant", "content": reply})
    
    # تخزين في Google Sheets
    sheet.append_row([sender, incoming_msg, reply])
    
    # الرد عالواتساب
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)
    
    return str(resp)

if __name__ == "__main__":
    app.run()
