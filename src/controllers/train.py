import pandas as pd 
from sklearn_pandas import DataFrameMapper
import sys


class Train:
    def __init__(self, aCSVTrain, aCSVTest, aCSVResult):
        self.arqCSVTrain = aCSVTrain        
        self.arqCSVTest = aCSVTest
        self.arqCSVResult = aCSVResult

        self.df = pd.read_csv(aCSVTrain)
        self.df_final = pd.read_csv(aCSVTrain)

    def getDeckComplete(self):
        return self.df_final.to_json(orient='records')


    def arqResultExiste(self):
        try: 
            os.path.isfile(self.arqCSVResult)
            self.df_final = pd.read_csv(self.arqCSVResult)
            return True
        except:
            return False

    def findCardById(self, id):        
        return self.df_final[self.df_final.id==id].to_json(orient='records')

    def fit(self):
        #criando uma variavel auxiliar pra manipular o Dataframe Original (challenge_train)
        inputs = self.df

        # importando a biblioteca LabelEncoder, para transformar labels em números inteiros. 
        from sklearn.preprocessing import LabelEncoder

        #Criando as variaveis de manipulação dos labels
        le_type = LabelEncoder()
        le_god = LabelEncoder()
        le_strategy = LabelEncoder()

        inputs['type_n'] = le_type.fit_transform(inputs['type'])
        inputs['god_n'] = le_god.fit_transform(inputs['god'])
        inputs['strategy_n'] = le_strategy.fit_transform(inputs['strategy'])

        #Retirando a coluna alvo
        inputs = self.df.drop('strategy', axis = 'columns')
        #Criando um novo Dataframe somente com a coluna alvo, a que queremos "aprender"
        target = self.df['strategy_n']
        #Retirando do Dataframe de entradas a coluna alvo
        inputs = inputs.drop('strategy_n', axis = 'columns')

        #Retirando do Dataframe as colunas que são do tipo labels e que não agregam na árvore de decisão que usaremos a seguir
        inputs_n = inputs.drop(['id','name','type','god'], axis='columns')

        #importando a biblioteca de árvore
        from sklearn import tree

        #Criando uma variável modelo de árvore de decisão
        model = tree.DecisionTreeClassifier()

        #Ensinando o modelo a partir dos resultados
        model.fit(inputs_n.values, target)

        #model.score(inputs_n,target) # como os dados de entrada são os mesmos do de validação, o score é 1

        #Cria um DF com os dados de test
        df_test = pd.read_csv(self.arqCSVTest)
        
        #Cria colunas inteiras a partir das colunas labels
        df_test['type_n'] = le_type.fit_transform(df_test['type'])
        df_test['god_n'] = le_god.fit_transform(df_test['god'])

        #Cria o DF result com a coluna strategy preenchida a partir dos dados aprendidos no modelo
        df_result = df_test
        df_result['strategy'] = df_test['name']
        alist = []
        for indice, linha in df_result.iterrows():    
            card = [linha.mana, linha.attack, linha.health, le_type.transform([linha.type])[0], le_god.transform([linha.god])[0]]
            prev = le_strategy.inverse_transform(model.predict([card]))[0]
            alist.append(prev)
        df_result['strategy'] = alist

        #Cria um novo DF result sem as colunas auxiliares criadas dos labels type e god
        df_result_f = df_result.drop(['type_n','god_n'], axis = 'columns')

        #Cria um novo DF dos dados de train sem as colunas auxiliares criadas dos labels type e god
        df_f = self.df.drop(['type_n','god_n', 'strategy_n'], axis = 'columns')

        #Cria um novo DF com os dados dos dois DF, os dos dados de train e dos dados de test
        self.df_final = pd.concat([df_f, df_result_f])

        #Exporta o DF criado para um arquivo CSV        
        self.df_final.to_csv(self.arqCSVResult, encoding = 'utf-8', index=False)
    


def main(args):
    train = Train(args[1], args[2], args[3])
    
    train.fit()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))