---
title: "{{ .title }}"
asin: "{{ .asin }}"
date: "{{ .date }}"
draft: false
---

{{ .blurb }}

{{< amzlink asin="{{ .asin }}" title="{{ .title }}" img="{{ .img }}" >}}

## Verdict

Perfect for midnight chills.

{{< amzbtn asin="{{ .asin }}" label="Buy on Amazon" >}}
