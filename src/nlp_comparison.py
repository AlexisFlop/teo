# -*- coding: utf-8 -*-
# Comparación: spaCy sí analiza oraciones en NL y decide adjuntos, etc.

import spacy
from spacy import displacy
from pathlib import Path

SENTS = [
    "The dog sleeps.",
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
        if t.pos_ == "ADP":  # preposición, p.ej. 'with'
            head = t.head
            kind = "VERB" if head.pos_ == "VERB" else ("NOUN" if head.pos_ in ("NOUN", "PROPN") else head.pos_)
            print(f" - '{t.text} ...' attaches to '{head.text}' [{kind}]")

    # Guarda el árbol de dependencias como HTML para el informe
    html = displacy.render(doc, style="dep", options={"compact": True}, page=True)
    out = Path(f"dep_tree_{idx + 1}.html")
    out.write_text(html, encoding="utf-8")
    print(f"\n[OK] Árbol guardado en: {out.resolve()}")


def main():
    nlp = spacy.load("en_core_web_sm")
    for i, s in enumerate(SENTS):
        analyze(s, i, nlp)


if __name__ == "__main__":
    main()
