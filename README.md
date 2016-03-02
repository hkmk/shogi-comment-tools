# shogi-comment-tools
Tools for Shogi Commentary Corpus

# get.sh
Get Shogi game records with comments from <http://www.meijinsen.jp>.
Games are played by human experts and comments are written by human.

## Usage
1. Become a paid member of <http://www.meijinsen.jp>. (In Japanese)

2. Export cookies.txt and overwrite cookies.txt in this directory.

3. Remove tmp/ and kif/ if exist.

4. Run get.sh.
Game records are saved to kif/ directory.

# cleansing.sh
Convert characters in comments to ones in JISX 0208.
Converted files are saved to kif_clean/ directory.
If you want to customize, edit jisx/replace.

This script requires mojimoji module.

```
pip install mojimoji
```
