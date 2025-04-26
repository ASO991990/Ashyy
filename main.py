from flask import Flask, request, Response
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# الاتصال مع Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Ashyy Patients").sheet1

# تخزين بيانات المستخدم
user_data = {}

questions = [
    "شو اسمك الكامل؟",
    "قديش عمرك؟",
    "من أي بلد انت؟",
    "شو نوع البتر يلي عندك؟ (تحت الركبة / فوق الركبة / يد / إصبع...)",
    "بأي جهة (يمين أو شمال)؟",
    "تتذكر بأي سنة صار البتر؟",
    "شو سبب البتر؟ (حادث / مرض / حرب / خلقي...)",
    "شو حالتك الاجتماعية؟ (عازب / متزوج / مع أطفال...)",
    "بشكل عام، كيف بتحس حالك نفسياً؟ (مبسوط / مضغوط / تعبان...)",
    "معك طرف اصطناعي حالياً؟ (نعم / لا)",
    "ممكن تحكيلي شوي عن نوع الطرف وكيف حاسه؟ (اذا مافي طرف، اكتب 'لا')",
    "معك محامي بخصوص الاطراف او التأمينات؟ (نعم / لا)"
]

field_names = [
    "name",
    "age",
    "country",
    "amputation_type",
    "side",
    "amputation_year",
    "reason",
    "social_status",
    "mental_status",
    "have_prosthesis",
    "prosthesis_details",
    "have_lawyer"
]

@app.route('/message', methods=['POST'])
def message():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '').strip()

    reply = ""

    if from_number not in user_data:
        user_data[from_number] = {"step": 0, "answers": []}
        reply = ("أهلا وسهلا فيك مع Ashyy من مركز ASO!\n"
                 "أنا معك بخطواتك الجاي. خلينا نبلش...\n\n" +
                 questions[0])
    else:
        step = user_data[from_number]["step"]
        if step < len(questions):
            user_data[from_number]["answers"].append(incoming_msg)
            user_data[from_number]["step"] += 1

            if user_data[from_number]["step"] < len(questions):
                reply = questions[user_data[from_number]["step"]]
            else:
                # حفظ البيانات في Google Sheets
                answers = user_data[from_number]["answers"]
                row_data = [answers[i] if i < len(answers) else "" for i in range(len(field_names))]
                row_data.append(from_number)
                sheet.append_row(row_data)

                reply = ("شكراً من القلب على ثقتك!\n"
                         "أنا Ashyy موجود دايمًا أدعمك خطوة بخطوة.\n"
                         "إذا بتحب تتواصل مع سكرتاريا ASO، هذا الرقم: 050-9959101.\n"
                         "ASO - دايمًا معك على طول الطريق!")

                del user_data[from_number]  # نمسح بيانات المستخدم بعد الإنهاء
        else:
            reply = "خلصنا التسجيل! إذا بتحب تحكي معنا، تواصل عالرقم: 050-9959101"

    return Response(f"<Response><Message>{reply}</Message></Response>", mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
