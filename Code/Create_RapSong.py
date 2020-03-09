from gtts import gTTS 
import tensorflow as tf
import gpt_2_simple as gpt2
import random
import tarfile
import requests
import os

filepath="checkpoint_RapgodTrained3.tar"
googefileid= "1-0LAvjKMX2xG7_pbY3C2lH15891ko5oh"


def extract():
    """Copies the checkpoint folder from a mounted Google Drive."""
    with tarfile.open(filepath, 'r') as tar:
        tar.extractall()
    os.remove(filepath)
    print("File",filepath, "Removed!")



def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)


# download_file_from_google_drive(googefileid,filepath)
# extract()
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='RapgodTrained3')

def createsong():
    temp= random.randint(7,9)/10
    print(temp)
    text= gpt2.generate(sess,
            run_name='RapgodTrained3',
            length= 200,
            temperature=temp,
            prefix=' ',
            nsamples=5,
            batch_size=5,
            return_as_list=True
            )
            
    text= text[0]
    return text

def RapText():
    text = createsong()
    Rap = open(r"RapSong.txt","w+") 
    Rap.write(text)
    print(text)

def MP3():
    fileHandler = open("RapSong.txt", "r")
    myText =fileHandler.read().replace("\n", " ")
    language = 'en'
    output = gTTS(text=myText, lang=language, slow=False)
    output.save("RapSong.mp3")
    fileHandler.close()
    os.system("start RapSong.mp3")

RapText()
MP3()