#!/usr/bin/env python3
"""editor-md step 5: verify known broken patterns are gone."""
import os, re, sys

CHECKS = [
    (re.compile(r'[ÍI]{2}[nN]dice'), 'doubled Índice char'),
    (re.compile(r'\bSumri[oa]\b'), 'Sumário broken'),
    (re.compile(r'\bCaptul[ao]\b', re.IGNORECASE), 'Capítulo broken'),
    (re.compile(r'\bTtul[ao]s?\b', re.IGNORECASE), 'Título broken'),
    (re.compile(r'\bOBRIGATRI[AO]\b'), 'OBRIGATÓRIA broken'),
    (re.compile(r'\bobrigatri[ao]\b'), 'obrigatório broken'),
    (re.compile(r'^\s*\d{1,3}\s*$', re.MULTILINE), 'isolated page number'),
    (re.compile(r'estrategiaconcursos\.com\.br'), 'platform URL remaining'),
    (re.compile(r'PDF exclusivo para'), 'watermark remaining'),
    (re.compile(r'==> picture'), 'picture placeholder remaining'),
    (re.compile(r'\n{4,}'), 'excessive blank lines (>3)'),
]

def verify_file(path: str) -> list:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    # Skip frontmatter
    fm_end = 0
    if content.startswith('---'):
        idx = content.find('---', 3)
        if idx > 0:
            fm_end = idx + 3
    body = content[fm_end:]
    issues = []
    for pat, label in CHECKS:
        for m in pat.finditer(body):
            line_num = body[:m.start()].count('\n') + 1
            snippet = m.group()[:40].replace('\n', '↵')
            issues.append((line_num, label, snippet))
    return issues


def process(target: str) -> int:
    paths = []
    if os.path.isfile(target):
        paths = [target]
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for f in files:
                if f.endswith('.md'):
                    paths.append(os.path.join(root, f))

    total_issues = 0
    for path in sorted(paths):
        issues = verify_file(path)
        if issues:
            print(f"\n{path}: {len(issues)} issues")
            for line, label, snippet in issues[:5]:
                print(f"  line {line}: [{label}] {repr(snippet)}")
            if len(issues) > 5:
                print(f"  ... +{len(issues)-5} more")
            total_issues += len(issues)

    print(f"\n{'CLEAN' if total_issues == 0 else 'ISSUES FOUND'}: {total_issues} total across {len(paths)} files")
    return total_issues


if __name__ == '__main__':
    sys.exit(process(sys.argv[1] if len(sys.argv) > 1 else '.'))
