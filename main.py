from flask import Flask, request, Response
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# إعداد الاتصال بجوجل شيت
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Ashyy Patients").sheet1  # اسم الشيت بالضبط

# تخزين حالة كل مستخدم
user_data = {}

@app.route('/message', methods=['POST'])
def message():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '').strip()

    reply = ""

    if from_number not in user_data:
        user_data[from_number] = {"step": 0}

    step = user_data[from_number]["step"]

    if step == 0:
        reply = ("أهلا وسهلا فيك مع Ashyy من مركز ASO!\n"
                 "أنا معك بخطواتك الجاي. خلينا نبلش نتعرف عليك...\n"
                 "شو اسمك الكامل؟")
        user_data[from_number]["step"] = 1

    elif step == 1:
        user_data[from_number]["name"] = incoming_msg
        reply = "قديش عمرك؟"
        user_data[from_number]["step"] = 2

    elif step == 2:
        user_data[from_number]["age"] = incoming_msg
        reply = "من أي بلد انت؟"
        user_data[from_number]["step"] = 3

    elif step == 3:
        user_data[from_number]["country"] = incoming_msg
        reply = "شو نوع البتر يلي عندك؟ (تحت الركبة / فوق الركبة / يد / إصبع...)" 
        user_data[from_number]["step"] = 4

    elif step == 4:
        user_data[from_number]["amputation_type"] = incoming_msg
        reply = "بأي جهة (يمين أو شمال)؟"
        user_data[from_number]["step"] = 5

    elif step == 5:
        user_data[from_number]["side"] = incoming_msg
        reply = "تتذكر بأي سنة صار البتر؟"
        user_data[from_number]["step"] = 6

    elif step == 6:
        user_data[from_number]["amputation_year"] = incoming_msg
        reply = "شو سبب البتر؟ (حادث / مرض / حرب / خلقي...)"
        user_data[from_number]["step"] = 7

    elif step == 7:
        user_data[from_number]["reason"] = incoming_msg
        reply = "شو حالتك الاجتماعية؟ (عازب / متزوج / مع أطفال...)"
        user_data[from_number]["step"] = 8

    elif step == 8:
        user_data[from_number]["social_status"] = incoming_msg
        reply = "بشكل عام، كيف بتحس حالك نفسياً؟ (مبسوط / مضغوط / تعبان...)"
        user_data[from_number]["step"] = 9

    elif step == 9:
        user_data[from_number]["mental_status"] = incoming_msg
        reply = "معك طرف اصطناعي حالياً؟ (نعم / لا)"
        user_data[from_number]["step"] = 10

    elif step == 10:
        user_data[from_number]["have_prosthesis"] = incoming_msg
        if incoming_msg.lower() == "نعم":
            reply = "ممكن تحكيلي شوي عن نوع الطرف وكيف حاسه؟"
            user_data[from_number]["step"] = 11
        else:
            reply = "معك محامي بخصوص الاطراف او التأمينات؟ (نعم / لا)"
            user_data[from_number]["step"] = 12

    elif step == 11:
        user_data[from_number]["prosthesis_details"] = incoming_msg
        reply = "معك محامي بخصوص الاطراف او التأمينات؟ (نعم / لا)"
        user_data[from_number]["step"] = 12

    elif step == 12:
        user_data[from_number]["have_lawyer"] = incoming_msg

        # تسجيل كل البيانات بجوجل شيت
        sheet.append_row([
            user_data[from_number].get("name", ""),
            user_data[from_number].get("age", ""),
            user_data[from_number].get("country", ""),
            user_data[from_number].get("amputation_type", ""),
            user_data[from_number].get("side", ""),
            user_data[from_number].get("amputation_year", ""),
            user_data[from_number].get("reason", ""),
            user_data[from_number].get("social_status", ""),
            user_data[from_number].get("mental_status", ""),
            user_data[from_number].get("have_prosthesis", ""),
            user_data[from_number].get("prosthesis_details", ""),
            user_data[from_number].get("have_lawyer", ""),
            from_number
        ])

        reply = ("شكراً من القلب على ثقتك!\n"
                 "أنا Ashyy موجود دايمًا تدعمني خطوة بخطوة.\n"
                 "إذا بتحب تحكي مع سكرتاريا ASO، إحنا دايمًا جاهزين: 050-9959101.\n"
                 "ASO - دايمًا معك على طول الطريق!")

        del user_data[from_number]  # حذف بيانات المستخدم بعد التخزين

    return Response(f"<Response><Message>{reply}</Message></Response>", mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
