"""
Preprocessing: get readable text from html and check if the main language is english
Output = Text of htmlpage or none if no text or no english text
"""

import re
from typing import Optional

import cld2
from bs4 import BeautifulSoup

WARCTYPE = "WARC-Type"
CHARACTERS_TO_INCLUDE = "[^A-Za-z0-9.,!?'&:-]"


def preprocess_text(payload: str) -> Optional[str]:
    for line in payload.splitlines():
        if line.startswith(WARCTYPE) and line.split(": ")[1] != "response":
            return None
        else:
            break

    html = payload[payload.find("<html") :]

    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style", "textarea"]):
        script.decompose()
    text = soup.get_text(separator=" ", strip=True)

    try:
        _, _, languages = cld2.detect(text)
        if languages[0].language_code != "en":
            return None
    except ValueError:
        return None

    return " ".join(re.sub(CHARACTERS_TO_INCLUDE, " ", text).split())
