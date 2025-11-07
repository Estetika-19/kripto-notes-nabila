from cryptography.fernet import Fernet

# Kunci simetris tetap (bisa di-generate dan disimpan jika mau)
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_file(input_path, output_path):
    with open(input_path, 'rb') as f:
        data = f.read()
    encrypted = cipher.encrypt(data)
    with open(output_path, 'wb') as f:
        f.write(encrypted)

def decrypt_file(input_path, output_path):
    with open(input_path, 'rb') as f:
        data = f.read()
    decrypted = cipher.decrypt(data)
    with open(output_path, 'wb') as f:
        f.write(decrypted)
