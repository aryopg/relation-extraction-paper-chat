from pubmed_utils import download_pubmed_by_pmid
from relation_extraction_utils import (
    relation_extraction_predict,
    named_entity_recognition_predict,
    prediction_pipeline,
)


if __name__ == "__main__":
    # download_pubmed_by_pmid("32606233")

    # publication = download_pubmed_by_pmid("32606233", save_to_csv=False)
    publication = download_pubmed_by_pmid("29630008", save_to_csv=False)

    publication_text = publication.title + "\n" + publication.abstract
    print(publication_text)
    doc, re_predictions = prediction_pipeline(publication_text)
    print(doc)
    print(re_predictions)
    # prediction = relation_extraction_predict(publication_text)
