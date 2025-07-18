import fitz  # PyMuPDF - For reading and extracting text from a PDF file
import spacy # process and clean text. Breaks the text into words (tokens), removes punctuation, and helps normalize the input
import json

# Load spaCy’s English NLP model
nlp = spacy.load("en_core_web_sm")


# Takes in PDF content as bytes, opens the PDF in memory using 
# PyMuPDF and loops through each page and collects the text
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# Uses spaCy to tokenize the text, removes non-alphabets, 
# and converts words to lowercase to prepare for mathcing
def extract_skills(text: str, known_skills: list[str]) -> list[str]:
    doc = nlp(text)
    tokens = {token.text.lower() for token in doc if token.is_alpha}

    # Loops through known skills json and if a match is found, 
    # the skill is added to the list and is returned
    found_skills = []
    for skill in known_skills:
        if skill.lower() in tokens:
            found_skills.append(skill)
    return sorted(found_skills)


#Extract resume text, finds matching skills, and returns a final list of matched skills
def parse_resume(pdf_bytes: bytes, known_skills: list[str]) -> list[str]:
    text = extract_text_from_pdf(pdf_bytes)
    return extract_skills(text, known_skills)
