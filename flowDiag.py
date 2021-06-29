import sys
import os
import collections
from multipledispatch import dispatch
import six
import subprocess
import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw

PIXEL_ON = 0  # PIL color to use for "on"
PIXEL_OFF = 255  # PIL color to use for "off"

class flowDiag(object):
	
    def __init__(self):
        self.title = ''
        self.fileName = ''
        self.maxLen = 0
        self.node = []
        self.flow = collections.OrderedDict()
        self.infile = False
        self.fd = None
    
    def readFile(self):
        
        six.print_("Reading File......")
        with open(self.fileName,'r') as fd:
            line_num = 0
            sig_cnt = 0
            for line in fd:
                line_num += 1
                if line.find('title') != -1:
                    self.title = line.strip('title').strip(' ')
                    pass
                
                if line.replace('\n',''):
                    if line.find('->') != -1:
                        res = line.split(':')[0].split('->')
                        if len(res) == 2:
                            if str(res[0]) not in self.node:
                                self.node.append(str(res[0]))
                            
                            if str(res[1]) not in self.node:
                                self.node.append(str(res[1]))
                            
                            tag = line.split(':',1)
                            tag = tag[1].strip(' ')
                            
                            if len(tag) > self.maxLen:
                                self.maxLen = len(tag)
                            
                            lst = [str(res[0]), str(res[1]), str(tag)]
                            self.flow[sig_cnt] = lst
                            sig_cnt += 1
                        
                        if len(res) != 2:
                            six.print_("Invalid line !!!!")
                            six.print_(str(self.fileName) + ".. " + str(line_num) + "....."+ str(line))
                            sys.exit(1)
            return 0
        six.print_("Unable to Open File : ",self.fileName)
        sys.exit(1)
    
    @dispatch(str)
    def drawCmdLine(self,file_name):
        
        self.fileName = file_name
        self.readFile()
        self.infile = False
        self.printFlow()
        
            
    @dispatch()
    def drawCmdLine(self):
        
        self.getNodes()
        self.infile = False
        print(self.flow)
        self.printFlow()
            
    @dispatch(list)
    def addflow(self,lis):
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
        
        self.title = str(name)
            
    def drawPicture(self,file_name):
        
        with open('textimg.txt','w') as fd:
            self.fileName = file_name
            self.readFile()
            self.infile = True
            self.fd = fd
            self.printFlow()
            fd.close()
            
            image = self.text_image('textimg.txt')
            image.save('text2img.png')
            
            if os.path.isfile('textimg.txt'):
                os.remove('textimg.txt')
            
            
    def text_image(self,text_path):
        
        grayscale = 'L'
        # parse the file into lines
        with open(text_path) as text_file:  # can throw FileNotFoundError
            lines = tuple(l.rstrip() for l in text_file.readlines())
            
        large_font = 20  # get better resolution with larger size
        font_path = 'cour.ttf'  # Courier New. works in windows. linux may need more explicit path
        try:
            font = PIL.ImageFont.truetype(font_path, size=large_font)
        except IOError:
            font = PIL.ImageFont.load_default()
        
        # make the background image based on the combination of font and lines
        pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
        max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
        # max height is adjusted down because it's too large visually for spacing
        test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        max_height = pt2px(font.getsize(test_string)[1])
        max_width = pt2px(font.getsize(max_width_line)[0])
        height = max_height * len(lines)  # perfect or a little oversized
        width = int(round(max_width + 40))  # a little oversized
        image = PIL.Image.new(grayscale, (width, height), color=PIXEL_OFF)
        draw = PIL.ImageDraw.Draw(image)

        # draw each line of text
        vertical_position = 5
        horizontal_position = 5
        line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
        for line in lines:
            draw.text((horizontal_position, vertical_position),
                      line, fill=PIXEL_ON, font=font)
            vertical_position += line_spacing
        # crop the text
        c_box = PIL.ImageOps.invert(image).getbbox()
        image = image.crop(c_box)
        return image
        
    def printFlow(self):
        nodes = {}
        for i,v in enumerate(self.node):
            nodes[str(v)] = i
        
        dist = self.maxLen + 6
        title = " "*dist + str(self.title)
        node_line = ""
        counter = 0
        word_len = 0
        gap = 0
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
            six.print_(node_line)
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
        go_on = 0
        row_padding = " "*3 + "|"
        draw = False
        gapf = True
        incall = False
        last_incall = False
        while(max_row):
            if not self.infile:
                six.print_(row_padding,end="")
            else:
                self.fd.write(row_padding)
            if not goon:
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
                                six.print_(signal[2].strip() + " "*(self.maxLen + word_len + 3 - int(len(signal[2].strip()))) + "|",end="")
                            else:
                                self.fd.write(signal[2].strip() + " "*(self.maxLen + word_len + 3 - int(len(signal[2].strip()))) + "|")
                        elif last_incall:
                            if j == start-1:
                                if goon == 0:
                                    if not self.infile:
                                        six.print_(" "*(self.maxLen + word_len + 3) + "|" + signal[2].strip(),end="")
                                    else:
                                        self.fd.write(" "*(self.maxLen + word_len + 3) + "|" + signal[2].strip())
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
            if not goon:
                max_row -= 1
            
    def getNodes(self):
        
        for v in self.flow.values():
            if str(v[0]) not in self.node:
                self.node.append(str(v[0]))
            
            if str(v[1]) not in self.node:
                self.node.append(str(v[1]))
                
            if len(v[2]) > self.maxLen:
                self.maxLen = len(v[2])