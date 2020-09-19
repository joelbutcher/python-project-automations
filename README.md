# Python Automation
A simple Python script using the PyGithub package to automate project creation

## Requirements
- This file requires the PyGithub package and can be installed via `pip install PyGithub`

## Usage
I originally wrote this script to be run via a bash command. To do the same, follow these steps:

Create a new shell script:

```bash
touch .commands.sh 
```

Copy the contents below into the sell script:

```bash
#!/bin/bash

function create(){
    cd
    create.py $1
    cd "YOU_PROJECT_PATH/{$1}"
}
```

Create the Python file

*make sure that the file is in the same directory as your new shell script and that all the global variables are configured to your preference*

Make the shell script executable:

```bash
source .commands.sh
```

Run the command:

```bash
create my-new-project
```
