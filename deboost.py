import os
import subprocess
import sys
import time
cputypestring = "vendor_id"
cputypeline = []
cpuinfopath = "/proc/cpuinfo"
amdboostpath = "/sys/devices/system/cpu/cpufreq/boost"
intelboostpath = "sys/devices/system/cpu/intel_pstate"
with open(cpuinfopath, 'r') as f:
    for line in f:
        if line.find(cputypestring) != -1:
            cputypeline.append(line.rstrip('\n'))
cputype = cputypeline[0].split()[2]


def boost_enable():
    if cputype == "AuthenticAMD":
        f=open(amdboostpath, 'w')
        f.write("1")
    elif cputype == "GenuineIntel":
        f=open(intelboostpath, 'w')
        f.write("1")
    sys.exit(0)

proc = subprocess.Popen(sys.argv[1])

def boost_disable():
    if os.path.isdir("/var/lib/optimus-manager"):
        f=open("/var/lib/optimus-manager/tmp/state.json", 'r').read().split("}")[0].split("\"")[11]
        if f != "igpu" and cputype == "AuthenticAMD":
            f=open(amdboostpath, 'w')
            f.write("0")
        elif f != "igpu" and cputype == "GenuineIntel":
            f=open(intelboostpath, 'w')
            f.write("0")
    else:
        print("Switch to hybrid/nvidia mode.")
        sys.exit(1)
try:
    while proc:
        boost_disable()
        time.sleep(10)
except KeyboardInterrupt:
    boost_enable()
finally:
    boost_enable()
