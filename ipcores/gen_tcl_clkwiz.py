import json

ipcore_param = {
    # ip 核的种类
    '_meta_type': 'clk_wiz',

    # ip 核的 component name
    '_meta_name': 'ipcore_0',

    ############### 可调整的参数 ↓ ###############
    'CLKOUT1_REQUESTED_OUT_FREQ': '50.000',

    'CLKOUT2_USED': 'false',
    'CLKOUT2_REQUESTED_OUT_FREQ': '23.456',
}

def gen_tcl_clkwiz(ipcore_param):
    output = ''

    name = ipcore_param["_meta_name"]
    output += f'create_ip -name clk_wiz -vendor xilinx.com -library ip -version 6.0 -module_name {name}\n'

    output += f'set_property -dict [list'

    for k,v in ipcore_param.items():
        if "_meta_" in k:
            continue
        if v == '':
            continue
        output += f' CONFIG.{k} {{{v}}}'

    output += f'] [get_ips {name}]\n'

    return output

if __name__ == "__main__":
    print(gen_tcl_clkwiz(ipcore_param))
