import psutil
import time
import os

THRESHOLD = 75.0
cloud_vm_triggered = False

print("🚀 Starting Local VM Resource Monitoring...")

try:
    while True:
        cpu = psutil.cpu_percent(interval=2)
        memory = psutil.virtual_memory().percent

        print(f"CPU: {cpu}% | Memory: {memory}%")

        if (cpu > THRESHOLD or memory > THRESHOLD) and not cloud_vm_triggered:
            print("\n🔥 Threshold exceeded! Triggering GCP VM...\n")

            os.system(
                "gcloud compute instances create burst-vm-1 "
                "--machine-type=e2-micro "
                "--zone=us-central1-a "
                "--tags=http-server "
                "--metadata-from-file startup-script=start.sh"
            )

            print("✅ Cloud VM Created Successfully!")
            cloud_vm_triggered = True

        time.sleep(5)

except KeyboardInterrupt:
    print("\nStopped by user")
