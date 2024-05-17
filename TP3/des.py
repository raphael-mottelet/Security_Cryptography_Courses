import base64
from des_tables import PC1, PC2, IP, IP_inv, E, P, S_BOXES, SHIFTS

def permute(block, table):
    return [block[x - 1] for x in table]

def string_to_bit_array(text):
    return [int(bit) for char in text for bit in f"{ord(char):08b}"]

def bit_array_to_string(array):
    return ''.join(chr(int(''.join(map(str, byte)), 2)) for byte in nsplit(array, 8))

def nsplit(s, n):
    return [s[k:k + n] for k in range(0, len(s), n)]

def xor(t1, t2):
    return [x ^ y for x, y in zip(t1, t2)]

def shift_left(array, n):
    return array[n:] + array[:n]

def generate_keys(key):
    key = permute(key, PC1)
    left, right = nsplit(key, 28)
    keys = []
    for i, shift in enumerate(SHIFTS):
        left, right = shift_left(left, shift), shift_left(right, shift)
        round_key = permute(left + right, PC2)
        keys.append(round_key)
        print(f"Clé dérivée {i + 1}: {''.join(map(str, round_key))}")
    return keys

def substitute(d_e):
    result = []
    for i, block in enumerate(nsplit(d_e, 6)):
        row, col = int(f"{block[0]}{block[5]}", 2), int(''.join(map(str, block[1:5])), 2)
        result.extend(int(bit) for bit in f"{S_BOXES[i][row][col]:04b}")
    return result

def des_crypt(block, keys):
    block = permute(block, IP)
    left, right = nsplit(block, 32)
    for i, key in enumerate(keys):
        temp = permute(substitute(xor(key, permute(right, E))), P)
        left, right = right, xor(left, temp)
        print(f"Cycle {i + 1}: L = {''.join(map(str, left))}, R = {''.join(map(str, right))}")
    return permute(right + left, IP_inv)

def pad_message(message):
    pad_len = 8 - (len(message) % 8)
    return message + chr(pad_len) * pad_len

def encrypt(plaintext, keys):
    plaintext = pad_message(plaintext)
    plaintext_blocks = nsplit(string_to_bit_array(plaintext), 64)
    encrypted_blocks = [des_crypt(block, keys) for block in plaintext_blocks]
    return bit_array_to_string(sum(encrypted_blocks, []))

def main():
    key = input("Entrez la clé (8 caractères): ")
    message = input("Entrez le message à chiffrer: ")

    if len(key) != 8:
        print("La clé doit contenir exactement 8 caractères.")
        return

    key_bits = string_to_bit_array(key)
    keys = generate_keys(key_bits)

    ciphertext = encrypt(message, keys)
    ciphertext_base64 = base64.b64encode(ciphertext.encode()).decode()
    print("Message chiffré (base64):", ciphertext_base64)

if __name__ == "__main__":
    main()
