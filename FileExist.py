import os

def FileEx(id,File):
    path = "./jobs/%s/"%id + File
    f_exist = os.path.exists(path)
    if f_exist:
        f_addr = "http://202.38.79.96:18887/%s/%s"%(id,File)
    else:
        f_addr = ""
    return f_addr

def FilesEx(id):
    compiling_log = FileEx(id,"compiling.log")
    timing_rpt = FileEx(id,"results/timing.rpt")
    util_rpt = FileEx(id,"results/util.rpt")
    top_bit = FileEx(id,"results/top.bit")
    return {"bitstream": top_bit,"compiling_log": compiling_log,"timing_rpt": timing_rpt,"util_rpt": util_rpt}
