import os
from edalize import get_edatool
import time

#vivado_exec = '/opt/Xilinx/Vivado/2020.2/bin/vivado'
vivado_exec = '/tools/Xilinx/Vivado/2019.2/bin/vivado'
vivado_tools_dir = 'vivado_tools'
vivado_ip_dir = 'vivado_tools/ip'
tcl_build = 'build.tcl'
# vivado_mode = 'tcl'
vivado_mode = 'batch'


def compile(jobdir, id, filenames, device, webcode):
    print(jobdir, id, filenames, device, webcode)
    tcl_build_path = os.path.join(os.getcwd(), vivado_tools_dir, tcl_build)
    ip_dir = os.path.join(os.getcwd(), vivado_ip_dir)
    work_root = os.path.join(jobdir, id)
    if (webcode == False):
        os.system('unzip -o ' + work_root + '/' + filenames[0] + ' -d ' + work_root)
    else:
        mypath = '/home/fpgaol2/cedit/code/'+id
        list_dir = os.listdir(mypath)
        
        for file in list_dir:
            filepath = mypath + '/' + file
            os.system('cp '+ filepath + ' ' + work_root)

    os.system(vivado_exec + ' -mode ' + vivado_mode + ' -source ' + tcl_build_path + 
            ' -tclargs ' + work_root + ' ' + device + ' ' + ip_dir)

