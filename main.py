from fastapi import FastAPI, Request
import pandas as pd

file_2 = 'data/osoby.json'
file_3 = 'data/uczelnie.json'


app = FastAPI()


@app.post('/')
async def tool2(request: Request) -> dict:
    persons_df = pd.read_json(file_2)
    university_df = pd.read_json(file_3)

    data = await request.json()
    input_text = data.get('input', "")
    if input_text.startswith("test"):
        return {'output': input_text}

    df = pd.merge(persons_df, university_df, left_on='uczelnia', right_on='id')

    answer = df[df['nazwa'].str.contains(input_text, case=False)]

    output=[]
    if not answer.empty:
        for _,row in answer.iterrows():
            output.append(f"Uczelnia {row['uczelnia']} zatrudnia : {row['imie']}, nazwisko: {row['nazwisko']}, wiek: {row['wiek']}, płeć: {row['plec']}")
    else: 
        output.append('Nie znaleziono danych o pracownikach')

    while len('\n'.join(output)) > 1024:
        output.pop()
    
    print(f"Input text: {input_text}")
    print(f"Output: {output}")
    return{'output' : '\n'.join(output)}







