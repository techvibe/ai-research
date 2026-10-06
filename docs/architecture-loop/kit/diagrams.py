#!/usr/bin/env python3
"""Generate notation-independent C4 SVG views and editable Mermaid sources."""
from __future__ import annotations
import argparse
import html
import json
import math
import re
import textwrap
from pathlib import Path
from gates import file_hash, ArtifactStore

COLORS = {"person": "#596574", "external": "#596574", "system": "#173B59",
          "container": "#25638C", "component": "#087F82", "code": "#655395"}


def escape(s):
    return html.escape(str(s), quote=True)


def mermaid_label(s):
    return str(s).replace('"', "'").replace("\n", " ").replace("[", "(").replace("]", ")")


def render_view(a, view, model_hash):
    elements = {x["id"]: x for x in a["elements"]}
    relationships = {x["id"]: x for x in a["relationships"]}
    for i in view["nodes"]:
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", i):
            raise ValueError("Element IDs must be Mermaid-safe identifiers: " + i)
    width, height = view.get("size", [1200, 850])
    positions = view.get("positions", {})
    nodes = {}
    for i, node in enumerate(view["nodes"]):
        nodes[node] = positions.get(node, [70 + (i % 3) * 380, 180 + (i // 3) * 245, 300, 145])
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" data-model-sha256="{model_hash}">',
             '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9" fill="#60758B"/></marker></defs>',
             f'<rect width="{width}" height="{height}" fill="#FFFFFF"/>',
             f'<text x="40" y="44" font-family="DejaVu Sans,Arial" font-size="26" font-weight="bold" fill="#12324A">{escape(view["title"])}</text>',
             f'<text x="40" y="78" font-family="DejaVu Sans,Arial" font-size="17" fill="#52677A">Scope: {escape(elements[view["scope"]]["name"])} · {escape(view["scope"])}</text>']
    internal = [nodes[n] for n in view["nodes"] if elements[n].get("parent") == view["scope"]]
    if internal:
        x0 = min(n[0] for n in internal) - 22
        y0 = min(n[1] for n in internal) - 38
        x1 = max(n[0] + n[2] for n in internal) + 22
        y1 = max(n[1] + n[3] for n in internal) + 22
        parts += [f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="14" fill="#F4F8FA" stroke="#849AAF" stroke-dasharray="7,5"/>',
                  f'<text x="{x0+14}" y="{y0+23}" font-family="DejaVu Sans,Arial" font-size="15" fill="#536C80">Boundary: {escape(elements[view["scope"]]["name"])}</text>']
    edges = []
    labels = []
    for rid in view.get("edges", []):
        rel = relationships[rid]
        x, y, w, h = nodes[rel["source"]]
        tx, ty, tw, th = nodes[rel["target"]]
        cx, cy, dx, dy = x+w/2, y+h/2, tx+tw/2-(x+w/2), ty+th/2-(y+h/2)
        norm = max(abs(dx)/(w/2), abs(dy)/(h/2), 0.01)
        tnorm = max(abs(dx)/(tw/2), abs(dy)/(th/2), 0.01)
        start = (cx+dx/norm, cy+dy/norm)
        end = (tx+tw/2-dx/tnorm, ty+th/2-dy/tnorm)
        route = view.get("routes", {}).get(rid)
        points = route if route else [start, end]
        point_string = " ".join(f"{p[0]},{p[1]}" for p in points)
        edges.append(f'<polyline points="{point_string}" fill="none" stroke="#60758B" stroke-width="2" marker-end="url(#arrow)"/>')
        lx, ly = view.get("label_positions", {}).get(rid, [(start[0]+end[0])/2, (start[1]+end[1])/2-10])
        label = rel["label"] + (" · " + rel["protocol"] if view["level"] in (2, 3) else "")
        lines = textwrap.wrap(label, 31)
        bw = min(290, max(len(t) for t in lines)*8+18)
        labels.append(f'<rect x="{lx-bw/2}" y="{ly-15}" width="{bw}" height="{len(lines)*18+8}" rx="4" fill="#FFFFFF" fill-opacity="0.97"/>')
        for j, line in enumerate(lines):
            labels.append(f'<text x="{lx}" y="{ly+j*18}" text-anchor="middle" font-family="DejaVu Sans,Arial" font-size="14" fill="#344F63">{escape(line)}</text>')
    parts += edges
    for node, (x, y, w, h) in nodes.items():
        el = elements[node]
        color = COLORS.get(el["type"], "#596574")
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{color}"/>')
        parts.append(f'<text x="{x+16}" y="{y+25}" font-family="DejaVu Sans,Arial" font-size="16" fill="#DFEDF7">{escape(el["type"].upper())} · {escape(node)}</text>')
        yy = y+51
        for line in textwrap.wrap(el["name"], max(16, int((w-30)/12))):
            parts.append(f'<text x="{x+16}" y="{yy}" font-family="DejaVu Sans,Arial" font-size="24" font-weight="bold" fill="#FFFFFF">{escape(line)}</text>'); yy += 25
        detail = el.get("code_ref") if el["type"] == "code" else el["description"]
        for line in textwrap.wrap(detail, max(18, int((w-30)/12))):
            parts.append(f'<text x="{x+16}" y="{yy+2}" font-family="DejaVu Sans,Arial" font-size="20" fill="#FFFFFF">{escape(line)}</text>'); yy += 24
        extra = " / ".join(el.get("members", [])) if el["type"] == "code" else el.get("technology", "")
        for line in textwrap.wrap(extra, max(20, int((w-30)/9))):
            parts.append(f'<text x="{x+16}" y="{yy+4}" font-family="DejaVu Sans,Arial" font-size="16" fill="#DFEDF7">{escape(line)}</text>'); yy += 20
        if el["status"] == "proposed":
            parts.append(f'<text x="{x+w-15}" y="{y+24}" text-anchor="end" font-family="DejaVu Sans,Arial" font-size="12" fill="#FFF3C6">PROPOSED</text>')
    parts += labels
    for i, line in enumerate(textwrap.wrap(view["legend"], 135)):
        parts.append(f'<text x="40" y="{height-72+i*20}" font-family="DejaVu Sans,Arial" font-size="14" fill="#52677A">{escape(line)}</text>')
    parts.append('</svg>')
    m = [f"%% model-sha256: {model_hash}", "%% " + view["title"], "%% Scope: " + view["scope"], "%% " + view["legend"]]
    if view["level"] == 4:
        m.append("classDiagram")
        m.append("direction TB")
        for node in view["nodes"]:
            el = elements[node]
            m.append(f'  class {node}["{mermaid_label(el["name"])}"] {{')
            for member in el.get("members", []):
                m.append("    +" + member)
            m.append("  }")
            m.append(f'  note for {node} "{mermaid_label(el["code_ref"])}; {el["status"]}"')
        for rid in view.get("edges", []):
            rel = relationships[rid]
            m.append(f'  {rel["source"]} ..> {rel["target"]} : {mermaid_label(rel["label"])}')
    else:
        m.append("flowchart TB")
        inside = [n for n in view["nodes"] if elements[n].get("parent") == view["scope"]]
        def node_line(node):
            el = elements[node]
            tech = ("; " + el["technology"]) if el.get("technology") else ""
            return f'    {node}["{mermaid_label(el["name"])} ({el["type"]}{tech}) - {mermaid_label(el["description"])}"]'
        if inside:
            m.append(f'  subgraph scope_{view["scope"]}["{mermaid_label(elements[view["scope"]]["name"])}"]')
            m += [node_line(n) for n in inside]
            m.append("  end")
        m += [node_line(n) for n in view["nodes"] if n not in inside]
        for rid in view.get("edges", []):
            rel = relationships[rid]
            protocol = " / " + rel["protocol"] if view["level"] > 1 else ""
            m.append(f'  {rel["source"]} -->|"{mermaid_label(rel["label"]+protocol)}"| {rel["target"]}')
    return "\n".join(parts), "\n".join(m) + "\n"


def generate(root):
    store = ArtifactStore(root)
    a = store.read("architecture.json")
    digest = file_hash(store.path("architecture.json"))
    store.path("diagrams").mkdir(exist_ok=True)
    for view in a["views"]:
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", view["id"]):
            raise ValueError("View ID must be a safe filename")
        svg, mermaid = render_view(a, view, digest)
        store.path("diagrams/" + view["id"] + ".svg").write_text(svg, encoding="utf-8")
        store.path("diagrams/" + view["id"] + ".mmd").write_text(mermaid, encoding="utf-8")
    print(f"Generated {len(a['views'])} views as SVG and Mermaid")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run")
    generate(Path(parser.parse_args().run).resolve())
