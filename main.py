from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel, Field

import joblib
import pandas as pd
from typing import Optional

app = FastAPI(
    title="API desafio MLE",
    description="Esta é uma API para obtenção da melhor estratégia.",
    version="1.0.0"
)

# Carregar o modelo salvo
model = joblib.load('best_model.pkl')
#carregar as cartas no dataframe
df1 = pd.read_csv('challenge_train.csv')
df2 = pd.read_csv('challenge_test.csv')

df = pd.concat([df1, df2], ignore_index=True)
del df1 
del df2

# Definir 'id' como índice
df.set_index('id', inplace=True)

# Ajustar dicionários id2type e type2id / id2god e god2id / strategy2id e id2strategy
types = df['type'].unique().tolist()
id2type = {id: type for id, type in enumerate(types)}
type2id = {type: id for id, type in enumerate(types)}

gods = df['god'].unique().tolist()
id2god = {id: god for id, god in enumerate(gods)}
god2id = {god: id for id, god in enumerate(gods)}

strategies = df['strategy'].unique().tolist()
strategy2id = {strategy : id for id, strategy in enumerate(strategies)}
id2strategy = {id: strategy for id, strategy in enumerate(strategies)}


class Card(BaseModel):
    id: int = Field(..., description="Identificador único da carta no banco de dados do jogo")

class PredictData(BaseModel):
    id: int = Field(None, description = "ID da carta")
    mana: int = Field(None, description="Custo de mana para colocar a carta na mesa")
    attack: int = Field(None, description="Dano que a carta causa ao oponente")
    health: int = Field(None, description="Resistência ao dano ou durabilidade da carta")
    type: str = Field(None, description="Tipo ['spell','creature','weapon','god power']")
    god: str = Field(None, description="Deus ['death','neutral','deception','nature','light','war','magic']")
    strategy: Optional[str] = Field(None, description="Estágio do jogo ['early','late']")



@app.post("/predict", 
          response_model= PredictData, 
          summary= "Predizer a estratégia com base na carta", 
          description = "Prediz a estratégia com base no ID da carta informada.")
async def predict(input_data: Card = Body(..., example = {
    "id": "id da carta" 
})):
    """"
    Prediz qual a melhor estratégia se early ou late com base na carta informada.

    - **id**: id de uma carta existente no dataset train ou test
    """
    try:
        # Converter os dados de entrada em um DataFrame
        #input = pd.DataFrame([input_data.dict()])
        
        df2 = df.loc[[input_data.id]]
        
        #transformar os dados type e god em numéricos
        df2['type_'] = df2.type.apply(lambda x: type2id.get(x))
        df2['god_'] = df2.god.apply(lambda x: god2id.get(x))

        #df_predict com  somente as colunas que serão usadas
        df_predict = df2.drop(columns=['strategy', 'god', 'name', 'type'])
        
        # Fazer a previssão de estratégia
        predictions = model.predict(df_predict)
        
        # Adicionar as previsões ao DataFrame
        df_predict['strategy_'] = predictions

        df_predict['type'] = df_predict.type_.apply(lambda x: id2type.get(x))
        df_predict['god'] = df_predict.god_.apply(lambda x: id2god.get(x))
        df_predict['strategy'] = df_predict.strategy_.apply(lambda x: id2strategy.get(x))

        
        df_result = df_predict.drop(columns=['type_', 'god_', 'strategy_'])
        
        df_result['id'] = input_data.id
        
        
        # Retornar as previsões como JSON
        return df_result.to_dict(orient='records')[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

