# quick+dirty: working days per month. works. messy on purpose.
import calendar, sys

def run(year, holiday_lines):
    holidays = set()
    skipped = 0
    for ln in holiday_lines:
        ln = ln.strip()
        if not ln:
            continue
        try:
            m, d = map(int, ln.split("-"))
            if not (1 <= m <= 12 and 1 <= d <= 31):
                raise ValueError
            if calendar.weekday(year, m, d) >= 5:
                continue          # weekend holiday: no effect, consumed
            holidays.add((m, d))
        except ValueError:
            skipped += 1
            continue
    rows = ["month,workdays"]
    for month in range(1, 13):
        days = calendar.monthrange(year, month)[1]
        wd = sum(1 for d in range(1, days + 1)
                 if calendar.weekday(year, month, d) < 5
                 and (month, d) not in holidays)
        rows.append(f"{month},{wd}")
    return "\n".join(rows) + "\n", skipped

if __name__ == "__main__":
    out, skipped = run(int(sys.argv[1]), open(sys.argv[2]).read().splitlines()
                       if len(sys.argv) > 2 else [])
    sys.stderr.write(f"skipped {skipped}\n")
    sys.stdout.write(out)
