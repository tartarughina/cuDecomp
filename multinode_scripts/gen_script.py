from jinja2 import Template

# Load the template
template_content = """
#!/bin/bash -l

#PBS -A {{ project_name }}
#PBS -l walltime=1:00:00
#PBS -l filesystems=home:eagle:grand
#PBS -N {{ name }}_{{ type }}_{{ nodes }}_{{ size }}
#PBS -m bea
#PBS -M {{ email }}
#PBS -V
#PBS -l select={{nodes}}:ncpus=4:ngpus=4
#PBS -r y

{% if nodes == 1 %}
export LD_LIBRARY_PATH={% for lib in libs %}{{lib}}:{% endfor %}$LD_LIBRARY_PATH
{% else %}
export NCCL_NET_GDR_LEVEL=PHB
export NCCL_CROSS_NIC=1
export NCCL_COLLNET_ENABLE=1
export NCCL_NET="AWS Libfabric"
export LD_LIBRARY_PATH={% for lib in libs %}{{lib}}:{% endfor %}/soft/libraries/hwloc/lib:/soft/libraries/aws-ofi-nccl/v1.9.1-aws/lib:$LD_LIBRARY_PATH
export FI_CXI_DISABLE_HOST_REGISTER=1
export FI_MR_CACHE_MONITOR=userfaultfd
export FI_CXI_DEFAULT_CQ_SIZE=131072
{% endif %}

module load craype-accel-nvidia80

# Number of GPUs per rank --> 1:1
ngpus=1
# Number of ranks per node
nranks=4
# Medium batch size is the only one picked for multinode tests

{% if sizes|length == 1 %}
size={{ sizes[0] }}
{% endif %}

# Log dir path
log_path={{ log_path }}

if [ ! -d "$log_path" ]; then
    mkdir -p "$log_path"
fi

NNODES=$(wc -l < $PBS_NODEFILE)
NTOTRANKS=$(( NNODES * nranks ))

cd {{ bin_path }}

{% if sizes|length > 1 %}
for size in{% for size in sizes %} {{ size }}{% endfor %}; do
{% endif %}
for i in {1..{{ exec_times }}}; do
    mpirun --envall --np "${NTOTRANKS}" --ppn "${nranks}" \\
    --hostfile "$PBS_NODEFILE" --cpu-bind list:0,8,16,24 \\
    {{ exec }} {{ def_arg }}{% if def_arg %} {% endif %}{{ opt_arg }}{% if opt_arg %} {% endif %}> "${log_path}/{{ type }}_gpus_${NTOTRANKS}_size_${size}_iter_${i}.txt"
done
{% if sizes|length > 1 %}
done
{% endif %}

"""

# Define rendering context
context = {
    "project_name": "project123",
    "name": "test",
    "type": "performance",
    "nodes": 1,
    "sizes": [1024],
    "email": "user@example.com",
    "libs": ["/path/to/lib1", "/path/to/lib2"],
    "log_path": "/path/to/logs",
    "bin_path": "/path/to/bin",
    "exec_times": 3,
    "exec": "./my_program",
    "def_arg": "--default",
    "opt_arg": ""
}

# Render the template
template = Template(template_content)
output = template.render(context)

# Save to file or print
with open("pbs_script.sh", "w") as f:
    f.write(output)

print("PBS script rendered successfully!")
