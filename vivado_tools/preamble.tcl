# top module should be called "top"
if { $argc != 3 } {
        puts "Usage: build.tcl proj_path device ip_dir"
		exit
    }

set proj_path [lindex $argv 0]
set device [lindex $argv 1]
set ip_dir [lindex $argv 2]
cd $proj_path

# create_project -part $device -force v_proj
# set_property target_language Verilog [current_project]

# use non-project mode

create_project -in_memory 
set_part $device
# set_part xc7a100tcsg324-1

#read_ip $ip_dir/clk_wiz_0/clk_wiz_0.xci
#upgrade_ip -quiet [get_ips *]
#generate_target {all} [get_ips *]

read_verilog [glob ./*.v]
read_xdc [glob ./*.xdc]

set outputDir ./results
file mkdir $outputDir

