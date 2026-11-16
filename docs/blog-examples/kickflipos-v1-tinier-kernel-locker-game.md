# Making My Tiny Linux OS Tinier: An 88% Smaller Kernel, a Save Disk and a Real-Time Game in Shell

**Author:** Sam Burwood

**Versions covered:** Linux 6.18.63, BusyBox 1.36.1, GRUB 2.12, QEMU on Ubuntu 24.04, GitHub Actions (`ubuntu-24.04` runner)
**Reading time:** ~10 minutes
**Repo:** [github.com/samburwood23/kickflipOS](https://github.com/samburwood23/kickflipOS)

---

## TL;DR

> KickflipOS v1 builds its own Linux kernel and BusyBox from source instead of borrowing Ubuntu's.
> The kernel went from 15 MB to 1.8 MB and the whole ISO from 21 MB to 7.9 MB. **The surprise was
> that the smallest kernel I could build still needed 672 options switched on, and getting the last
> two right was the hardest part:** the new kernel booted to a black screen until I found out how
> GRUB hands the display over. Along the way KickflipOS got a "locker" disk that saves your high
> scores, a real-time skate game written entirely in shell, and a GitHub Action that boots every
> build three times in QEMU.

---

## Where It Started

[Version 0](kickflipos-tiny-linux-os.md) of KickflipOS was a kernel, BusyBox and ~260 lines of
shell, all copied from my Ubuntu install. It worked, but it had three problems:

- **It only built on Ubuntu**, because `build.sh` copied `/boot/vmlinuz-$(uname -r)` and `/bin/busybox`.
- **It forgot everything at power-off.** The whole OS lives in RAM.
- **Nothing tested it but me.** Every change meant booting VirtualBox and poking around by hand.

### Baseline Metrics

Measured with `ls -l` on the build output, building on the same Ubuntu 24.04 machine:

| | v0 (borrowed) |
| --- | --- |
| Kernel (`vmlinuz`) | 15.1 MB (Ubuntu's 6.8 generic kernel) |
| initramfs | 2.2 MB |
| Bootable ISO | 21.0 MB |
| Can anyone else build it? | Only on Ubuntu, with that exact kernel installed |

---

## The Plan

1. **Build my own kernel and BusyBox from source** at pinned versions.
2. **Add a locker**: a virtual disk that keeps `/root` between boots.
3. **Write a real-time game**, because the existing one (`skate`) is turn-based.
4. **Automate it**: build and boot-test every push on GitHub.

---

## Part 1: A Kernel With Only What KickflipOS Needs

### Why Ubuntu's kernel is 15 MB

Ubuntu's kernel has to boot on almost any PC ever made. Counting options in the two configs
(`grep -c '=y$'` and `grep -c '=m$'`):

| | Built in (`=y`) | Loadable modules (`=m`) |
| --- | --- | --- |
| Ubuntu 24.04 generic | 3,074 | 6,275 (155 MB in `/lib/modules`) |
| KickflipOS | 672 | 0 |

KickflipOS only ever runs on one kind of hardware: a VirtualBox or QEMU virtual machine. So the
kernel only needs that VM's disk controller, keyboard and display.

### Starting from nothing

The kernel has a target for exactly this: `make tinyconfig` produces the smallest config that
still compiles. It can't boot anything useful, so on top of it I apply a fragment of 46 options,
grouped by what they're for:

```
# Boot from an initramfs
CONFIG_BLK_DEV_INITRD=y
CONFIG_RD_GZIP=y
CONFIG_DEVTMPFS=y

# Hardware: PCI, ACPI (so `bail` can power off), keyboard
CONFIG_PCI=y
CONFIG_ACPI=y
CONFIG_KEYBOARD_ATKBD=y

# Disks for the locker: VirtualBox IDE (PIIX) and SATA (AHCI), ext2 via ext4
CONFIG_ATA_PIIX=y
CONFIG_SATA_AHCI=y
CONFIG_EXT4_FS=y
CONFIG_EXT4_USE_FOR_EXT2=y
```

`ACPI` is the one I'd have forgotten. Without it, `poweroff -f` halts the CPU but the VM window stays
open, because there's nothing to tell the virtual hardware to switch off.

### Making sure the options actually stick

Kconfig quietly drops any option whose dependencies aren't met. You ask for `CONFIG_FB_VESA=y`,
something it depends on is off, and the final `.config` just doesn't have it. No error.

That's the same trap as last time, when `2>/dev/null` hid a missing command. So this time
`build.sh` checks every line of the fragment against the final config and refuses to continue
if one didn't make it:

```sh
check_fragment() { # .config fragment
  grep -E '^(CONFIG_|# CONFIG_)' "$2" | while IFS= read -r line; do
    case "$line" in
      "# CONFIG_"*) name=${line#\# }; name=${name%% *}
                    if grep -q "^$name=" "$1"; then echo "  $name should be off" >&2; exit 1; fi ;;
      *)            if ! grep -qx "$line" "$1"; then echo "  $line didn't stick" >&2; exit 1; fi ;;
    esac
  done || { echo "Config check failed for $1 (a dependency is probably missing)" >&2; exit 1; }
}
```

### Pinning the source

`versions.sh` names an exact tag *and* commit hash for each project. `build.sh` does a shallow
`git clone` and refuses to build if `git rev-parse HEAD` doesn't match, so every build, on my
laptop or in CI, compiles exactly the same code.

BusyBox gets the same treatment. Building it myself fixed last time's font bug properly: Ubuntu's
BusyBox doesn't include `setfont`, but mine does (`CONFIG_SETFONT=y`). I no longer have to copy
the real `setfont` and its libraries in from Ubuntu.

### The bug: a black screen

The new kernel booted fine in text mode. The **KickflipOS - drop in** entry, which asks GRUB for
800×600 graphics, showed a black screen. It was the right resolution, so GRUB had set the mode,
but nothing was drawn on it.

**What I checked first.** I booted with a serial log (`console=ttyS0 console=tty0 loglevel=7`).
There were no `vesafb` lines at all, even though `FB_VESA` was in the config and `vesafb.o` had
been compiled. So the driver existed but never found a device to drive.

**What shifted my thinking.** I booted the same kernel with QEMU's `-kernel` and `vga=0x315`,
which makes the kernel's own setup code switch video modes instead of GRUB. Then the log said:

```
vesafb: mode is 800x600x24, linelength=2400, pages=10
fb0: VESA VGA frame buffer device
```

The driver works. The difference is how the mode gets handed over. GRUB describes the screen in a
way that the kernel's firmware-framebuffer code (`sysfb`) only turns into a device if
`CONFIG_SYSFB_SIMPLEFB` is on. Ubuntu's kernel has it on, which is why v0 never hit this.

**The fix** was two more lines in the fragment:

```
# GRUB's gfxpayload hands over the mode as a 'simple framebuffer'
CONFIG_SYSFB_SIMPLEFB=y
CONFIG_FB_SIMPLE=y
```

---

## Part 2: The Locker

The idea is simple: attach a small blank virtual disk, and KickflipOS mounts it at `/root`. High
scores, files and shell history then survive reboots. Two things made it harder than it sounds.

### Never format the wrong disk

`init` formats the locker automatically on first boot. That's convenient, and dangerous if
someone attaches a disk that has data on it. So it only formats a disk that already has the
locker label, or one whose first megabyte is **all zero bytes**, which is how a freshly created
VirtualBox disk starts out:

```sh
for d in /dev/sda /dev/sdb /dev/sdc; do
  [ -b "$d" ] || continue
  if ! blkid "$d" | grep -q 'LABEL="kickflip"'; then
    [ -z "$(head -c 1048576 "$d" | tr -d '\000' | head -c 1)" ] || continue
    mke2fs -L kickflip "$d" >/dev/null 2>&1 || continue
    fresh=1
  fi
  if mount -t ext2 -o sync "$d" /root; then
    ...
```

`tr -d '\000'` deletes the zero bytes. If anything is left, the disk isn't blank and gets skipped.

### Surviving the VM window's close button

BusyBox's `mke2fs` makes ext2, which has no journal, and BusyBox has no `fsck` to repair it. People
*will* close the VirtualBox window instead of typing `bail`. So the locker is mounted with
`-o sync`: every write goes straight to disk. That's slow for big files, but a high score is a few
bytes, and nothing gets stuck in a cache when the power goes.

One more surprise: the kernel's ext2 driver is marked **DEPRECATED** in 6.18. The ext4 driver can
mount ext2 filesystems instead (`CONFIG_EXT4_USE_FOR_EXT2=y`), so that's what KickflipOS uses.

---

## Part 3: A Real-Time Game in Shell

**Street Cruise** is a side-scroller: cones roll towards you, SPACE ollies over them, and K
kickflips in the air for bonus points. It's 143 lines of BusyBox `ash`.

### The trick: waiting for a key *is* the frame timer

```sh
while :; do
  key=""
  IFS= read -r -t $delay -n 1 key     # wait up to $delay seconds for one key
  ...move the street, check for a crash, draw...
done
```

BusyBox's `read` accepts fractional timeouts, so `-t 0.10` gives about 10 frames a second, dropping
to `0.045` as your score climbs. Every frame uses only shell built-ins (`printf`, `${track:8:1}`
substrings, `$RANDOM`), so the loop never starts a new process. That's what keeps it smooth on a
VM with one CPU.

### Three bugs, all found by actually playing it

I played it in QEMU by sending keypresses through QEMU's monitor (`sendkey spc`) and taking
screenshots (`screendump`):

| What the screenshot showed | Cause | Fix |
| --- | --- | --- |
| "cones cleared 0", no matter how often I pressed space | `read` splits on `$IFS`, which includes space, so a space keypress reads as an empty string | `IFS= read -r` |
| `sh: %: invalid format` in mid-air | The kickflip animation draws the board as `%`, and I passed it as `printf`'s format string | `printf "%s" "$board"` |
| Pressing Q straight after a crash did nothing | The code that discards keys mashed during the crash ran *after* printing "Q to quit", so it ate the Q | Drain the keys *before* printing the prompt |

The first one is a classic, and I'd still never have spotted it by reading the code.

---

## Part 4: Every Push Gets Booted

`tests/smoke_test.py` uses only the Python standard library and boots the OS three times:

1. **On a serial console, with a blank disk.** It runs `trick`, `ollie`, `stoke` and `locker`,
   writes a high score, and types `bail`. If the VM doesn't exit, ACPI power-off is broken.
2. **Again, on the same disk.** The high score must still be there. Then it starts `cruise`,
   doesn't press anything, and waits for the first cone to hit.
3. **From the real ISO, through GRUB, on a virtual screen.** This is the path a VirtualBox user
   takes, and the one the black-screen bug lived on.

For the third boot there's no text to read, so the test reads pixels instead. KickflipOS repaints
console colour 0 to "asphalt" (`#15151a`) at boot. The test takes screenshots until more than half
the sampled pixels are exactly that colour. That one check proves GRUB loaded the kernel, the
framebuffer works, `init` ran and `skatecolors` ran. On a good build it reads 98%.

A GitHub Action runs `build.sh` and the test on every push. It takes about 6 minutes, mostly
compiling the kernel, and saves the final screenshot so I can see what the build looked like.

---

## Final Results

### Metrics

Same method as the baseline: `ls -l` on the build output. Build time is wall-clock `time ./build.sh`
on a 4-core cloud VM with nothing cached.

| | v0 (borrowed) | v1 (built from source) | Change |
| --- | --- | --- | --- |
| Kernel | 15.1 MB | 1.8 MB | **−88%** |
| initramfs | 2.2 MB | 1.3 MB | −41% |
| Bootable ISO | 21.0 MB | 7.9 MB | **−63%** |
| First build | seconds (nothing to compile) | 2 min 27 s | slower, once |
| Rebuild after editing a script | seconds | seconds | same |
| Automated checks per build | 0 | 16 | |

The initramfs shrank even though my BusyBox (2.5 MB, statically linked) is a little *bigger* than
Ubuntu's (2.1 MB). v0 also had to carry `setfont` and a full copy of glibc, and v1 doesn't.

### What Else Changed

- **It builds on any Linux machine** with a compiler, not just Ubuntu with the right kernel.
- **Every push is tested** on GitHub, on a machine that has never seen KickflipOS before.
- **Progress is saved** if you attach a locker.

---

## Lessons Learned

- **Check that config options stuck.** Kconfig silently drops options with missing dependencies,
  just as `2>/dev/null` silently hid a missing command last time. A ten-line check in `build.sh`
  turns "silently wrong" into "fails loudly".
- **When a driver compiles but never prints anything, look at how the hardware is handed over.**
  `vesafb` was fine. GRUB's `gfxpayload` just describes the screen in a way only
  `SYSFB_SIMPLEFB` turns into a device. Booting with `vga=` instead of GRUB isolated that in one try.
- **A real-time game needs a real player.** All three game bugs were invisible in the code and
  obvious in a screenshot after a few seconds of play.
- **Test the path users take.** Booting with QEMU's `-kernel` is fast and handy for the serial
  tests, but it skips GRUB, and GRUB was where the black screen lived.
- **What I'd do differently:** write the pixel check first. Using "is the screen mostly asphalt?"
  as an end-to-end test would have caught the black screen before I'd built anything else.

---

## When NOT to Do This

- **If you just want an OS that works:** borrowing your distro's kernel (v0) is a perfectly good
  way to start. Compiling your own costs an extra 2.5 minutes per clean build and needs ~2 GB of
  disk for the kernel source.
- **If you'd need many drivers:** a tinyconfig kernel boots on exactly the VMs it was made for.
  Real hardware needs real drivers. At that point, [Buildroot](https://buildroot.org) manages
  configs, toolchains and packages for you.

---

## Further Reading

- [Kernel docs: Kconfig and `make tinyconfig`](https://docs.kernel.org/kbuild/kconfig.html)
- [Kernel docs: the framebuffer console](https://docs.kernel.org/fb/fbcon.html)
- [GRUB manual: `gfxpayload`](https://www.gnu.org/software/grub/manual/grub/html_node/gfxpayload.html)
- [Part one: building the first version of KickflipOS](kickflipos-tiny-linux-os.md)
- [The KickflipOS repo](https://github.com/samburwood23/kickflipOS): `./build.sh`, boot, type `cruise`
