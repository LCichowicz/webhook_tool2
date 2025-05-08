from fastapi import FastAPI, Request
import pandas as pd

file_2 = '/data/osoby.json'
file_3 = '/data/uczelnie.json'


app = FastAPI()


@app.post('/tool2')
async def tool2(request: Request) -> dict:
    persons_df = pd.read_json(file_2)
    university_df = pd.read_json(file_3)

    data = await request.json()
    input_text = data['input']
    if input_text.startswith("test"):
        return {'output': input_text}

    df = pd.merge(persons_df, university_df, on='uczelnia')

    answer = df[df['nazwa'].str.contains(input_text, case=False)]

    output=[]
    if not answer.empty:
        for _,row in answer.iterrows():
            output.append(f"Uczelnia {row['uczelnia']} zatrudnia : {row['imie']}, nazwisko: {row['nazwisko']}, wiek: {row['wiek']}, płeć: {row['plec']}")
    else: 
        output.append('Nie znaleziono danych o pracownikach')

    while len('\n'.join(output)) > 1024:
        output.pop()

    return{'output' : '\n'.join(output)}







