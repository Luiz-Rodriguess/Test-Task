# Test Task

## Luiz Rodrigues

### Introduction

This project was assigned to me by a company whose name won't be disclosed out of respect and to preserve anonymity.

The project consists of a program that synchronizes two folders: a source folder and a replica folder. The replica folder is maintained as an identical copy of the contents in the source folder.

The project was developed in Python version 3.12, and it's recommended to use the same or a compatible version.

### How ro run the project

In a terminal you need to run the following command:

```bash
python3 sync.py path/to/source path/to/replica timeout_in_seconds path/to/logfile
```

**Note:** To stop running the program you can wither stop it using CTRL+C or with a task manager, since it was not specified the program stops its execution after finishing the syncronization it had started. This behaviour can be changed depending on what is desired.

### Program structure

```txt
project/
├── src/
│   ├── sync.py
│   └── Logger.py
├── source/
├── replica/
├── log.txt
└── README.md

```

The program consists in two files contained in a main file called *sync.py* which handles the syncronization of the two folders, and a auxilary file *Logger.py*, that contains a class to help log the information.