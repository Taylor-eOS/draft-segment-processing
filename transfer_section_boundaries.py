full_path = "full.txt"
summaries_path = input("Input file (input.txt): ") or "input.txt"
output_path = "output.txt"

with open(full_path, "r", encoding="utf-8") as f:
    full_text = f.read()
with open(summaries_path, "r", encoding="utf-8") as f:
    summaries_text = f.read()
marker = "\n\n "
plain = "\n\n"
full_segments = []
current = []
i = 0
while i < len(full_text):
    if full_text[i:i+len(marker)] == marker:
        current.append(full_text[i+len(marker)-1:i+len(marker)])
        full_segments.append(("".join(current), True))
        current = []
        i += len(marker)
    elif full_text[i:i+len(plain)] == plain:
        full_segments.append(("".join(current), False))
        current = []
        i += len(plain)
    else:
        current.append(full_text[i])
        i += 1
if current:
    full_segments.append(("".join(current), False))
split_after = set()
for idx, (seg, is_split) in enumerate(full_segments):
    if is_split:
        split_after.add(idx)
summary_segments = summaries_text.split(plain)
if len(summary_segments) != len(full_segments):
    raise ValueError(f"Segment count mismatch: full.txt has {len(full_segments)}, summaries has {len(summary_segments)}")
output_text = summary_segments[0]
for idx in range(1, len(summary_segments)):
    separator = marker if (idx - 1) in split_after else plain
    output_text += separator + summary_segments[idx]
with open(output_path, "w", encoding="utf-8") as f:
    f.write(output_text)
