Gabrielle Boyce – Homework 4: Tech Shell READ ME
Box 222 Comp Sci
Date: 2-14-2017

DESCRIPTION:
        This is a very simple Tech Shell. It will parse through entered commands, tokenize them, and run them as commands like a normal shell. It will handle the special characters: “<”, “>”, and “>>”. It handles the built-in commands “pwd” “exit” and “cd”. It handles not-built-in commands. Space, tab, and vertical tab are the optional delimiters for tokens as well. Shell does not handle piping.

PROCESS:
        *TOKENIZING: Shell receives the entered commands, and will first parse through them and separate them by tokens. It does this by using space, tab, and vertical tab as delimiters. Non-special characters will be referred to as “normal tokens”. Special characters (i.e. redirection characters) will be referred to as “special tokens”. When special characters are entered, such as “<”, “>” and “>>”, it will store a number associated with the specific character in the variable scf. Once the normal tokens are created, it will store them in a character array arr. If scf is not equal to zero (meaning it holds a special token), it will then store that token in the array.
        *CATEGORIZING: Shell then passes arr (now the collection of tokens) to the checker function. The checker function will categorize the tokens based on whether the token is built-in or not-built-in. It checks the first token of arr for three possible conditions: “pwd”, “exit”, and “cd”. If the first token is “pwd”, it will then call the prwd function which will print the working directory. If the first token is “exit”, it will simply call an exit within the checker function and the program will exit. If the first token is “cd”, it will call the chd function and change the directory based on the path the user entered after. If the first token is none of these, it will then call the notbuilt function.
        *EXECUTING NON-BUILT: Once the notbuilt function is called, the shell will begin by spawning a child process. It will then execute the args entered if there are no special characters. If there are special characters, it will check which character is entered and use fopen() on the file depending on which character. Once fopen() has occurred, it will spawn the process afterwards.

ERROR CATCHING:
 Shell is equipped to handle the errors:
1)        If the command entered is not recognized
2)        If the child process fails to be created
3)        If the command fails to execute
4)        If in case of “cd” incorrect path entered

LIMITATIONS:
Shell does not handle piping commands.

SAMPLES TO ENTER:
        “ls -l”
        “ls > ls.out”
        “ls>ls.out”
        “wc < ls.out”
        “ls >> ls.out”
        “pwd”
        “cd ..”
        “exit”
