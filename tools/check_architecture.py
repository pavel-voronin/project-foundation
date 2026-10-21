#!/usr/bin/env python3
"""Check declared module boundaries and local documentation links; no game/GPU needed."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors: list[str] = []
    catalog = json.loads((ROOT / 'architecture/modules.json').read_text(encoding='utf-8'))
    modules = catalog['modules']
    names = {m['name'] for m in modules}
    by_name = {m['name']: m for m in modules}
    if len(names) != len(modules):
        errors.append('Duplicate module names')
    if len({m['path'] for m in modules}) != len(modules):
        errors.append('Duplicate module paths')
    if len({m['package'] for m in modules}) != len(modules):
        errors.append('Duplicate module packages')

    portable = {'foundation-api', 'foundation-runtime', 'graphics-api',
                'graphics-runtime', 'presentation', 'platform-api'}
    integrations = {'adapter-pz', 'graphics-vulkan', 'graphics-vulkan-interop',
                    'platform-glfw'}
    for module in modules:
        name = module['name']
        base = (ROOT / module['path']).resolve()
        if not base.is_relative_to(ROOT):
            errors.append(f'{name}: module path leaves repository')
            continue
        deps = set(module['dependencies'])
        if len(deps) != len(module['dependencies']):
            errors.append(f'{name}: duplicate dependency')
        if deps - names:
            errors.append(f'{name}: unknown dependencies {sorted(deps - names)}')
        if name in portable and deps - portable:
            errors.append(f'{name}: portable module depends on integration/composition')
        if name in integrations and deps - portable:
            errors.append(f'{name}: integration depends on another integration/composition')
        for required in ['README.md', 'build.gradle',
                         'src/main/java/' + module['package'].replace('.', '/') + '/package-info.java']:
            if not (base / required).is_file():
                errors.append(f'{name}: missing {required}')
        for source in base.glob('src/**/*.java'):
            code = source.read_text(encoding='utf-8')
            code = re.sub(r'/\*.*?\*/|//[^\n]*', '', code, flags=re.S)
            allowed_native = {
                'zombie': {'adapter-pz'},
                'org.lwjgl.vulkan': {'graphics-vulkan', 'graphics-vulkan-interop'},
                'org.lwjgl.glfw': {'platform-glfw'},
                'org.lwjgl.opengl': {'adapter-pz'},
                'org.lwjglx': {'adapter-pz'},
            }
            for namespace, owners in allowed_native.items():
                if re.search(r'\b' + re.escape(namespace) + r'\.', code) and name not in owners:
                    errors.append(f'{source.relative_to(ROOT)}: forbidden namespace {namespace}')
            for imported in re.findall(r'\bimport\s+(?:static\s+)?([\w.*]+)\s*;', code):
                owner = next((m['name'] for m in sorted(modules, key=lambda item: -len(item['package']))
                              if imported.startswith(m['package'] + '.')), None)
                if owner and owner != name and owner not in deps:
                    errors.append(f'{name}: undeclared import from {owner}')

    visited: set[str] = set()
    active: set[str] = set()

    def visit(name: str) -> None:
        if name in active:
            errors.append(f'Dependency cycle through {name}')
            return
        if name in visited or name not in by_name:
            return
        active.add(name)
        for dependency in by_name[name]['dependencies']:
            visit(dependency)
        active.remove(name)
        visited.add(name)

    for name in names:
        visit(name)

    markdown = [p for p in ROOT.rglob('*.md')
                if not {'.git', '.gradle', 'build'}.intersection(p.relative_to(ROOT).parts)]
    for document in markdown:
        text = document.read_text(encoding='utf-8')
        for link in re.findall(r'\]\(([^\s)]+)\)', text):
            parsed = urlsplit(link.strip('<>'))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (document.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(ROOT):
                errors.append(f'{document.relative_to(ROOT)}: link leaves repository: {link}')
            elif not target.exists():
                errors.append(f'{document.relative_to(ROOT)}: broken local link: {link}')

    if errors:
        for error in errors:
            print(f'ERROR: {error}', file=sys.stderr)
        return 1
    print(f'Architecture OK: {len(modules)} modules; dependency graph, source boundaries '
          f'and links in {len(markdown)} Markdown files checked.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
