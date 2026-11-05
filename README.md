# Linux Lab

[![Checks](https://github.com/IcaroRamosDM/linux-lab/actions/workflows/checks.yml/badge.svg)](https://github.com/IcaroRamosDM/linux-lab/actions/workflows/checks.yml)

A small Python command-line lab for inspecting a Linux process and its filesystem,
directly or inside a container. It uses only the Python standard library.

## Run

~~~sh
python3 app.py
python3 app.py --json
python3 app.py --directory /tmp --json
make test
~~~

The report includes the operating system, kernel, architecture, Python version,
numeric process UID/GID, the runtime's reported logical CPU count and disk usage.
It does not scan environment variables, credentials or network configuration.
An unavailable directory returns exit status 1 with an error message.
The CPU count is a runtime report and does not establish the container's CPU quota.

## Container

~~~sh
docker build -t linux-lab .
docker run --rm --read-only --network none --cap-drop ALL linux-lab --json
~~~

The image runs as UID/GID 10001 and forwards arguments to the CLI.
The application does not need root privileges or a writable application directory.

## Author

**Icaro Ramos Rodrigues dos Santos**<br>
Electronic Engineer

Embedded Systems | Firmware | C | C++ | Python | Dart | Assembly | Hardware Design | PCB Design | STM32 | ARM Cortex-M | Linux | Windows | RISC-V | Verilog | SystemVerilog | UVM | Design Verification | Instrumentation | Signal Processing | Qt | FLTK

GitHub: [IcaroRamosDM](https://github.com/IcaroRamosDM)<br>
LinkedIn: [icaro-ramos-r](https://www.linkedin.com/in/icaro-ramos-r/)<br>
[icaroelt@gmail.com](mailto:icaroelt@gmail.com)
