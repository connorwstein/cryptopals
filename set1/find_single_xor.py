from set1.single_xor import decrypt_single_byte_xor

lines = []
with open('4.txt') as f:
    lines = f.readlines()
best_score, best_text = float('inf'), ""
for l in lines:
    text, score, _ = decrypt_single_byte_xor(l)
    if score < best_score:
        best_score = score
        best_text = text
print(best_text, best_score)
