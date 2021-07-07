import six
import sys
import os
from flowdiagram import flowdiagram

def main():
    res = sys.argv
    if len(res) == 2:
        try:
            action = res[1]
            if action == "create":
                file_path = six.moves.input("[Flowdiagram] Please Provide Flow File Path (i.e. .txt file) : ")
                    
                if os.path.splitext(file_path)[1].strip('.') != 'txt':
                    six.print_("[Flowdiagram] Invalid File!!!")
                    sys.exit(1)
                
                if not os.path.isfile(file_path):
                    six.print_("[Flowdiagram] File does not exist!!!!")
                    sys.exit(1)
                    
                diagram = flowdiagram()
                
                six.print_("[Flowdiagram] What you want to do create ?")
                run = True
                while(run):
                    mode = six.moves.input("[Flowdiagram] 1 : Create Flow on command line \n[Flowdiagram] 2 : Create Flow picture \n[Flowdiagram] 3 : Exit\n[Flowdiagram] Your Choice : ")
                    
                    if mode == '1' or mode == '2' or mode == '3':
                        run = False
                    else:    
                        six.print_("[Flowdiagram] Invalid Input!!! \n[Flowdiagram] Please Choose from 1 , 2 , 3")
                
                if mode == '1':
                    diagram.drawCmdLine(file_path)
                elif mode == '2':
                    diagram.drawPicture(file_path)
                else:
                    six.print_("BYE BYE!!")
                    sys.exit(1)
            else:
                six.print_("[Flowdiagram] Invalid Action!!! \n[Flowdiagram] Use python -m flowdiagram create")
                sys.exit(1)
        except KeyboardInterrupt:
            six.print_("\n[Flowdiagram] Interrupted by User!!!")
    else:
        six.print_("[Flowdiagram] Invalid Command !! \n[Flowdiagram] Use python -m flowdiagram create")

if  __name__ == '__main__':
    main()