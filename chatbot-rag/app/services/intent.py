CONTACT_KEYWORDS = [
    "hablar con alguien",
    "contacto",
    "asesor",
    "vendedor",
    "llamada",
    "me pueden contactar",
    "hablar con una persona"
]


def wants_human_contact(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in CONTACT_KEYWORDS)
