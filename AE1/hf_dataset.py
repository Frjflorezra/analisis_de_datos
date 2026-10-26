import pandas as pd
from datasets import load_dataset


class HFDatasetLoader:

    def __init__(self, dataset_id: str, split: str = "train"):
        self.dataset_id = dataset_id
        self.split = split

    def cargar(self) -> pd.DataFrame:
        dataset = load_dataset(
            self.dataset_id,
            split=self.split
        )

        return dataset.to_pandas()