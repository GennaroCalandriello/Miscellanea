from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)
openai.api_key = ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    prompt = data["message"]
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return jsonify({"response": response.choices[0].text.strip()})


if __name__ == "__main__":
    app.run(debug=True)
