BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def char_to_ascii(char):
    ascii_code = ord(char)
    print(f"char_to_ascii('{char}') -> {ascii_code}")
    return ascii_code

def ascii_to_bin(ascii_code):
    bin_str = f"{ascii_code:08b}"
    print(f"ascii_to_bin({ascii_code}) -> '{bin_str}'")
    return bin_str

def bin_to_base64char(bin_str):
    index = int(bin_str, 2)
    base64_char = BASE64_CHARS[index]
    print(f"bin_to_base64char('{bin_str}') -> '{base64_char}'")
    return base64_char

def base64char_to_bin(base64_char):
    index = BASE64_CHARS.index(base64_char)
    bin_str = f"{index:06b}"
    print(f"base64char_to_bin('{base64_char}') -> '{bin_str}'")
    return bin_str

def bin_to_ascii(bin_str):
    ascii_code = int(bin_str, 2)
    print(f"bin_to_ascii('{bin_str}') -> {ascii_code}")
    return ascii_code

def ascii_to_char(ascii_code):
    char = chr(ascii_code)
    print(f"ascii_to_char({ascii_code}) -> '{char}'")
    return char

def encode_base64(input_str):
    ascii_codes = [char_to_ascii(char) for char in input_str]
    bin_str = ''.join([ascii_to_bin(ascii_code) for ascii_code in ascii_codes])
    bin_chunks = [bin_str[i:i+6] for i in range(0, len(bin_str), 6)]
    bin_chunks[-1] = bin_chunks[-1].ljust(6, '0')
    base64_chars = [bin_to_base64char(chunk) for chunk in bin_chunks]
    base64_str = ''.join(base64_chars)
    while len(base64_str) % 4 != 0:
        base64_str += '='
    print(f"encode_base64('{input_str}') -> '{base64_str}'")
    return base64_str

def decode_base64(base64_str):
    padding_count = base64_str.count('=')
    base64_str = base64_str.rstrip('=')
    bin_str = ''.join([base64char_to_bin(char) for char in base64_str])
    bin_chunks = [bin_str[i:i+8] for i in range(0, len(bin_str), 8)]
    if padding_count:
        bin_chunks = bin_chunks[:-padding_count]
    ascii_codes = [bin_to_ascii(chunk) for chunk in bin_chunks]
    decoded_chars = [ascii_to_char(ascii_code) for ascii_code in ascii_codes]
    decoded_str = ''.join(decoded_chars)
    print(f"decode_base64('{base64_str}') -> '{decoded_str}'")
    return decoded_str

def main():
    input_str = input("Entrez la chaîne à encoder en Base 64: ")
    encoded_str = encode_base64(input_str)
    print(f"Chaîne encodée: {encoded_str}")
    
    encoded_input = input("Entrez la chaîne Base 64 à décoder: ")
    decoded_str = decode_base64(encoded_input)
    print(f"Chaîne décodée: {decoded_str}")

if __name__ == "__main__":
    main()
