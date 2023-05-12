import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ipcores.gen_tcl_clkwiz import gen_tcl_clkwiz
from ipcores.gen_tcl_distmem import gen_tcl_distmem

from ipcores.gen_tcl_clkwiz import ipcore_param     # for test

with open('vivado_tools/preamble.tcl', "r") as f:
    content = f.read()
    print(content)

print(gen_tcl_clkwiz(ipcore_param))

print("""
generate_target all [get_ips]
synth_ip [get_ips]
""")

with open('vivado_tools/epilog.tcl', "r") as f:
    content = f.read()
    print(content)
