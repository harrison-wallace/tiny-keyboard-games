# tinyeducation

## About 

In this repo I will be storing resources to help teach children as I embark on the journey of learning myself to teach my children.


## Games: Toddler learning games

### Game 1 Alphabet Learning Game

#### Description
This is a simple educational game built with Pygame to help young children (like toddlers) learn the letters of the alphabet and basic keyboard skills. The game displays each letter full-screen, plays its corresponding sound on a loop with a 1-second gap, and provides fun visual and audio feedback when the correct key is pressed:
- The background turns green for 3 seconds.
- The letter bounces.
- Stars appear as a reward.

The game tracks a score and shows it at the end. It's designed to be immersive and engaging for kids around 3 years old.

### Installation
1. Ensure you have Python 3 installed (tested on Python 3.10+).
2. Install Pygame:  
   ```
   pip install pygame
   ```
3. Download the alphabet sound files from [Sound City Reading](https://www.soundcityreading.net/individual-alphabet-sounds---abc-order.html) and place them in the project directory. The files should be named `alphasounds-a.mp3`, `alphasounds-b.mp3`, ..., `alphasounds-z.mp3`.
4. (Optional) Add a success sound file named `correct.wav` (e.g., a free "ding" sound from online resources like freesound.org).

### Usage
Run the game with:  
```
python game.py
```
- Press the matching key for the displayed letter to advance.
- Press ESC to exit.
- The game runs in full-screen mode.

## Credits
- **Alphabet Sounds**: Provided by [Sound City Reading](https://www.soundcityreading.net/individual-alphabet-sounds---abc-order.html). These materials are copyrighted by Kathryn J. Davis, but permission is granted for parents, teachers, and tutors to use them for educational purposes with their students. Thank you to Sound City Reading for making these resources freely available!
- **Font**: [School](https://www.dafont.com/school-5.font) dafont
