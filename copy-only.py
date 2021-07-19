import shutil
import subprocess

print("Starting Plot Copy to USB...")
subprocess.call("gnome-terminal -- rsync -ahu --progress --remove-source-files /mnt/sdb/thread1/*.plot /mnt/SEA-8TB-1/", shell=True)
subprocess.call("gnome-terminal -- rsync -ahu --progress --remove-source-files /mnt/sdb/thread2/*.plot /mnt/SEA-8TB-2/", shell=True)
