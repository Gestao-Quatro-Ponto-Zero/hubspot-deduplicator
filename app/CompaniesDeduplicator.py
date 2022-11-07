from ctypes.wintypes import tagPOINT
from doctest import master
from heapq import merge
from string_grouper import match_strings, match_most_similar, \
	group_similar_strings, compute_pairwise_similarities, \
	StringGrouper
import pandas as pd
import requests
import numpy as np

class CompaniesDeduplicator:
    """
        Companies Deduplicator class. 
        
        Process csv file and merge companies in the Hubspot. 
        
        Here we need ot specify file to a csv with the specified columns:
        
        - company_id: int|str contains the company_id from hubspot
        - company_name: str contains the name of the company on hubspot (duplicated)
        - faixa_de_funcionarios: str contains the faixa de funcionario field.
        - faixa_de_faturamento: str contains the faixa de faturamento field from hubspot.
        - createdate: str string like timestamp, came from CSV and direct from Bigquery. 
        - last_activity_date: str timestamp like string, came from CSV and direct from Bigquery.
    """

    def __init__(self,csv_file: str):
        self.file_path = csv_file
        self.raw_df = pd.read_csv(self.file_path)
        self._process_raw_df_()

    def _process_raw_df_(self):
        self.raw_df["company_id"] = self.raw_df["company_id"].astype(int)
        self.raw_df["createdate"] = pd.to_datetime(self.raw_df["createdate"])
        self.raw_df["last_activity_date"] = pd.to_datetime(self.raw_df["last_activity_date"])
        self.raw_df["createdate_delta"] = pd.Timestamp.today().date() - self.raw_df["createdate"].dt.date
        self.raw_df["last_activity_delta"] = pd.Timestamp.today().date() - self.raw_df["last_activity_date"].dt.date
        self.raw_df["createdate_delta"] = self.raw_df["createdate_delta"].dt.days
        self.raw_df["last_activity_delta"] = self.raw_df["last_activity_delta"].dt.days
        self.raw_df["createdate"] = self.raw_df["createdate"].dt.date
        self.raw_df["last_activity_date"] = self.raw_df["last_activity_date"].dt.date
        self.raw_df = self.raw_df[[
            "company_id",
            "company_name",
            "createdate",
            "last_activity_date",
            "createdate_delta",
        ]]
        self.raw_df.sort_values(by=["company_name","createdate_delta"],ascending=True,inplace=True,ignore_index=True)

    @staticmethod
    def _union_ints_arrays_(two_dimension_array: np.array, order_id: list = [0,1]):
        new_int_array = []

        for value in two_dimension_array:
            union_int = list(value)
            union_int.sort()
            union_int = str(union_int[order_id[0]]) + str(union_int[order_id[1]])
            new_int_array.append(union_int)
        
        return np.array(new_int_array)

    @staticmethod
    def _setup_df_for_matching_(df: pd.DataFrame, duplicate_column: str, id_column: str = None):
        
        df_master = df[df[duplicate_column].isnull()==False]
        master_series = df_master[duplicate_column].astype(str)

        if id_column:
            master_id = df_master[id_column].astype(int)
            return master_series,master_id

        return master_series



    @staticmethod
    def get_matched_df(
        key_series: pd.Series, 
        key_ids: pd.Series, 
        duplicated_series: pd.Series,
        duplicated_ids: pd.Series,
        min_similarity: int = 0.8, 
        similarity_filter: int = 0.8,
        ) -> pd.DataFrame:

        key_series.rename("key_series",inplace=True)
        key_ids.rename("key_ids",inplace=True)
        duplicated_series.rename("duplicated_series",inplace=True)
        duplicated_ids.rename("duplicated_ids",inplace=True)

        sg = StringGrouper(key_series)
        df_matched = sg.match_strings(master=key_series, master_id=key_ids, min_similarity=min_similarity,duplicates=duplicated_series, duplicates_id=duplicated_ids)
        df_matched["similarity"] = df_matched["similarity"].round(4)
        df_matched = df_matched[df_matched["similarity"]>=similarity_filter]
        df_matched = df_matched[df_matched["left_key_ids"] != df_matched["right_duplicated_ids"]]
    
        return df_matched

    def _compare_two_rows_(self,row_1,row_2):
        df = pd.concat([row_1,row_2])


    def _avaliate_row_score_(self,id_1: int,id_2: int):
        df = self.raw_df
        row_1 = df.loc[df["company_id"]==id_1]
        row_2 = df.loc[df["company_id"]==id_2]
        
        df_avaliate_score = pd.concat([row_1,row_2])
        
        
        df_avaliate_score.sort_values(by="createdate_delta",ascending=False,inplace=True)
        primary_id = df_avaliate_score["company_id"].values[0]
        merge_id = df_avaliate_score["company_id"].values[1]
        
        
        return int(primary_id),int(merge_id)
        
      


