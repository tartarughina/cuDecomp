import os
import subprocess

def get_oversub(oversub: int) -> str:
    if oversub == 1:
        return "OVER1"
    elif oversub == 2:
        return "OVER2"
    else:
        return ""


def main():
    grid_sizes = [128, 256, 512]
    iterations = 5
    output_dir = "tg_over_log"
    gpus = 4

    os.makedirs(output_dir, exist_ok=True)

    for oversub in range(1,3):
        for size in grid_sizes:
            for i in range(1, iterations+1):

                command = f"mpirun -n {gpus} ./tg -n {size} -u --oversub {oversub}"

                result_file = os.path.join(output_dir, f"{get_oversub(oversub)}_gpus_{gpus}_size_{size}_iter_{i}.txt")

                print(f"Running command: {command}")

                # Run the command and capture the output
                with open(result_file, "w") as output_file:
                    subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.STDOUT)

                print(f"Results saved to: {result_file}")


if __name__ == "__main__":
    main()
