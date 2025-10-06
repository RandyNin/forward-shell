
# 🐚 Forward-Shell (Educational Project)

Forward-Shell is an **pentesting tool** that allows simulating an **interactive shell** when you only have access to a simple **webshell**.  
It is especially useful in scenarios where a **firewall or egress restrictions** prevent you from opening a reverse shell connection.  

Instead of being stuck with single-command execution, Forward-Shell uses **named pipes** and **base64-encoded commands** to simulate a pseudo-terminal, making interaction smoother.

---

## 🚀 Features

- 📡 Send commands to a remote webshell
- 💻 Simulate an interactive pseudo-terminal
- 📝 Special commands:
  - `!enum-suid` → Enumerates SUID binaries
  - `!help` → Displays available commands
- 🔒 Useful when reverse shells are blocked by firewalls
- 🧹 Cleanup functions to remove traces (`stdin`, `stdout` pipes)

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/RandyNin/forward-shell.git
cd forward-shell

# Install requirements
pip install -r requirements.txt
````

---

## ⚡ Usage

Example execution:

```bash
python3 main.py -u "http://target.com/shell.php"
```

### Inside Forward-Shell

Once running, you can:

- Type commands directly (e.g., `ls`, `id`, `whoami`)
    
- Use special commands:
    - ``!help``
    - ``!enum-suid``

To simulate a pseudo-terminal:

```bash
script /dev/null -c bash
```

---

## 📚 Requirements

- Python **3.10+**

- `requests` library (for Windows Firefox functionality)
  
-  `termcolor` library (for terminal color display)

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🖼️ Architecture

```text
 Attacker (Forward-Shell)           Victim (Webshell + Firewall)
 ---------------------              ----------------------------
   main.py  ------>  sends cmds  ----X---->  Reverse shell blocked
   forward_shell.py  <------ works via HTTP requests to shell.php
```

---

## ⚠️ Disclaimer

This software is provided **for educational purposes only**.  
It must only be used in **authorized environments** such as labs or CTFs.  
The author assumes **no liability** for any misuse of this code.
