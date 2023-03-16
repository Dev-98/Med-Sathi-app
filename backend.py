import easyocr,os
import pandas as pd
from thefuzz import fuzz
from string import digits, punctuation
from playsound import playsound



def image_reader(path):
    reader = easyocr.Reader(['en'])

    results = reader.readtext(path)
    p = '==============='
    text = ' ' 
    for result in results:
        text += result[1] + ' '

    print(p,'\n',text,'\n',p)

    remove_digits = str.maketrans('', '', punctuation)
    remove_digits2 = str.maketrans('', '', digits)

    res = text.translate(remove_digits)
    res = res.translate(remove_digits2)

    new_text = ""
    for txt in str(res).split():
        if (len(txt) > 4):
            new_text += txt + " "
   
    print(p,'\n',new_text,'\n',p)

    return new_text


def similarity_check(data,text):
    l=[]
    for i in data["Medicine"]:
        score = fuzz.partial_token_sort_ratio(i, text)
        l.append(score)
        index = sorted(list(enumerate(l)), reverse=True, key=lambda x: x[1])[0][0]
        if score >= 70:
            bimari = data["Disease"][index]
        elif score < 70 :
            bimari = 'Not available in database'
            
    return bimari

def voice_model(bimari):
    if bimari == 'Asthama':
        playsound('project Files/sounds/asthama.mp3')

    elif bimari == 'Headache':
        playsound('project Files/sounds/head.mp3')

    elif bimari == 'Kidney':
        playsound('project Files/sounds/kidney.mp3')

    elif bimari == 'Body Pain':
        playsound('project Files/sounds/body.mp3')

    elif bimari == 'Fever':
        playsound('project Files/sounds/fever.mp3')

    elif bimari == 'Allergy':
        
        playsound('project Files\\sounds\\allergy.mp3')
    elif bimari == 'Gas':
        
        playsound('project Files/sounds/gas.mp3')
    else:
        playsound('project Files/sounds/none.mp3')

def disease_finder(img_path):
    
    data = pd.read_csv("project files/medicine data.csv")
    
    text = image_reader(img_path)
    bimari = similarity_check(data,text)
    return bimari
    # voice_model(bimari)   

if __name__ == "__main__":

    # capture.image()
    path='project Files\\med images\\paracetamol.jpeg'

    bimari = disease_finder(path)
    print('\n',bimari)

