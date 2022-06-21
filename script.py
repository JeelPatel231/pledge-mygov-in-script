import requests # for making api requests
import base64 # for decoding base64-image
from hashlib import md5 # for tokenizing OTP

SLUG_NAME = 'constitution-day' # slug name -> edit accordingly about the certificate you want

headers={'Content-Type': 'application/json; charset=UTF-8'} # predefined headers

json_data={
    'type' : 'individual', # type, edit only if you know what you're doing
    "is_new":"true", 
    "prefix":"", # prefix
    "new-prefix":"", # empty works, no need to add
    "name":"", # your name // will be on certificate
    "gender":"", # gender -> male, female, other
    "dob":"", # dd-mm-yyyy formatted DOB
    "pincode":"", # pincode
    "state":"", # state
    "district":"", # district
    "email":"", # email
    "identity":"", # phone number
    "insert_to_mygov":"on",
    "salutation":"", # salutation
    "lang":"en"
}

# constants
GENERATE = "pledge"
DOWNLOAD = "certificate"

def check_registered(o):
    return o.get('email') == 'Email already registered' or o.get('identity') == 'Mobile already exists'

def tokenize_otp() -> str:
    otp = input("insert otp : ")
    token = md5((md5(json_data['identity'].encode()).hexdigest()+':'+md5(otp.encode()).hexdigest()).encode()).hexdigest()
    print(token)
    return token

# route = GENERATE = pledge to make certificate in the account
# route = DOWNLOADS = certificate to download certificate in the pc
def gen_certificate(route):
    o = requests.post(f'https://pledgeapi.mygov.in/api/v2/{SLUG_NAME}/{route}',headers=headers,json=json_data).json()
    print(o)
    if (check_registered(o)) : return
    auth_head = headers | {'Authorization': tokenize_otp() }
    k = requests.post(f'https://pledgeapi.mygov.in/api/v2/{SLUG_NAME}/{route}',headers=auth_head,json=json_data).json()
    print(k)

    if route == DOWNLOAD:
        with open(f"certificate-{SLUG_NAME}.png", "wb") as fh:
            fh.write(base64.decodebytes(k['data'].replace('data:image/jpeg;base64,','').encode('utf-8')))

if __name__ == "__main__":
    print("starting generate")
    gen_certificate(GENERATE)
    print("starting download")
    gen_certificate(DOWNLOAD)
