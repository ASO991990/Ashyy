from flask import Flask, request

app = Flask(__name__)

# ذاكرة بسيطة تحفظ المرحلة لكل مستخدم
user_sessions = {}

@app.route('/whatsapp', methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')

    if from_number not in user_sessions:
        user_sessions[from_number] = {"stage": "welcome"}

    stage = user_sessions[from_number]["stage"]

    if stage == "welcome":
        reply = ("أهلاً وسهلاً فيك مع مركز ASO!\n"
                 "معك Ashyy، المساعد الشخصي الذكي بإشراف أخصائيين أطراف صناعية معتمدين.\n"
                 "شو نوع البتر عندك؟\n"
                 "١. تحت الركبة\n"
                 "٢. فوق الركبة\n"
                 "٣. طرف علوي\n"
                 "اكتب رقم الخيار.")
        user_sessions[from_number]["stage"] = "bter_type"

    elif stage == "bter_type":
        if incoming_msg in ["1", "2", "3"]:
            user_sessions[from_number]["bter_type"] = incoming_msg
            reply = ("أي جهة البتر؟\n"
                     "١. يمين\n"
                     "٢. يسار\n"
                     "٣. الطرفين\n"
                     "اكتب رقم الخيار.")
            user_sessions[from_number]["stage"] = "side"
        else:
            reply = "رجاءً اختار ١ أو ٢ أو ٣ لنوع البتر."

    elif stage == "side":
        if incoming_msg in ["1", "2", "3"]:
            user_sessions[from_number]["side"] = incoming_msg
            reply = ("هل عندك طرف اصطناعي حالي؟\n"
                     "١. نعم\n"
                     "٢. لا\n"
                     "اكتب رقم الخيار.")
            user_sessions[from_number]["stage"] = "has_prosthesis"
        else:
            reply = "رجاءً اختار ١ أو ٢ أو ٣ للجهة."

    elif stage == "has_prosthesis":
        if incoming_msg in ["1", "2"]:
            user_sessions[from_number]["has_prosthesis"] = incoming_msg
            reply = ("شو نوع المشكلة الأساسية اللي بتحسها؟\n"
                     "١. وجع بالجلد\n"
                     "٢. التهابات\n"
                     "٣. عدم توازن\n"
                     "٤. شيء آخر\n"
                     "اكتب رقم الخيار.")
            user_sessions[from_number]["stage"] = "problem"
        else:
            reply = "رجاءً اختار ١ أو ٢ بوضوح."

    elif stage == "problem":
        if incoming_msg in ["1", "2", "3", "4"]:
            user_sessions[from_number]["problem"] = incoming_msg
            reply = ("حابب نرتبلك استشارة شخصية مع أخصائي أطراف صناعية من مركز ASO؟\n"
                     "١. نعم\n"
                     "٢. لا\n"
                     "اكتب رقم الخيار.")
            user_sessions[from_number]["stage"] = "consult"
        else:
            reply = "رجاءً اختار ١، ٢، ٣ أو ٤ لنوع المشكلة."

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
            reply = "رجاءً اختار ١ أو ٢ عشان نكمل."

    else:
        reply = "صار في خطأ بسيط، ممكن تكتب مرحبا نبدأ من أول وجديد؟"

    response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

    return response, 200, {'Content-Type': 'application/xml'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
