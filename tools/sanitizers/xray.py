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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config", nargs="?", default="-",
                    help="config file path, or '-' / omitted for stdin")
    ap.add_argument("-d", "--domain", action="append", default=[],
                    help="own domain to replace with example.com (repeatable)")
    ap.add_argument("-k", "--key", action="append", default=[],
                    help="extra key whose value to redact (repeatable), e.g. -k path")
    args = ap.parse_args()

    if args.config == "-":
        text = sys.stdin.read()
    else:
        with open(args.config, encoding="utf-8") as f:
            text = f.read()
    print(sanitize(text, args.domain, args.key), end="")


if __name__ == "__main__":
    main()