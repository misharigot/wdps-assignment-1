from bs4 import BeautifulSoup
import cld2
import re
from typing import Optional

WARCTYPE = "WARC-Type"


def preprocess_text(payload: str) -> Optional[str]:
    for line in payload.splitlines():
        if line.startswith(WARCTYPE) and line.split(": ")[1] != "response":
            return
        else:
            break

    html = payload[payload.find("<html"):]

    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style", "textarea"]):
        script.decompose()
    text = soup.get_text(separator=" ", strip=True)

    try:
        _, _, languages = cld2.detect(text)
        if languages[0].language_code != "en":
            return
    except ValueError:
        return

    return (" ".join(re.sub("[^A-Za-z0-9.!?]", " ", text).split())).lower()
