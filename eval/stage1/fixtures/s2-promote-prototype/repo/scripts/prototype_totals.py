# quick prototype: route stats from access-log CSV. works. messy on purpose.
import csv, sys

def main(text):
    seen = set(); out = {}; skipped = 0
    for row in csv.reader(text.splitlines()):
        if len(row) != 3: skipped += 1; continue
        route, status, ms = row
        try: ms = float(ms)
        except ValueError: skipped += 1; continue
        key = (route, status, ms)
        if key in seen: skipped += 1; continue   # dup line: keep first
        seen.add(key)
        c, t = out.get(route, (0, 0.0)); out[route] = (c + 1, t + ms)
    lines = ["route,count,total_ms"]
    for r in sorted(out):
        c, t = out[r]; lines.append(f"{r},{c},{t:g}")
    return "\n".join(lines) + "\n", skipped

if __name__ == "__main__":
    out, skipped = main(open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read())
    sys.stderr.write(f"skipped {skipped}\n")
    sys.stdout.write(out)
