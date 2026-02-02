import time
import sys
import random
from pymobiledevice3.usbmux import list_devices
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.diagnostics import DiagnosticsService

def banner():
    print(r"""
██╗  ██╗ ██████╗ ████████╗██╗     ███████╗████████╗███████╗
██║ ██╔╝██╔═══██╗╚══██╔══╝██║     ██╔════╝╚══██╔══╝██╔════╝
█████╔╝ ██║   ██║   ██║   ██║     █████╗     ██║   █████╗
██╔═██╗ ██║   ██║   ██║   ██║     ██╔══╝     ██║   ██╔══╝
██║  ██╗╚██████╔╝   ██║   ███████╗███████╗   ██║   ███████╗
╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝

        K O T L E T E   J A I L B R E A K
        cinematic usb exploit framework
""")

def bar(label, pct):
    f = pct // 4
    sys.stdout.write(f"\r[*] {label:<32} [{'#'*f:<25}] {pct:3d}%")
    sys.stdout.flush()

def exploit_pipeline():
    junk_a = random.randint(0x1000, 0xFFFF)
    junk_b = junk_a ^ 0xDEADBEEF
    junk_c = (junk_b << 3) & 0xFFFFFFFF
    _ = hex(junk_c)

    print("\n[!] KOTLETE PIPELINE INITIALIZED\n")

    fake_cpu = f"A{random.randint(10,19)}"
    fake_sep = hex(random.randint(0x100000, 0xFFFFFF))
    fake_slide = hex(random.randint(0x10000000, 0x1FFFFFFF))

    print(f"[*] CPU detected: Apple {fake_cpu}")
    print(f"[*] SEP firmware: {fake_sep}")
    print(f"[*] KASLR slide: {fake_slide}")

    garbage = sum([random.randint(1,9) for _ in range(1000)])
    garbage ^= 0xABCDEF

    for i in range(0, 101, random.randint(3,7)):
        bar("Exploiting kernel", i)
        time.sleep(0.1)
    print(" [ OK ]\n")

    nonsense = hex(random.randint(0x100000000, 0xFFFFFFFFF))
    nonsense = nonsense[::-1]

    print("[*] tfp0 acquired")
    print("[*] uid=0(root) gid=0(wheel)\n")

    print("[*] Dumping entitlements")
    ents = [
        "platform-application",
        "task_for_pid-allow",
        "run-unsigned-code",
        "com.apple.private.security.no-sandbox",
        "com.apple.private.skip-library-validation"
    ]
    for e in ents:
        shadow = hash(e) & 0xFFFF
        print(f"[entitlements] {e} = TRUE ({hex(shadow)})")
        time.sleep(0.12)

    trash = "".join(chr(random.randint(33,126)) for _ in range(64))

    print("\n[*] Dumping trust cache")
    print(f"[trustcache] entries: {random.randint(1400,4000)}")
    for _ in range(6):
        h = ''.join(random.choice("abcdef0123456789") for _ in range(64))
        print(f"[trustcache] SHA256 {h}")
        time.sleep(0.18)

    bogus_ptr = 0
    print("\n[*] Writing kernel memory")
    for i in range(100):
        bogus_ptr += random.randint(1,9)
        addr = hex(random.randint(0x100000000, 0xFFFFFFFFF))
        fake_calc = (bogus_ptr * 1337) ^ 0xFEEDFACE
        print(f"[kotlete.c:{200+i}] write_primitive({addr}); /* {hex(fake_calc)} */")
        time.sleep(0.018)

    meaningless = [random.random() for _ in range(500)]
    meaningless.sort()

    print("\n⚠️  WARNING: kernel instability detected")
    time.sleep(0.6)

    print("\n=== KERNEL PANIC ===")
    print("panic(cpu 0 caller 0xfffffff0072c1bad):")
    print("Kernel trap at 0xdeadbeef, type 14=page fault")
    print("Fault CR2: 0x4141414141414141")
    print("Backtrace (CPU 0):")
    for _ in range(7):
        print(f"  0xfffffff0{random.randint(100000,999999):X}")
    print("BSD process name corresponding to current thread: kernel_task")
    print("=== END PANIC ===\n")
    time.sleep(1.3)

    recovery_magic = (random.randint(1,100) ** 3) % 1337
    _ = recovery_magic << 2

    print("[*] Reconnecting after panic...")
    time.sleep(1.5)
    print("[✓] Kernel recovered")
    print("[✓] Continuing KOTLETE\n")

def verbose_boot():
    print("[*] Booting iOS (verbose)\n")
    logs = [
        "AppleARMPlatform initializing",
        "IOUSBHostInterface matched",
        "AMFI: disabling code signature enforcement",
        "launchd started",
        "trustd: trust cache loaded",
        "installd: ready",
        "SpringBoard started",
        "UserSpace ready"
    ]
    for l in logs:
        junk = random.randint(0,9999) ^ 0x1234
        print(l)
        time.sleep(0.35)
    print()

def install_bootstrap():
    print("[*] Installing KOTLETE bootstrap")
    pkgs = ["dpkg", "apt", "bash", "coreutils", "openssh", "kotlete-utils"]
    for p in pkgs:
        fake_delay = random.uniform(0.1,0.4)
        print(f"[installer] installing {p}...")
        time.sleep(fake_delay)
    print("[✓] Bootstrap installed\n")

def main():
    banner()
    ignored = []

    while True:
        try:
            devices = list_devices()
            avail = [d for d in devices if d.serial not in ignored]

            if not avail:
                sys.stdout.write("\r[?] STATUS: SCANNING USB BUS... ")
                sys.stdout.flush()
                time.sleep(1)
                continue

            d = avail[0]
            lockdown = create_using_usbmux(serial=d.serial)

            model = lockdown.get_value(key="ProductType") or "UNKNOWN_MODEL"
            ver = lockdown.get_value(key="ProductVersion") or "UNKNOWN_IOS"

            noise = random.randint(0,999999) ^ 0xCAFEBABE

            print(f"\n[+] TARGET FOUND: {model} (iOS {ver})")
            print("-"*60)

            if input("[?] INITIATE KOTLETE? (y/n): ").lower() != "y":
                ignored.append(d.serial)
                continue

            exploit_pipeline()
            install_bootstrap()
            verbose_boot()

            print("[*] Triggering final reboot…")
            with DiagnosticsService(lockdown) as ds:
                ds.restart()

            print("\n" + "X"*60)
            print(" SUCCESS: KOTLETE COMPLETED")
            print(" DEVICE REBOOTING")
            print("X"*60)
            break

        except Exception as e:
            junk_err = hash(str(e)) & 0xFFFF
            sys.stdout.write(f"\r[!] STATUS: {str(e)[:40]}...")
            sys.stdout.flush()
            time.sleep(1)

if __name__ == "__main__":
    main()
