<h1 align="center">Welcome to Mancala 👋</h1>
<p>
</p>

>Mancala is an ancient board game with many variants. We will be focused on the popular (in the US) Kalah version. Briefly, this variant of Mancala is a two-player board game where each player has a row of M pits where each pit is initially filled with K stones. For this project, we will use the standard setup of six pits each initially containing four stones. (Such attributed can be reassigned) To each player’s right on the boardis a store. The objective for each player is to accumulate as many stones as possible into their own store.
>
>Each turn proceeds by the active player choosing a pit, then removing all the stones, then sowing the stones into pits counter-clockwise, including the store and opponents pits if enough stones are in the original pit. If the last stone is sowed into the store, then the player gets to take another turn. If the last stone is sowed into one of the player’s own empty pits, then the player captures any stones in their opponents pit directly across the board. Play continues until either player runs out of stones.

You can play it online [here](https://www.mathplayground.com/mancala.html)

## Requirements
copy
math
random
argparse

## Usage

Player options:  
human= human as the player  
random = random legal moves  
minmax = uses minimax algorithm to choose next move  
alphabeta = minmax using alpha-beta pruning  



For Linux users:  
`./src/play.py Player1 Player2`   
e.g.  
`./src/play.py radom human`  

For windows users:  
`python ./src/play.py Player1 Player2`   
e.g.  
`python ./src/play.py radom human`  

the maximum depth of the player can be changed with a default value of 6  
e.g.  
`python ./src/play.py minimax alphabeta -d1 6 -d2 8`  

![](https://github.com/ycchen00/Mancala/blob/master/assets/begingame.png)  

![](https://github.com/ycchen00/Mancala/blob/master/assets/gameover.png)

## Document
The writeup includes some designs and experiments between algorithms: [writeup](https://github.com/ycchen00/Mancala/blob/master/writeup.pdf)

## References
- [Leonie-/mancala-python: Mancala in Python](https://github.com/Leonie-/mancala-python)
- [naigutstein/Mancala: Alpha-Beta Pruning and Minimax (Python)](https://github.com/naigutstein/Mancala)
- [qqhann/Mancala: Mancala board game, written in python. The rule is Kalah and can be extended.](https://github.com/qqhann/Mancala)

## Author

👤 **Yuchi Chen**

* Website: https://ycchen00.github.io/
* Github: [@ycchen00](https://github.com/ycchen00)
* LinkedIn: [yuchi-chen](https://www.linkedin.com/in/yuchi-chen/)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_