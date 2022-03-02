import os
from shutil import copyfile

def LogEx(id):
    path = "./jobs/%s/"%id
    direxist = os.path.exists(path)
    if not direxist:
        return 0
    fileaddr = "./jobs/%s/results/top.bit"%id
    file_exist = os.path.exists(fileaddr)
    source = "./compiling.log"
    target = path + "raw.log"
    result = path + "compiling.log"
    startline = "CompilingPrjid%s\n"%id
    endline = "CompilingPrjid%sFinish\n"%id
    error = ""
    errorline = "ERROR:"
    errorpath = path + "error.log"
    copyfile(source,target)
    with open(source,'w') as f:
        pass
    with open(target,'r') as f:
        with open(result,'w') as fp:
            line = f.readline()
            while line :
                if line == startline:
                    fp.write(line)
                    line = f.readline()
                    while line and line != endline:
                        fp.write(line)
                        if not file_exist:
                            linesplit = line.split()
                            if linesplit:
                                if linesplit[0] == errorline:
                                    error += line
                        line = f.readline()
                    if line == endline:
                        fp.write(line)
                    break
                else:
                    line = f.readline()
    with open(errorpath,'w') as f:
        f.write(error)