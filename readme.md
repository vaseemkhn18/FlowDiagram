# Flow Diagram/Sequence Diagram Creation Python Library

## Table of Content:
- [Overview](#overview)
   - [Setup](#setup)
- [Usage](#usage)
- [Methods](#methods)

## Overview

FlowDiagram is a Python Library to create Sequence Diagram in Command Line or Image (.PNG)

### Setup

#### Installtion via PIP:
    pip install flowdiagram

#### Manual Installation:
This package requires:
-  multipledispatch==0.6.0
-  six==1.16.0
-  Pillow==8.2.0

First install above packages
Download tar.gz from pypi and untar it
Go to untarred directory
Execute below command
    python setup.py install

## Usage

Using this library we can generate Sequence Diagram on Command Line or a Image (.PNG) via both python script or flow text file.

### Generate Sequence Diagram via flow text file

Flow Text File Example:

```
title Example Flow

Bob->Alice: Hi! Alice
Alice->Bob: Hi! Bob
Bob->Alice: '''Are you free?
tomorrow'''
Alice->Bob: I think so, why?
Bob->Alice: Want to see a movie?
Alice->Bob: Sure.
Bob->Alice: Great!
Alice->Bob: See you later.
Bob->Alice: Bye.
```
The ``->`` is used to draw a message between two
participants.
Participants do not have to be explicitly declared.

To have a dotted arrow, you use ``-->``

***NOTE*** Do not use ``-->`` or ``<-`` or ``<--`` instead of ``->``.
This will impact flow diagram.

To provide multiple line message please start and end message with ``'''``

For Example:
```
Bob->Alice: '''Are you free?
tomorrow'''
```
***NOTE*** if a single line message will be sliced into multiple line as per the flow diagram size requirements.

To execute module use below command:
```
python -m flowdiagram create
```
Example :
```
linus> python -m flowdiagram create
[Flowdiagram] Please Provide Flow File Path (i.e. .txt file) : callflow.txt
[Flowdiagram] What you want to do create ?
[Flowdiagram] 1 : Create Flow on command line
[Flowdiagram] 2 : Create Flow picture
[Flowdiagram] 3 : Exit
[Flowdiagram] Your Choice : 1
[Flowdiagram] Reading File......


             Example Flow


  Bob                         Alice
   |                             |
   |Hi! Alice                    |
   |---------------------------->|
   |                             |
   |Hi! Bob                      |
   |<----------------------------|
   |                             |
   |Are you free?                |
   |tomorrow                     |
   |---------------------------->|
   |                             |
   |I think so, why?             |
   |<----------------------------|
   |                             |
   |Want to see a movie?         |
   |---------------------------->|
   |                             |
   |Sure.                        |
   |<----------------------------|
   |                             |
   |Great!                       |
   |---------------------------->|
   |                             |
   |See you later.               |
   |<----------------------------|
   |                             |
   |Bye.                         |
   |---------------------------->|
   |                             |

```

### Generate Sequence Diagram via python script

Test Script Example:
```
>>> from flowdiagram  import flowdiagram
>>>
>>> sqd = flowdiagram()
>>> sqd.setTitle('Script Flow Example')
>>>
>>>
>>> sqd.addFlow(['Node 1','Node 2','First message'])
>>> sqd.addFlow(['Node 2','Node 1','Second message'])
>>> sqd.addFlow(['Node 1','Node 2','Third message'])
>>> sqd.addFlow(['Node 2','Node 2','Really Long long long long long long long long long message'])
>>> sqd.addFlow(['Node 2','Node 2','Really Long long long long long long and \nmulti line message'])
>>> sqd.addFlow(['Node 1','Node 2','Really Long long long long long long and \nmulti line message'])
>>> sqd.addFlow(['Node 1','Node 1','Really Long long long long long long and \nmulti line message'])
>>> sqd.addFlow(['Node 1','Node 1','Really Long long long long long long long long long message'])
>>> sqd.addFlow(['Node 1','Node 2','Second last message'])
>>> sqd.addFlow(['Node 2','Node 1','Last message \n BYE BYE!!!!!'])
>>>
>>> sqd.drawCmdLine()

```

***Output:***
```


                      Script Flow Example


  Node 1                                                Node 2
   |                                                     |
   |First message                                        |
   |---------------------------------------------------->|
   |                                                     |
   |Second message                                       |
   |<----------------------------------------------------|
   |                                                     |
   |Third message                                        |
   |---------------------------------------------------->|
   |                                                     |
   |                                                     |Really Long long long long long long long lo
   |                                                     |ng long message
   |                                                     |---
   |                                                     |  |
   |                                                     |<--
   |                                                     |
   |                                                     |
   |                                                     |Really Long long long long long long and
   |                                                     |multi line message
   |                                                     |---
   |                                                     |  |
   |                                                     |<--
   |                                                     |
   |                                                     |
   |Really Long long long long long long and             |
   |multi line message                                   |
   |---------------------------------------------------->|
   |                                                     |
   |Really Long long long long long long and             |
   |multi line message                                   |
   |---                                                  |
   |  |                                                  |
   |<--                                                  |
   |                                                     |
   |Really Long long long long long long long lo         |
   |ng long message                                      |
   |---                                                  |
   |  |                                                  |
   |<--                                                  |
   |                                                     |
   |Second last message                                  |
   |---------------------------------------------------->|
   |                                                     |
   |Last message                                         |
   | BYE BYE!!!!!                                        |
   |<----------------------------------------------------|
   |                                                     |

```

To create image from the flow use ``drawPicture()`` method

```
>>> sqd.drawPicture()
[Flowdiagram] File created Successfully...
[Flowdiagram] Path : C:\Users\myUser\Flowdiagram.png
>>>
```

Output:
[Flowdiagram.png](https://github.com/vaseemkhn18/FlowDiagram/blob/master/src/Flowdiagram.png)

## Methods

