from flask import Flask, json, jsonify, render_template, request, redirect, url_for, session, flash, send_file
# from flask_bcrypt import Bcrypt
import hashlib
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
from crypto.steganography import railfence_encrypt, lsb_hide, lsb_extract, railfence_decrypt
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename
from db import get_db, create_tables
from config import DES_KEY
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import hashlib, base64

# ------------------------------------------------------------
# Inisialisasi Flask & Library
# ------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "kriptografisia"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # route untuk redirect jika belum login

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    data = cur.fetchone()
    conn.close()
    if data:
        return User(data['id'], data['username'])
    return None

# debug helpers — letakkan setelah app = Flask(__name__)
import functools
def debug_print(label):
    def wrapper(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            try:
                print(f"--- DEBUG {label} --- session keys: {dict(session)}")
            except Exception:
                print(f"--- DEBUG {label} --- session unavailable")
            return fn(*args, **kwargs)
        return wrapped
    return wrapper

# quick debug route to inspect session from browser
@app.route('/_debug_session')
def _debug_session():
    return jsonify(dict(session))

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
def index():
    if not current_user.is_authenticated:
        flash('Silakan login dulu ⚠️', 'warning')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session.get('username'))

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    data = cur.fetchone()
    conn.close()
    if data:
        return User(data['id'], data['username'])
    return None

# --------------------------
# Route login yang diperbarui
# --------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username'].strip()
        p = request.form['password']

        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s", (u,))
        user = cur.fetchone()
        conn.close()

        if user:
            hashed_input = hashlib.blake2b(p.encode(), digest_size=32).hexdigest()
            if hashed_input == user['passhash']:
                user_obj = User(user['id'], user['username'])

                login_user(user_obj)
                session['user_id'] = user['id']
                session['username'] = user['username']


                flash(f'Login berhasil! Selamat datang, {u}', 'success')
                return redirect(url_for('index'))
            else:
                flash('Password salah ❌', 'danger')
        else:
            flash('Username tidak ditemukan ⚠️', 'warning')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm = request.form['confirm']

        # Validasi input kosong
        if not username or not password or not confirm:
            flash('Semua field wajib diisi ⚠️', 'warning')
            return render_template('register.html')

        # Cek konfirmasi password
        if password != confirm:
            flash('Konfirmasi password tidak cocok ❌', 'danger')
            return render_template('register.html')

        # Hash password dengan BLAKE2b
        hashed_pass = hashlib.blake2b(password.encode(), digest_size=32).hexdigest()

        conn = get_db()
        cur = conn.cursor()

        # Cek apakah username sudah ada
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing = cur.fetchone()
        if existing:
            conn.close()
            flash('Username sudah terdaftar, silakan gunakan yang lain ⚠️', 'warning')
            return render_template('register.html')

        # Simpan akun baru
        cur.execute('INSERT INTO users (username, passhash) VALUES (%s, %s)', (username, hashed_pass))
        conn.commit()
        conn.close()

        flash('Akun berhasil dibuat 🎉 Silakan login sekarang.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))

@app.route('/encrypt_file', methods=['GET', 'POST'])
@login_required
def encrypt_file_page():
    uploads_folder = "static/uploads"
    os.makedirs(uploads_folder, exist_ok=True)

    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('File tidak valid.', 'danger')
            return redirect(request.url)

        input_path = os.path.join(uploads_folder, file.filename)
        file.save(input_path)

        output_filename = f"encrypted_{file.filename}"
        output_path = os.path.join(uploads_folder, output_filename)

        # Jalankan fungsi enkripsi (contoh: RC4)
        encrypt_file(input_path, output_path)

        return send_file(output_path, as_attachment=True, download_name=output_filename)

    return render_template('encrypt_file.html')

@app.route('/encrypt_text')
@login_required

def encrypt_text():
    print("=== DEBUG /encrypt_text ===")
    print("Authenticated:", current_user.is_authenticated)
    print("Session:", session)

    if not current_user.is_authenticated:
        # user belum login
        return render_template('encrypt_text.html', require_login=True, diaries=[])

    diaries = []
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT id, title, content_encrypted
            FROM notes
            WHERE user_id=%s
            ORDER BY id DESC
        """, (session['user_id'],))
        rows = cur.fetchall()
        conn.close()
        diaries = [
            {'id': r['id'], 'title': r['title'], 'content': r['content_encrypted']}
            for r in rows
        ]
    except Exception as e:
        print("Fetch diaries error:", e)
        diaries = []

    return render_template('encrypt_text.html', require_login=False, diaries=diaries)


@app.route('/save_diary', methods=['POST'])
@login_required
def save_diary():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'error': 'Unauthorized'})

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    pin = data.get('pin')

    if not all([title, content, pin]):
        return jsonify({'success': False, 'error': 'Missing fields'})

    try:
        # 🔐 Enkripsi dua tahap
        encrypted_text = encrypt_stream_cipher(content, pin)
        encrypted_text = encrypt_rail_fence(encrypted_text, 3)

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO notes (user_id, title, content_encrypted)
            VALUES (%s, %s, %s)
        """, (session['user_id'], title, encrypted_text))
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        print("DB Save Error:", e)
        return jsonify({'success': False, 'error': str(e)})

@app.route('/decrypt_diary', methods=['POST'])
def decrypt_diary():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'error': 'Unauthorized'})

    data = request.get_json()
    encrypted_text = data.get('content')
    pin = data.get('pin')

    if not encrypted_text or not pin or len(str(pin)) != 6:
        return jsonify({'success': False, 'error': 'Missing fields or invalid PIN'})

    try:
        # urutan kebalikan dari enkripsi:
        step1 = decrypt_rail_fence(encrypted_text, 3)         # rail fence decrypt
        original = decrypt_stream_cipher(step1, str(pin))    # stream cipher decrypt menggunakan pin
        return jsonify({'success': True, 'decrypted_text': original})
    except Exception as e:
        print("Decrypt error:", e)
        return jsonify({'success': False, 'error': str(e)})
    


UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --------------------------------
# DES utils
# --------------------------------
def pad8(b): return b + bytes([8 - len(b) % 8]) * (8 - len(b) % 8)
def unpad8(b): return b[:-b[-1]]

def des_encrypt(text):
    iv = get_random_bytes(8)
    cipher = DES.new(DES_KEY, DES.MODE_CBC, iv)
    enc = cipher.encrypt(pad8(text.encode()))
    return base64.b64encode(iv + enc).decode()

def des_decrypt(b64):
    raw = base64.b64decode(b64)
    iv, ct = raw[:8], raw[8:]
    cipher = DES.new(DES_KEY, DES.MODE_CBC, iv)
    return unpad8(cipher.decrypt(ct)).decode()

# --------------------------------
# ROUTE: Steganografi (Rail Fence + LSB)
# --------------------------------
@app.route('/steganography', methods=['GET', 'POST'])
@login_required
def steganography_page():
    result_image = None
    decrypted = None
    filename = None

    if not current_user.is_authenticated:
        return redirect('/login')

    if request.method == "POST":
        # Deteksi apakah form berisi 'message' (enkripsi) atau hanya 'image' (dekripsi)
        if "message" in request.form:
            # ---------- PROSES ENKRIPSI ----------
            message = request.form["message"]
            image = request.files["image"]

            if image and message:
                image_path = os.path.join(UPLOAD_FOLDER, image.filename)
                image.save(image_path)

                # Enkripsi teks dengan Rail Fence
                encrypted_text = railfence_encrypt(message, 3)

                # Sisipkan pesan terenkripsi ke gambar menggunakan LSB
                output_path = os.path.join(UPLOAD_FOLDER, "stego_" + image.filename)
                lsb_hide(image_path, encrypted_text, output_path)

                result_image = "uploads/" + "stego_" + image.filename

        elif "image" in request.files:
            # ---------- PROSES DEKRIPSI ----------
            image = request.files['image']
            filename = secure_filename(image.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(path)

            # Ekstrak pesan dari gambar
            secret = lsb_extract(path)

            # Dekripsi teks dengan Rail Fence Cipher
            decrypted = railfence_decrypt(secret, 3)

    return render_template("steganography.html",
                           result_image=result_image,
                           decrypted=decrypted,
                           filename=filename)
# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
