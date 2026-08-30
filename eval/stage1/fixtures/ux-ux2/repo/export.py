#!/usr/bin/env python3
"""Weekly export: scores.json -> export.csv (downstream jobs read it)."""
import csv, json, sys

def main():
    scores = json.load(open("scores.json"))
    with open("export.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["user", "score"])
        for user, info in sorted(scores.items()):
            w.writerow([user, info["score"]])
    print("exported")

if __name__ == "__main__":
    main()
