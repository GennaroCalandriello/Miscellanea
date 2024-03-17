import openai
import numpy as np
import string

frase = input("Inserisci la frase:  ")
openai.api_key = "zoccol"
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": frase}],
)
void = []

with open("inventaRaffaele.txt", "w") as file:

    file.write(void)

stringa = str(completion.choices[0].message)
stringa.rstrip(string.punctuation)

with open("interaction.txt", "w") as interaction:
    interaction.write(stringa)

print("Done!")

