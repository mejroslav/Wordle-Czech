translation_table = {
    ord("Á"): ord("A"),
    ord("É"): ord("E"),
    ord("Ě"): ord("E"),
    ord("Í"): ord("I"),
    ord("Ó"): ord("O"),
    ord("Ú"): ord("U"),
    ord("Ů"): ord("U"),
    ord("Ý"): ord("Y"),
    ord("Č"): ord("C"),
    ord("Ď"): ord("D"),
    ord("Ň"): ord("N"),
    ord("Ř"): ord("R"),
    ord("Š"): ord("S"),
    ord("Ť"): ord("T"),
    ord("Ž"): ord("Z"),
}
def remove_diacritics(s: str) -> str:
    """Remove hooks and dashes from a word or letter."""
    return s.translate(translation_table)

class inDict:
    def __init__(self):
        self.d = {}
    def __getitem__(self, key):
        return self.d[remove_diacritics(key)]
    def __setitem__(self, key, val):
        self.d[remove_diacritics(key)] = val