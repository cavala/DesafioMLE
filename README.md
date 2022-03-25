# Desafio MLE

O projeto desafio MLE tem por objetivo expor uma API em python que traga a estratégia de uma carta através de seu ID. Separei a parte faz a "adivinhação" da estratégia em duas partes, para que o processamento ficasse assíncrono. Assim, ele gera as estratégias para o arquivo challenge_test.csv com base no challenge_train.csv e depois concatena os dois arquivos num só, chamado challenge_result.csv. 
A API apenas consulta os dados do challenge_result e devolve um json com o card completo, incluindo a strategy.

A parte que faz o treinamento fica no arquivo abaixo:

        src\controllers\train.py

É possível executar só a parte que faz o treinamento através do comando abaixo, com os csv's de entrada na mesma pasta.

        python3 train.py 'challenge_train.csv' 'challenge_test.csv' 'challenge_result.csv'

O método de machine learning escolhido foi o de Arvore de decisão, dado o tipo do problema.
Esboçei a solução(train.py) no Jupiter/Anaconda e depois fui adicionando complexidade. Expor a usando o framework Flask e por último coloquei no Docker.

Build da imagem docker

        docker build --tag python-docker .
        

Instanciando uma imagem

         docker run -t -d -p 5000:5000 python-docker
         
A api fica exposta em http://localhost:5000/         

Os testes unitários ainda não funcionam.

