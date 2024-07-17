import requests, json, os
import pandas as pd
from dotenv import load_dotenv
import openai
import tiktoken
import re
from datetime import datetime

load_dotenv()

openai.api_key = os.environ['OPENAI_KEY']

modelli = ['picanto', 'stonic', 'ceed', 'Xceed', 'niro', 'sportage', 'EV6', 'sorento', 'EV9']

def get_profiles(platform):
    if platform == 'instagram':
        response = requests.get(url = f"https://api.emplifi.io/3/{platform}/profiles", 
                                auth = (os.environ['ACCESS_TOKEN'], os.environ["SECRET_KEY"]))
        ig_profiles = json.loads(response.text)
        df_profiles_ig = pd.DataFrame.from_dict(ig_profiles['profiles'])

        return df_profiles_ig[df_profiles_ig['name'] == 'Kia Italia']['id']
    elif platform == 'facebook':
        response = requests.get(url = f"https://api.emplifi.io/3/{platform}/profiles", 
                                auth = (os.environ['ACCESS_TOKEN'], os.environ["SECRET_KEY"]))
        fb_profiles = json.loads(response.text)
        df_profiles_fb = pd.DataFrame.from_dict(fb_profiles['profiles'])

        return df_profiles_fb[df_profiles_fb['name'] == 'Kia Italia']['id']

def get_data(platform, date_start, date_end):
    if platform == 'instagram':
        params = {
            "profiles" : [{"id" : "17841400626477518", "platform" : "instagram"}],
            "date_start" : date_start,
            "date_end" : date_end,
            "fields" : ["author", "community_type", "content_type", "created_time", "id", "message", "messages", "origin", "parent_post", "profileId", "response_first", "post_labels", "url"],
            "limit" : 100,
            "sort" : [{"field" : "created_time", "order" : "asc"}]
        }
        response = requests.post(url = "https://api.emplifi.io/3/community/posts", 
                                auth = (os.environ['ACCESS_TOKEN'], os.environ["SECRET_KEY"]), json = params)
        
        final = json.loads(response.text)
        community = pd.DataFrame.from_dict(final['data']['posts'])
        
        return community
    else:
        params = {
            "profiles" : [{"id" : "304377699433", "platform" : "facebook"}],
            "date_start" : date_start,
            "date_end" : date_end,
            "fields" : ["author", "community_type", "content_type", "created_time", "id", "message", "messages", "origin", "parent_post", "profileId", "response_first", "post_labels", "url"],
            "limit" : 100,
            "sort" : [{"field" : "created_time", "order" : "asc"}]
        }
        response = requests.post(url = "https://api.emplifi.io/3/community/posts", 
                                auth = (os.environ['ACCESS_TOKEN'], os.environ["SECRET_KEY"]), json = params)
        
        final = json.loads(response.text)
        community = pd.DataFrame.from_dict(final['data']['posts'])
        
        return community

def create_conversations(df, platform, start_date, end_date):
    conversazioni = pd.DataFrame(columns=['nome', 'data', 'ora', 'provenienza', 'label', 'messaggio', 'origine', 'url'])
    messaggi = []
    data = []
    ora = []
    autore = []
    canale = []
    url = []
    label = []
    provenienza = []

    for i, el in df.iterrows():
        if len(el['messages']) > 0:
            for subel in el['messages']:
                if "message" in subel:
                    if subel['message'] == "This message is no longer available because the story it’s connected to has expired.":
                        messaggi.append('Storia scaduta')
                        data.append(subel['created_time'].split('T')[0])
                        ora.append(subel['created_time'].split('T')[1].split('+')[0])
                        autore.append(el['author']['name'])
                        url.append(el['url'])
                        label.append(el['post_labels'])
                        canale.append(f'ig {el["community_type"]}' if platform == 'instagram' else f'fb {el["community_type"]}')
                        if subel['origin'] == "Brand's Content":
                            provenienza.append('Kia')
                        else:
                            provenienza.append('utente')
                    elif subel['message'] == "Currently, we're not able to display the content of this message. Please check it on Instagram.":
                        messaggi.append('Impossibile visualizzare contenuto')
                        data.append(subel['created_time'].split('T')[0])
                        ora.append(subel['created_time'].split('T')[1].split('+')[0])
                        autore.append(el['author']['name'])
                        url.append(el['url'])
                        label.append(el['post_labels'])
                        canale.append(f'ig {el["community_type"]}' if platform == 'instagram' else f'fb {el["community_type"]}')
                        if subel['origin'] == "Brand's Content":
                            provenienza.append('Kia')
                        else:
                            provenienza.append('utente')
                    elif subel['message'] == "This message was deleted by the user.":
                        messaggi.append("Messaggio eliminato dall'utente")
                        data.append(subel['created_time'].split('T')[0])
                        ora.append(subel['created_time'].split('T')[1].split('+')[0])
                        autore.append(el['author']['name'])
                        url.append(el['url'])
                        label.append(el['post_labels'])
                        canale.append(f'ig {el["community_type"]}' if platform == 'instagram' else f'fb {el["community_type"]}')
                        if subel['origin'] == "Brand's Content":
                            provenienza.append('Kia')
                        else:
                            provenienza.append('utente')
                    else:
                        messaggi.append(subel['message'])
                        data.append(subel['created_time'].split('T')[0])
                        ora.append(subel['created_time'].split('T')[1].split('+')[0])
                        autore.append(el['author']['name'])
                        url.append(el['url'])
                        label.append(el['post_labels'])
                        canale.append(f'ig {el["community_type"]}' if platform == 'instagram' else f'fb {el["community_type"]}')
                        if subel['origin'] == "Brand's Content":
                            provenienza.append('Kia')
                        else:
                            provenienza.append('utente')
                else:
                    if el['community_type'] == 'fb mention_story_mention':
                        messaggi.append('Menzione alla storia')
                        data.append(subel['created_time'].split('T')[0])
                        ora.append(subel['created_time'].split('T')[1].split('+')[0])
                        autore.append(el['author']['name'])
                        url.append(el['url'])
                        label.append(el['post_labels'])
                        canale.append(f'ig {el["community_type"]}' if platform == 'instagram' else f'fb {el["community_type"]}')
                        if subel['origin'] == "Brand's Content":
                            provenienza.append('Kia')
                        else:
                            provenienza.append('utente')
                    else:
                        messaggi.append('messaggio non disponibile')
                        data.append(subel['created_time'].split('T')[0])
                        ora.append(subel['created_time'].split('T')[1].split('+')[0])
                        autore.append(el['author']['name'])
                        url.append(el['url'])
                        label.append(el['post_labels'])
                        canale.append(f'ig {el["community_type"]}' if platform == 'instagram' else f'fb {el["community_type"]}')
                        if subel['origin'] == "Brand's Content":
                            provenienza.append('Kia')
                        else:
                            provenienza.append('utente')
        if el['message'] != 'VUOTO':
            messaggi.append(el['message'])
            data.append(el['created_time'].split('T')[0])
            ora.append(el['created_time'].split('T')[1].split('+')[0])
            autore.append(el['author']['name'])
            url.append(el['url'])
            label.append(el['post_labels'])
            canale.append(f'ig {el["community_type"]}' if platform == 'instagram' else f'fb {el["community_type"]}')
            provenienza.append('utente')
            
    conversazioni['nome'] = autore
    conversazioni['data'] = data
    conversazioni['ora'] = ora
    conversazioni['messaggio'] = messaggi
    conversazioni['origine'] = canale
    conversazioni['url'] = url
    conversazioni['provenienza'] = provenienza
    conversazioni['label'] = label

    conversazioni = conversazioni[(conversazioni['data'] >= start_date.split('T')[0]) & (conversazioni['data'] <= end_date.split('T')[0])]

    return conversazioni

def create_final_df(conversazioni):
    df_final = pd.DataFrame(columns=['DATA', 'ORA', 'BEFORE DEADLINE', 'NOME UTENTE', 'CANALE', 'MODELLO', 'TARGA', 'TELAIO', 
                                        'CONCESSIONARIA', 'COMMENTO UTENTE', 'SENTIMENT', 'URL POST PADRE', 'PROPOSTA RISP JAKALA'])
    
    df_final['DATA'] = [el for el in conversazioni['data']]
    df_final['ORA'] = [el for el in conversazioni['ora']]
    df_final['BEFORE DEADLINE'] = ['No' for _ in range(len(conversazioni))]
    df_final['NOME UTENTE'] = [el for el in conversazioni['nome']]
    df_final['PROVENIENZA'] = [el for el in conversazioni['provenienza']]
    df_final['CANALE'] = [el for el in conversazioni['origine']]
    df_final['MODELLO'] = [' ' for _ in range(len(conversazioni))]
    df_final['TARGA'] = [' ' for _ in range(len(conversazioni))]
    df_final['TELAIO'] = [' ' for _ in range(len(conversazioni))]
    df_final['CONCESSIONARIA'] = [' ' for _ in range(len(conversazioni))]
    df_final['COMMENTO UTENTE'] = [el for el in conversazioni['messaggio']]
    df_final['SENTIMENT'] = [' ' for _ in range(len(conversazioni))]
    df_final['LABEL'] = [el for el in conversazioni['label']]
    df_final['URL POST PADRE'] = [el for el in conversazioni['url']]
    df_final['PROPOSTA RISP JAKALA'] = [' ' for _ in range(len(conversazioni))]

    df_final = df_final[df_final['NOME UTENTE'] != 'Kia Italia']

    return df_final

def before_deadline(df_final, platform):
    if platform == 'instagram':
        chat_utenti = df_final[df_final['CANALE'] != 'ig mention_post_and_media_tag']
    elif platform == 'facebook':
        chat_utenti = df_final[df_final['CANALE'] != 'fb mention_post_and_media_tag']

    lista_utenti = chat_utenti['NOME UTENTE'].value_counts().index

    community = pd.DataFrame(columns=df_final.columns)

    for el in lista_utenti:
        subdf = chat_utenti[chat_utenti['NOME UTENTE'] == el]
        subdf = subdf.sort_values(by=['DATA', 'ORA'])
        community = pd.concat([community, subdf], axis=0)
    community.reset_index(drop=True, inplace=True)

    temp = pd.DataFrame(columns=community.columns)
    for el in lista_utenti:
        subdf = community[community['NOME UTENTE'] == el]
        subdf['DATETIME'] = subdf['DATA'] + ' ' + subdf['ORA']
        subdf.reset_index(drop=True, inplace=True)
        if len(subdf) == 1:
            community[community['NOME UTENTE'] == el]['BEFORE DEADLINE'] = 'No'
            temp = pd.concat([temp, subdf], axis=0)
        else:
            for i, el in subdf.iterrows():
                if el['PROVENIENZA'] == 'utente':
                    for j, el2 in subdf.iloc[i+1:,:].iterrows():
                        if el2['PROVENIENZA'] == 'Kia':
                            differenza_ore = (datetime.strptime(el2['DATETIME'], "%Y-%m-%d %H:%M:%S") - datetime.strptime(el['DATETIME'], "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600
                            if differenza_ore <= 2:
                                subdf.at[i, 'BEFORE DEADLINE'] = 'Si'
            temp = pd.concat([temp, subdf], axis=0)
            
    temp.reset_index(drop=True, inplace=True)

    final_community = temp.copy()
    final_community.drop(columns=['DATETIME'], inplace=True)
    final_community = final_community[(final_community['PROVENIENZA'] == 'utente')]
    final_community.reset_index(drop=True, inplace=True)

    return final_community

def count_token(text):
    enc = tiktoken.get_encoding("cl100k_base")
    enc = tiktoken.encoding_for_model("gpt-4-0125-preview")
    tokens = enc.encode(text)
    return len(tokens)

def divide_batch(df, first_batch_max_tokens, other_batches_max_tokens):
    batches = []
    current_batch = []
    current_batch_total = 0
    first_batch = True
    row_number = 0  # contatore per il numero di riga0

    for index, row in df.iterrows():
        text_tokens = row['Token Count']

        if first_batch:
            max_tokens = first_batch_max_tokens
        else:
            max_tokens = other_batches_max_tokens

        if (current_batch_total + text_tokens) > max_tokens:
            if first_batch:
                start_number = row_number  # salva il numero di righe del primo batch
            batches.append(pd.DataFrame(current_batch))
            current_batch = []
            current_batch_total = 0
            first_batch = False
            row_number = 0  # resetta il contatore del numero di riga

        row_dict = row.to_dict()
        row_dict['input ai'] = re.sub(r"""
            [,.;@#?!&$]+  # Accept one or more copies of punctuation
            \ *           # plus zero or more copies of a space,
            """,
            " ",          # and replace it with a single space
            row_dict['input ai'], flags=re.VERBOSE)
        current_batch.append(row_dict)
        current_batch_total += text_tokens
        row_number += 1

    # Aggiungi l'ultimo batch se non è vuoto
    if current_batch:
        batches.append(pd.DataFrame(current_batch))

    return batches

def generate_responses(df_in):
    prompt0 = """Sei l'assistente di un Social Media Manager che gestisce le pagine social di Kia, una grande casa automobilistica. Il tuo compito è quello di leggere i commenti che vengono lasciati 
        sui canali social dagli utenti e cercare di estrapolare alcune informazioni.
        \n Le informazioni che devi estrapolare sono:
        \n 1. Modello dell'auto. Cerca di trovare una tra queste parole """ + ', '.join(modelli) + """ 
        \n 2. Targa dell'auto. Ricordati che le targe hanno il formato "AA000AA"
        \n 3. Numero di telaio dell'auto. Il numero di telaio è composto da 17 caratteri alfanumerici.
        \n 4. Concessionario dove l'auto è stata comprata.
        \n 5. Sentiment del messaggio: classifica il sentiment utilizzando le parole "Positivo", "Neutro", "Negativo".

        \n I dati che ti verranno forniti presenteranno il nome utente di chi ha commentato e il commento stesso.
        \n Il tuo compito è quindi di leggere i commenti e identificare, se presenti, queste informazioni. Il risultato dovrà essere un file json like strutturato in questo modo:
        \n {
                "risposte": [
                        \n{
                                \n"nome utente": inserisci il nome utente che leggi in input
                                \n"modello": inserisci il nome del modello;
                                \n"targa": inserisci il numero di targa;
                                \n"telaio": inserisci il numero di telaio;
                                \n"concessionario": inserisci il nome del concessionario;
                                \n"sentiment": inserisci il sentiment;
                        \n}
                \n]
        \n} 
        
        \n####Istruzioni dettagliate####:
        \n 1. La targa è una parola alfanumerica strutturata così: AA000AA.
        \n 2. Il numero di telaio è composto da 17 caratteri alfanumerici.
        \n 3. Il nome utente lo trovi prima della parola "ha commentato".
        \n 4. Il concessionario è solitamente vicino al nome di una città.
        \n 5. Analizza il sentiment del messaggio con "Positivo", "Neutro", "Negativo". Se trovi un commento simile a "messaggio non disponibile" oppure "storia scaduta" imposta automaticamente il sentiment a "Neutro"
        \n 6. Ricordati che è possibile che queste informazioni non siano presenti all'interno di alcuni commenti, in questo caso sostituisci targa, modello, telaio e concessionario con la parola "NO"
        \n 7. Analizza tutti i commenti senza tralasciarne nemmeno uno.
        """
    
    message_array = []
    system = {"role": "system", "content": prompt0}
    message_array.append(system)
    df_final = pd.DataFrame(columns=['Utente', 'Modello', 'Targa', 'Numero Telaio', 'Concessionario', 'Sentiment'])

    for i, el in df_in.iterrows():
        if i % 10 == 0:
            print(f'Commento numero {i}')
        system = {"role": "system", "content": prompt0}
        message_array.append(system)
        prompt_user = f"Classifica il seguente commento: {el['input ai']}"
        
        message_user = {"role": "user", "content": prompt_user}
        message_array.append(message_user)

        success = False
        while not success:
            response_message = openai.chat.completions.create(model='gpt-4o', messages=message_array, response_format={'type': 'json_object'}, 
                                                            temperature=0, frequency_penalty=0, presence_penalty=0, top_p=0.3)
            success = True
        
        result_json = json.loads(response_message.choices[0].message.content)
        with open('out/output.json', 'w') as f:
            json.dump(result_json, f)

        with open('out/output.json', 'r') as file:
            data = json.load(file)

        df = pd.DataFrame(columns=df_final.columns)
        nome_utente = []
        modello = []
        targa = []
        telaio = []
        conce = []
        sentiment = []

        for i in range(len(data['risposte'])):
            nome_utente.append(data['risposte'][i]['nome utente'].strip())
            modello.append(data['risposte'][i]['modello'].strip())
            targa.append(data['risposte'][i]['targa'].strip())
            telaio.append(data['risposte'][i]['telaio'].strip())
            conce.append(data['risposte'][i]['concessionario'].strip())
            sentiment.append(data['risposte'][i]['sentiment'].strip())

        df['Utente'] = nome_utente
        df['Modello'] = modello
        df['Targa'] = targa
        df['Numero Telaio'] = telaio
        df['Concessionario'] = conce
        df['Sentiment'] = sentiment

        df_final = pd.concat([df_final, df])
            
        message_array.pop(1)
        
    df_final.reset_index(drop=True, inplace=True)

    df_in['MODELLO'] = df_final['Modello']
    df_in['TARGA'] = df_final['Targa']
    df_in['TELAIO'] = df_final['Numero Telaio']
    df_in['CONCESSIONARIA'] = df_final['Concessionario']
    df_in['SENTIMENT'] = df_final['Sentiment']

    return df_in