#!/usr/bin/env python3
"""Redact secrets in an Xray config by plain text replacement, for sharing it safely."""
import argparse
import re
import sys

KEYS = ["id", "password", "auth", "email", "privateKey", "publicKey", "shortId", "pinSHA256", "address"]


def redact_strings(s):
    """Replace every non-empty "string" in s with "REDACTED"; keep "" as is."""
    return re.sub(r'"[^"]*"', lambda q: q[0] if q[0] == '""' else '"REDACTED"', s)


def sanitize(text, domains=(), extra_keys=()):
    keys = "|".join(map(re.escape, KEYS + list(extra_keys)))
    text = re.sub(rf'("(?:{keys})"\s*:\s*)("[^"]*")', lambda m: m[1] + redact_strings(m[2]), text)
    text = re.sub(r'("shortIds"\s*:\s*\[)([^\]]*)', lambda m: m[1] + redact_strings(m[2]), text)
    for d in domains:
        text = text.replace(d, "example.com")
    return text


def read_pasted():
    """Read pasted JSON line by line; stop once the top-level {...} / [...] closes."""
    lines, depth, started, in_str, esc = [], 0, False, False, False
    for line in sys.stdin:
        lines.append(line)
        for c in line:
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            elif c == '"':
                in_str = True
            elif c in "{[":
                depth, started = depth + 1, True
            elif c in "}]":
                depth -= 1
        if started and depth <= 0:
            break
    return "".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("-f", "--file", metavar="PATH", help="read the config from a file")
    src.add_argument("-s", "--stdin", action="store_true",
                     help="read the config from stdin (prompts you to paste if interactive)")
    ap.add_argument("-d", "--domain", action="append", default=[],
                    help="own domain to replace with example.com (repeatable)")
    ap.add_argument("-k", "--key", action="append", default=[],
                    help="extra key whose value to redact (repeatable), e.g. -k path")
    args = ap.parse_args()

    if args.stdin and sys.stdin.isatty():  # interactive: prompt, finish automatically
        print("Paste your config; it finishes by itself once the JSON is complete.", file=sys.stderr)
        text = read_pasted()
        print("-" * 40, file=sys.stderr)
    elif args.stdin:  # piped input: read everything silently
        text = sys.stdin.read()
    else:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    out = sanitize(text, args.domain, args.key)
    print(out, end="" if out.endswith("\n") else "\n")


if __name__ == "__main__":
    main()