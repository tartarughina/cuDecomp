import os
import subprocess

def get_mode(mode: int) -> str:
    if mode == 0:
        return "noUM"
    elif mode == 1:
        return "UM"
    elif mode == 2:
        return "UMT"
    else:
        return ""


def main():
    grid_sizes = [256, 512, 1024]
    iterations = 5
    output_dir = "bench_log"
    gpus = 4

    os.makedirs(output_dir, exist_ok=True)

    for mode in range(3):
        for size in grid_sizes:
            for i in range(1, iterations+1):

                command = f"mpirun -n {gpus} ./benchmark_c2c -b 4 -x {size} -y {size} -z {size}"

                if mode == 1:
                    command += " -m"
                elif mode == 2:
                    command += " -m -u"

                result_file = os.path.join(output_dir, f"{get_mode(mode)}_gpus_{gpus}_size_{size}_iter_{i}.txt")

                print(f"Running command: {command}")

                # Run the command and capture the output
                with open(result_file, "w") as output_file:
                    subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.STDOUT)

                print(f"Results saved to: {result_file}")


if __name__ == "__main__":
    main()
