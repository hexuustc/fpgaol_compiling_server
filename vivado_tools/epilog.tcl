synth_design -top top
opt_design
place_design
phys_opt_design
route_design

write_bitstream -verbose -force $outputDir/top.bit
report_utilization -file $outputDir/util.rpt
report_timing_summary -file $outputDir/timing.rpt

