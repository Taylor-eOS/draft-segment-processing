import math
import re
import unicodedata
from collections import Counter

INPUT_FILE = "input.txt"
OUTPUT_FILE = "segment_keywords_output.txt"
MIN_WORD_LENGTH = 6
TOP_N_WORDS_PER_SEGMENT = 12
MIN_LOG_LIKELIHOOD = 6.63


def read_segments(file_path):
    with open(file_path, "r", encoding="utf-8") as file_handle:
        raw_text = file_handle.read()
    normalized_text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    raw_segments = re.split(r"\n\s*\n+", normalized_text)
    segments = []
    for raw_segment in raw_segments:
        stripped_segment = raw_segment.strip()
        if stripped_segment:
            segments.append(stripped_segment)
    return segments


def normalize_word(word):
    decomposed = unicodedata.normalize("NFKD", word)
    ascii_word = "".join(character for character in decomposed if not unicodedata.combining(character))
    return ascii_word.lower()


def tokenize_segment(segment_text):
    raw_tokens = re.findall(r"[A-Za-z][A-Za-z'\-]*[A-Za-z]|[A-Za-z]", segment_text)
    cleaned_tokens = []
    for raw_token in raw_tokens:
        stripped_token = raw_token.strip("'-")
        normalized_token = normalize_word(stripped_token)
        if len(normalized_token) >= MIN_WORD_LENGTH:
            cleaned_tokens.append(normalized_token)
    return cleaned_tokens


def build_segment_word_counts(segments):
    segment_word_counts = []
    for segment_text in segments:
        tokens = tokenize_segment(segment_text)
        word_counts = Counter(tokens)
        segment_word_counts.append(word_counts)
    return segment_word_counts


def build_vocabulary(segment_word_counts):
    vocabulary = set()
    for word_counts in segment_word_counts:
        vocabulary.update(word_counts.keys())
    return vocabulary


def build_total_counts_per_word(segment_word_counts, vocabulary):
    total_counts = {word: 0 for word in vocabulary}
    for word_counts in segment_word_counts:
        for word, count in word_counts.items():
            total_counts[word] += count
    return total_counts


def log_likelihood_ratio(count_in_segment, total_in_segment, count_in_corpus, total_in_corpus):
    if count_in_segment == 0:
        return 0.0
    expected_in_segment = total_in_segment * (count_in_corpus / total_in_corpus)
    if expected_in_segment <= 0:
        return 0.0
    count_outside_segment = count_in_corpus - count_in_segment
    total_outside_segment = total_in_corpus - total_in_segment
    expected_outside_segment = total_outside_segment * (count_in_corpus / total_in_corpus)
    statistic = 2.0 * count_in_segment * math.log(count_in_segment / expected_in_segment)
    if count_outside_segment > 0 and expected_outside_segment > 0:
        statistic += 2.0 * count_outside_segment * math.log(count_outside_segment / expected_outside_segment)
    if count_in_segment < expected_in_segment:
        statistic = -statistic
    return statistic


def compute_keyness_scores(segment_word_counts, total_counts, total_words_in_corpus):
    all_scores = []
    for word_counts in segment_word_counts:
        total_in_segment = sum(word_counts.values())
        scores_for_segment = {}
        for word, count_in_segment in word_counts.items():
            count_in_corpus = total_counts[word]
            statistic = log_likelihood_ratio(count_in_segment, total_in_segment, count_in_corpus, total_words_in_corpus)
            if statistic >= MIN_LOG_LIKELIHOOD:
                scores_for_segment[word] = statistic
        all_scores.append(scores_for_segment)
    return all_scores


def rank_top_words(score_dictionary, top_n):
    ranked_items = sorted(score_dictionary.items(), key=lambda item: item[1], reverse=True)
    return [word for word, score in ranked_items[:top_n]]


def write_report(segments, keyness_scores, output_path):
    with open(output_path, "w", encoding="utf-8") as output_handle:
        total_segments = len(segments)
        for segment_index in range(total_segments):
            top_words = rank_top_words(keyness_scores[segment_index], TOP_N_WORDS_PER_SEGMENT)
            word_list_text = ", ".join(top_words) if top_words else "(none found)"
            output_handle.write(f"Segment {segment_index + 1}: {word_list_text}\n")


def main():
    segments = read_segments(INPUT_FILE)
    if not segments:
        print("No segments found in input file. Check that the file exists and contains blank-line-separated text.")
        return
    total_segments = len(segments)
    segment_word_counts = build_segment_word_counts(segments)
    vocabulary = build_vocabulary(segment_word_counts)
    total_counts = build_total_counts_per_word(segment_word_counts, vocabulary)
    total_words_in_corpus = sum(total_counts.values())
    keyness_scores = compute_keyness_scores(segment_word_counts, total_counts, total_words_in_corpus)
    write_report(segments, keyness_scores, OUTPUT_FILE)
    print(f"Processed {total_segments} segments. Report written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
