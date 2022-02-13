import spacy

nlp = spacy.load("he_ner_news_trf")
text = """מרגלית דהן
מספר זהות 11278904-5

2/12/2001
ביקור חוזר מ18.11.2001
במסגרת בירור פלפיטציות ואי סבילות למאמצים,מנורגיות קשות ע"ר שרירנים- ביצעה מעבדה שהדגימה:
המוגלובין 9, מיקרוציטי היפוכרומטי עם RDW 19,
פריטין 10, סטורציית טרנספרין 8%. 
מבחינת עומס נגיפי HIV- undetectable ומקפידה על HAART
"""

doc = nlp(text)
for entity in doc.ents:
    print(f"{entity.text} \t {entity.label_}: {entity._.confidence_score:.4f} ({entity.start_char},{entity.end_char})")
