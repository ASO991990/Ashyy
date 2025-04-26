from flask import Flask, request, Response

app = Flask(__name__)

# تعريف متغيرات لتخزين البيانات مبدئياً
user_data = {}

@app.route('/message', methods=['POST'])
def message():
    incoming_msg = request.values.get('Body', '').strip().lower()
    from_number = request.values.get('From', '').strip()

    reply = ""

    if from_number not in user_data:
        user_data[from_number] = {"step": 0}

    step = user_data[from_number]["step"]

    if step == 0:
        reply = "أهلاً فيك بمركز ASO! أنا Ashyy. شو اسمك الكامل؟"
        user_data[from_number]["step"] = 1

    elif step == 1:
        user_data[from_number]["name"] = incoming_msg
        reply = "قديش عمرك؟"
        user_data[from_number]["step"] = 2

    elif step == 2:
        user_data[from_number]["age"] = incoming_msg
        reply = "من أي بلد أنت؟"
        user_data[from_number]["step"] = 3

    elif step == 3:
        user_data[from_number]["country"] = incoming_msg
        reply = "شو سبب البتر؟ (حادث، مرض، حرب، آخر...)"
        user_data[from_number]["step"] = 4

    elif step == 4:
        user_data[from_number]["reason"] = incoming_msg
        reply = "البتر بأي جهة؟ (يمين أو شمال؟)"
        user_data[from_number]["step"] = 5

    elif step == 5:
        user_data[from_number]["side"] = incoming_msg
        reply = "البتر من فوق الركبة ولا تحت الركبة؟"
        user_data[from_number]["step"] = 6

    elif step == 6:
        user_data[from_number]["amputation_level"] = incoming_msg
        reply = "شكراً لإجاباتك! فريق ASO رح يتواصل معك قريباً. لو ما تواصلنا خلال يومين، اتصل عالرقم 0509959101."

        # هون نقدر نرسل المعلومات لجوجل شيت بالمستقبل!

    return Response(f"<Response><Message>{reply}</Message></Response>", mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
