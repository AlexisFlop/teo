import spacy

nlp = spacy.load("en_core_web_sm")


def textAnalyzer(text):
    doc = nlp(text)

    print(f"Texto: {text}")
    print("\nAnálisis:")

    for token in doc:
        print(f"'{token.text}' -> POS: {token.pos_}, Lemma: {token.lemma_}")

    print("\nEntidades:")
    for ent in doc.ents:
        print(f"'{ent.text}' -> {ent.label_}")

    print("-" * 50)


strings = [
    "The book costs 25 dollars.",
    "Mary was born in 1990 in Madrid.",
    "The meeting is on December 15th.",
    "Int Flamenco;"
]

for text in strings:
    textAnalyzer(text)