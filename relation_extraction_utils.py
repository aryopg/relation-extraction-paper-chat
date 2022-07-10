import kindred
import pickle
import spacy

ner_nlp = spacy.load(
    "/Users/aryopg/Documents/learning/relation-extraction-paper-chat/lg_ner_classifier"
)

with open("lg_re_classifier.pickle", "rb") as model_file:
    re_model = pickle.load(model_file)


def relation_extraction_predict(ner_doc):
    entities = []
    for entity in ner_doc.ents:
        entities += [
            kindred.Entity(
                entity.label_, entity.text, [(entity.start_char, entity.end_char)]
            )
        ]
    kindred_doc = kindred.Document(text=ner_doc.text, entities=entities)

    kindred_corpus = kindred.Corpus()
    kindred_corpus.addDocument(kindred_doc)
    re_model.predict(kindred_corpus)

    return kindred_corpus.getRelations()


def named_entity_recognition_predict(text: str):
    doc = ner_nlp(text)
    return doc


def prediction_pipeline(text: str):
    doc, tuple_entities, ner_texts = named_entity_recognition_predict(text)

    re_predictions = []
    for tuple_entity, ner_text in zip(tuple_entities, ner_texts):
        re_prediction = relation_extraction_predict(ner_text)
        pred = max(re_prediction, key=lambda x: x["score"])["label"]
        if pred == "1":
            re_predictions += [
                ("is_associated", tuple_entity[0].text, tuple_entity[1].text)
            ]
    return doc, re_predictions
