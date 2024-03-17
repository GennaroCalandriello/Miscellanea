import tkinter as tk
from tkinter import scrolledtext
import openai
from decouple import config

openai.api_key =""

root = tk.Tk()
root.title("chatGPT GUI")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

input_label = tk.Label(frame, text="Chiedi pure maestro: ")
input_label.pack()
input_text = tk.Text(frame, wrap=tk.WORD, width=150, height=5)
input_text.pack()


def get_GPT_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()


def submit_query():

    query = input_text.get("1.0", tk.END)
    if query:
        response = get_GPT_response(query)
        output_text.configure(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, response)
        output_text.configure(state="disabled")


submit_button = tk.Button(frame, text="Submit", command=submit_query)
submit_button.pack(pady=10)

output_label = tk.Label(frame, text="ChatGPT risponde: ")
output_label.pack()

output_text = scrolledtext.ScrolledText(
    frame, wrap=tk.WORD, width=150, height=50, state="disabled"
)
output_text.pack()

root.mainloop()
