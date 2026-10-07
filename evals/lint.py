"""Deterministic STE-ES checks over one answer. Also runs alone: python3 lint.py file.md"""

import re
import sys

GERUND_FALSE = {
    "cuando", "comando", "comandos", "mando", "bando", "ando", "demando", "fernando", "orlando",
    # first-person presents that end like a gerund
    "recomiendo", "entiendo", "atiendo", "defiendo", "extiendo", "pretendo", "enciendo", "tiendo",
}
FILLER = [
    r"básicamente", r"cabe destacar", r"cabe mencionar", r"cabe aclarar",
    r"es importante (?:destacar|mencionar|notar|tener en cuenta)",
    r"en resumen", r"en definitiva", r"sin duda", r"claramente", r"simplemente",
    r"espero que (?:te|le) sirva", r"no dudes en", r"¡excelente", r"¡buena pregunta",
]
NOMINAL = [r"\brealiz\w+", r"\befectu\w+", r"llev\w+ a cabo", r"proced\w+ a\b"]
# "estás" is the same in tuteo and voseo, so it counts for neither.
TUTEO = r"\b(?:tú|puedes|tienes|debes|quieres|necesitas|sabes|haces|vienes|sigues|corres|usas|revisas)\b"
# Approximate. Presents in -ás/-és/-ís are unambiguous enough; imperatives in -á/-é/-í are
# not (they collide with preterites and futures), so only a list of common dev verbs counts.
VOSEO_PRESENT = r"\b\w{2,}(?:ás|és|ís)\b"
VOSEO_PRESENT_FALSE = {
    "más", "después", "además", "demás", "inglés", "francés", "atrás", "detrás", "jamás",
    "país", "través", "interés", "estás", "quizás", "compás", "anís", "revés", "cortés",
}
VOSEO_IMPERATIVES = {
    "revisá", "corré", "fijate", "probá", "mirá", "agregá", "borrá", "usá", "abrí", "hacé", "poné",
    "pusheá", "commiteá", "creá", "cambiá", "buscá", "copiá", "pegá", "configurá", "instalá",
    "ejecutá", "reiniciá", "chequeá", "leé", "escribí", "decime", "avisame", "sacá", "pasá",
    "rebaseá", "mergeá", "verificá", "confirmá", "andá", "esperá", "seguí", "volvé", "tené",
}
DIAGRAM_CHARS = re.compile(r"[┌┐└┘│├┤┬┴┼►◄▼▲→←↓↑⇒]|──>")
# ASCII arrows count only in blocks without a language tag: in code they are operators.
ASCII_ARROW = re.compile(r"-->|->|<--")



def split_prose(text):
    """Return (prose, code_blocks). Tables and code blocks are not prose."""
    code = re.findall(r"```(\w*)\n?(.*?)```", text, re.S)
    prose = re.sub(r"```.*?```", " ", text, flags=re.S)
    prose = "\n".join(l for l in prose.splitlines() if not l.lstrip().startswith("|"))
    return prose, code


def sentences(prose):
    parts = re.split(r"(?<=[.!?])\s+|\n+", prose)
    return [p for p in (re.sub(r"[#>*_`-]", " ", s).strip() for s in parts) if p]


def lint(text):
    prose, code = split_prose(text)
    low = prose.lower()
    words = re.findall(r"\b[\wáéíóúñü]+\b", low)
    sents = sentences(prose)
    gerunds = [w for w in words if re.fullmatch(r"\w+(?:ando|iendo|yendo)", w) and w not in GERUND_FALSE]
    voseo = sum(1 for w in re.findall(VOSEO_PRESENT, low) if w not in VOSEO_PRESENT_FALSE)
    voseo += sum(1 for w in words if w in VOSEO_IMPERATIVES) + len(re.findall(r"\bvos\b", low))
    return {
        "words": len(words),
        "words_total": len(re.findall(r"\b[\wáéíóúñü]+\b", text.lower())),
        "sentences": len(sents),
        "long_sentence": sum(1 for s in sents if len(s.split()) > 25),
        "semicolon": prose.count(";"),
        "gerund": len(gerunds),
        "filler": sum(len(re.findall(p, low)) for p in FILLER),
        "nominalization": sum(len(re.findall(p, low)) for p in NOMINAL),
        "tuteo": len(re.findall(TUTEO, low)),
        "voseo": voseo,
        "diagram": any(DIAGRAM_CHARS.search(body) or (not lang and ASCII_ARROW.search(body))
                       for lang, body in code),
    }


VIOLATIONS = ["long_sentence", "semicolon", "gerund", "filler", "nominalization", "tuteo"]


def per100(r):
    return 100 * sum(r[k] for k in VIOLATIONS) / max(r["words"], 1)


if __name__ == "__main__":
    for f in sys.argv[1:]:
        r = lint(open(f).read())
        print(f, {**r, "per100": round(per100(r), 2)})
