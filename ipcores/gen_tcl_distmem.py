ipcore_param = {
    # ip 核的种类
    '_meta_type': 'dist_mem_gen',

    # ip 核的 component name
    '_meta_name': 'ipcore_0',

    ############### 可调整的参数 ↓ ###############
    'depth': 16,
    'data_width': 16,

    # {rom, single_port_ram, simple_dual_port_ram, dual_port_ram}
    'memory_type': 'rom',
    'default_data_radix': '16',     # {2, 10, 16}
    'default_data': '0000',

    # NOTE: vivado creates temporary dir for the ipcore in `.srcs/sources_1/ip/ipcore_name`
    'coefficient_file': '../../../../qwq.coe',
}

def gen_tcl_distmem(ipcore_param):
    output = ''

    name = ipcore_param["_meta_name"]
    output += f'create_ip -name dist_mem_gen -vendor xilinx.com -library ip -version 8.0 -module_name {name}\n'

    for k,v in ipcore_param.items():
        if "_meta_" in k:
            continue
        if v == '':
            continue
        output += f'set_property -dict [list CONFIG.{k} {{{v}}}] [get_ips {name}]\n'

    return output

if __name__ == "__main__":
    print(gen_tcl_distmem(ipcore_param))
