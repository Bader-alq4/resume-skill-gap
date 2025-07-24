import fitz  # PyMuPDF - For reading and extracting text from a PDF file
import spacy # process and clean text. Breaks the text into words (tokens), removes punctuation, and helps normalize the input
import json
from pathlib import Path
import difflib
import re  # Make sure this is imported


# Load spaCy’s English NLP model
nlp = spacy.load("en_core_web_sm")


# Load a list of skills from known_skills.json. 
# Defaults to 'known_skills.json' in this directory"
def load_known_skills(path: Path | str = None) -> list[str]:
    if path is None:
        path = Path(__file__).parent.parent / "known_skills.json"
    return json.loads(Path(path).read_text())


def normalize_skill(raw: str, known_skills: list[str], cutoff: float = 0.7) -> str:
    """
    Normalize a raw skill string to a canonical skill:
    1. exact match
    2. substring match
    3. fuzzy match (difflib)
    4. fallback: return original input
    """
    word = raw.strip()
    if not word:
        return word

    lw = word.lower()
    known_lc = [s.lower() for s in known_skills]

    # 1. Exact match
    for skill in known_skills:
        if skill.lower() == lw:
            return skill

    # 2. Substring match
    for skill in known_skills:
        if skill.lower() in lw:
            return skill

    # 3. Fuzzy match
    match = difflib.get_close_matches(lw, known_lc, n=1, cutoff=cutoff)
    if match:
        idx = known_lc.index(match[0])
        return known_skills[idx]

    # 4. Fallback: not found
    return word


# Takes in PDF content as bytes, opens the PDF in memory using 
# PyMuPDF and loops through each page and collects the text
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_skills(text: str, known_skills: list[str]) -> list[str]:
    """
    Extract skills from text using:
      1. regex exact matches
      2. spaCy named entities
      3. normalization (fuzzy match)
    """
    # 1. Exact matches using regex
    pattern = re.compile(r"\b(?:" + "|".join(map(re.escape, known_skills)) + r")\b", re.IGNORECASE)
    found = {m.group(0) for m in pattern.finditer(text)}

    # 2. Named Entity Recognition
    doc = nlp(text)
    for ent in doc.ents:
        if ent.text in known_skills:
            found.add(ent.text)

    # 3. Normalize everything
    normalized = [normalize_skill(s, known_skills) for s in found]
    return sorted(set(normalized))

def extract_user_skills_manual(manual_input: str, known_skills: list[str]) -> list[str]:
    """
    Parse and normalize comma-separated manual input skills.
    Returns a cleaned and deduplicated list.
    """
    raw_skills = [s.strip() for s in manual_input.split(",") if s.strip()]
    normalized = [normalize_skill(s, known_skills) for s in raw_skills]
    return sorted(set(normalized))


#Extract resume text, finds matching skills, and returns a final list of matched skills
def parse_resume(pdf_bytes: bytes, known_skills: list[str]) -> list[str]:
    text = extract_text_from_pdf(pdf_bytes)
    return extract_skills(text, known_skills)