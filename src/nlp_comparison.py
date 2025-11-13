import spacy
from spacy import displacy
from pathlib import Path

SENTS = [
    "Thedogsleeps.",
    "The dog sees a man with a telescope.",
    "The man sleeps with a telescope.",
    "Hello world.",
]


def analyze(sentence: str, idx: int, nlp):
    print("\n" + "=" * 70)
    print(f"Sentence {idx + 1}: {sentence}")
    doc = nlp(sentence)

    print("\nTOKENS (text | POS | dep → head):")
    for t in doc:
        print(f"{t.text:>12} | {t.pos_:<6} | {t.dep_:<10} → {t.head.text}")

    print("\nNOUN CHUNKS:")
    for nc in doc.noun_chunks:
        print(f" - {nc.text}  (head: {nc.root.head.text} | dep: {nc.root.dep_})")

    print("\nPREPOSITIONS (attachment):")
    for t in doc:
        if t.pos_ == "ADP":
            head = t.head
            kind = "VERB" if head.pos_ == "VERB" else ("NOUN" if head.pos_ in ("NOUN", "PROPN") else head.pos_)
            print(f" - '{t.text} ...' attaches to '{head.text}' [{kind}]")


def main():
    nlp = spacy.load("en_core_web_sm")
    for i, s in enumerate(SENTS):
        analyze(s, i, nlp)


if __name__ == "__main__":
    main()
