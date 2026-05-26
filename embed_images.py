#!/usr/bin/env python3
"""Replace Pino slider section and embed new images as base64 data URIs."""
import base64
import io
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow not installed. Run: pip install Pillow")

HTML_FILE = Path(__file__).parent / "index.html"
IMAGES_DIR = Path(__file__).parent / "images"
MAX_WIDTH = 1200
QUALITY = 72

# Maps the placeholder path used in HTML -> actual local PNG file
IMAGES = {
    "/mnt/user-data/uploads/IMG_2077.jpeg": IMAGES_DIR / "IMG_2077.png",
    "/mnt/user-data/uploads/IMG_2055.jpeg": IMAGES_DIR / "IMG_2055.png",
    "/mnt/user-data/uploads/IMG_2068.jpeg": IMAGES_DIR / "IMG_2068.png",
    "/mnt/user-data/uploads/IMG_2052.jpeg": IMAGES_DIR / "IMG_2052.png",
    "/mnt/user-data/uploads/IMG_2075.jpeg": IMAGES_DIR / "IMG_2075.png",
    "/mnt/user-data/uploads/IMG_2057.jpeg": IMAGES_DIR / "IMG_2057.png",
    "/mnt/user-data/uploads/IMG_2079.jpeg": IMAGES_DIR / "IMG_2079.png",
    "/mnt/user-data/uploads/IMG_2065.jpeg": IMAGES_DIR / "IMG_2065.png",
    "/mnt/user-data/uploads/IMG_2074.jpeg": IMAGES_DIR / "IMG_2074.png",
    "/mnt/user-data/uploads/IMG_2054.jpeg": IMAGES_DIR / "IMG_2054.png",
}

NEW_SLIDERS = """
  <div class="chapter"><div class="chapter-line"></div><span class="chapter-label">Parrilla &amp; outdoor kitchen</span><div class="chapter-line"></div></div>
  <div class="ba-wrap" style="height:380px" data-pct="50" aria-label="Before and after: parrilla">
    <img class="ba-before" src="/mnt/user-data/uploads/IMG_2077.jpeg" alt="Before: crumbling parrilla with exposed pipes">
    <div class="ba-after"><img src="/mnt/user-data/uploads/IMG_2055.jpeg" alt="After: glowing parrilla at sunset"></div>
    <div class="ba-divider" style="left:50%"></div>
    <div class="ba-handle" style="left:50%"><svg viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2.5" stroke-linecap="round"><path d="M8 9l-4 3 4 3M16 9l4 3-4 3"/></svg></div>
    <span class="ba-lbl ba-lbl-b">Before</span><span class="ba-lbl ba-lbl-a">After</span>
  </div>

  <div class="chapter"><div class="chapter-line"></div><span class="chapter-label">Living room</span><div class="chapter-line"></div></div>
  <div class="ba-wrap" style="height:380px" data-pct="50" aria-label="Before and after: living room">
    <img class="ba-before" src="/mnt/user-data/uploads/IMG_2068.jpeg" alt="Before: dated living room with dark furniture">
    <div class="ba-after"><img src="/mnt/user-data/uploads/IMG_2052.jpeg" alt="After: bright living room with rattan pendants"></div>
    <div class="ba-divider" style="left:50%"></div>
    <div class="ba-handle" style="left:50%"><svg viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2.5" stroke-linecap="round"><path d="M8 9l-4 3 4 3M16 9l4 3-4 3"/></svg></div>
    <span class="ba-lbl ba-lbl-b">Before</span><span class="ba-lbl ba-lbl-a">After</span>
  </div>

  <div class="chapter"><div class="chapter-line"></div><span class="chapter-label">Kitchen</span><div class="chapter-line"></div></div>
  <div class="ba-wrap" style="height:380px" data-pct="50" aria-label="Before and after: kitchen">
    <img class="ba-before" src="/mnt/user-data/uploads/IMG_2075.jpeg" alt="Before: red cabinets and dark wood shelving">
    <div class="ba-after"><img src="/mnt/user-data/uploads/IMG_2057.jpeg" alt="After: renovated kitchen with open shelving"></div>
    <div class="ba-divider" style="left:50%"></div>
    <div class="ba-handle" style="left:50%"><svg viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2.5" stroke-linecap="round"><path d="M8 9l-4 3 4 3M16 9l4 3-4 3"/></svg></div>
    <span class="ba-lbl ba-lbl-b">Before</span><span class="ba-lbl ba-lbl-a">After</span>
  </div>

  <div class="chapter"><div class="chapter-line"></div><span class="chapter-label">Patio</span><div class="chapter-line"></div></div>
  <div class="ba-wrap" style="height:380px" data-pct="50" aria-label="Before and after: patio">
    <img class="ba-before" src="/mnt/user-data/uploads/IMG_2079.jpeg" alt="Before: bare patio with worn tiles">
    <div class="ba-after"><img src="/mnt/user-data/uploads/IMG_2065.jpeg" alt="After: renovated patio with umbrella table"></div>
    <div class="ba-divider" style="left:50%"></div>
    <div class="ba-handle" style="left:50%"><svg viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2.5" stroke-linecap="round"><path d="M8 9l-4 3 4 3M16 9l4 3-4 3"/></svg></div>
    <span class="ba-lbl ba-lbl-b">Before</span><span class="ba-lbl ba-lbl-a">After</span>
  </div>

  <div class="chapter"><div class="chapter-line"></div><span class="chapter-label">Dining room</span><div class="chapter-line"></div></div>
  <div class="ba-wrap" style="height:380px" data-pct="50" aria-label="Before and after: dining room">
    <img class="ba-before" src="/mnt/user-data/uploads/IMG_2074.jpeg" alt="Before: dark colonial dining table">
    <div class="ba-after"><img src="/mnt/user-data/uploads/IMG_2054.jpeg" alt="After: Tolix dining set with striped linen"></div>
    <div class="ba-divider" style="left:50%"></div>
    <div class="ba-handle" style="left:50%"><svg viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2.5" stroke-linecap="round"><path d="M8 9l-4 3 4 3M16 9l4 3-4 3"/></svg></div>
    <span class="ba-lbl ba-lbl-b">Before</span><span class="ba-lbl ba-lbl-a">After</span>
  </div>

  """

# ── helpers ────────────────────────────────────────────────────────────────

def encode_image(local_path: Path) -> str:
    if not local_path.exists():
        sys.exit(f"Image not found: {local_path}")
    img = Image.open(local_path)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    if img.width > MAX_WIDTH:
        ratio = MAX_WIDTH / img.width
        img = img.resize((MAX_WIDTH, int(img.height * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=QUALITY, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/jpeg;base64,{b64}"

# ── Step 1: read file ───────────────────────────────────────────────────────

print("Reading index.html …")
html = HTML_FILE.read_text(encoding="utf-8")

# ── Step 2: replace slider section ─────────────────────────────────────────

# The Instagram link block ends with </a> followed by the slider section
# which ends just before <blockquote class="pull-quote">
START_MARKER = "@pino.amare\n</a>"
END_MARKER = "  <blockquote class=\"pull-quote\">"

start_idx = html.find(START_MARKER)
if start_idx == -1:
    sys.exit("ERROR: Could not find Instagram start marker")

# Insert point is right after START_MARKER
insert_at = start_idx + len(START_MARKER)

end_idx = html.find(END_MARKER, insert_at)
if end_idx == -1:
    sys.exit("ERROR: Could not find blockquote end marker")

# Confirm we found the slider section
old_section = html[insert_at:end_idx]
if "ba-wrap" not in old_section:
    sys.exit(f"ERROR: Expected slider content between markers, got:\n{old_section[:200]}")

print(f"Found slider section: {old_section.count('ba-wrap')} existing sliders -> replacing with 5")

html = html[:insert_at] + NEW_SLIDERS + html[end_idx:]

# ── Step 3: encode images ───────────────────────────────────────────────────

for placeholder, local_path in IMAGES.items():
    if placeholder not in html:
        print(f"  WARNING: {placeholder} not found in HTML (may already be encoded)")
        continue
    print(f"  Encoding {local_path.name} ...")
    data_uri = encode_image(local_path)
    html = html.replace(placeholder, data_uri)
    print(f"    -> {len(data_uri) // 1024} KB")

# ── Step 4: write file ──────────────────────────────────────────────────────

print("Writing index.html …")
HTML_FILE.write_text(html, encoding="utf-8")
print("Done.")
