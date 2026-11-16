# Building a Tiny Skateboard-Themed Linux OS (and the Three Bugs That Taught Me How Booting Works)

**Author:** Sam Burwood

**Versions covered:** Ubuntu 24.04 host, VirtualBox (Oracle's repository build), BusyBox 1.36.1, GRUB 2.12
**Reading time:** ~8 minutes
**Repo:** [github.com/samburwood23/kickflipOS](https://github.com/samburwood23/kickflipOS)

---

## TL;DR

> I built KickflipOS, a Linux OS that boots in VirtualBox, greets you with a skater mascot called
> Ollie and ships with a terminal skate game. It's the kernel I was already running, one BusyBox
> binary and about 260 lines of shell and config. **The surprise was how little an "operating
> system" needs to be: the kernel unpacks one archive into RAM and runs one script.** The bugs
> were the interesting part. Ubuntu's VirtualBox wouldn't install, a font command failed silently
> at boot, and the VirtualBox settings screen didn't show the option the guides said it would.
> Each fix was a lesson in not trusting what you assume is there.

---

## The Challenge

### Background

I wanted to understand what actually happens between pressing the power button and seeing a
prompt, and I wanted something more fun than a tutorial distro. So the goal was an OS with a
personality: skateboard-themed boot messages, a mascot, custom colours and a game. I built it by
vibe coding with an AI assistant, describing what I wanted and testing what came back.

The architecture is about as small as Linux gets:

```
GRUB (boot menu) ──▶ Linux kernel ──▶ unpacks initramfs into RAM ──▶ runs /init ──▶ shell
```

- **Kernel:** borrowed from my Ubuntu install (`/boot/vmlinuz-$(uname -r)`). No compiling.
- **Userland:** `busybox-static`, a single binary that provides `sh`, `ls`, `vi`, `mount` and
  about 300 other commands.
- **The OS itself:** an `init` script plus a handful of commands (`skate`, `ollie`, `trick`,
  `bail`...) in a folder called `rootfs/`.
- **Packaging:** `cpio` + `gzip` turn `rootfs/` into an initramfs, and `grub-mkrescue` wraps it
  with the kernel into a bootable ISO.

Here is the whole of "boot", from `rootfs/init`, trimmed:

```sh
#!/bin/busybox sh
/bin/busybox --install -s /bin      # create ls, cat, vi... as symlinks
mount -t proc proc /proc
mount -t sysfs sys /sys
mount -t devtmpfs dev /dev
hostname kickflip
skatecolors                          # repaint the console palette
exec setsid cttyhack sh -l           # hand over to an interactive shell
```

That's the bit that clicked for me. PID 1 is just a program. Whatever it does *is* the OS.

### What Was Going Wrong

Three things broke, in this order.

**1. VirtualBox wouldn't install.** `sudo apt install virtualbox-qt` ended with:

```
Building for 7.0.0-42-generic
Error! Bad return status for module build on kernel: 7.0.0-42-generic (x86_64)
dpkg: error processing package virtualbox-dkms (--configure):
 installed virtualbox-dkms package post-installation script subprocess returned error exit status 10
```

**2. The custom console font never loaded.** The boot script called
`setfont ... 2>/dev/null`. The screen looked normal, there was no error, and the font just
wasn't there.

**3. VirtualBox's Storage settings didn't offer "Choose a disk file…"**, so I couldn't attach the
ISO the way every guide described.

### Why It Mattered

The first bug blocked everything. The second is the kind that survives for months, because a
silent failure in a boot script looks exactly like success unless you know what "right" should
look like. The third cost the most time for the least reason.

### What I Tried First (and Why It Failed)

- **For the font**, the first plan used BusyBox's `setfont` applet, because BusyBox "has
  everything". The build ran fine and the ISO booted fine. Nothing told us the command didn't
  exist, because `2>/dev/null` was throwing the evidence away.
- **For attaching the ISO**, I clicked through the Storage page looking for the CD icon from the
  instructions. The layout varies between VirtualBox 7.x versions, and the option wasn't where
  the guide said.
- **The first boot** looked "done" until we looked at a screenshot: the prompt read `@kickflip:~`
  with no username, BusyBox's own banner sat above the welcome screen, and the game menu scrolled
  off the screen instead of redrawing.

---

## Root Cause

| Symptom | Root cause |
| --- | --- |
| `virtualbox-dkms` build fails | Ubuntu 24.04's packaged VirtualBox (7.0.16) predates the 7.0 kernel series, so its kernel module doesn't compile against the newer kernel APIs |
| Font silently not loaded | Ubuntu's `busybox-static` is built **without** the `setfont` applet. `busybox --list \| grep setfont` prints nothing. |
| `@kickflip` with no username | The prompt's `\u` looks the user up in `/etc/passwd`, and a from-scratch rootfs doesn't have one |
| BusyBox banner on the welcome screen | `ash` prints it when an interactive shell starts, after `init` has already cleared the screen |
| No "Choose a disk file" option | The VM already had an IDE controller, but the settings UI didn't expose the option in this version |

---

## The Solution

### Approach

Stop trusting what *should* be there and check what *is* there: inside the built OS, in the
running VM, and on the actual screen.

### Implementation

#### Step 1: Get VirtualBox from the vendor, not the distro

Clear the half-installed packages, then install from Oracle's repository, whose current release
builds against newer kernels:

```bash
sudo apt purge virtualbox virtualbox-qt virtualbox-dkms
sudo apt install linux-headers-$(uname -r) build-essential
wget -O- https://www.virtualbox.org/download/oracle_vbox_2016.asc \
  | sudo gpg --yes --dearmor --output /usr/share/keyrings/oracle-virtualbox-2016.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/oracle-virtualbox-2016.gpg] https://download.virtualbox.org/virtualbox/debian noble contrib" \
  | sudo tee /etc/apt/sources.list.d/virtualbox.list
sudo apt update && apt-cache search ^virtualbox-   # then install the newest listed
```

#### Step 2: Bundle the real `setfont`, with exactly the libraries it needs

The `setfont` from Ubuntu's `kbd` package turned out to need nothing but libc:

```
$ ldd /usr/bin/setfont
    linux-vdso.so.1
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
    /lib64/ld-linux-x86-64.so.2
```

So `build.sh` copies the binary and whatever `ldd` reports into the rootfs, at the same paths:

```sh
if [ ! -f rootfs/usr/bin/setfont ]; then
  mkdir -p rootfs/usr/bin
  cp "$(command -v setfont)" rootfs/usr/bin/setfont
  for lib in $(ldd "$(command -v setfont)" | grep -o '/[^ ]*'); do
    mkdir -p "rootfs$(dirname "$lib")"
    cp -L "$lib" "rootfs$lib"
  done
fi
```

This pattern works for any small dynamically linked tool you want inside a minimal OS.

#### Step 3: Fix what the screenshot showed

```sh
# rootfs/etc/passwd: one line gives the prompt a username
root:x:0:0:root:/root:/bin/sh
```

Adding `clear` as the first line of `rootfs/etc/profile` hides the BusyBox banner. The skate game
now clears and redraws its menu every turn, with a one-line status message, instead of printing
a new menu below the old one.

#### Step 4: Attach the ISO from the command line

```bash
VBoxManage storageattach KickflipOS --storagectl "IDE" --port 0 --device 0 \
  --type dvddrive --medium ~/kickflipOS/kickflipos.iso
```

If you run `VBoxManage storagectl ... --add ide` first and get
`Storage controller named 'IDE' already exists`, that's good news. The controller is there, and
you can skip straight to `storageattach`.

### Rollout

Every change was tested by booting the ISO in QEMU and taking screenshots through QEMU's monitor
(`screendump`) after typing commands with `sendkey`. That loop is how bugs 2 and 3 were caught
before they reached VirtualBox: `busybox --list` in the test build showed `setfont` missing, and
the screenshots showed the prompt and menu problems.

---

## Results

### Metrics

Measured on the test build (Ubuntu 24.04's 6.8 kernel, `ls -l` on the build output):

| | Size |
| --- | --- |
| Whole bootable ISO | 21 MB |
| ...of which the kernel | 15 MB |
| initramfs (everything that is "KickflipOS", gzipped) | 2.2 MB |
| ...of which BusyBox (uncompressed) | 2.1 MB |
| Hand-written code and config (`wc -l`) | ~260 lines |

The ISO built on your machine will differ slightly, because it uses whichever kernel you're running.

### Qualitative Improvements

- The OS boots with the skate palette, a bold Terminus font, a themed GRUB menu and Ollie's
  welcome screen.
- The whole project fits in one git repo, and `./build.sh` rebuilds it in seconds.
- I now understand the boot process well enough to explain it on one slide.

---

## Lessons Learned

- **`2>/dev/null` in a boot script hides missing commands, not just noise.** Before silencing a
  command, check it exists in the image you're building (`busybox --list`, `ls rootfs/usr/bin`).
  We only found the missing `setfont` because we checked; the boot never complained.
- **Distro packages lag new kernels.** Anything that builds a kernel module (VirtualBox, some GPU
  and Wi-Fi drivers) can break on a kernel newer than the distro release. When `dkms` fails, try
  the vendor's repository before debugging the module.
- **Look at the screen, not just the exit code.** Three of the five problems in the root cause
  table only showed up in a screenshot.
- **When a GUI doesn't match the guide, use the CLI.** `VBoxManage` does exactly the same thing
  regardless of how the settings window is laid out in your version.
- **What I'd do differently:** take a screenshot of the first boot before writing any personality
  code. A two-minute check would have caught the missing username straight away.

---

## Takeaways

### When to Use This Approach

- You want to *understand* Linux booting, not just use a distro.
- You want a fun, finishable side project. This took an afternoon, and a lot of that was the
  VirtualBox install.
- You're teaching someone else how an OS starts up.

### When NOT to Use It

- You want a usable daily OS. There's no package manager, no networking setup and no persistent
  storage. Everything lives in RAM and resets on reboot.
- You want to distribute the ISO. It contains GPL binaries (the kernel and BusyBox) copied from
  your machine, and redistributing them comes with source obligations. The repo deliberately
  `.gitignore`s them and has `build.sh` copy them from your machine instead.

### Alternative Solutions We Considered

- **Linux From Scratch:** builds everything from source. Brilliant for learning, but days of work
  rather than an afternoon.
- **Buildroot:** generates a complete embedded Linux, including a custom kernel. The better choice
  once you want networking or a GUI.
- **Debian `live-build`:** remasters a full distro. The right tool if you want a real desktop OS
  with your own branding.

---

## Further Reading

- [BusyBox](https://busybox.net): what's in the box, and how applets work
- [Kernel docs: ramfs, rootfs and initramfs](https://docs.kernel.org/filesystems/ramfs-rootfs-initramfs.html):
  how the kernel unpacks and runs `/init`
- [Linux From Scratch](https://www.linuxfromscratch.org): the deep end
- [The KickflipOS repo](https://github.com/samburwood23/kickflipOS): `./build.sh`, boot, type `skate`

