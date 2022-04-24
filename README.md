# MEQChallenge

This is response to challenge by MEQ for software engineer position

# To run: 
pip install requirements.text
python3 main.py



# Comments
Shown graph is for the following state transposition tree:
{'A': {'1': 'R', '2': 'H', '3': 'U'}, 'B': {'1': 'E', '2': 'Q', '3': 'P'}, 'C': {'1': 'R', '2': 'U', '3': 'J'}, 'D': {'1': 'E', '2': 'M', '3': 'F'}, 'E': {'1': 'Q', '2': 'X', '3': 'J'}, 'F': {'1': 'M', '2': 'Y', '3': 'E'}, 'G': {'1': 'R', '2': 'U', '3': 'S'}, 'H': {'1': 'T', '2': 'U', '3': 'V'}, 'I': {'1': 'C', '2': 'B', '3': 'V'}, 'J': {'1': 'R', '2': 'I', '3': 'O'}, 'K': {'1': 'P', '2': 'L', '3': 'G'}, 'L': {'1': 'P', '2': 'K', '3': 'G'}, 'M': {'1': 'E', '2': 'T', '3': 'M'}, 'N': {'1': 'G', '2': 'Y', '3': 'I'}, 'O': {'1': 'B', '2': 'G', '3': 'X'}, 'P': {'1': 'R', '2': 'D', '3': 'K'}, 'Q': {'1': 'P', '2': 'R', '3': 'Z'}, 'R': {'1': 'O', '2': 'M', '3': 'U'}, 'S': {'1': 'H', '2': 'W', '3': 'I'}, 'T': {'1': 'Z', '2': 'N', '3': 'L'}, 'U': {'1': 'H', '2': 'X', '3': 'Y'}, 'V': {'1': 'G', '2': 'Y', '3': 'I'}, 'W': {'1': 'O', '2': 'F', '3': 'H'}, 'X': {'1': 'G', '2': 'O', '3': 'S'}, 'Y': {'1': 'X', '2': 'O', '3': 'P'}, 'Z': {'-': 'A'}}

Using networkx instead of graphviz as graphviz seems outdated and didn't work well with latest python
Unfortunately not easy to print labels (1,2,3) for edges 