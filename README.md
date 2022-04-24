# MEQChallenge

This is response to challenge by MEQ for software engineer position

# To run: 
pip install requirements.text
python3 main.py



# Comments
Shown graph is for the following state transposition tree:
{'A': {'1': 'U', '2': 'Z', '3': 'N'}, 'B': {'1': 'E', '2': 'F', '3': 'G'}, 
'C': {'1': 'B', '2': 'V', '3': 'I'}, 'D': {'1': 'C', '2': 'W', '3': 'K'}, 
'E': {'1': 'Q', '2': 'E', '3': 'O'}, 'F': {'1': 'X', '2': 'J', '3': 'G'}, 
'G': {'1': 'M', '2': 'K', '3': 'Y'}, 'H': {'1': 'R', '2': 'C', '3': 'E'}, 
'I': {'1': 'C', '2': 'W', '3': 'N'}, 'J': {'1': 'R', '2': 'S', '3': 'K'}, 
'K': {'1': 'U', '2': 'T', '3': 'Z'}, 'L': {'1': 'E', '2': 'O', '3': 'C'}, 
'M': {'1': 'E', '2': 'N', '3': 'J'}, 'N': {'1': 'O', '2': 'M', '3': 'C'}, 
'O': {'1': 'B', '2': 'V', '3': 'Y'}, 'P': {'1': 'R', '2': 'Z', '3': 'T'},
'Q': {'1': 'P', '2': 'J', '3': 'L'}, 'R': {'1': 'O', '2': 'W', '3': 'H'},
'S': {'1': 'U', '2': 'Q', '3': 'J'}, 'T': {'1': 'M', '2': 'L', '3': 'E'}, 
'U': {'1': 'I', '2': 'R', '3': 'O'}, 'V': {'1': 'D', '2': 'M', '3': 'X'}, 
'W': {'1': 'T', '2': 'I', '3': 'Q'}, 'X': {'1': 'R', '2': 'M', '3': 'Y'}, 
'Y': {'1': 'V', '2': 'W', '3': 'R'}, 'Z': {'-': 'A'}}

Using networkx instead of graphviz as graphviz seems outdated and didn't work well with latest python
Unfortunately not easy to print labels (1,2,3) for edges 