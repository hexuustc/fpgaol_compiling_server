import os
from edalize import get_edatool
import time

vivado_exec = '/opt/Xilinx/Vivado/2020.2/bin/vivado'
vivado_tools_dir = 'vivado_tools'
vivado_ip_dir = 'vivado_tools/ip'
tcl_build = 'build.tcl'
vivado_mode = 'tcl'
# vivado_mode = 'batch'

def compile(jobdir, id, filenames, device):
    print(jobdir, id, filenames, device)
    tcl_build_path = os.path.join(os.getcwd(), vivado_tools_dir, tcl_build)
    ip_dir = os.path.join(os.getcwd(), vivado_ip_dir)
    work_root = os.path.join(jobdir, id)
    os.system(vivado_exec + ' -mode ' + vivado_mode + ' -source ' + tcl_build_path + 
            ' -tclargs ' + work_root + ' ' + device + ' ' + ip_dir)

# def compile(jobdir, id, filenames, device):
    # print(jobdir, id, filenames, device)
    # # time.sleep(5)
    # # return
    # name = id
    # tool_options = {
        # 'part': device,
    # }

    # work_root = os.path.join(jobdir, id)

    # files = []
    # for filename in filenames:
        # _, extension = os.path.splitext(filename)
        # filetype = {'.v': 'verilogSource', '.xdc': 'xdc'}[extension]
        # files.append({'name': filename, 'file_type': filetype})

    # tool = 'vivado'
    # edam = {
        # 'files': files,
        # 'name': name,
        # 'tool_options': {'vivado': tool_options},
    # }

    # backend = get_edatool(tool)(edam=edam, work_root=work_root)
    # backend.configure()
    # backend.build()

