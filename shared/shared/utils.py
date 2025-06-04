# shared/utils.py

def format_date_range(start, end):
    return f"{start} → {end}"

def truncate_text(text, max_len=200):
    """Trunca el texto a un máximo de caracteres, añadiendo '…' si es necesario."""
    if len(text) <= max_len:
        return text
    return text[:max_len].rstrip() + "…"

def print_divider(title=""):
    """Imprime una línea divisoria con un título opcional."""
    line = "=" * 80
    if title:
        centered = f" {title} ".center(80, "=")
        print(centered)
    else:
        print(line)
