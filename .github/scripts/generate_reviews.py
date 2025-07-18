#!/usr/bin/env python3
import csv, datetime, json, os, pathlib, textwrap
import openai
force = True        # rewrite even if file already exists
openai.api_key = os.environ["OPENAI_KEY"]

CSV      = pathlib.Path("data/reviews.csv")
DATE     = datetime.date.today().isoformat()
OUTDIR   = pathlib.Path("content/reviews")
TEMPLATE = """---
title: "{title}"
asin: "{asin}"
date: "{date}"
draft: false
description: "{blurb}"
images: ["{img}"]
cover:
  image: "{img}"
ai_filled: true
---

{summary}

## Why we liked it 👍
{pros}

## Why it might not work for you 👎
{cons}

## Full spoiler-free review
{review}

{{< amzlink asin="{asin}" title="{title}" img="{img}" >}}

{{< amzbtn asin="{asin}" label="Buy on Amazon" >}}
"""

def ai_review(title, blurb):
    prompt = (
        f'Title: "{title}"\n'
        f'Blurb: "{blurb}"\n\n'
        "Provide JSON with keys summary (≈150 words), "
        "pros (2 bullet points), cons (2 bullet points), "
        "review (≈300-word spoiler-free)."
    )
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a concise horror-book reviewer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    content = resp.choices[0].message.content
    data = json.loads(content)
    return (
        textwrap.fill(data["summary"], 80),
        "\n".join(f"- {p}" for p in data["pros"]),
        "\n".join(f"- {c}" for c in data["cons"]),
        textwrap.fill(data["review"], 80),
    )

with CSV.open(newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        slug = (
            row["title"]
            .lower().replace(" ", "-")
            .replace("’", "").replace("'", "")
        )
        out_file = OUTDIR / f"{slug}.md"

        summary, pros, cons, review = ai_review(row["title"], row["blurb"])

        md = TEMPLATE.format(
            title=row["title"].strip(),
            asin=row["asin"].strip(),
            date=DATE,
            blurb=row["blurb"].strip(),
            img=row["img"].strip(),
            summary=summary,
            pros=pros,
            cons=cons,
            review=review,
        )

        OUTDIR.mkdir(parents=True, exist_ok=True)
        if force or not out_file.exists():
            out_file.write_text(md)
            print("WROTE", out_file)
