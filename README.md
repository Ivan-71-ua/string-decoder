# String Decoder

Simple script to restore a piece of English text that has its letters scrambled
and replaced with `*` placeholders and no spaces.  It uses the [wordfreq]
package to obtain a list of common English words and performs a dynamic
programming search to segment the text and replace missing letters using anagram
matching.

## Usage

```bash
pip install wordfreq
python restore_text.py
```
