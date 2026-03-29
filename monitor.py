import psutil
import time
import os
import subprocess

HIGH_THRESHOLD = 75
LOW_THRESHOLD = 30
COOLDOWN = 60

last_action_time = 0

def is_vm_running():
    result = subprocess.run(
        "gcloud compute instances describe burst-vm-1 --zone=us-central1-a",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.returncode == 0

print("Smart Auto-Scaling Started...\n")

try:
    while True:
        cpu = psutil.cpu_percent(interval=2)
        memory = psutil.virtual_memory().percent

        print(f"CPU: {cpu}% | Memory: {memory}%")

        vm_running = is_vm_running()  # REAL CHECK
        current_time = time.time()

        # SCALE OUT
        if (cpu > HIGH_THRESHOLD or memory > HIGH_THRESHOLD) and not vm_running:
            if current_time - last_action_time > COOLDOWN:
                print("\nScaling OUT (Creating VM)...\n")

                os.system(
                    "gcloud compute instances create burst-vm-1 "
                    "--machine-type=e2-micro "
                    "--zone=us-central1-a "
                    "--tags=http-server "
                    "--metadata-from-file startup-script=start.sh"
                )

                last_action_time = current_time

        # SCALE IN
        elif (cpu < LOW_THRESHOLD and memory < LOW_THRESHOLD) and vm_running:
            if current_time - last_action_time > COOLDOWN:
                print("\nScaling IN (Deleting VM)...\n")

                os.system(
                    "gcloud compute instances delete burst-vm-1 "
                    "--zone=us-central1-a --quiet"
                )

                last_action_time = current_time

        time.sleep(5)

except KeyboardInterrupt:
    print("\nStopped")
