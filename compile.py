import os
from edalize import get_edatool


def compile(jobdir, id, filenames, device):
    name = id
    tool_options = {
        'part': device,
    }

    work_root = os.path.join(jobdir, id)

    files = []
    for filename in filenames:
        _, extension = os.path.splitext(filename)
        filetype = {'.v': 'verilogSource', '.xdc': 'xdc'}[extension]
        files.append({'name': filename, 'file_type': filetype})

    tool = 'vivado'
    edam = {
        'files': files,
        'name': name,
        'tool_options': {'vivado': tool_options},
    }

    backend = get_edatool(tool)(edam=edam, work_root=work_root)
    backend.configure()
    backend.build()

