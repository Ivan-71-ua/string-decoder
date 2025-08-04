"""
Text restoration from a corrupted English string.

Approach:
1. Build an index of English words.
2. Recover spaces using dynamic programming (score = word frequency).
3. For every token check anagrams that match letters and wildcards '*'.
   Choose the candidate with the best frequency score.
"""

import re
from collections import defaultdict, Counter
from wordfreq import top_n_list, zipf_frequency

# -------------------------------------------------------------
# Build dictionary and anagram index (≈50k most frequent words)
# -------------------------------------------------------------
WORDLIST = top_n_list("en", 50000)
WORDSET = set(WORDLIST)

ANAGRAMS = defaultdict(list)
for w in WORDSET:
    ANAGRAMS["".join(sorted(w))].append(w)


# -------------------------------------------------------------
# Candidate generator for a corrupted "word"
# -------------------------------------------------------------
def candidates(chunk: str):
    letters = [c for c in chunk if c != "*"]
    mask = Counter(letters)
    missing = chunk.count("*")
    length = len(chunk)

    result = []
    for key, words in ANAGRAMS.items():
        if len(key) != length:
            continue
        c = Counter(key)
        if all(c[ch] >= mask[ch] for ch in mask) and \
           sum(c.values()) - sum(mask.values()) == missing:
            result.extend(words)
    return result or [chunk]  # fallback if nothing found


# -------------------------------------------------------------
# Dynamic programming segmentation with scoring
# -------------------------------------------------------------
def restore(text: str):
    n = len(text)
    best = [(None, -1e9)] * (n + 1)  # (previous_index, score)
    best[0] = (0, 0.0)

    max_word_len = 20  # reasonable max English word length

    for i in range(1, n + 1):
        for j in range(max(0, i - max_word_len), i):
            chunk = text[j:i]
            if len(chunk) == 1 and chunk.lower() not in {"a", "i"}:
                continue  # avoid splitting into meaningless single letters
            for cand in candidates(chunk.lower()):
                score = best[j][1] + zipf_frequency(cand, "en") * len(cand) - 1.0
                if score > best[i][1]:
                    best[i] = (j, score, cand)

    # backtrack
    words = []
    i = n
    while i > 0:
        j, _, w = best[i]
        words.append(w)
        i = j
    return " ".join(reversed(words))


if __name__ == "__main__":
    corrupted = (
        "Al*cew*sbegninnigtoegtver*triedofsitt*ngbyh*rsitsreonhtebnakandofh*vingnothi"
        "gtodoonc*ortw*cesh*hdapee*edintoth*boo*h*rsiste*wasr*adnigbuti*hadnopictu*es"
        "orc*nve*sati*nsinitandwhatisth*useofab**kth*ughtAlic*withou*pic*u*esorco*ver"
        "sa*ions"
    )
    print(restore(corrupted))
