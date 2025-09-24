class GlyphLoader:
    def __init__(self):
        self.registry = {}

    def register(self, uri, func):
        self.registry[uri] = func

    def load(self, uri):
        if uri in self.registry:
            return self.registry[uri]()
        else:
            print(f"[WARN] Glyph not found: {uri}")
