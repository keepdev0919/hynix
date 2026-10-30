#!/usr/bin/env python3
"""CSV를 요약(profile)하고 brief.json과 합쳐 한 장짜리 브리핑 화면을 만든다(build). 표준 라이브러리만 쓴다."""
import argparse
import csv
import json
import re
import statistics
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

OUT = Path(".brief")
RAW_ROWS = 300
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")
WEEKDAYS = "월화수목금토일"


def number(value):
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return None


def read(path):
    for encoding in ("utf-8-sig", "cp949"):
        try:
            with open(path, newline="", encoding=encoding) as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"{path}: 인코딩을 읽을 수 없습니다")


def column_profile(name, values):
    filled = [v for v in values if (v or "").strip() != ""]
    info = {"name": name, "missing": len(values) - len(filled), "unique": len(set(filled))}
    if not filled:
        info["type"] = "empty"
        return info
    numbers = [n for n in map(number, filled) if n is not None]
    if all(DATE.match(v) for v in filled):
        days = sorted({v[:10] for v in filled})
        info.update(type="date", min=days[0], max=days[-1], days=len(days), gaps=date_gaps(days))
    elif len(numbers) == len(filled):
        info.update(type="number", min=min(numbers), max=max(numbers), mean=round(statistics.mean(numbers), 2),
                    median=statistics.median(numbers), zeros=sum(n == 0 for n in numbers))
    else:
        info.update(type="text", top=Counter(filled).most_common(8))
    return info


def date_gaps(days):
    """주말 외에 비어 있는 날짜."""
    try:
        have = {date.fromisoformat(d) for d in days}
    except ValueError:
        return []
    gaps, day = [], min(have)
    while day < max(have):
        if day not in have and day.weekday() < 5:
            gaps.append(day.isoformat())
        day += timedelta(days=1)
    return gaps


def signals(rows, columns):
    found = []
    numeric = [c["name"] for c in columns if c["type"] == "number"]
    for c in columns:
        if c["missing"]:
            found.append({"kind": "missing", "column": c["name"], "detail": f"빈 칸 {c['missing']}줄"})
        if c.get("zeros"):
            found.append({"kind": "zeros", "column": c["name"], "detail": f"0인 줄 {c['zeros']}개. 진짜 0인지 기록 누락인지 확인 필요"})
        if c.get("gaps"):
            found.append({"kind": "date_gaps", "column": c["name"], "detail": f"평일인데 기록 없는 날 {len(c['gaps'])}일: {', '.join(c['gaps'][:8])}"})
        if c["type"] == "number" and c["max"] > 0:
            lo, hi = statistics.quantiles([number(r[c["name"]]) for r in rows if number(r[c["name"]]) is not None], n=4)[0::2]
            spread = hi - lo
            if spread and c["max"] > hi + 3 * spread:
                found.append({"kind": "outlier", "column": c["name"], "detail": f"다른 값보다 크게 튀는 값 있음 (최대 {c['max']})"})
    for a in numeric:
        for b in numeric:
            if a == b:
                continue
            pairs = [(number(r[a]), number(r[b])) for r in rows]
            pairs = [(x, y) for x, y in pairs if x is not None and y is not None]
            equal = sum(x == y for x, y in pairs)
            if pairs and all(x <= y for x, y in pairs) and equal >= max(3, len(pairs) * 0.02):
                found.append({"kind": "ceiling", "column": a, "other": b,
                              "detail": f"{a}이(가) {b}을(를) 넘지 않고 {equal}줄에서 같음. 넘친 수요가 기록되지 않았을 수 있음"})
    dup = len(rows) - len({tuple(r.items()) for r in rows})
    if dup:
        found.append({"kind": "duplicates", "column": "", "detail": f"완전히 같은 줄 {dup}개"})
    return found


def load_all(data_dir):
    files = sorted(Path(data_dir).rglob("*.csv"))
    if not files:
        raise SystemExit(f"{data_dir}에 CSV가 없습니다")
    return {str(p.relative_to(data_dir)): read(p) for p in files}


def profile(tables):
    result = {}
    for name, rows in tables.items():
        columns = [column_profile(c, [r.get(c) for r in rows]) for c in (rows[0] if rows else {})]
        result[name] = {"rows": len(rows), "columns": columns, "signals": signals(rows, columns), "sample": rows[:3]}
    return result


def key_of(row, spec):
    name, _, part = spec.partition(":")
    value = row.get(name, "")
    if not part:
        return value
    day = date.fromisoformat(value[:10])
    if part == "weekday":
        return f"{day.weekday()}{WEEKDAYS[day.weekday()]}"
    if part == "week":
        return (day - timedelta(days=day.weekday())).isoformat()
    if part == "month":
        return value[:7]
    raise ValueError(f"모르는 날짜 단위: {part}")


def compare(left, op, right):
    a, b = number(left), number(right)
    if a is None or b is None:
        a, b = str(left), str(right)
    return {">=": a >= b, "<=": a <= b, "==": a == b, "!=": a != b, ">": a > b, "<": a < b}[op]


def aggregate(rows, view):
    agg = view["agg"]
    if agg == "count":
        return len(rows)
    if agg == "rate":
        when = view["when"]
        hits = sum(compare(r.get(when["left"]), when["op"], r.get(when["right"], when["right"])) for r in rows)
        return round(hits / len(rows) * 100, 1) if rows else None
    values = [number(r.get(view["value"])) for r in rows]
    values = [v for v in values if v is not None]
    if not values:
        return None
    if agg == "sum":
        return round(sum(values), 1)
    if agg == "mean":
        return round(statistics.mean(values), 1)
    if agg == "ratio":
        under = sum(n for n in (number(r.get(view["over"])) for r in rows) if n is not None)
        return round(sum(values) / under * 100, 1) if under else None
    raise ValueError(f"모르는 agg: {agg}")


def compute(view, tables):
    rows = tables[view["file"]]
    for column, wanted in (view.get("filter") or {}).items():
        rows = [r for r in rows if r.get(column) == str(wanted)]
    keys = view["group_by"]
    groups = defaultdict(list)
    for r in rows:
        groups[tuple(key_of(r, k) for k in keys)].append(r)
    points = [{"x": k[0], "series": k[1] if len(k) > 1 else "", "y": aggregate(g, view), "n": len(g)}
              for k, g in sorted(groups.items())]
    for p in points:
        p["x"] = re.sub(r"^\d(?=[월화수목금토일]$)", "", p["x"])
    unit = "%" if view["agg"] in ("rate", "ratio") else ""
    return {**view, "points": points, "unit": unit, "rows_used": len(rows)}


def build(data_dir):
    tables = load_all(data_dir)
    prof = profile(tables)
    brief_path = OUT / "brief.json"
    if not brief_path.exists():
        raise SystemExit(".brief/brief.json을 먼저 쓰세요")
    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    views, errors = [], []
    for view in brief.get("views", []):
        try:
            views.append(compute(view, tables))
        except (KeyError, ValueError) as e:
            errors.append(f"{view.get('title')}: {e!r}")
    payload = {"brief": {**brief, "views": views}, "profile": prof, "errors": errors,
               "raw": {n: r[:RAW_ROWS] for n, r in tables.items()}}
    template = (Path(__file__).parent / "viewer.html").read_text(encoding="utf-8")
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    (OUT / "index.html").write_text(template.replace("__DATA__", data), encoding="utf-8")
    print(f"만듦: .brief/index.html (차트 {len(views)}개)")
    for e in errors:
        print("차트 오류:", e)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["profile", "build"])
    parser.add_argument("--data", default="data")
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    if args.command == "profile":
        prof = profile(load_all(args.data))
        (OUT / "profile.json").write_text(json.dumps(prof, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"만듦: .brief/profile.json (파일 {len(prof)}개)")
        for name, p in prof.items():
            print(f"- {name}: {p['rows']}줄, 신호 {len(p['signals'])}개")
    else:
        build(args.data)


if __name__ == "__main__":
    main()
