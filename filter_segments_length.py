input_path = "input.txt"
output_path = "output.txt"
min_words = 20
max_words = 1000

def read_segments(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    raw_segments = content.split("\n\n")
    segments = []
    for raw in raw_segments:
        stripped = raw.strip("\n")
        if stripped.strip() == "":
            continue
        segments.append(stripped)
    return segments

def count_words(segment):
    return len(segment.split())

def filter_segments(segments):
    kept_segments = []
    for segment in segments:
        word_count = count_words(segment)
        if word_count < min_words:
            continue
        if word_count > max_words:
            continue
        kept_segments.append(segment)
    return kept_segments

def write_segments(path, segments):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(segments))
        f.write("\n")

def main():
    segments = read_segments(input_path)
    original_count = len(segments)
    kept_segments = filter_segments(segments)
    removed_count = original_count - len(kept_segments)
    write_segments(output_path, kept_segments)
    print(f"Original segments: {original_count}")
    print(f"Removed segments: {removed_count}")
    print(f"Remaining segments: {len(kept_segments)}")
    print(f"Written to: {output_path}")

if __name__ == "__main__":
    main()
