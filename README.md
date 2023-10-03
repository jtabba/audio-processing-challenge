**Docs**

For use:

1. Install dependencies
2. Replace `directory` with the path to target audio files
3. Initialise processing via terminal `python3 index.py` while in the root of this directory

Information

This script uses OpenAi's Whisper library to transform audio files into text. The purpose of this script is to identify the amount of consecutive numbers spoken, if at all, and the amount of numbers spoken. This is achieved by breaking the resulting text into an array of its characters, checking if any are numbers, and if so whether they are a consecutive sequence, and then adding the data to a dictionary which is used to create a CSV.

Speech analysis is a slow process and multiprocessing has been incorporated as a result to improve the speed of analysis.
