# VikFwdMod

A PyQt6 graphical launcher for `parametric_density.py`, a script that forward-models galaxy cluster X-ray surface brightness profiles using the Vikhlinin density model, with optional LSQ initialisation and MCMC sampling.

---

## Requirements

| Package | Purpose |
|---|---|
| `PyQt6` | GUI framework |
| `PyQt6-WebEngine` | Embedded terminal tabs |
| `pywinpty` | Windows PTY — **Windows only**, not needed on Linux/macOS |

**Windows:**
```bash
pip install PyQt6 PyQt6-WebEngine pywinpty
```

**Linux / macOS:**
```bash
pip install PyQt6 PyQt6-WebEngine
```

The terminal uses the built-in Python `pty` module on Linux/macOS (no extra package required) and `pywinpty` on Windows. The shell opened is PowerShell on Windows and `$SHELL` (e.g. bash, zsh) on Unix.

> **Note:** `PyQt6-WebEngine` is ~100 MB. If you skip it the GUI shows a fallback message in the terminal area but everything else still works.

---

## Usage

```bash
python vikfwdmod.py
```

Point the **Script** field to your copy of `parametric_density.py` (browse or type the path). The **Python** field defaults to `python3` — change it to match your environment (e.g. a conda env or a full path).

---

## Interface overview

The window is split into two panels.

### Left panel: Parameters

| Group | Fields |
|---|---|
| **Script** | Python executable and path to `parametric_density.py` |
| **Core** | Number of parallel cores (`-1` = all), cluster name |
| **Cluster Parameters** | nH (TBabs), kT [keV], redshift z, RA/Dec [deg J2000], R500 [arcmin] |
| **MCMC Sampling** | nsteps, nwalkers, nburn (0 = adaptive) |
| **LSQ Initialisation** | Enable standard multi-start (`--lsq-init`), smart batch refinement (`--lsq-smart-init`), or LSQ-only mode; configure nstarts, nbatches, seed, max-nfev, window tightening |
| **Gaussian Priors** | Add Gaussian priors around the LSQ best-fit solution; configure rchi2 tolerance, prior scale, max fraction at boundary |
| **Model Options** | Free background (`--fit-bkg`), full Vikhlinin model with second beta component (`--full-vikhlinin-em`), fix epsilon, fix named parameters after LSQ |

### Right panel: Command and Terminals

**Command Preview** shows the full command line built from the current parameters. It is live and bidirectional: paste any valid `parametric_density.py` command into the box and all fields in the left panel will be auto-populated from it.

**Terminal tabs** provide one or more full interactive terminal sessions (xterm.js + PTY). Each tab runs an independent shell. Use the **＋** button in the top-right corner of the tab bar to open additional terminals. Tabs are closable — the last tab cannot be closed.

**Control bar:**

| Button | Action |
|---|---|
| **Put in terminal** | Insert the built command into the currently active terminal tab — without pressing Enter, so you can review or edit it first |
| **Copy command** | Copy the full command string to the clipboard |

**Presets** let you save and reload named parameter configurations to `~/.pc_density_presets.json`. Useful for switching between clusters without re-entering everything.

---

## Typical remote-server workflow

1. Open the GUI and fill in the cluster parameters.
2. A terminal tab opens automatically with a local shell.
3. Run `ssh user@your-server` to log into the remote machine.
4. Navigate to the directory that contains the data and `parametric_density.py`.
5. Click **Put in terminal**. The command is inserted at the prompt without executing — review it, then press Enter when ready.
6. Monitor the run directly in the terminal.
7. Open additional terminal tabs with **＋** for parallel sessions (e.g. a second SSH connection or a local shell alongside).

---

## Preset file

Presets are stored as JSON at `~/.pc_density_presets.json` and survive GUI restarts. Each preset saves all parameter values, the Python executable path, and the script path.
