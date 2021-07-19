import shutil
import subprocess

total, used, free = shutil.disk_usage("/mnt/sdb")
print("Free: %d GiB" % (free // (2**30)))

while free > 600:
	subprocess.call("~/chia-plotter/build/chia_plot farmkey subjey /mnt/sdb/ /mnt/ramdisk/ 15", shell=True)
	total, used, free = shutil.disk_usage("/mnt/sdb")
	print("Free: %d GiB" % (free // (2**30)))
print("Starting Plot Copy to USB...")
subprocess.call("rsync -ahu --progress --remove-source-files /mnt/sdb/*.plot /mnt/USB-8TB-5/", shell=True)
