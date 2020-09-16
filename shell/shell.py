#! /usr/bin/env python3
import os, sys, re, time

pid = os.getpid()



if "PS1" in os.environ:
    ps1=os.environ["PS1"]
else:
    ps1="$"
commands = ""

while True:
    path = os.getcwd()
    commands = input(ps1)
    commands = commands.strip()
    if commands == "exit":
        break
    elif commands == "":
        break
    else:
        if "|" in commands:
            command = commands.split("|")
            command[0] = command[0].strip()
            command[0] = command[0].strip()
            rc = os.fork()
            if rc == 0:
                pr,pw = os.pipe()
                for f in (pr,pw):
                    os.set_inheritable(f,True)
                parent=os.fork()#forking twice to keep better tracker
                if parent==0:#child is sending output to parent
                    os.close(1)#snippet modified from pipe demo
                    os.dup2(pw,1)
                    for fd in (pr,pw):
                        os.close(fd)
                    tokens=commands[0].split(" ",1)#tokenizing args
                    try:#in case the whole path is given
                        os.execve(tokens[0],tokens,os.environ)
                    except FileNotFoundError:
                        pass
                    for dir in re.split(":",os.environ["PATH"]):#searching for program in PATH
                        program= "%s/%s" % (dir,tokens[0])
                        try:
                            os.execve(program,tokens,os.environ)
                        except FileNotFoundError:
                            pass
                        print(tokens[0] + ": command not found.") 
                else:#parent receives the output of child
                    os.wait()
                    os.close(0)#closed to allow piping
                    os.dup2(pr,0)
                    for fd in (pr,pw):
                        os.close(fd)
                    tokens=commands[1].split(" ",1)#tokenizing the args
                    try:#in case the whole path is given up front
                        os.execve(tokens[0],tokens,os.environ)
                    except FileNotFoundError:
                        pass
                    for dir in re.split(":",os.environ["PATH"]):#searching for the program in PATH.
                        program= "%s/%s" % (dir,tokens[0])
                        try:
                            os.execve(program,tokens,os.environ)
                        except FileNotFoundError:
                            pass
                    print(tokens[0] + ": command not found.")
                    sys.exit()
            else:
                os.wait()
        elif "<" in commands:
            command=commands.split("<")
            command[0],command[1]=command[0].strip(),command[1].strip()
            rc = os.fork()
            if rc==0:
                pr,pw=os.pipe()
                for f in (pr,pw):
                    os.set_inheritable(f,True)
                piping=os.fork()
                if piping==0:
                    os.close(1)
                    os.dup2(pw,1)
                    for fd in (pr,pw):
                        os.close(fd)
                    tokens=command[1].split(" ",1)
                    try:
                        os.execve(tokens[0],tokens,os.environ)
                    except FileNotFoundError:
                        pass
                    for dir in re.split(":",os.environ["PATH"]):
                        program= "%s/%s" % (dir,tokens[0])
                        try:
                            os.execve(program,tokens,os.environ)
                        except FileNotFoundError:
                            pass
                        print(tokens[0] + ": command not found.") 
                else:#now command 0 receives output from command 1
                    os.wait()
                    os.close(0)
                    os.dup2(pr,0)
                    for fd in (pr,pw):
                        os.close(fd)
                    command[0].replace('\n','')
                    tokens=command[0].split(" ",1)
                    try:
                        os.execve(tokens[0],tokens,os.environ)
                    except FileNotFoundError:
                        pass
                    for dir in re.split(":",os.environ["PATH"]):
                        program= "%s/%s" % (dir,tokens[0])
                        try:
                            os.execve(program,tokens,os.environ)
                        except FileNotFoundError:
                            pass
                    print(tokens[0] + ": command not found.")
                    sys.exit()
            else:
                os.wait()
        elif ">" in commands:
            io=commands.split(">")
            io[0]=io[0].strip()
            io[1]=io[1].strip()
            tokens=io[0].split(" ",1)
            if tokens[0] == "exit":
                print("Now exiting shell")
                sys.exit()
            elif tokens[0] == "cd":
                if len(tokens)>1: 
                    try:
                        os.chdir(tokens[1])
                    except FileNotFoundError:
                        print ("No such file or folder")
                        pass
                else:
                    if "HOME" in os.environ:
                        os.chdir(os.environ["HOME"])
                    else:
                        pass
            else:
                rc = os.fork()
                if rc==0:
                    if response!="":
                        os.close(1)
                        sys.stdout=open(io[1],"w")
                        os.set_inheritable(1,True)
                        try:
                            os.execve(tokens[0],tokens,os.environ)
                        except FileNotFoundError:
                            pass
                        for dir in re.split(":",os.environ["PATH"]):
                            program= "%s/%s" % (dir,tokens[0])
                            try:
                                os.execve(program,tokens,os.environ)
                            except FileNotFoundError:
                                pass
                        print(tokens[0] + ": command not found.")
                        sys.exit()
                    else:
                        sys.exit()
                else:
                    os.wait()
        else:
            tokens = commands.split(" ",1)
            if tokens[0] == "cd":
                if len(tokens)>1: 
                    try:
                        os.chdir(tokens[1])
                    except FileNotFoundError:
                        print ("No such file or folder")
                        pass
                else:
                    if "HOME" in os.environ:#couldn't remember if you have to export HOME or not
                        os.chdir(os.environ["HOME"])
                    else:
                        pass
                #else:
                    #os.chdir(path+tokens[1])
                    #if "HOME" in os.environ:#couldn't remember if you have to export HOME or not
                        #os.chdir(os.environ["HOME"])
                    #else:
                        #pass
            if tokens[0] == "ls":
                #do ls stuff
                print("LS was pressed")
            elif tokens[0] == "pwd":
                print(path)
            elif tokens[0] == "sleep":
                if len(tokens) > 1:
                    timetosleep = int(tokens[1])
                    time.sleep(timetosleep)
                else:
                    print("Please enter a time after the sleep command")
            else:
                rc = os.fork()
                if rc == 0:
                    if commands != "":
                        try:#in case the whole path is given
                            os.execve(tokens[0],tokens,os.environ)
                        except FileNotFoundError:
                            pass
                        for dir in re.split(":",os.environ["PATH"]):#searches for the program in PATH
                            program= "%s/%s" % (dir,tokens[0])
                            try:
                                os.execve(program,tokens,os.environ)
                            except FileNotFoundError:
                                pass
                        print(tokens[0] + ": command not found.")  
                        sys.exit()#exits in case it's not found





