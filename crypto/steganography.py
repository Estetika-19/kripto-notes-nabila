from PIL import Image
from io import BytesIO

# ========== RAIL FENCE CIPHER ==========

def railfence_encrypt(text, key):
    rail = [''] * key
    row, step = 0, 1
    for ch in text:
        rail[row] += ch
        if row == 0:
            step = 1
        elif row == key - 1:
            step = -1
        row += step
    return ''.join(rail)

def railfence_decrypt(cipher, key):
    n = len(cipher)
    rail = [['\n'] * n for _ in range(key)]
    dir_down, row, col = None, 0, 0
    for i in range(n):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1
    index = 0
    for i in range(key):
        for j in range(n):
            if rail[i][j] == '*' and index < n:
                rail[i][j] = cipher[index]
                index += 1
    result = []
    row, col = 0, 0
    for i in range(n):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        if rail[row][col] != '\n':
            result.append(rail[row][col])
            col += 1
        row += 1 if dir_down else -1
    return ''.join(result)


# ========== LSB STEGANOGRAPHY ==========

def lsb_hide(input_image_path, secret_text, output_image_path):
    img = Image.open(input_image_path).convert("RGB")
    encoded = img.copy()
    width, height = img.size
    index = 0

    # ubah teks ke biner + tanda akhir (00000000 sebagai terminator)
    binary_secret = ''.join(format(ord(c), '08b') for c in secret_text)
    binary_secret += '00000000'

    for row in range(height):
        for col in range(width):
            if index < len(binary_secret):
                pixel = list(img.getpixel((col, row)))
                for n in range(3):  # RGB
                    if index < len(binary_secret):
                        pixel[n] = pixel[n] & ~1 | int(binary_secret[index])
                        index += 1
                encoded.putpixel((col, row), tuple(pixel))
    encoded.save(output_image_path)


def lsb_extract(image_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    bits = []

    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for n in range(3):
                bits.append(str(pixel[n] & 1))

    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        val = int(''.join(byte), 2)
        if val == 0:  # terminator
            break
        chars.append(chr(val))
    return ''.join(chars)
