from app import HubspotCompaniesService,CompaniesDeduplicator
import typer
from rich import print
from rich.progress import track
import pandas as pd
from __config__ import *
from logic.manual_processing import manual_processing

def aumatic_processing(controller:CompaniesDeduplicator):
    pass    



def main():
    print("[bold blue]Bem vindo a aplicação de Deduplicação de Empresas no Hubspot do G4[/bold blue]")
    print("[italic green]-----------------")
    print("Quem desenvolveu essa aplicação -> [red]Renaldo Cavalcante [/red]")
    print("[italic green]-----------------")
    print("[bold]:warning: Siga o passo a passo de forma adequada para evitar maiores [bold red]riscos[/bold red] ao [bold orange3]Hubspot[/bold orange3], se você não tem experiência com [bold orange3]Hubpspot[/bold orange3] ou programação [bold red]NÃO[/bold red] prossiga[/bold]")
    print("[italic green]-----------------")
    print("[bold]Então bora, lá começar a resolver os seus problemas[/bold]")
    
    typer.confirm("Você é do time de tecnologia ou tem completa certeza do que está fazendo???", abort=True)
    print("[italic green]-----------------")
    csv_file = ""
    csv_checkcer = False
    
    while csv_file[-4:] != ".csv":
        csv_file = typer.prompt("Escreva o caminho para o arquivo .csv da empresa (Exemplo: './empresas.csv' ")
        if csv_file[-4:] != ".csv":
            print("[bold red]O nome do arquivo precisa terminar com .csv[/bold red]")
    
    print("[italic green]-----------------")
    
    while csv_checkcer != True:
        try:
            brute_df = pd.read_csv(csv_file)
        except Exception:
            print(f"[bold red]ERRO!!![/bold red]")
            raise typer.Exit("Ocorreu um erro com o arquivo")
        else:
            print(f"[bold reverse]'[italic]{csv_file}[/italic]' foi armazenado com sucesso")
            csv_checkcer = True
    
    print("[italic green]-----------------")
    
    try:
        companies_deduplicator = CompaniesDeduplicator(csv_file)
    except KeyError:
        print(f"[reverse red] Arquivo não está no formato correto:sad:")
        print(""" O arquivo .csv precisa ter as seguintes colunas: \n [bold]company_id | company_name | createdate | last_activity_date[/bold]""")
        
    
    print("[italic green]-----------------")
    print("[reverse] Dataframe Carregado com Sucesso")
    print(companies_deduplicator.raw_df)
    print("[italic green]-----------------")
    print("[reverse blue]Como a aplicação vai funcionar daqui pra frente")
    #time.sleep(2)
    print("A aplicação vai percorrer a tabela acima, nome a nome, buscando duplicadas dentro dela mesmo.")
    #time.sleep(2)
    print("A seguir eu vou te pedir para confirmar a opção se você vai querer o merge de forma automática ou não.")
    #time.sleep(2)
    print("[purple]Antes disso vou explicar dois conceitos importantes.[/purple] \n [bold blue]Similaridade:[/bold blue][bold]é o quanto de similaridade em percentual o modelo estatístico vai cuspir resultados[/bold] \n [bold blue]Filtro de Similaridade:[/bold blue][bold] é o filtro que utiliza-se para normalizar os dados, em caso de dúvida utiliza os dois com o mesmo valor[/bold]")
    #time.sleep(2)
    print("O merge automático só pode ocorrer para a similaridade de 100% ou mais, \n [bold reverse red]EM HIPÓTESE ALGUMA EDITE O CÓDIGO PARA CONSEGUIR ULTRAPASSAR ESSA REGRA")
    #time.sleep(2)
    print("[italic green]-----------------")
    similarity_percent = typer.prompt("Qual o percentual de Similaridade que deseja?",default=0.8,)
    similarity_filter = typer.prompt("Qual o percentual do filtro de similaridade que deseja?",default=1)
    print("[italic green]-----------------")
    print("[reverse] Informe o Acess Key do hubspot abaixo")
    hubspot_access_token = typer.prompt("INFORM A ACCESS KEY DO APP DO HUBSPOT?",hide_input=True)
    print("[italic green]-----------------")
    companies_deduplicator.raw_df.to_csv(BASE_CSV)
    manual_processing(similarity_percent,similarity_filter,hubspot_access_token=hubspot_access_token)
        


if __name__ == "__main__":
    typer.run(main)