#!/usr/bin/env python3
"""editor-md step 1: deterministic artifact removal from PDF→MD conversions."""
import os, re, sys

PATTERNS = [
    # Watermarks / student info
    re.compile(r'PDF exclusivo para[^\n]*\n?'),
    re.compile(r'\d{11} - \w[^\n]*\n?'),           # CPF - Nome
    re.compile(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}[^\n]*\n?'),  # email lines
    re.compile(r'rm\d{6,}[^\n]*\n?', re.IGNORECASE),  # RM number
    # Platform URLs (estrategiaconcursos, etc.)
    re.compile(r'[^\n]*estrategiaconcursos\.com\.br[^\n]*\n?'),
    re.compile(r'[^\n]*www\.estrategia[^\n]*\n?'),
    re.compile(r'[^\n]*app\.estrategia[^\n]*\n?'),
    # Picture placeholders
    re.compile(r'==> picture \[\d+ x \d+\][^\n]*\n?'),
    re.compile(r'-{3,} Start of picture text -{3,}\n?'),
    re.compile(r'-{3,} End of picture text -{3,}\n?'),
    # TOC dot lines
    re.compile(r'^[^\n]*\.{5,}\s*\d+[^\n]*$', re.MULTILINE),
    # Page numbers (isolated on their own line)
    re.compile(r'^\s*\d{1,4}\s+\d{1,4}\s*$', re.MULTILINE),  # "16 167"
    re.compile(r'^\s*\d{1,4}\s*$', re.MULTILINE),
    # Author + Aula header lines
    re.compile(r'^[ \t]*[-*•]?[ \t]*\*?\*?[\w À-úÀ-ÿ,\.]+Aula \d+[ \t]*\*?\*?[ \t]*$', re.MULTILINE),
    re.compile(r'^[ \t]*\*+[ \t]*[\w À-úÀ-ÿ,\.]+Aula \d+[^\n]*$', re.MULTILINE),
    re.compile(r'^[ \t]*[-*][ \t]+\*\d+[ \t]*$', re.MULTILINE),  # "- *1"
    # Social media promo
    re.compile(r'^[^\n]*(?:Instagram|YouTube|Telegram|Canal no|TELEGRAM|inscreva)[^\n]*$', re.MULTILINE | re.IGNORECASE),
    re.compile(r'^[^\n]*(?:Ol[aá][aá]|grande abra[çc]o|prazer contar|nossos canais|tirar D[úu]vidas)[^\n]*$', re.MULTILINE | re.IGNORECASE),
    re.compile(r'^[^\n]*amigos do Estrat[eé]gia[^\n]*$', re.MULTILINE | re.IGNORECASE),
    # Garbled table rows (TOC artifacts)
    re.compile(r'^\|[\s]*\)[ \t]+[^\|]+\|\d+\|[ \t]*$', re.MULTILINE),
    re.compile(r'^\|[ \t]*\n\|[ \t]*\)[^\|]+\|\d+\|[ \t]*$', re.MULTILINE),
    re.compile(r'^\|[ \t]*$', re.MULTILINE),
    # Base64
    re.compile(r'data:[a-z]+/[a-z+\-]+;base64,[A-Za-z0-9+/=\n]{20,}'),
    # HTML remnants
    re.compile(r'<br\s*/?>', re.IGNORECASE),
    re.compile(r'<style[^>]*>.*?</style>', re.DOTALL | re.IGNORECASE),
    re.compile(r'<svg[^>]*>.*?</svg>', re.DOTALL | re.IGNORECASE),
    re.compile(r'<img[^>]*/?>', re.IGNORECASE),
    re.compile(r'<[a-z][^>]{0,60}>', re.IGNORECASE),
    # Empty bold markers
    re.compile(r'^\*\*\s*\*\*$', re.MULTILINE),
    # CGE-AM repeated course title
    re.compile(r'^\*\*CGE-AM \([^)]+\)[^\n]*\*\*\s*$', re.MULTILINE),
    # Blank line runs (last — always run)
    re.compile(r'\n{4,}'),
]

def clean_file(path: str) -> bool:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Preserve frontmatter
    fm_end = 0
    if content.startswith('---'):
        idx = content.find('---', 3)
        if idx > 0:
            fm_end = idx + 3
    fm, body = content[:fm_end], content[fm_end:]
    orig = body

    for pat in PATTERNS:
        if pat.pattern == r'\n{4,}':
            body = pat.sub('\n\n\n', body)
        else:
            body = pat.sub('', body)

    if body != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fm + body)
        return True
    return False


def process(target: str):
    paths = []
    if os.path.isfile(target):
        paths = [target]
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for f in files:
                if f.endswith('.md'):
                    paths.append(os.path.join(root, f))

    changed = sum(1 for p in paths if clean_file(p))
    print(f"Step 1 done: {changed}/{len(paths)} files modified")


if __name__ == '__main__':
    process(sys.argv[1] if len(sys.argv) > 1 else '.')
