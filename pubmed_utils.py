import os
from typing import Optional

from Bio import Entrez
import pandas as pd

from datetime import datetime

Entrez.email = "aryopg@gmail.com"


GLOBAL_CSV_PATH = "publications_list.csv"


class Publication:
    def __init__(self, pmid: str, title: str, abstract: str, completed_year: int):
        self.pmid = pmid
        self.title = title
        self.abstract = abstract
        self.completed_year = completed_year

    def save(self, csv_path: str):
        # Save to a centralized CSV file
        # pubmed id, title, abstract, timestamp added
        df = pd.DataFrame(
            {
                "pmid": [self.pmid],
                "title": [self.title],
                "abstract": [self.abstract],
                "completed_year": [self.completed_year],
                "added_at": [datetime.now()],
            }
        )
        df.to_csv(csv_path, mode="a", header=not os.path.exists(csv_path))


def download_pubmed_by_pmid(pmid: str, save_to_csv: bool = True) -> Publication:
    # download from pubmed
    print(f"Downloading publication {pmid}")

    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="xml")
    record = Entrez.read(handle)
    title = record["PubmedArticle"][0]["MedlineCitation"]["Article"]["ArticleTitle"]
    abstract = record["PubmedArticle"][0]["MedlineCitation"]["Article"]["Abstract"][
        "AbstractText"
    ][0]
    completed_year = int(
        record["PubmedArticle"][0]["MedlineCitation"]["DateCompleted"]["Year"]
    )

    publication = Publication(
        pmid=pmid, title=title, abstract=abstract, completed_year=completed_year
    )

    if save_to_csv:
        print(f"Saving publication to global CSV {GLOBAL_CSV_PATH}")
        publication.save(csv_path=GLOBAL_CSV_PATH)

    return publication


def get_publications_list(num_publications: Optional[int] = None) -> pd.DataFrame:
    publications_list = pd.read_csv(GLOBAL_CSV_PATH, index_col=0)
    publications_list["added_at"] = pd.to_datetime(publications_list["added_at"])
    publications_list = publications_list.sort_values(by="added_at", ascending=False)
    publications_list = publications_list.set_index("pmid")

    if num_publications:
        return publications_list[["title", "added_at"]].head(num_publications)
    else:
        return publications_list[["title", "added_at"]]
