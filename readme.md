# G4 - Deduplicador de Empresad do Hubspot. 

## Objetivo do Produto. 
Tornar menos oneroso operacionalmente deduplicar as empresas do hubspot e transformar isso em um processo de constante aplicação. Não somente Ad-Hoc. 


## Premissas
- Vai ser inicialmente uma CLI Application, por causa do tempo de desenvolvimento disso. 
- Vamos aplicar esse processo através desse produto de forma recorrente na empresa, isso acontecerá pelo time do Thiago de CRM. 



# Como Utilizar

## 1. Instalando depêndencias previamente previamente. 

**Download do Python**
Faça do Download da Versão no  3.10.6 ou 3.10.8 no link [Python Download](https://www.python.org/downloads/release/python-3108/)

**Instalação das biblitecas**
Em um terminal a sua escolha após a instalação do Python. 
```bash
pip install -r requirements.txt

ou 

pip3 install -r requirements.txt
```

## 2. Importar empresas que deseja checar duplicadas.

**Campos Necessários que precisam exsitir no arquivo.csv**
- company_id: Id da empresa no hubspot. 
- company_name: Nome da empresa no Hubspot, esse é o campo chave que vamos checar duplicados.
- faixa_de_funcionarios: Campo do hubspot de faixa de funcionarios da empresa.
- faixa_de_faturamento: Campo do hubspot de faixa de faturamento da empresa.
- createdate: data de criação da company no hubspot. 
- last_activity_date: data da última atividade no hubspot.

**Formato do Arquivo**
O formato do arquivo tem que ser OBRIGATÓRIAMENTE .csv. 


## 3. Rodando a Aplicação

**Rodando o código via terminal**
1. Abra um terminal e vá até o diretório que foi feito do download da aplicaçào. 
2. Digite o seguinte comando dentro do terminal
    ```bash
    python3 main.py
    ```
3. Siga o passo a descrito dentro do terminal

