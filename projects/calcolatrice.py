import numpy as np

sum = 1.74 * 2 + 0.8 + 2.45 + 6 + 4.50 + 0.81 + 0.51 + 0.47 + 3.35 + 1.56 + 0.37
print(sum)

# media ponderata esam
# lista voti
voti = [26, 27, 28, 29, 29, 30, 29, 29, 26]
# lista crediti
crediti = [9, 9, 9, 9, 9, 9, 9, 9, 6]
# media ponderata
media_ponderata = np.average(voti, weights=crediti)
print(media_ponderata)
innovantesimi = media_ponderata * 90 / 30
print(innovantesimi)
