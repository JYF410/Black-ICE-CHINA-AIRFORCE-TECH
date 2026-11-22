# -*- coding: utf-8 -*-
"""Minimal Clausewitz script parser for HOI4 mod auditing.

Handles: key = value, key = { ... }, @var definitions, quoted strings,
comments, and repeated keys (collected into lists).
"""
import re
import os


class Node(dict):
    """dict subclass that keeps repeated keys as list values."""

    def add(self, k, v):
        if k in self:
            cur = self[k]
            if isinstance(cur, list) and getattr(self, "_multikey", None) and k in self._multikey:
                cur.append(v)
            else:
                self[k] = [cur, v]
                if not hasattr(self, "_multikey") or self._multikey is None:
                    self._multikey = set()
                self._multikey.add(k)
        else:
            self[k] = v


TOKEN_RE = re.compile(
    r"""
    (?P<ws>\s+)
  | (?P<comment>\#[^\n]*)
  | (?P<string>"(?:[^"\\]|\\.)*")
  | (?P<lbrace>\{)
  | (?P<rbrace>\})
  | (?P<eq>=)
  | (?P<scalar>[^\s{}=#"]+)
""",
    re.VERBOSE,
)


def tokenize(text):
    pos = 0
    n = len(text)
    out = []
    while pos < n:
        m = TOKEN_RE.match(text, pos)
        if not m:
            pos += 1
            continue
        pos = m.end()
        kind = m.lastgroup
        if kind in ("ws", "comment"):
            continue
        val = m.group()
        if kind == "string":
            out.append(("scalar", val[1:-1]))
        elif kind == "lbrace":
            out.append(("{", "{"))
        elif kind == "rbrace":
            out.append(("}", "}"))
        elif kind == "eq":
            out.append(("=", "="))
        else:
            out.append(("scalar", val))
    return out


class Parser:
    def __init__(self, tokens):
        self.t = tokens
        self.i = 0

    def parse_block(self, stop_at_rbrace=False):
        node = Node()
        while self.i < len(self.t):
            kind, val = self.t[self.i]
            if kind == "}":
                self.i += 1
                return node
            if kind == "scalar":
                key = val
                self.i += 1
                if self.i >= len(self.t):
                    break
                k2, v2 = self.t[self.i]
                if k2 != "=":
                    # bare token inside an inline list
                    node.setdefault("_items", [])
                    if isinstance(node["_items"], list):
                        node["_items"].append(key)
                    continue
                if k2 == "=":
                    self.i += 1
                    if self.i >= len(self.t):
                        break
                    k3, v3 = self.t[self.i]
                    if k3 == "{":
                        self.i += 1
                        sub = self.parse_block(True)
                        node.add(key, sub)
                    elif k3 == "scalar":
                        self.i += 1
                        node.add(key, v3)
                    elif k3 == "}":
                        # empty value
                        node.add(key, "")
                    else:
                        self.i += 1
                else:
                    # bare token (e.g. inside inline list) -> ignore
                    continue
            else:
                self.i += 1
        return node


def parse_text(text):
    toks = tokenize(text)
    p = Parser(toks)
    return p.parse_block()


def parse_file(path):
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        return parse_text(f.read())


def as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def scalars(v):
    """Return list of scalar strings from a value that may be a list of strings
    or an inline list (parsed as Node holding `_items`)."""
    if v is None:
        return []
    if isinstance(v, Node):
        return [x for x in v.get("_items", []) if isinstance(x, str)]
    if isinstance(v, list):
        out = []
        for x in v:
            if isinstance(x, str):
                out.append(x)
            elif isinstance(x, Node):
                out.extend(y for y in x.get("_items", []) if isinstance(y, str))
        return out
    if isinstance(v, str):
        return [v]
    return []


def inline_list(text):
    """Parse `{ a b c }` style content (no '=' inside) into string list."""
    return [s for s in re.split(r"\s+", text.strip()) if s]


# --- helpers for resolving @variables -------------------------------------

def collect_vars(tree):
    """Collect top-level @NAME = number definitions (any depth)."""
    out = {}

    def walk(node):
        if isinstance(node, Node):
            for k, v in node.items():
                if isinstance(k, str) and k.startswith("@"):
                    try:
                        out[k] = float(v)
                    except (TypeError, ValueError):
                        pass
                elif isinstance(v, Node):
                    walk(v)
                elif isinstance(v, list):
                    for x in v:
                        if isinstance(x, Node):
                            walk(x)
    walk(tree)
    return out


def resolve(v, vars_):
    if isinstance(v, str):
        s = v.strip()
        if s.startswith("@"):
            return vars_.get(s)
        try:
            return float(s)
        except ValueError:
            return s
    return v


def iter_named(node, name):
    """Yield sub-nodes stored under `name` (handles repeated key lists)."""
    if not isinstance(node, Node):
        return
    v = node.get(name)
    if v is None:
        return
    for item in as_list(v):
        if isinstance(item, Node):
            yield item


def load_dir(path, pattern="*.txt"):
    import glob
    return sorted(glob.glob(os.path.join(path, pattern)))
