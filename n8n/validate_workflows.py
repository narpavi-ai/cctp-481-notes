#!/usr/bin/env python3
"""Structural check on the generated n8n workflows.

This does NOT prove a workflow imports - only a live n8n instance can do that,
and node schemas change between releases. What it does catch is the class of
mistake that is easy to make by hand and invisible until class: a connection
pointing at a node that does not exist, a sub-node wired with the wrong
connection type, an agent with no model, a duplicate node name.

    python3 n8n/validate_workflows.py
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = "@n8n/n8n-nodes-langchain"

# Which connection type each sub-node must use to reach its root node.
SUBNODE_CONNECTION = {
    f"{PKG}.lmChatGoogleGemini": "ai_languageModel",
    f"{PKG}.memoryBufferWindow": "ai_memory",
    f"{PKG}.toolCode": "ai_tool",
    f"{PKG}.chatHitlTool": "ai_tool",   # human approval gate
    "n8n-nodes-base.httpRequest": "ai_tool",   # usableAsTool - the Open-Meteo weather tool
    f"{PKG}.outputParserStructured": "ai_outputParser",
}
ROOT_NODES = {f"{PKG}.agent", f"{PKG}.chainLlm"}


def check(path):
    wf = json.load(open(path))
    errs, warns = [], []
    nodes = wf.get("nodes", [])
    by_name = {}
    for n in nodes:
        for key in ("name", "type", "typeVersion", "position", "parameters"):
            if key not in n:
                errs.append(f"node {n.get('name', '?')!r} missing {key!r}")
        if n["name"] in by_name:
            errs.append(f"duplicate node name {n['name']!r}")
        by_name[n["name"]] = n

    conns = wf.get("connections", {})
    for src, kinds in conns.items():
        if src not in by_name:
            errs.append(f"connection from unknown node {src!r}")
            continue
        for kind, branches in kinds.items():
            for branch in branches:
                for link in branch:
                    if link["node"] not in by_name:
                        errs.append(f"{src!r} -> unknown node {link['node']!r}")
                    if link.get("type") != kind:
                        errs.append(f"{src!r}: connection kind {kind!r} but link type {link.get('type')!r}")
            # a sub-node must use its own connection type
            expected = SUBNODE_CONNECTION.get(by_name[src]["type"])
            if expected and kind != expected:
                errs.append(f"{src!r} wired as {kind!r}, expected {expected!r}")

    # every root node needs a language model
    for n in nodes:
        if n["type"] in ROOT_NODES:
            fed = [s for s, k in conns.items() if "ai_languageModel" in k
                   and any(l["node"] == n["name"] for b in k["ai_languageModel"] for l in b)]
            if not fed:
                errs.append(f"{n['name']!r} has no ai_languageModel connected")

    # tools need a description - it is the prompt the model reads
    for n in nodes:
        if n["type"] == f"{PKG}.toolCode":
            if not n["parameters"].get("description", "").strip():
                errs.append(f"tool {n['name']!r} has an empty description")
            if not n["parameters"].get("jsCode", "").strip():
                errs.append(f"tool {n['name']!r} has no code")
        if n["type"] == "n8n-nodes-base.httpRequest":
            # wired as a tool, so it needs a toolDescription for the model to read
            if not n["parameters"].get("toolDescription", "").strip():
                errs.append(f"HTTP tool {n['name']!r} has an empty toolDescription")
            if not n["parameters"].get("url", "").strip():
                errs.append(f"HTTP tool {n['name']!r} has no url")

    if not any(n["type"].endswith(".stickyNote") for n in nodes):
        warns.append("no sticky note - students get no on-canvas explanation")
    return errs, warns


def main():
    files = sorted(glob.glob(os.path.join(HERE, "*.json")))
    if not files:
        sys.exit("no workflow JSON found - run build_workflows.py first")
    total = 0
    for path in files:
        errs, warns = check(path)
        total += len(errs)
        name = os.path.basename(path)
        status = "FAIL" if errs else "ok  "
        print(f"{status} {name}")
        for e in errs:
            print(f"       ERROR {e}")
        for w in warns:
            print(f"       warn  {w}")
    print(f"\n{len(files)} workflow(s), {total} error(s).")
    print("Structure only - import each one into a real n8n instance before class.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
