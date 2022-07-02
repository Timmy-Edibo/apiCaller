
from fastapi import FastAPI, Form, Body, UploadFile, File
from pydantic import BaseModel
import requests
import wikipedia
from fastapi.responses import JSONResponse

app_id = '23a97c5b'
app_key = '6e93bcd93c88da0bb38d0a165d5ba6a3'


app = FastAPI()


@app.get("/api")
def read_root():
    return {"Hello": "World"}

@app.post("/api/dictionary/{meaninfy}")
def dictionary(meaningfy:str):

    url = f'https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/{meaningfy.lower()}'
    response = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
    r = response.json()


    extract_etymology = r['results'][0]['lexicalEntries'][0]['entries'][0]['etymologies'][0]
    extract_pronouciation = r['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']
    extract_definition = r['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
    extract_example = r['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'][0]['text']
    extract_synonym = r['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms']
    
    sn = []
    for each in extract_synonym:
        synonym = each['text']
        sn.append(synonym)

    description = {'entymology': extract_etymology,
                'pronouciation': extract_pronouciation,
                'definition': extract_definition,
                'examples': extract_example,
                'synonym': sn
    }

    return {'description': description}
    

@app.post("/api/phone/{number}")
def ValidatePhoneNumber(number):
    
    url = "https://phonenumbervalidatefree.p.rapidapi.com/ts_PhoneNumberValidateTest.jsp"
    querystring = {"number":number, "country":"UY"}
    headers = {
        "X-RapidAPI-Key": "0d38549a84msh403c99cd08ef92fp14be12jsn56de97a8b528",
        "X-RapidAPI-Host": "phonenumbervalidatefree.p.rapidapi.com"
    }

    response = requests.get( url, headers=headers, params=querystring)
    r = response.json()
    return {'response': r}


@app.post("/api/wiki/{wiki}")
def wiki(wiki:str):
   search = wikipedia.page(wiki)
   
   context = {
       'title': search.title,
       'link': search.url,
       'details': search.summary,
   }
   return {'data': context}

class WhatsappPost(BaseModel):
    message:str
    phone_number: str

@app.post("/api/whatsapp/")
def wiki2(post:WhatsappPost):

    url = "https://getitsms-whatsapp-apis.p.rapidapi.com/45"

    querystring = {"your_number": post.phone_number,"your_message": post.message}

    payload = {
        "key1": "value",
        "key2": "value"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "0d38549a84msh403c99cd08ef92fp14be12jsn56de97a8b528",
        "X-RapidAPI-Host": "getitsms-whatsapp-apis.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    # print(response.text)
    return {'data': "message sent successsfully to {post.phone_number}"}


class LangTranslate(BaseModel):
    content: str


# (trans: LangTranslate, 
@app.post('/api/language')
def language_translator(trans: LangTranslate = Body(embed=True)):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = f"source=en&target=ha&q={trans.content}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "0d38549a84msh403c99cd08ef92fp14be12jsn56de97a8b528",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)
    res_convert = response.json()
    x = res_convert['data']['translations'][0]
    return {'data': x}



@app.post("/login/")
async def login(username: str = Form(), password: str = Form(), file: UploadFile = File()):
    return {"username": username}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}    


# @app.get("/uploadfile/")
# async def get_upload_file():
#     return {"filename": file}    
