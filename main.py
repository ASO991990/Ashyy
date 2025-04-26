from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
    incoming_msg = request.values.get('Body', '').lower()
    print(f"Received message: {incoming_msg}")

    response_message = "أهلاً وسهلاً! أنا Ashyy من مركز ASO. كيف فيني أساعدك اليوم؟"

    return Response(f"<Response><Message>{response_message}</Message></Response>", mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
