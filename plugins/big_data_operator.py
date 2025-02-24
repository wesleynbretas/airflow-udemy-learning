from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd

class BigDataOperator(BaseOperator):
    
    @apply_defaults
    def __init__(self, path_to_csv_file, path_to_save_file, sep=";", type_file="parquet", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.path_to_csv_file = path_to_csv_file
        self.path_to_save_file = path_to_save_file
        self.sep = sep
        self.type_file = type_file

    def execute(self, context):
        df = pd.read_csv(self.path_to_csv_file, sep=self.sep)

        if self.type_file == "parquet":
            df.to_parquet(self.path_to_save_file)
        elif self.type_file == "json":
            df.to_json(self.path_to_save_file)
        else:
            raise ValueError("Type file is not valid")






