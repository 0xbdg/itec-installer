import subprocess

fs = subprocess.run(["lsblk", '-ln','-o', 'NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE'],stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=True, check=True).stdout.strip().split('\n')

fs_disk = []

for f in fs:
    dev = f.split(None,4) 
    if dev[2] == "part":
        fs_disk.append(("/dev/"+dev[0] if not len(dev) < 1 else "None", f"size:{dev[1] if not len(dev) < 2 else "None"}|fstype:{"None" if len(dev) < 5 else dev[4]}|mnt:{"None" if len(dev) < 4 else dev[3]}"))

print(len(fs_disk))
if len(fs_disk) <= 0:
    print(True)

else:
    print(False)
