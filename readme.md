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
```
    pip install flowdiagram
```

#### Manual Installation:
1. This package requires:
    -  multipledispatch==0.6.0
    -  six==1.16.0
    -  Pillow==8.2.0

2. First install above packages.
3. Download tar.gz from pypi and untar it.
4. Go to untarred directory.
5. Execute below command:
```
    python setup.py install
```

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

**NOTE** Do not use ``-->`` or ``<-`` or ``<--`` instead of ``->``.
This will impact flow diagram.

To provide multiple line message please start and end message with ``'''``

For Example:
```
Bob->Alice: '''Are you free?
tomorrow'''
```
**NOTE** if a single line message will be sliced into multiple line as per the flow diagram size requirements.

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

**Output:**
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
>>> from flowdiagram  import flowdiagram
>>>
>>> sqd = flowdiagram()
>>> sqd.addTitle('Example Flow')
>>> sqd.addFlow(['Bob','Alice','Hi! Alice'])
>>> sqd.addFlow(['Alice','Bob','Hi! Bob'])
>>> sqd.addFlow(['Bob','Alice','Are you free? \ntomorrow'])
>>> sqd.addFlow(['Alice','Bob','I think so, why?'])
>>> sqd.addFlow(['Bob','Alice','Want to see a movie?'])
>>> sqd.addFlow(['Alice','Bob','Sure .'])
>>> sqd.addFlow(['Bob','Alice','Great !'])
>>> sqd.addFlow(['Alice','Bob','See You later'])
>>> sqd.addFlow(['Bob','Alice','Bye .'])
>>> sqd.drawPicture()
[Flowdiagram] File created Successfully...
[Flowdiagram] Path : C:\Users\myUser\Flowdiagram.png
>>>
```

**Output**:

![Flowdiagram.png!](https://github.com/vaseemkhn18/FlowDiagram/blob/master/src/Flowdiagram.png "Flowdiagram")

## Methods

flowdiagram class consists of below methods:

#### flowdiagram.setTitle(<span style="color:blue">str</span>)
This method is used to set the title of the Sequence/Flow Diagram.
For Example:
```
>>> from flowdiagram  import flowdiagram
>>> sqd = flowdiagram()
>>> sqd.setTitle('Script Flow Example')
```

#### flowdiagram.addFlow(<span style="color:blue">list</span>)
This method is used to add flow of the Sequence/Flow Diagram.
Format of the list is ``['source','destination','message']``
**NOTE** if you want to add multiple lines message just add ``'\n'`` for next line. 
For Example:
```
>>> from flowdiagram  import flowdiagram
>>> sqd = flowdiagram()
>>> sqd.setTitle('Script Flow Example')
>>> sqd.addFlow(['Node 1','Node 2','First message \nmulti line'])
```

#### flowdiagram.drawCmdLine()
This method is used to draw Sequence/Flow Diagram of added flow on command line.
For Example:
```
>>> from flowdiagram  import flowdiagram
>>> sqd = flowdiagram()
>>> sqd.setTitle('Script Flow Example')
>>> sqd.addFlow(['Node 1','Node 2','First message'])
>>> sqd.addFlow(['Node 2','Node 1','Second message'])
>>> sqd.drawCmdLine()



                      Script Flow Example


  Node 1                                                Node 2
   |                                                     |
   |First message                                        |
   |---------------------------------------------------->|
   |                                                     |
   |Second message                                       |
   |<----------------------------------------------------|
   |                                                     |

```

### flowdiagram.drawCmdLine(<span style="color:blue">str</span>)
This method is used to draw Sequence/Flow Diagram of added flow on command line via file.
This method takes file path as an argument.
File content [Example](#Generate Sequence Diagram via flow text file)
For Example:
```
>>> from flowdiagram  import flowdiagram
>>> sqd = flowdiagram()
>>> myFile = 'C:\\Users\\myUser\\callflow.txt'
>>> sqd.drawCmdLine(myFile)



                      Script Flow Example


  Node 1                                                Node 2
   |                                                     |
   |First message                                        |
   |---------------------------------------------------->|
   |                                                     |
   |Second message                                       |
   |<----------------------------------------------------|
   |                                                     |

```

#### flowdiagram.drawPicture()
This method is used to create IMAGE of Sequence/Flow Diagram of added flow.
For Example:
```
>>> from flowdiagram  import flowdiagram
>>> sqd = flowdiagram()
>>> sqd.setTitle('Script Flow Example')
>>> sqd.addFlow(['Node 1','Node 2','CER'])
>>> sqd.addFlow(['Node 2','Node 1','CEA'])
>>> sqd.addFlow(['Node 1','Node 2','CCR-I'])
>>> sqd.addFlow(['Node 2','Node 1','CCA-I'])
>>> sqd.addFlow(['Node 1','Node 2','CCR-T'])
>>> sqd.addFlow(['Node 2','Node 1','CCA-T'])
>>> sqd.addFlow(['Node 1','Node 2','DPR'])
>>> sqd.addFlow(['Node 2','Node 1','DPA'])
>>> sqd.drawPicture()
[Flowdiagram] File created Successfully...
[Flowdiagram] Path : C:\Users\myUser\Flowdiagram.png
>>>
```

![Flowdiagram_2.png!](https://github.com/vaseemkhn18/FlowDiagram/blob/master/src/Flowdiagram_2.png "Flowdiagram")

### flowdiagram.drawPicture(<span style="color:blue">str</span>)
This method is used to create IMAGE of Sequence/Flow Diagram via file.
This method takes file path as an argument.
File content [Example](#Generate Sequence Diagram via flow text file)
For Example:
```
>>> from flowdiagram  import flowdiagram
>>> sqd = flowdiagram()
>>> myFile = 'C:\\Users\\myUser\\callflow.txt'
>>> sqd.drawPicture(myFile)
[Flowdiagram] File created Successfully...
[Flowdiagram] Path : C:\Users\myUser\Flowdiagram.png
>>>
```
![Flowdiagram_2.png!](https://github.com/vaseemkhn18/FlowDiagram/blob/master/src/Flowdiagram_2.png "Flowdiagram")

