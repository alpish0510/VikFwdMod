# pc_density_gui

A PyQt6 graphical launcher for `pc_parametric_density.py` — a script that forward-models galaxy cluster X-ray surface brightness profiles using the Vikhlinin density model, with optional LSQ initialisation and MCMC sampling.

---

## Requirements

| Package | Purpose |
|---|---|
| `PyQt6` | GUI framework |
| `PyQt6-WebEngine` | Embedded terminal tab |
| `pywinpty` | Windows PTY (needed for the terminal) |

Install everything at once:

```bash
pip install PyQt6 PyQt6-WebEngine pywinpty
```

> **Note:** `PyQt6-WebEngine` is ~100 MB. If you only need the local runner and command builder, you can skip it — the GUI will show a fallback message in the Terminal tab but everything else still works.

---

## Usage

```bash
python pc_density_gui.py
```

Point the **Script** field to your copy of `pc_parametric_density.py` (browse or type the path). The **Python** field defaults to `python3` — change it to match your environment (e.g. a conda env or a full path).

---

## Interface overview

The window is split into two panels.

### Left — Parameters

| Group | Fields |
|---|---|
| **Script** | Python executable and path to `pc_parametric_density.py` |
| **Core** | Number of parallel cores (`-1` = all), cluster name |
| **Cluster Parameters** | nH (TBabs), kT [keV], redshift z, RA/Dec [deg J2000], R500 [arcmin] |
| **MCMC Sampling** | nsteps, nwalkers, nburn (0 = adaptive) |
| **LSQ Initialisation** | Enable standard multi-start (`--lsq-init`), smart batch refinement (`--lsq-smart-init`), or LSQ-only mode; configure nstarts, nbatches, seed, max-nfev, window tightening |
| **Gaussian Priors** | Add Gaussian priors around the LSQ best-fit solution; configure rchi2 tolerance, prior scale, max fraction at boundary |
| **Model Options** | Free background (`--fit-bkg`), full Vikhlinin model with second β component (`--full-vikhlinin-em`), fix ε, fix named parameters after LSQ |

### Right — Command & Output

**Command Preview** — shows the full command line built from the current parameters. It is live and bidirectional: paste any valid `pc_parametric_density.py` command into the box and all fields in the left panel will be auto-populated from it.

**Output tabs:**

- **Terminal** — a full interactive terminal (xterm.js + Windows ConPTY). Use it to `ssh` into a remote server, navigate to your data, and then use *Inject to Terminal* to fire the built command there.
- **Script Output** — read-only log of local subprocess runs, with colour-coded warnings, errors, and success lines.

**Control bar:**

| Button | Action |
|---|---|
| **▶ RUN locally** | Run the built command on this machine; output appears in the Script Output tab |
| **■ STOP** | Kill the local process tree (Windows `taskkill /F /T`) |
| **⌨ Inject to Terminal** | Type the built command into the Terminal tab and press Enter — useful after SSH-ing into a remote server |
| **Copy command** | Copy the full command string to the clipboard |
| **Clear output** | Clear the Script Output tab |

**Presets** — save and reload named parameter configurations to `~/.pc_density_presets.json`. Useful for switching between clusters without re-entering everything.

---

## Typical remote-server workflow

1. Open the GUI and fill in the cluster parameters.
2. Switch to the **Terminal** tab — a PowerShell session opens automatically.
3. `ssh user@your-server` to log into the remote machine.
4. Navigate to the directory that contains the data and `pc_parametric_density.py`.
5. Click **⌨ Inject to Terminal** — the GUI types the full command into the terminal and presses Enter.
6. Monitor the run directly in the terminal.

---

## Typical local workflow

1. Fill in parameters.
2. Check the **Command Preview** — adjust if needed (edits sync back to the fields).
3. Click **▶ RUN locally**.
4. Watch output in the **Script Output** tab.

---

## Preset file

Presets are stored as JSON at `~/.pc_density_presets.json` and survive GUI restarts. Each preset saves all parameter values, the Python executable path, and the script path.
