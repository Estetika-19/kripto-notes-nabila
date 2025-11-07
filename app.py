from flask import Flask, json, jsonify, render_template, request, redirect, url_for, session, flash, send_file
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os

# ------------------------------------------------------------
# Inisialisasi Flask & Library
# ------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "kriptografisia"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# ------------------------------------------------------------
# Simulasi database (sementara pakai dictionary)
# ------------------------------------------------------------
users = {}

# ------------------------------------------------------------
# Kelas User
# ------------------------------------------------------------
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# ------------------------------------------------------------
# Fungsi Enkripsi & Dekripsi File
# ------------------------------------------------------------
def rc4_encrypt(data: bytes, key: str) -> bytes:
    """RC4 stream cipher untuk enkripsi dan dekripsi (simetris)."""
    S = list(range(256))
    j = 0
    out = []

    # Key-scheduling algorithm (KSA)
    key_bytes = [ord(c) for c in key]
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudo-random generation algorithm (PRGA)
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(byte ^ K)

    return bytes(out)

def encrypt_file(input_path, output_path, key="defaultkey"):
    with open(input_path, "rb") as file:
        data = file.read()
    encrypted_data = rc4_encrypt(data, key)
    with open(output_path, "wb") as file:
        file.write(encrypted_data)


def decrypt_file(input_path, output_path, key="defaultkey"):
    with open(input_path, "rb") as file:
        data = file.read()
    decrypted_data = rc4_encrypt(data, key)  # RC4 itu simetris, pakai fungsi yang sama
    with open(output_path, "wb") as file:
        file.write(decrypted_data)

def encrypt_stream_cipher(text, key):
    # contoh sederhana aja
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

def encrypt_rail_fence(text, key):
    rail = [''] * key
    direction_down = False
    row = 0
    for char in text:
        rail[row] += char
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1
    return ''.join(rail)

# -- Rail Fence decrypt (pastikan ada di file sebelum route /decrypt_diary) --
def decrypt_rail_fence(cipher_text: str, key: int) -> str:
    if key == 1:
        return cipher_text
    # membuat matrix berukuran key x len(cipher_text)
    rail = [['\n' for _ in range(len(cipher_text))] for _ in range(key)]
    dir_down = None
    row, col = 0, 0

    # tandai posisi zig-zag
    for i in range(len(cipher_text)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1

    # isi karakter cipher ke posisi yang sudah ditandai
    index = 0
    for i in range(key):
        for j in range(len(cipher_text)):
            if rail[i][j] == '*' and index < len(cipher_text):
                rail[i][j] = cipher_text[index]
                index += 1

    # baca matrix zig-zag untuk mendapatkan plaintext hasil rail-decrypt stage
    result = []
    row, col = 0, 0
    for i in range(len(cipher_text)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        if rail[row][col] != '\n':
            result.append(rail[row][col])
            col += 1
        row += 1 if dir_down else -1

    return "".join(result)


# -- Stream cipher decrypt (XOR with key repeated) --
def decrypt_stream_cipher(ciphertext: str, key: str) -> str:
    # This must mirror encrypt_stream_cipher (XOR per-character)
    # We will operate on ordinal values and recreate characters.
    if not key:
        return ciphertext
    result_chars = []
    key_len = len(key)
    for i, c in enumerate(ciphertext):
        # convert to ord, xor, convert back
        orig_ord = ord(c) ^ ord(key[i % key_len])
        result_chars.append(chr(orig_ord))
    return "".join(result_chars)



# ------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------

@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/encrypt_file', methods=['GET', 'POST'])
def encrypt_file_page():
    uploads_folder = os.path.join('static', 'uploads')
    os.makedirs(uploads_folder, exist_ok=True)  # pastikan foldernya ada

    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('File tidak valid.', 'danger')
            return redirect(request.url)

        # Simpan file asli
        input_path = os.path.join(uploads_folder, file.filename)
        file.save(input_path)

        # Buat nama output terenkripsi
        output_filename = f"encrypted_{file.filename}"
        output_path = os.path.join(uploads_folder, output_filename)

        # Jalankan fungsi enkripsi
        encrypt_file(input_path, output_path)

        # Kirim file terenkripsi ke user
        return send_file(
            os.path.abspath(output_path),
            as_attachment=True,
            download_name=output_filename
        )

    return render_template('encrypt_file.html')


@app.route('/encrypt_text')
def encrypt_text():
    if 'user' not in session:
        return render_template('encrypt_text.html', require_login=True)

    # 🧾 Baca semua diary milik user yang sedang login
    diaries = []
    try:
        with open('data_diary.json', 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                if data.get('user') == session['user']:
                    diaries.append(data)
    except FileNotFoundError:
        pass  # belum ada diary tersimpan

    return render_template('encrypt_text.html', require_login=False, diaries=diaries)


@app.route('/save_diary', methods=['POST'])
def save_diary():
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'})

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    pin = data.get('pin')

    if not all([title, content, pin]):
        return jsonify({'success': False, 'error': 'Missing fields'})

    # 🔒 Lakukan enkripsi di sini
    encrypted_text = encrypt_stream_cipher(content, pin)
    encrypted_text = encrypt_rail_fence(encrypted_text, 3)

    # Simpan ke database (contoh sederhana file JSON dulu)
    diary_entry = {
    'user': session['user'],
    'title': title,
    'content': encrypted_text,
    'pin': str(pin)   # pastikan string, supaya leading zero aman
    }


    try:
        with open('data_diary.json', 'a', encoding='utf-8') as f:
            json.dump(diary_entry, f)
            f.write('\n')
        return jsonify({'success': True})
    except Exception as e:
        print("Save error:", e)
        return jsonify({'success': False, 'error': str(e)})
    
from flask import jsonify  # pastikan import jsonify ada di header file

@app.route('/decrypt_diary', methods=['POST'])
def decrypt_diary():
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'})

    data = request.get_json()
    encrypted_text = data.get('content')
    pin = data.get('pin')

    if not all([encrypted_text, pin]):
        return jsonify({'success': False, 'error': 'Missing fields'})

    try:
        # urutan kebalikan dari enkripsi:
        step1 = decrypt_rail_fence(encrypted_text, 3)         # rail fence decrypt
        original = decrypt_stream_cipher(step1, str(pin))    # stream cipher decrypt menggunakan pin
        return jsonify({'success': True, 'decrypted_text': original})
    except Exception as e:
        print("Decrypt error:", e)
        return jsonify({'success': False, 'error': str(e)})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user_id, user in users.items():
            if user.username == username and bcrypt.check_password_hash(user.password_hash, password):
                login_user(user)
                flash('Login berhasil!', 'success')
                session['user'] = username
                return redirect(url_for('dashboard'))

        flash('Username atau password salah!', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash('Password tidak cocok!', 'danger')
            return redirect(url_for('register'))

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = str(len(users) + 1)
        users[user_id] = User(user_id, username, password_hash)

        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
