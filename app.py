from flask import Flask, render_template, request
import pickle
import model

app = Flask(__name__)
app.secret_key = 'NaiveBayes'
prd = pickle.load(open('model.pkl', 'rb'))

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    test_mail = ""
    if request.method == "POST":
        test_mail = request.form.get("message")
        if test_mail:
            msgs = [test_mail]
            messages = model.prepare(msgs)
            prediction = prd.predict(messages)
            result = prediction[0].capitalize()
    return render_template("index.html", result=result, test_mail=test_mail)


if __name__ == '__main__':
    app.run(debug=True)
