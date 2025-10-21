// File: engine/glyphs.ts

type GlyphFactory = () => any;

export class GlyphLoader {
  private registry: Record<string, GlyphFactory> = {};

  register(uri: string, factory: GlyphFactory): void {
    this.registry[uri] = factory;
  }

  load(uri: string): any {
    const factory = this.registry[uri];
    if (factory) return factory();
    console.warn(`[WARN] Glyph not found: ${uri}`);
    return null;
  }
}
