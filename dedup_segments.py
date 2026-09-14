input_path = "input.txt"
output_path = "output.txt"

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

def remove_duplicates(segments):
    seen = set()
    unique_segments = []
    for segment in segments:
        key = segment.strip()
        if key in seen:
            continue
        seen.add(key)
        unique_segments.append(segment)
    return unique_segments

def write_segments(path, segments):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(segments))
        f.write("\n")

def main():
    segments = read_segments(input_path)
    original_count = len(segments)
    unique_segments = remove_duplicates(segments)
    removed_count = original_count - len(unique_segments)
    write_segments(output_path, unique_segments)
    print(f"Original segments: {original_count}")
    print(f"Removed duplicates: {removed_count}")
    print(f"Remaining segments: {len(unique_segments)}")
    print(f"Written to: {output_path}")

if __name__ == "__main__":
    main()
