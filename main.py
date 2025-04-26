from flask import Flask, request

app = Flask(__name__)

user_sessions = {}

def normalize_numbers(text):
    # تحويل الأرقام العربية لأرقام إنجليزية
    arabic_numbers = '٠١٢٣٤٥٦٧٨٩'
    english_numbers = '0123456789'
    table = str.maketrans(arabic_numbers, english_numbers)
    return text.translate(table)

@app.route('/whatsapp', methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip()
    incoming_msg = normalize_numbers(incoming_msg.replace(" ", "").lower())

    from_number = request.values.get('From', '')

    if from_number not in user_sessions:
        user_sessions[from_number] = {"stage": "welcome"}

    stage = user_sessions[from_number]["stage"]

    if stage == "welcome":
        reply = ("أهلاً وسهلاً فيك مع مركز ASO!\n"
                 "معك Ashyy، المساعد الشخصي الذكي بإشراف أخصائيين أطراف صناعية معتمدين.\n"
                 "شو نوع البتر عندك؟\n"
                 "1. تحت الركبة\n"
                 "2. فوق الركبة\n"
                 "3. طرف علوي\n"
                 "اكتب رقم الخيار.")
        user_sessions[from_number]["stage"] = "bter_type"

    elif stage == "bter_type":
        if incoming_msg in ["1", "2", "3"]:
            user_sessions[from_number]["bter_type"] = incoming_msg
            user_sessions[from_number]["stage"] = "side"
            reply = ("أي جهة البتر؟\n"
                     "1. يمين\n"
                     "2. يسار\n"
                     "3. الطرفين\n"
                     "اكتب رقم الخيار.")
        else:
            reply = "رجاءً اختار 1 أو 2 أو 3 لنوع البتر."

    elif stage == "side":
        if incoming_msg in ["1", "2", "3"]:
            user_sessions[from_number]["side"] = incoming_msg
            user_sessions[from_number]["stage"] = "has_prosthesis"
            reply = ("هل عندك طرف اصطناعي حالي؟\n"
                     "1. نعم\n"
                     "2. لا\n"
                     "اكتب رقم الخيار.")
        else:
            reply = "رجاءً اختار 1 أو 2 أو 3 للجهة."

    elif stage == "has_prosthesis":
        if incoming_msg in ["1", "2"]:
            user_sessions[from_number]["has_prosthesis"] = incoming_msg
            user_sessions[from_number]["stage"] = "problem"
            reply = ("شو نوع المشكلة الأساسية اللي بتحسها؟\n"
                     "1. وجع بالجلد\n"
                     "2. التهابات\n"
                     "3. عدم توازن\n"
                     "4. شيء آخر\n"
                     "اكتب رقم الخيار.")
        else:
            reply = "رجاءً اختار 1 أو 2 بوضوح."

    elif stage == "problem":
        if incoming_msg in ["1", "2", "3", "4"]:
            user_sessions[from_number]["problem"] = incoming_msg
            user_sessions[from_number]["stage"] = "consult"
            reply = ("حابب نرتبلك استشارة شخصية مع أخصائي أطراف صناعية من مركز ASO؟\n"
                     "1. نعم\n"
                     "2. لا\n"
                     "اكتب رقم الخيار.")
        else:
            reply = "رجاءً اختار 1 أو 2 أو 3 أو 4 لنوع المشكلة."

    elif stage == "consult":
        if incoming_msg in ["1", "2"]:
            if incoming_msg == "1":
                reply = ("ممتاز!\n"
                         "عشان نرتبلك استشارة شخصية مع أخصائي الأطراف الصناعية بمركز ASO، "
                         "تواصل معنا على الرقم: +972509959101.\n"
                         "شكراً لتواصلك مع Ashyy!")
            else:
                reply = "ولا يهمك، أنا موجود دائماً إذا بدك أي مساعدة ثانية!"
            user_sessions.pop(from_number)
        else:
            reply = "رجاءً اختار 1 أو 2 عشان نكمل."

    else:
        reply = "صار في خطأ بسيط، ممكن تكتب مرحبا نبدأ من أول وجديد؟"

    response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

    return response, 200, {'Content-Type': 'application/xml'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
