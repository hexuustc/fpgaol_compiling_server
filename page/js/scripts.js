$(document).ready(function () {
    $('#exampleled').click(function () {
        $('#inputJobId').val(Math.round(Math.random() * 8388607 + 8388608).toString(16));
        $('#inputXdcFile').text(exampleled[0]);
        $('#inputFile1').text(exampleled[1]);
        $('#XdcFileName').val("fpgaol01.xdc");
        $('#SrcFileName1').val("top.v");
    });
});


var exampleled = [`## This file is a general .xdc for the FGPA OL (adopted from Nexys4 DDR Rev. C)
        ## To use it in a project:
        ## - uncomment the lines corresponding to used pins
        ## - rename the used ports (in each line, after get_ports) according to the top level signal names in the project
        
        ## Clock signal
        #set_property -dict { PACKAGE_PIN E3    IOSTANDARD LVCMOS33 } [get_ports { clk }]; #IO_L12P_T1_MRCC_35 Sch=clk100mhz
        #create_clock -add -name sys_clk_pin -period 10.00 -waveform {0 5} [get_ports { clk }];
        
        
        ## FPGAOL LEDs
        
        set_property -dict { PACKAGE_PIN C17   IOSTANDARD LVCMOS33 } [get_ports { led[0] }]; #IO_L20N_T3_A19_15 Sch=ja[1]
        set_property -dict { PACKAGE_PIN D18   IOSTANDARD LVCMOS33 } [get_ports { led[1] }]; #IO_L21N_T3_DQS_A18_15 Sch=ja[2]
        set_property -dict { PACKAGE_PIN E18   IOSTANDARD LVCMOS33 } [get_ports { led[2] }]; #IO_L21P_T3_DQS_15 Sch=ja[3]
        set_property -dict { PACKAGE_PIN G17   IOSTANDARD LVCMOS33 } [get_ports { led[3] }]; #IO_L18N_T2_A23_15 Sch=ja[4]
        set_property -dict { PACKAGE_PIN D17   IOSTANDARD LVCMOS33 } [get_ports { led[4] }]; #IO_L16N_T2_A27_15 Sch=ja[7]
        set_property -dict { PACKAGE_PIN E17   IOSTANDARD LVCMOS33 } [get_ports { led[5] }]; #IO_L16P_T2_A28_15 Sch=ja[8]
        set_property -dict { PACKAGE_PIN F18   IOSTANDARD LVCMOS33 } [get_ports { led[6] }]; #IO_L22N_T3_A16_15 Sch=ja[9]
        set_property -dict { PACKAGE_PIN G18   IOSTANDARD LVCMOS33 } [get_ports { led[7] }]; #IO_L22P_T3_A17_15 Sch=ja[10]
        
        
        ## FPGAOL SWs
        
        set_property -dict { PACKAGE_PIN D14   IOSTANDARD LVCMOS33 } [get_ports { sw[0]}]; #IO_L1P_T0_AD0P_15 Sch=jb[1]
        set_property -dict { PACKAGE_PIN F16   IOSTANDARD LVCMOS33 } [get_ports { sw[1]}]; #IO_L14N_T2_SRCC_15 Sch=jb[2]
        set_property -dict { PACKAGE_PIN G16   IOSTANDARD LVCMOS33 } [get_ports { sw[2]}]; #IO_L13N_T2_MRCC_15 Sch=jb[3]
        set_property -dict { PACKAGE_PIN H14   IOSTANDARD LVCMOS33 } [get_ports { sw[3]}]; #IO_L15P_T2_DQS_15 Sch=jb[4]
        set_property -dict { PACKAGE_PIN E16   IOSTANDARD LVCMOS33 } [get_ports { sw[4]}]; #IO_L11N_T1_SRCC_15 Sch=jb[7]
        set_property -dict { PACKAGE_PIN F13   IOSTANDARD LVCMOS33 } [get_ports { sw[5]}]; #IO_L5P_T0_AD9P_15 Sch=jb[8]
        set_property -dict { PACKAGE_PIN G13   IOSTANDARD LVCMOS33 } [get_ports { sw[6]}]; #IO_0_15 Sch=jb[9]
        set_property -dict { PACKAGE_PIN H16   IOSTANDARD LVCMOS33 } [get_ports { sw[7]}]; #IO_L13P_T2_MRCC_15 Sch=jb[10]
       
        `,
    `\`timescale 1ns / 1ps
        //////////////////////////////////////////////////////////////////////////////////
        // Company: 
        // Engineer: FPGAOL Dev Group
        // 
        // Create Date: 19.08.2019 13:01:37
        // Design Name: 
        // Module Name: echo
        // Project Name: FPGAOL Example Project
        // Target Devices: 
        // Tool Versions: 
        // Description: 
        // 
        // Dependencies: 
        // 
        // Revision:
        // Revision 0.01 - File Created
        // Additional Comments:
        // 
        //////////////////////////////////////////////////////////////////////////////////
        
        
        module echo(
            input [7:0] sw,
            output [7:0] led
            );
        
        assign led = sw;
        
        endmodule
        `];