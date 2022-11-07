
from doctest import master
from multiprocessing.sharedctypes import Value
from app import HubspotCompaniesService,CompaniesDeduplicator
import typer
from rich import print
from rich.progress import track,Progress, SpinnerColumn, TextColumn
import pandas as pd
from __config__ import *
import time

def manual_processing(similarity: int, similirity_filter: int, hubspot_access_token: int):
    
    print("[reverse bold] Processo Manual Começou!!!")
    #Columns To bem Presented on Terminal
    columns = ["left_key_series","left_key_ids","right_duplicated_ids","right_duplicated_series","similarity"]
    
    #Base DF. 
    df_base_csv = CompaniesDeduplicator(BASE_CSV).raw_df
    #All Series and Ids' to check values that are duplicated
    all_series, all_ids = CompaniesDeduplicator._setup_df_for_matching_(df_base_csv,"company_name","company_id")
    
    
    #save csv as d
    #df_base_csv.to_csv(processed_path)
    #master_df = CompaniesDeduplicator(processed_path).raw_df
    try:
        temp_deduplicator = CompaniesDeduplicator(TEMP_CSV)
    except FileNotFoundError:
        temp_deduplicator = CompaniesDeduplicator(BASE_CSV)
        
    continue_df = False
        
    if len(df_base_csv) != len(temp_deduplicator.raw_df):
        print("[reverse bold]Já tem um Mergin em Execução, deseja continua-lo? Não é possível recuperar caso escolha a resposta negativa. ")
        continue_df = typer.confirm("Deseja Continuar?")
        
    if continue_df:
        master_df = temp_deduplicator.raw_df
    else:
        master_df  = df_base_csv
    
    name_ids = master_df[["company_name","company_id"]].values
    
    #index controller
    excluded_ids = []
    
    try:
        for value in name_ids:
            if value[1] in excluded_ids:
                continue
            print("[bold]------------------------[/bold][reverse bold]INFOS[/reverse bold][bold]------------------------[/bold]")
            print(f"[bold white reverse]CompanyName:{value[0]}, CompanyId: {value[1]}")
            
            key_series=pd.Series(value[0])
            key_id=pd.Series(value[1])
            
            try: 
                matched_df = CompaniesDeduplicator.get_matched_df(
                    key_series = key_series,
                    key_ids = key_id,
                    duplicated_series=all_series,
                    duplicated_ids=all_ids,
                    similarity_filter=similirity_filter,
                    min_similarity=similarity
                )
            except ValueError:
                print("[red reverse bold] Error on Value String")
                continue
        
            if len(matched_df) == 0:
                print(f"[reverse purple]SEM DADOS DUPLICADOS PARA:[/reverse purple] [reverse dodger_blue2]{key_series.values[0]}[/reverse dodger_blue2]")
                excluded_ids.append(value[1])
                continue
            
            print("[italic bold]-----------------")
            print(matched_df[columns])
            print("[italic bold]-----------------")
            print(f"[bold reverse blue1]Primary Object Key: [/bold reverse blue1][bold]{ list(matched_df.left_key_ids.unique()) } ")
            print(f"[bold reverse green1]Ids para Merge: { list(matched_df.right_duplicated_ids.values) } ")
            print(f"[reverse bold]Comandos: \n A: Aceitar Merges \n D: Negar Merges \n C: Cancelar Inserts")
            action = typer.prompt("Insira a ação")
            if action.upper() in (["A","D","C"]):
                if action.upper() == "A":
                    merge_confirm = True
                elif action.upper() == "D":
                    merge_confirm = False
                elif action.upper() == "C":
                    print("[reverse red bold]Merging Cancelado")
                    raise typer.Exit()
                        
            else:
                raise TypeError("Input incorreto")
            
            print("[italic bold]-----------------")
            
            if merge_confirm:
                
                total = 0
                print("[reverse bold]Merging Started")
                for i,values in zip(track(range(len(matched_df)), description="Mergeando Companies"), matched_df[["left_key_ids","right_duplicated_ids"]].values):
                    hubspot_service = HubspotCompaniesService(access_token=hubspot_access_token)
                    
                    response = hubspot_service.merge_companies(primary_object_id=values[0],object_id_to_merge=values[1])    
                    
                    if response.status_code == 200:
                        print(f"[reverse green bold]Merging complete {values[0]}:{values[1]}")
                    else:
                        print(f"[reverse red bold]Merging Failed {values[0]}:{values[1]}")
                        
                        try:
                            print(f"Response Json {response.json()}")
                        except Exception:
                            pass
                        
                        print("Proceed or Abort?")
                        proceed_after_api_error = typer.confirm("Proceed?")
                        
                        if proceed_after_api_error!=True :
                            typer.Exit()
                        
                    excluded_ids.append(values[0])
                    excluded_ids.append(values[1])
                    total += 1
    except Exception as e:
        master_df = master_df[master_df["company_id"].isin(excluded_ids)==False]
        master_df.to_csv(TEMP_CSV)
        raise e
    finally:
        if len(excluded_ids) > 1:
            master_df = master_df[master_df["company_id"].isin(excluded_ids)==False]
            master_df.to_csv(TEMP_CSV)