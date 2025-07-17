#!/usr/bin/env python3
import csv, datetime, pathlib, textwrap

CSV      = pathlib.Path("data/reviews.csv")
TEMPLATE = pathlib.Path("templates/review.md").read_text()
DATE     = datetime.date.today().isoformat()

with CSV.open(newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        md = TEMPLATE
        md = md.replace("{{ .title }}", row["title"].strip())
        md = md.replace("{{ .asin }}",  row["asin"].strip())
        md = md.replace("{{ .img }}",   row["img"].strip())
        md = md.replace("{{ .blurb }}", textwrap.fill(row["blurb"].strip(), 80))
        md = md.replace("{{ .date }}",  DATE)

        slug = (
            row["title"]
            .lower()
            .replace(" ", "-")
            .replace("’", "")
            .replace("'", "")
        )
        out = pathlib.Path(f"content/reviews/{slug}.md")
        if not out.exists():
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(md)
            print("NEW →", out)
