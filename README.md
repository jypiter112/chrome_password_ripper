<b>DISCLAIMER!</b>
<p>
Please DO NOT use this in any unethical way.
This python script is intended solely for educational purposes and as a proof of concept.
I do not take any responsibility for its use in any illegal activities or for any harm caused by misuse.
By using this tool, you acknowledge and agree that it is your responsibility to comply with all applicable laws and regulations.

Dependencies: python3
Modules/libs: json, base64, sqlite3, win32crypt, os, Cryptodome.Cipher

Tested on: Windows 11, Chrome installed

Program flow: Created as per user "yufmial google" answered in superuser article (credits below)
1. Find chrome path using Windows system environment variables
2. Locate Local State and Login Data files
3. Read encrypted_key json string from Local State file
4. Decode using base64 and remove "DPAPI" signature
5. Use CryptUnprotectData with Win32 API to reveal master_key
6. Open Login Data file with sqlite3 and query "SELECT origin_url, username_value, password_value FROM logins"
7. Decrypt password with master_key and save output
8. Save plaintext Pc name, Username, Url, Username and Password as plaintext to current working directory

Credits: https://superuser.com/questions/655573/decrypt-google-chrome-passwords
</p>
