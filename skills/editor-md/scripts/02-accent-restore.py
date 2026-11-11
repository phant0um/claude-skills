#!/usr/bin/env python3
"""editor-md step 2: domain-specific Portuguese accent restoration."""
import os, re, sys, json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DICT_PATH = SCRIPT_DIR.parent / 'references' / 'accent-dict.json'


def load_dict(domain: str) -> list[tuple]:
    with open(DICT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    entries = data.get('geral', [])
    if domain != 'geral':
        entries += data.get(domain, [])
    if domain == 'auto':
        for d in ('juridico', 'contabil'):
            entries += data.get(d, [])
    # deduplicate
    seen = set()
    result = []
    for broken, fixed in entries:
        if broken not in seen:
            seen.add(broken)
            result.append((broken, fixed))
    return result


def restore_file(path: str, fixes: list) -> bool:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    fm_end = 0
    if content.startswith('---'):
        idx = content.find('---', 3)
        if idx > 0:
            fm_end = idx + 3
    fm, body = content[:fm_end], content[fm_end:]
    orig = body
    for broken, fixed in fixes:
        body = body.replace(broken, fixed)
    # Fix execução + letter (over-correction: "execuçãodessas" → "execução dessas")
    body = re.sub(r'execução([a-zA-ZÀ-ÿ])', lambda m: 'execução ' + m.group(1), body)
    body = body.replace('instituiçãoções', 'instituições')
    body = body.replace('Instituiçãoções', 'Instituições')
    if body != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fm + body)
        return True
    return False


def process(target: str, domain: str = 'auto'):
    fixes = load_dict(domain)
    paths = []
    if os.path.isfile(target):
        paths = [target]
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for f in files:
                if f.endswith('.md'):
                    paths.append(os.path.join(root, f))
    changed = sum(1 for p in paths if restore_file(p, fixes))
    print(f"Step 2 done [{domain}]: {changed}/{len(paths)} files modified")


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    domain = 'auto'
    for arg in sys.argv[2:]:
        if arg.startswith('--domain='):
            domain = arg.split('=')[1]
        elif arg in ('juridico', 'contabil', 'geral', 'auto'):
            domain = arg
    process(target, domain)
