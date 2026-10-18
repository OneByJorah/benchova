#!/usr/bin/env python3
"""
System information collector: CPU, RAM, GPU, VRAM, CUDA, drivers, OS, versions.
"""
import json
import platform
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd: str, default=None, shell: bool = False):
    """Run a command and return its stdout.

    Args:
        cmd: Command string. When shell=False, split via shlex.
        default: Value returned on failure.
        shell: Set to True for pipe-based commands (e.g. ``lscpu | grep ...``).
    """
    try:
        args = cmd if shell else shlex.split(cmd)
        out = subprocess.run(args, shell=shell, capture_output=True, text=True, timeout=30)
        return out.stdout.strip() if out.returncode == 0 else default
    except Exception:
        return default


def _first_int(text):
    """Return the first integer found in text, or None."""
    m = re.search(r"\d+", text or "")
    return int(m.group()) if m else None


def collect():
    info = {
        "cpu": run("lscpu | grep 'Model name' | cut -d: -f2 | xargs", shell=True) or run("sysctl -n machdep.cpu.brand_string"),
        "cpu_cores": None,
        "ram_gb": None,
        "gpu": None,
        "vram_total_mb": None,
        "cuda_version": None,
        "driver_version": None,
        "os": platform.system(),
        "os_release": platform.release(),
        "kernel": platform.version(),
        "python_version": sys.version.split()[0],
        "ollama_version": None,
        "docker_version": None,
        "storage_speed": None,
        "pcie_info": None,
    }

    # CPU cores
    lscpu = run("lscpu")
    if lscpu:
        m = re.search(r"CPU\(s\):\s+(\d+)", lscpu)
        if m:
            info["cpu_cores"] = int(m.group(1))

    # RAM
    meminfo = run("cat /proc/meminfo | grep MemTotal", shell=True)
    if meminfo:
        kb = _first_int(meminfo)
        info["ram_gb"] = round(kb / 1024 / 1024, 1) if kb is not None else None

    # GPU + VRAM + CUDA + driver
    gpu_info = run("nvidia-smi --query-gpu=name,memory.total,driver_version,compute_cap --format=csv,noheader")
    if gpu_info:
        parts = [p.strip() for p in gpu_info.split(",")]
        info["gpu"] = parts[0] if len(parts) > 0 else None
        info["vram_total_mb"] = _first_int(parts[1]) if len(parts) > 1 else None
        info["driver_version"] = parts[2] if len(parts) > 2 else None

    cu = run("nvcc --version | grep release", shell=True) or run("cat /usr/local/cuda/version.txt 2>/dev/null", shell=True)
    if cu:
        m = re.search(r"(\d+\.\d+)", cu)
        info["cuda_version"] = m.group(1) if m else None

    # Ollama version
    ov = run("ollama --version")
    if ov:
        m = re.search(r"(\d+\.\d+\.\d+)", ov)
        info["ollama_version"] = m.group(1) if m else ov

    # Docker version
    dv = run("docker --version")
    if dv:
        m = re.search(r"(\d+\.\d+\.\d+)", dv)
        info["docker_version"] = m.group(1) if m else dv

    # Storage
    df = run("df -h / | tail -1", shell=True)
    if df:
        info["storage_speed"] = "N/A (use hdparm/benchmark for speed)"

    # PCIe
    lspci = run(r"lspci | grep -iE 'VGA|3D|NVIDIA'", shell=True)
    info["pcie_info"] = lspci or "N/A"

    return info


def save():
    info = collect()
    path = ROOT / "results" / "system_info.json"
    path.write_text(json.dumps(info, indent=2))
    print(f"[system_info] Saved to {path}")
    return info


if __name__ == "__main__":
    save()
