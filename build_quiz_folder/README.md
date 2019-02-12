# build_quiz_folder
This Python 3 script builds a ready-to-quiz folder for Geeks Who Drink Quizmasters.

## Requirements
1. [Python 3.5 or Later](https://www.python.org/downloads/)

2. [LXML installed](https://lxml.de/installation.html)

    Windows:
    <code>py -3 -m pip install lxml</code>
    
    UNIX:
    <code>python3 -m pip install lxml</code>

3. ZIP folder as distributed by Geeks Who Drink on OBYQM.

## Directions

### Add variables
1. Open build_quiz_folder.py
2. Add path to your audio clips folder on line 11. 
3. Add path to your master score sheet at line 12.
    - **If you're a Windows user, be sure to add an 'r' in front of each path!**
4. Save the script.

### Run Script
4. Open Command Prompt / Terminal
5. <code>cd path/to/script</code>

6a. Windows: 

<code>py -3 build_quiz_folder.py C:\path\to\quiz.zip</code>

6b. UNIX: 

<code>python3 build_quiz_folder.py path/to/quiz.zip</code>
