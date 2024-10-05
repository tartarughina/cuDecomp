## Memory footprint

The memory footprint of the library is dependent on the size of the spatial grid. The library requires the following memory allocations:

### tg -n size

- 256: 3200-3300
- 512: 7000-7100
- 1024: 37500-37600

### benchmark_c2c -x size -y size -z size

- 256: 2670-2820
- 512: 4020-4160
- 1024: 14780-14920
- 2048: out of memory

### benchmark_r2c -x size -y size -z size

- 256: 2580-2730
- 512: 3260-3400
- 1024: 8640-8780
- 2048: out of memory

## Oversubscription

The oversubscription of the GPU memory will be implemented as 1.5x and 2x the memory footprint of the benchmark.
As always the oversub will be imposed by allcating a non Unified Memory buffer that will impose any other Unified Memory allocation to be paged out to the host memory.
