# build_quiz_folder
This Python 3 script builds a ready-to-quiz folder for Geeks Who Drink Quizmasters.

## Requirements
1. Python 3.5 or later
2. LXML installed
3. ZIP folder, as distributed by Geeks Who Drink on OBYQM.

## Directions
1. Add path to your audio clips folder at 'audio_folder ='
2. Add path to your master score sheet at 'score_sheet ='
- If you're a Windows user, be sure to add an 'r' in front of the path!
3. SAVE
4. Open Command Prompt / Terminal
5. `cd path/to/script`
6. Windows: `py 3 build_quiz_folder.py C:\path\to\quiz.zip`
7. UNIX: `python3 build_quiz_folder.py path/to/quiz.zip`
