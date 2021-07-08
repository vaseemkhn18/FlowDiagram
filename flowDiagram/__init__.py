import sys
import os
import collections
from multipledispatch import dispatch
import six
import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw

class flowdiagram(object):
	
    def __init__(self):
        self.title = ''
        self.fileName = ''
        self.maxLen = 0
        self.node = []
        self.flow = collections.OrderedDict()
        self.infile = False
        self.fd = None
    
    def readFile(self):
        # Function to read provided flow file.
        six.print_("[Flowdiagram] Reading File......")
        with open(self.fileName,'r') as fd:
            line_num = 0
            sig_cnt = 0
            mstring = False
            for line in fd:
                line_num += 1
                if line.find('title') != -1:
                    self.title = line.strip('title').strip(' ')
                    pass
                
                if not mstring:
                    if line.replace('\n',''):
                        if line.find('->') != -1:
                            res = line.split(':')[0].split('->')
                            if len(res) == 2:
                                if str(res[0]) not in self.node:
                                    self.node.append(str(res[0]))
                                
                                if str(res[1]) not in self.node:
                                    self.node.append(str(res[1]))
                                
                                tag = line.split(':',1)
                                
                                if "'" == tag[1].strip()[0] and "'" == tag[1].strip()[1] and "'" == tag[1].strip()[2]:
                                    mstring = True
                                
                                tag = tag[1].strip(' ').lstrip('\'')
                                
                                if len(tag) > self.maxLen:
                                    self.maxLen = len(tag)
                                
                                if not mstring:
                                    lst = [str(res[0]), str(res[1]), str(tag)]
                                    self.flow[sig_cnt] = lst
                                    sig_cnt += 1
                            
                            if len(res) != 2:
                                six.print_("[Flowdiagram] Invalid line !!!!")
                                six.print_(str(self.fileName) + ".. " + str(line_num) + "....."+ str(line))
                                sys.exit(1)
                else:
                    tag += line.strip()
                    if tag[-3] == "'" and tag[-2] == "'" and tag[-1] == "'":
                        tag = tag.rstrip('\'')
                        lst = [str(res[0]), str(res[1]), str(tag)]
                        self.flow[sig_cnt] = lst
                        sig_cnt += 1
                        mstring = False
                
            return 0
        six.print_("[Flowdiagram] Unable to Open File : ",self.fileName)
        sys.exit(1)
    
    @dispatch(str)
    def drawCmdLine(self,file_name):
        # Function to create to create Seqeunce Diagram from provided flow file
        self.fileName = file_name
        self.readFile()
        self.infile = False
        self.printFlow()
        
            
    @dispatch()
    def drawCmdLine(self):
        # Function to create to create Seqeunce Diagram from added flow.
        self.getNodes()
        self.infile = False
        self.printFlow()
            
    @dispatch(list)
    def addFlow(self,lis):
        # Function to add flow of Sequence Diagram.
        mylst = []
        if len(lis) == 2:
            mylst.append(lis[0])
            mylst.append(lis[1])
            mylst.append(" ")
        
        if len(lis) == 3:
            mylst.append(lis[0])
            mylst.append(lis[1])
            mylst.append(lis[2])
            
        f_len = len(self.flow)
        
        if len(mylst) != 0:
            self.flow[f_len] = mylst
                
    def setTitle(self,name):
        # Function to set Title of the Sequemce Diagram
        self.title = str(name)
    
    @dispatch(str)
    def drawPicture(self,file_name):
        # Function to create .png file from the provided flow file.
        with open('textimg.txt','w') as fd:
            self.fileName = file_name
            self.readFile()
            self.infile = True
            self.fd = fd
            self.printFlow()
            fd.close()
            
            image = self.textImage('textimg.txt')
            image.save('Flowdiagram.png')
            six.print_("[Flowdiagram] File created Successfully...")
            six.print_("[Flowdiagram] Path : {}".format(os.path.join(os.getcwd(),'Flowdiagram.png')))
            
            if os.path.isfile('textimg.txt'):
                os.remove('textimg.txt')
            
    @dispatch()
    def drawPicture(self):
        # Function to create .png file from the added flow.
        with open('textimg.txt','w') as fd:
            self.getNodes()
            self.infile = True
            self.fd = fd
            self.printFlow()
            fd.close()
            
            image = self.textImage('textimg.txt')
            image.save('Flowdiagram.png')
            six.print_("[Flowdiagram] File created Successfully...")
            six.print_("[Flowdiagram] Path : {}".format(os.path.join(os.getcwd(),'Flowdiagram.png')))
            
            if os.path.isfile('textimg.txt'):
                os.remove('textimg.txt')
    
    def textImage(self,text_path):
        # Function to convert text into image.
        grayscale = 'L'
        PIXEL_ON = 0  # PIL color to use for "on"
        PIXEL_OFF = 255  # PIL color to use for "off"
        with open(text_path) as text_file:
            lines = tuple(l.rstrip() for l in text_file.readlines())
            
        large_font = 20
        font_path = 'cour.ttf'
        try:
            font = PIL.ImageFont.truetype(font_path, size=large_font)
        except IOError:
            font = PIL.ImageFont.load_default()
        
        pt2px = lambda pt: int(round(pt * 96.0 / 72))
        max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
        test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        max_height = pt2px(font.getsize(test_string)[1])
        max_width = pt2px(font.getsize(max_width_line)[0])
        height = max_height * len(lines)
        width = int(round(max_width + 60))
        image = PIL.Image.new(grayscale, (width, height), color=PIXEL_OFF)
        draw = PIL.ImageDraw.Draw(image)

        vertical_position = 5
        horizontal_position = 5
        line_spacing = int(round(max_height * 0.8))
        for line in lines:
            draw.text((horizontal_position, vertical_position),
                      line, fill=PIXEL_ON, font=font)
            vertical_position += line_spacing
        # crop the text
        c_box = PIL.ImageOps.invert(image).getbbox()
        image = image.crop(c_box)
        return image
        
    def printFlow(self):
        # Function to create Sequence Diagram.
        try:
            nodes = {}
            maxScreenSize = 168
            for i,v in enumerate(self.node):
                nodes[str(v)] = i
            
            if  len(self.node)==0:
                six.print_('[Flowdiagram] No Node Found')
                sys.exit(0)
            
            spacepernode = int(maxScreenSize/(len(self.node)))
            if self.maxLen > 44:
                self.maxLen = 44
            
            if self.maxLen > spacepernode:
                self.maxLen = spacepernode-4-len(self.node)
            
            dist = self.maxLen + 4
            title = " "*(int(self.maxLen/2)) + str(self.title)
            node_line = ""
            counter = 0
            word_len = 0
            gap = 0
            
            linnum = 0
            for nod in self.node:
                counter += 1
                if word_len < len(nod):
                    word_len = len(nod)
                if counter != len(self.node):
                    node_line += str(nod) + " "*dist
                else:
                    node_line += str(nod)
            if not self.infile:
                six.print_()
                six.print_()
                six.print_(title)
                six.print_()
                six.print_()
                six.print_(" "*2 + node_line)
            else:
                self.fd.write("\n")
                self.fd.write("\n")
                self.fd.write(title+"\n")
                self.fd.write("\n")
                self.fd.write("\n")
                self.fd.write(node_line+"\n")
                
            max_row = int(len(self.flow)*3)+5
            max_col = int(len(nodes)-1)
            counter = 0
            goon = 0
            row_padding = " "*3 + "|"
            draw = False
            gapf = True
            incall = False
            last_incall = False
            multi_line = False
            maxlinesize = self.maxLen
            note = []
            while(max_row):
                if not self.infile:
                    six.print_(row_padding,end="")
                else:
                    self.fd.write(row_padding)
                if not goon and not linnum:
                    gap += 1
                    if not gapf and counter != int(len(self.flow)-1):
                        counter += 1
                signal = self.flow[counter]
                if nodes[signal[0]] > nodes[signal[1]]:
                    head = "<"
                    start = nodes[signal[1]]
                    lend = nodes[signal[0]]
                    diff = nodes[signal[0]] - nodes[signal[1]]
                else:
                    head = ">"
                    start = nodes[signal[0]]
                    lend = nodes[signal[1]]
                    diff = nodes[signal[1]] - nodes[signal[0]]
                
                if gap < 3:
                    gapf = True
                    
                if gap == 3:
                    gapf = False
                    gap = 0
                
                orig_diff = diff
                
                if (start == lend) and (start == (len(self.node)-1)):
                    last_incall = True
                else:
                    last_incall = False
                
                if int(len(signal[2].strip())) > maxlinesize or  "\n" in signal[2].strip():
                    multi_line = True
                    
                for j in range(max_col):
                    if not gapf:
                        if j == start:
                            draw = True
                            if start == lend:
                                incall = True
                        
                        if j == lend:
                            draw = False
                        
                        if draw:
                            if diff == 1:
                                if head == "<":
                                    if orig_diff == 1:
                                        if not self.infile:
                                            six.print_(head + "-"*(self.maxLen + word_len + 2),end="")
                                        else:
                                            self.fd.write(head + "-"*(self.maxLen + word_len + 2))
                                    else:
                                        if not self.infile:
                                            six.print_("-"*(self.maxLen + word_len + 3),end="")
                                        else:
                                            self.fd.write("-"*(self.maxLen + word_len + 3))
                                if head == ">":
                                    if not self.infile:
                                        six.print_("-"*(self.maxLen + word_len + 2)+ head,end="")
                                    else:
                                        self.fd.write("-"*(self.maxLen + word_len + 2)+ head)
                            else:
                                if head == ">":
                                    if not self.infile:
                                        six.print_("-"*(self.maxLen + word_len + 3),end="")
                                    else:
                                        self.fd.write("-"*(self.maxLen + word_len + 3))
                                else:
                                    if orig_diff == diff:
                                        if not self.infile:
                                            six.print_(head + "-"*(self.maxLen + word_len + 2),end="")
                                        else:
                                            self.fd.write(head + "-"*(self.maxLen + word_len + 2))
                                    else:
                                        if not self.infile:
                                            six.print_("-"*(self.maxLen + word_len + 3),end="")
                                        else:
                                            self.fd.write("-"*(self.maxLen + word_len + 3))
                                diff -= 1
                        elif incall:
                            
                            if goon == 0:
                                if not self.infile:
                                    six.print_("-"*3 + " "*(self.maxLen + word_len),end="")
                                else:
                                    self.fd.write("-"*3 + " "*(self.maxLen + word_len))
                                goon += 1
                                gap = 3
                                incall = False
                            elif goon == 1:
                                if not self.infile:
                                    six.print_("  |" + " "*(self.maxLen + word_len),end="")
                                else:
                                    self.fd.write("  |" + " "*(self.maxLen + word_len))
                                goon += 1
                                gap = 3
                                incall = False
                            else:
                                if not self.infile:
                                    six.print_("<" + "--" +" "*(self.maxLen + word_len),end="")
                                else:
                                    self.fd.write("<" + "--" +" "*(self.maxLen + word_len))
                                goon = 0
                                incall = False
                                gap = 0
                        else:
                            if not self.infile:
                                six.print_(" "*(self.maxLen + word_len + 3),end="")
                            else:
                                self.fd.write(" "*(self.maxLen + word_len + 3))
                                               
                        if not self.infile:
                            six.print_("|",end="")
                        else:
                            self.fd.write("|")
                        
                        if j == len(nodes)-2:
                            if lend == j+1:
                                draw = False
                        
                    else:
                        if gap == 2:
                            if j == start:
                                if not self.infile:
                                    if multi_line:
                                        newLst = signal[2].strip().split("\n")
                                        note = self.detectOverflow(newLst,[])
                                        note = self.makeFlatList(note,[])
                                        six.print_(note[linnum] + " "*(self.maxLen + word_len + 3 - int(len(note[linnum]))) + "|",end="")
                                        linnum+=1
                                        if linnum == len(note):
                                            linnum = 0
                                            multi_line = False
                                    else:
                                        six.print_(signal[2].strip() + " "*(self.maxLen + word_len + 3 - int(len(signal[2].strip()))) + "|",end="")
                                else:
                                    if multi_line:
                                        newLst = signal[2].strip().split("\n")
                                        note = self.detectOverflow(newLst,[])
                                        note = self.makeFlatList(note,[])
                                        self.fd.write(note[linnum] + " "*(self.maxLen + word_len + 3 - int(len(note[linnum]))) + "|")
                                        linnum+=1
                                        if linnum == len(note):
                                            linnum = 0
                                            multi_line = False
                                    else:
                                        self.fd.write(signal[2].strip() + " "*(self.maxLen + word_len + 3 - int(len(signal[2].strip()))) + "|")
                            elif last_incall:
                                if j == start-1:
                                    if goon == 0:
                                        if not self.infile:
                                            if multi_line:
                                                newLst = signal[2].strip().split("\n")
                                                note = self.detectOverflow(newLst,[])
                                                note = self.makeFlatList(note,[])
                                                six.print_(" "*(self.maxLen + word_len + 3) + "|" + note[linnum],end="")
                                                linnum+=1
                                                if linnum == len(note):
                                                    linnum = 0
                                                    multi_line = False
                                            else:
                                                six.print_(" "*(self.maxLen + word_len + 3) + "|" + signal[2].strip(),end="")
                                        else:
                                            if multi_line:
                                                newLst = signal[2].strip().split("\n")
                                                note = self.detectOverflow(newLst,[])
                                                note = self.makeFlatList(note,[])
                                                self.fd.write(" "*(self.maxLen + word_len + 3) + "|" + note[linnum])
                                                linnum+=1
                                                if linnum == len(note):
                                                    linnum = 0
                                                    multi_line = False
                                            else:
                                                self.fd.write(" "*(self.maxLen + word_len + 3) + "|" + signal[2].strip())
                                        if linnum == len(note) or not multi_line:
                                            goon+=1
                                    elif goon == 1:
                                        if not self.infile:
                                            six.print_(" "*(self.maxLen + word_len + 3) + "|---",end="")
                                        else:
                                            self.fd.write(" "*(self.maxLen + word_len + 3) + "|---")
                                        goon+=1
                                    elif goon == 2:
                                        if not self.infile:
                                            six.print_(" "*(self.maxLen + word_len + 3) + "|  |",end="")
                                        else:
                                            self.fd.write(" "*(self.maxLen + word_len + 3) + "|  |")
                                        goon+=1
                                    else:
                                        if not self.infile:
                                            six.print_(" "*(self.maxLen + word_len + 3) + "|<--",end="")
                                        else:
                                            self.fd.write(" "*(self.maxLen + word_len + 3) + "|<--")
                                        goon = 0
                                        last_incall = False
                                else:
                                    if not self.infile:
                                        six.print_(" "*(self.maxLen + word_len + 3) + "|",end="")
                                    else:
                                        self.fd.write(" "*(self.maxLen + word_len + 3) + "|")
                            else:
                                if not self.infile:
                                    six.print_(" "*(self.maxLen + word_len + 3) + "|",end="")
                                else:
                                    self.fd.write(" "*(self.maxLen + word_len + 3) + "|")
                        else:
                            if not self.infile:
                                six.print_(" "*(self.maxLen + word_len + 3) + "|",end="")
                            else:
                                self.fd.write(" "*(self.maxLen + word_len + 3) + "|")
                            
                if counter == int(len(self.flow)-1) and gapf == False:
                    if not self.infile:
                        six.print_()
                        six.print_(row_padding,end="")
                        six.print_((" "*(self.maxLen + word_len + 3) + "|" )*max_col)
                    else:
                        self.fd.write("\n")
                        self.fd.write(row_padding)
                        self.fd.write((" "*(self.maxLen + word_len + 3) + "|" )*max_col)
                    break
                
                if not self.infile:
                    six.print_()
                else:
                    self.fd.write("\n")
                if not goon and not linnum:
                    max_row -= 1
        except KeyboardInterrupt:
            six.print_("\n[Flowdiagram] Interrupted by User!!!")
            
    def getNodes(self):
        # Function to fetch nodes from the added flow.
        for v in self.flow.values():
            if str(v[0]) not in self.node:
                self.node.append(str(v[0]))
            
            if str(v[1]) not in self.node:
                self.node.append(str(v[1]))
                
            if len(v[2]) > self.maxLen:
                self.maxLen = len(v[2])
                
    def detectOverflow(self,lst,out):
        #Function to detect if flow message is longer than space between nodes and slice them to required length
        maxlinesize = self.maxLen
        for mystr in lst:
            note = [mystr[x-maxlinesize:x] for x in range(maxlinesize,len(mystr)+maxlinesize,maxlinesize)]
            out.append(note)
        
        return out
    
    def makeFlatList(self,lst,out):
        # Function to convert nested list to single list.
        for i in lst:
            if type(i) == list:
                self.makeFlatList(i,out)
            else:
                out.append(i)
        
        return out
    
    def createflowfile(self):
        # Function to create .txt file from the added Flow.
        six.print_("[Flowdiagram] Making Flow file : flow.txt")
        with open('flow.txt','w') as fw:
            fw.write('title '+ str(self.title) +'\n')
            fw.write('\n')
            for key,val in self.flow.items():
                lst = val
                if '\n' in str(lst[2]):
                    newline = str(lst[0]) + "->" + str(lst[1]) + ": '''" + str(lst[2]) + "'''"
                else:
                    newline = str(lst[0]) + "->" + str(lst[1]) + ": " + str(lst[2])
                fw.write(str(newline)+'\n')
                
            fw.close()
            six.print_("[Flowdiagram] File created Successfully...")
            six.print_("[Flowdiagram] Path : {}".format(os.path.join(os.getcwd(),'flow.txt')))
