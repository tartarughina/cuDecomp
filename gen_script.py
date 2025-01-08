from jinja2 import Environment, FileSystemLoader
import os

template_name = 'script_template.j2'

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template(template_name)

def render_script(context, name, log, bin, exec, def_arg, nodes, types, sizes, opt_args):
    context["name"] = name
    context["log_path"] = log
    context["bin_path"] = bin
    context["exec"] = exec
    context["def_arg"] = def_arg

    for node in nodes:
        context['nodes'] = node

        for type, opt_arg in zip(types, opt_args):
            context['type'] = type
            context['opt_arg'] = opt_arg
            context['sizes'] = sizes[0] if node == 1 else sizes[1]

            with open(f"scripts/{name}_{type}_{node}.sh", "w") as f:
                f.write(template.render(context))

    print(f"{name} scripts rendered successfully!")

# Define rendering context
context = {
    "project_name": "SEEr-Polaris",
    "email": "rstrin4@uic.edu",
    "name": None,
    "type": None,
    "nodes": None,
    "sizes": None,
    "libs": ["$HOME/cuDecomp/lib"],
    "log_path": None,
    "bin_path": None,
    "exec_times": 10,
    "exec": None,
    "def_arg": None,
    "opt_arg": None
}

if 'scripts' not in os.listdir():
    os.mkdir('scripts')

nodes = [1, 2, 4, 8]
types = ['noUM', 'UM', 'UMT', 'OVER1', 'OVER2']

sizes = [[128,256,512], [256]]
opt_args = ['', '--unified_mem', '--unified_mem --um_tuning', '--unified_mem --oversub 1', '--unified_mem --oversub 2']

render_script(context, 'tg', '$HOME/cuDecomp/tg_log', '$HOME/cuDecomp/bin/examples/cc/taylor_green', './tg', '--skip -n ${size}', nodes, types, sizes, opt_args)

sizes = [[256,512,1024], [512]]
opt_args = ['', '--use-managed-memory', '--use-managed-memory --tuning', '--use-managed-memory --oversub 1', '--use-managed-memory --oversub 2']

render_script(context, 'c2c', '$HOME/cuDecomp/c2c_log', '$HOME/cuDecomp/bin/benchmark', './benchmark_c2c', '-b 4 --skip -x ${size} -y ${size} -z ${size}', nodes, types, sizes, opt_args)
