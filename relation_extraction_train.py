import pickle
import kindred

corpus = kindred.load("pubannotation", "/Users/aryopg/Downloads/AGAC_training/json")
train_corpus, dev_corpus = corpus.split(0.75)

prediction_corpus = dev_corpus.clone()
prediction_corpus.removeRelations()

print(train_corpus)

print("Training")
classifier = kindred.RelationClassifier(model="en_core_web_lg")
for i in range(100):
    print(f">>>> {i}")
    classifier.train(train_corpus)
print("Training Done")

print("Evaluating")
classifier.predict(prediction_corpus)
f1score = kindred.evaluate(dev_corpus, prediction_corpus, metric="f1score")
print(f"F1 score: {f1score}")

print("Saving")
with open("lg_re_classifier.pickle", "wb") as f:
    pickle.dump(classifier, f)
print("Saving Done")
