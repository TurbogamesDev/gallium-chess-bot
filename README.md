# Gallium: Yet Another Chess Bot
> A command-line chess bot that replies with random moves.

You can play a game of chess in your command line with Gallium. The bot isn't all that good at the game, but it knows how the pieces work.

## Requirements and Installation
Gallium requires python `3.10` or above (tested using `3.14.0`), and the [python-chess](https://github.com/niklasf/python-chess) library. 

### Installing python and python-chess
Grab the latest release of Python from [here](https://www.python.org/downloads/) and install python-chess by executing: 
```bash
pip install chess
```
If that did not work, try this:
- **Windows and Linux:** `python -m pip install chess`
- **MacOS:** `python3 -m pip install chess`

### Installing Gallium
You will have to install it from the source. Make sure that `main.py` and the `classes` folder are in the same directory.

## Usage
Execute `python main.py` to start a new game against the bot. You must reply in SAN (Standard Algebraic Notation). The program will quit once the game has ended.

## Support
If you need any help, open a [discussion](https://github.com/TurbogamesDev/gallium-chess-bot/discussions).

## Status and Roadmap
The project is currently active and in development.

Here is a roadmap of features that I plan to add to the bot, in no specific order:
- Implement minimax with piece-value evaluation
- Alpha-Beta pruning
- Slight randomness so that the bot doesn't always play the exact same moves
- In case of equally good moves, fuzz out the bottom two half moves of the search so that the bot picks the move where it can penalise the opponent more if they make a mistake.
- Propagative fuzzing, where if the move evaluations are still the same after fuzzing, it fuzzes the bottom four half moves, then six and so on.
- Lichess integration so that you can play against the bot on lichess.

## Contributing
Pull requests are welcome, but please discuss what you would like to improve in a pull request beforehand for major refactors.

You may create a fork of this repository and use the code for non-commercial purposes.