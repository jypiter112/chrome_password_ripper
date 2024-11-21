import json, base64, sqlite3, win32crypt
import Cryptodome.Cipher.AES as AES

path = # PATH HERE
login_data_path = # RELATIVE PATH HERE

master_key = b''
def decrypt_password(cipher_text: bytes) -> str:
    global master_key
    init_vec = cipher_text[3:15]
    encrypted_password = cipher_text[15:-16]
    cipher = AES.new(master_key, AES.MODE_GCM, init_vec)
    decrypted_password = cipher.decrypt(encrypted_password)
    decrypted_password = decrypted_password.decode()
    return decrypted_password
with open(path, "r", encoding="utf-8") as f:
    t = f.read()
    j = json.loads(t)
    key = j["os_crypt"]["encrypted_key"]
    bdecoded = base64.b64decode(key)
    dpapi_removed = bdecoded[5:]
    master_key = win32crypt.CryptUnprotectData(dpapi_removed, None, None, None, 0)[1]
con = sqlite3.connect(login_data_path)
cur = con.cursor()
try:
    cur.execute("SELECT origin_url, username_value, password_value FROM logins")
except Exception as e:
    print("Couldnt oben sqlite3 db, error:", e)
    exit(1)
rows = cur.fetchall()
decrypted_rows = []
for row in rows:
    cipher_text = row[2]
    decrypted_pass = decrypt_password(cipher_text)
    decrypted_rows.append({
        "url":row[0],
        "username":row[1],
        "password":decrypted_pass
    })
con.close()

for row in decrypted_rows:
    print(row)
