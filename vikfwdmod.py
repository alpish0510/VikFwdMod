#!/usr/bin/env python3
"""
GUI launcher for pc_parametric_density.py
Requires: PyQt6  →  pip install PyQt6
"""

import sys
import os
import json
import shlex
import threading
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QScrollArea,
    QFrame, QSplitter, QTextEdit, QFileDialog, QMessageBox, QGroupBox,
    QSpinBox, QDoubleSpinBox, QComboBox, QSizePolicy, QInputDialog,
    QTabWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, pyqtSlot, QUrl
from PyQt6.QtGui import QFont

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebChannel import QWebChannel
    _WEBENGINE_OK = True
except ImportError:
    _WEBENGINE_OK = False


# ─────────────────────────────────────────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────────────────────────────────────────
DARK = {
    "bg":        "#0e1117",
    "surface":   "#161b22",
    "surface2":  "#1c2230",
    "border":    "#2a3141",
    "accent":    "#4f9eff",
    "accent2":   "#7ec8f7",
    "text":      "#e2e8f0",
    "text_dim":  "#6b7a99",
    "success":   "#3dd68c",
    "warning":   "#f5a623",
    "error":     "#f87171",
    "highlight": "#1e3a5f",
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {DARK['bg']};
    color: {DARK['text']};
    font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
    font-size: 13px;
}}
QGroupBox {{
    background-color: {DARK['surface']};
    border: 1px solid {DARK['border']};
    border-radius: 8px;
    margin-top: 14px;
    padding: 8px 10px 10px 10px;
    font-weight: 600;
    font-size: 12px;
    color: {DARK['accent2']};
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 6px;
    background-color: {DARK['surface']};
}}
QGroupBox QLabel {{
    background-color: transparent;
}}
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
    background-color: {DARK['surface2']};
    border: 1px solid {DARK['border']};
    border-radius: 5px;
    padding: 4px 8px;
    color: {DARK['text']};
    selection-background-color: {DARK['highlight']};
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
    border: 1px solid {DARK['accent']};
}}
QLineEdit[invalid="true"] {{
    border: 1px solid {DARK['error']};
    background-color: #2a1a1a;
}}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    background-color: {DARK['border']};
    border: none;
    width: 16px;
}}
QCheckBox {{
    spacing: 8px;
    color: {DARK['text']};
}}
QCheckBox::indicator {{
    width: 15px;
    height: 15px;
    border: 1px solid {DARK['border']};
    border-radius: 3px;
    background-color: {DARK['surface2']};
}}
QCheckBox::indicator:checked {{
    background-color: {DARK['accent']};
    border-color: {DARK['accent']};
    image: none;
}}
QCheckBox::indicator:checked {{
    background-color: {DARK['accent']};
}}
QPushButton {{
    background-color: {DARK['surface2']};
    border: 1px solid {DARK['border']};
    border-radius: 6px;
    padding: 6px 16px;
    color: {DARK['text']};
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: {DARK['highlight']};
    border-color: {DARK['accent']};
    color: {DARK['accent2']};
}}
QPushButton:pressed {{
    background-color: {DARK['accent']};
    color: #fff;
}}
QPushButton#run_btn {{
    background-color: {DARK['accent']};
    color: #fff;
    font-weight: 700;
    font-size: 14px;
    padding: 8px 24px;
    border: none;
    border-radius: 7px;
    letter-spacing: 0.05em;
}}
QPushButton#run_btn:hover {{
    background-color: {DARK['accent2']};
    color: #000;
}}
QPushButton#run_btn:disabled {{
    background-color: {DARK['border']};
    color: {DARK['text_dim']};
}}
QPushButton#stop_btn {{
    background-color: #3a1a1a;
    color: {DARK['error']};
    border: 1px solid {DARK['error']};
    font-weight: 700;
    padding: 8px 24px;
    border-radius: 7px;
}}
QPushButton#stop_btn:hover {{
    background-color: {DARK['error']};
    color: #fff;
}}
QTextEdit#console {{
    background-color: #080c10;
    border: 1px solid {DARK['border']};
    border-radius: 6px;
    color: #a8c7a0;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 12px;
    padding: 8px;
    selection-background-color: {DARK['highlight']};
}}
QTextEdit#cmd_preview {{
    background-color: {DARK['surface2']};
    border: 1px solid {DARK['accent']};
    border-radius: 5px;
    color: {DARK['accent2']};
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 12px;
    padding: 6px 10px;
}}
QScrollBar:vertical {{
    background: {DARK['bg']};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {DARK['border']};
    border-radius: 4px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{
    background: {DARK['accent']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QLabel#section_label {{
    color: {DARK['accent2']};
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}}
QLabel#hint {{
    color: {DARK['text_dim']};
    font-size: 11px;
}}
QLabel#status_ok  {{ color: {DARK['success']}; font-size: 12px; font-weight: 600; }}
QLabel#status_err {{ color: {DARK['error']};   font-size: 12px; font-weight: 600; }}
QLabel#status_run {{ color: {DARK['warning']}; font-size: 12px; font-weight: 600; }}
QTabWidget::pane {{
    border: 1px solid {DARK['border']};
    border-radius: 6px;
    background: {DARK['surface']};
}}
QTabBar::tab {{
    background: {DARK['surface2']};
    border: 1px solid {DARK['border']};
    padding: 6px 16px;
    margin-right: 2px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    color: {DARK['text_dim']};
    font-size: 12px;
}}
QTabBar::tab:selected {{
    background: {DARK['surface']};
    border-bottom: 2px solid {DARK['accent']};
    color: {DARK['accent2']};
    font-weight: 600;
}}
QSplitter::handle {{
    background: {DARK['border']};
    width: 2px;
}}
"""


# ─────────────────────────────────────────────────────────────────────────────
#  SCROLL-SAFE SPINBOXES  (wheel ignored unless widget has keyboard focus)
# ─────────────────────────────────────────────────────────────────────────────
class _SpinBox(QSpinBox):
    def wheelEvent(self, e):
        e.ignore()

class _DoubleSpinBox(QDoubleSpinBox):
    def wheelEvent(self, e):
        e.ignore()



# ─────────────────────────────────────────────────────────────────────────────
#  PTY BRIDGE  (Python ↔ xterm.js via QWebChannel)
# ─────────────────────────────────────────────────────────────────────────────
class PtyBridge(QObject):
    """Exposes PTY I/O to JavaScript through QWebChannel.

    Windows : uses pywinpty + PowerShell
    Linux/macOS : uses the built-in pty module + $SHELL
    """
    data_ready = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        # Windows
        self._pty = None
        # Unix
        self._master_fd = None
        self._proc = None

    # ── start ─────────────────────────────────────────────────────────────
    def start(self, cols: int = 120, rows: int = 30):
        if sys.platform == "win32":
            self._start_windows(cols, rows)
        else:
            self._start_unix(cols, rows)

    def _start_windows(self, cols, rows):
        try:
            import winpty
            self._pty = winpty.PTY(cols, rows)
            self._pty.spawn("powershell.exe")
        except Exception as e:
            self.data_ready.emit(
                f"\r\n\x1b[31m[PTY error: {e}]\x1b[0m\r\n"
                f"\x1b[33mInstall pywinpty:  pip install pywinpty\x1b[0m\r\n"
            )
            return
        self._running = True
        threading.Thread(target=self._read_loop_windows, daemon=True).start()

    def _start_unix(self, cols, rows):
        import pty, subprocess, fcntl, termios, struct
        shell = os.environ.get("SHELL", "/bin/bash")
        try:
            self._master_fd, slave_fd = pty.openpty()
            fcntl.ioctl(slave_fd, termios.TIOCSWINSZ,
                        struct.pack("HHHH", rows, cols, 0, 0))
            self._proc = subprocess.Popen(
                [shell],
                stdin=slave_fd, stdout=slave_fd, stderr=slave_fd,
                close_fds=True,
            )
            os.close(slave_fd)
        except Exception as e:
            self.data_ready.emit(
                f"\r\n\x1b[31m[PTY error: {e}]\x1b[0m\r\n"
            )
            return
        self._running = True
        threading.Thread(target=self._read_loop_unix, daemon=True).start()

    # ── read loops ────────────────────────────────────────────────────────
    def _read_loop_windows(self):
        import time
        while self._running and self._pty:
            try:
                data = self._pty.read(blocking=False)
                if data:
                    self.data_ready.emit(data)
                else:
                    time.sleep(0.01)
            except Exception:
                break
        self._running = False

    def _read_loop_unix(self):
        import select
        while self._running and self._master_fd is not None:
            try:
                r, _, _ = select.select([self._master_fd], [], [], 0.1)
                if r:
                    data = os.read(self._master_fd, 4096)
                    if data:
                        self.data_ready.emit(data.decode("utf-8", errors="replace"))
                    else:
                        break
            except OSError:
                break
        self._running = False

    # ── input / resize ────────────────────────────────────────────────────
    @pyqtSlot(str)
    def send_input(self, data: str):
        if not self._running:
            return
        try:
            if self._pty is not None:
                self._pty.write(data)
            elif self._master_fd is not None:
                os.write(self._master_fd, data.encode("utf-8"))
        except Exception:
            pass

    @pyqtSlot(int, int)
    def resize_pty(self, cols: int, rows: int):
        try:
            if self._pty is not None and self._running:
                self._pty.set_size(cols, rows)
            elif self._master_fd is not None:
                import fcntl, termios, struct
                fcntl.ioctl(self._master_fd, termios.TIOCSWINSZ,
                            struct.pack("HHHH", rows, cols, 0, 0))
        except Exception:
            pass

    # ── cleanup ───────────────────────────────────────────────────────────
    def stop(self):
        self._running = False
        if self._pty:
            try:
                self._pty.close()
            except Exception:
                pass
            self._pty = None
        if self._master_fd is not None:
            try:
                os.close(self._master_fd)
            except Exception:
                pass
            self._master_fd = None
        if self._proc:
            try:
                self._proc.terminate()
            except Exception:
                pass
            self._proc = None


# ─────────────────────────────────────────────────────────────────────────────
#  TERMINAL WIDGET  (xterm.js inside QWebEngineView)
# ─────────────────────────────────────────────────────────────────────────────
_TERMINAL_HTML = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:100%; height:100%; background:#0e1117; overflow:hidden; }
#terminal { width:100%; height:100%; }
</style>
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/xterm@5.3.0/css/xterm.css">
</head>
<body>
<div id="terminal"></div>
<script src="https://cdn.jsdelivr.net/npm/xterm@5.3.0/lib/xterm.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xterm-addon-fit@0.8.0/lib/xterm-addon-fit.js"></script>
<script src="qrc:///qtwebchannel/qwebchannel.js"></script>
<script>
var term = new Terminal({
  fontFamily: "'JetBrains Mono','Fira Code',monospace",
  fontSize: 13,
  theme: {
    background: '#0e1117', foreground: '#e2e8f0',
    cursor: '#4f9eff', selectionBackground: '#1e3a5f',
    black:'#0e1117', brightBlack:'#6b7a99',
  },
  cursorBlink: true,
  allowProposedApi: true,
});
var fitAddon = new FitAddon.FitAddon();
term.loadAddon(fitAddon);
term.open(document.getElementById('terminal'));

new QWebChannel(qt.webChannelTransport, function(channel) {
  var bridge = channel.objects.bridge;

  bridge.data_ready.connect(function(data) {
    term.write(data);
  });

  term.onData(function(data) {
    bridge.send_input(data);
  });

  term.onResize(function(sz) {
    bridge.resize_pty(sz.cols, sz.rows);
  });

  fitAddon.fit();
});

window.addEventListener('resize', function() {
  if (typeof fitAddon !== 'undefined') fitAddon.fit();
});
</script>
</body>
</html>
"""


class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)

        if not _WEBENGINE_OK:
            msg = QLabel(
                "Embedded terminal requires additional packages.\n\n"
                "  pip install PyQt6-WebEngine pywinpty\n\n"
                "Restart the GUI after installing."
            )
            msg.setStyleSheet(
                f"color:{DARK['warning']}; padding:20px; font-size:13px;"
            )
            msg.setAlignment(Qt.AlignmentFlag.AlignTop)
            lay.addWidget(msg)
            self._ok = False
            return

        self._bridge = PtyBridge(self)
        self._channel = QWebChannel(self)
        self._channel.registerObject("bridge", self._bridge)

        self._view = QWebEngineView(self)
        self._view.page().setWebChannel(self._channel)
        self._view.setHtml(_TERMINAL_HTML, QUrl("about:blank"))
        self._view.loadFinished.connect(self._on_loaded)

        lay.addWidget(self._view)
        self._ok = True

    def _on_loaded(self, ok: bool):
        if ok and self._ok:
            self._bridge.start()

    def inject(self, text: str):
        """Type text (+ Enter) into the terminal as if the user typed it."""
        if self._ok:
            self._bridge.send_input(text + "\r")

    def put_text(self, text: str):
        """Place text into the terminal input line without pressing Enter."""
        if self._ok:
            self._bridge.send_input(text)

    def stop(self):
        if self._ok:
            self._bridge.stop()


# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _label(text, hint=None):
    lbl = QLabel(text)
    lbl.setMinimumWidth(160)
    if hint:
        lbl.setToolTip(hint)
    return lbl


def _hsep():
    f = QFrame()
    f.setFrameShape(QFrame.Shape.HLine)
    f.setStyleSheet(f"color: {DARK['border']}; background: {DARK['border']}; max-height:1px;")
    return f


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class DensityGUI(QMainWindow):
    PRESETS_FILE = Path.home() / ".pc_density_presets.json"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("pc_parametric_density — MCMC launcher")
        self.setMinimumSize(1180, 780)
        self._updating_preview = False
        self._active_terminal: "TerminalWidget | None" = None
        self._terminal_counter = 0
        self._build_ui()
        self._load_presets_file()
        self._update_preview()

    # ── UI SKELETON ──────────────────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(3)

        # LEFT: param panel
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_inner = QWidget()
        left_scroll.setWidget(left_inner)
        self._param_layout = QVBoxLayout(left_inner)
        self._param_layout.setSpacing(10)
        self._param_layout.setContentsMargins(4, 4, 4, 4)
        self._build_params()
        self._param_layout.addStretch()

        # RIGHT: command + console
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(4, 0, 0, 0)
        right_layout.setSpacing(8)
        self._build_right(right_layout)

        splitter.addWidget(left_scroll)
        splitter.addWidget(right)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 4)

        root.addWidget(splitter)

    # ── PARAM PANEL ──────────────────────────────────────────────────────────
    def _build_params(self):
        lay = self._param_layout

        # ── header ──
        title = QLabel("VIKHLININ PROFILE FORWARD MODELING")
        title.setStyleSheet(
            f"font-size:15px; font-weight:800; color:{DARK['accent']};"
            f"letter-spacing:0.15em; padding-bottom:2px;"
        )
        lay.addWidget(title)
        sub = QLabel("LSQ initialisation + MCMC sampling")
        sub.setStyleSheet(f"color:{DARK['text_dim']}; font-size:10px; margin-bottom:6px;")
        lay.addWidget(sub)

        # Script path
        lay.addWidget(self._make_script_picker())

        # ── groups ──
        lay.addWidget(self._group_core())
        lay.addWidget(self._group_physics())
        lay.addWidget(self._group_mcmc())
        lay.addWidget(self._group_lsq())
        lay.addWidget(self._group_priors())
        lay.addWidget(self._group_model())

        # ── preset bar ──
        lay.addWidget(_hsep())
        lay.addWidget(self._make_preset_bar())

    def _make_script_picker(self):
        box = QGroupBox("Script")
        lay = QGridLayout(box)
        lay.setSpacing(6)
        self.script_path = QLineEdit()
        self.script_path.setPlaceholderText("Path to pc_parametric_density.py …")
        self.script_path.textChanged.connect(self._update_preview)
        browse = QPushButton("Browse")
        browse.setFixedWidth(88)
        browse.clicked.connect(self._browse_script)
        self.python_exe = QLineEdit("python3")
        self.python_exe.setFixedWidth(130)
        self.python_exe.textChanged.connect(self._update_preview)
        lay.addWidget(QLabel("Python:"), 0, 0)
        lay.addWidget(self.python_exe, 0, 1)
        lay.addWidget(QLabel("Script:"), 1, 0)
        lay.addWidget(self.script_path, 1, 1)
        lay.addWidget(browse, 1, 2)
        return box

    # ── Core ──
    def _group_core(self):
        box = QGroupBox("Core")
        lay = QGridLayout(box)
        lay.setSpacing(6)

        self.num_cores = _SpinBox()
        self.num_cores.setRange(-1, 256)
        self.num_cores.setValue(8)
        self.num_cores.setToolTip("-1 = use all available cores")
        self.num_cores.valueChanged.connect(self._update_preview)

        self.cluster = QLineEdit("J023218.3-442048")
        self.cluster.textChanged.connect(self._update_preview)

        lay.addWidget(_label("Num cores", "−1 = all cores"), 0, 0)
        lay.addWidget(self.num_cores, 0, 1)
        lay.addWidget(_label("Cluster name"), 1, 0)
        lay.addWidget(self.cluster, 1, 1)
        return box

    # ── Physics ──
    def _group_physics(self):
        box = QGroupBox("Cluster Parameters")
        lay = QGridLayout(box)
        lay.setSpacing(6)

        def dbl(val, decs=6, lo=-1e9, hi=1e9):
            w = _DoubleSpinBox()
            w.setDecimals(decs)
            w.setRange(lo, hi)
            w.setValue(val)
            w.valueChanged.connect(self._update_preview)
            return w

        self.nh   = dbl(0.017261, 9, 0, 1e6)
        self.kT   = dbl(7.19,    3, 0, 200)
        self.z    = dbl(0.292,   4, 0, 10)
        self.ra   = dbl(38.076336, 6, -360, 360)
        self.dec  = dbl(-44.346873, 6, -90, 90)
        self.r500 = dbl(5.449646, 6, 0, 1e4)

        rows = [
            ("nH  (TBabs)",      self.nh,   "XSPEC nH parameter"),
            ("kT  [keV]",        self.kT,   "Cluster temperature"),
            ("Redshift z",       self.z,    "Cluster redshift"),
            ("RA  [deg]",        self.ra,   "Right ascension J2000"),
            ("Dec [deg]",        self.dec,  "Declination J2000"),
            ("R500 [arcmin]",    self.r500, "R500 radius in arcmin"),
        ]
        for i, (lbl, w, tip) in enumerate(rows):
            lay.addWidget(_label(lbl, tip), i, 0)
            lay.addWidget(w, i, 1)
        return box

    # ── MCMC ──
    def _group_mcmc(self):
        box = QGroupBox("MCMC Sampling")
        lay = QGridLayout(box)
        lay.setSpacing(6)

        self.nsteps = _SpinBox(); self.nsteps.setRange(1, 100000); self.nsteps.setValue(1000)
        self.nsteps.valueChanged.connect(self._update_preview)

        self.nwalkers = _SpinBox(); self.nwalkers.setRange(2, 2000); self.nwalkers.setValue(40)
        self.nwalkers.valueChanged.connect(self._update_preview)

        self.nburn = _SpinBox(); self.nburn.setRange(0, 50000); self.nburn.setValue(0)
        self.nburn.setSpecialValueText("adaptive")
        self.nburn.valueChanged.connect(self._update_preview)

        lay.addWidget(_label("nsteps"),   0, 0); lay.addWidget(self.nsteps, 0, 1)
        lay.addWidget(_label("nwalkers"), 1, 0); lay.addWidget(self.nwalkers, 1, 1)
        lay.addWidget(_label("nburn"),    2, 0); lay.addWidget(self.nburn, 2, 1)

        hint = QLabel("nwalkers should be ≥ 2 × ndim  (ndim ≈ 6–9)")
        hint.setObjectName("hint")
        lay.addWidget(hint, 3, 0, 1, 2)
        return box

    # ── LSQ ──
    def _group_lsq(self):
        box = QGroupBox("LSQ Initialisation")
        lay = QGridLayout(box)
        lay.setSpacing(6)

        self.lsq_init       = QCheckBox("--lsq-init  (standard multi-start)")
        self.lsq_smart_init = QCheckBox("--lsq-smart-init  (smart batch refinement)")
        self.lsq_only       = QCheckBox("--lsq-only  (skip MCMC)")

        for cb in (self.lsq_init, self.lsq_smart_init, self.lsq_only):
            cb.stateChanged.connect(self._update_preview)
            cb.stateChanged.connect(self._toggle_lsq_sub)

        def sp(lo, hi, val):
            w = _SpinBox(); w.setRange(lo, hi); w.setValue(val)
            w.valueChanged.connect(self._update_preview)
            return w

        def dbl2(val):
            w = _DoubleSpinBox(); w.setDecimals(2); w.setRange(0, 10); w.setValue(val)
            w.valueChanged.connect(self._update_preview)
            return w

        self.lsq_nstarts  = sp(1, 200, 10)
        self.lsq_nbatches = sp(1, 50,  5)
        self.lsq_seed     = sp(0, 99999, 42)
        self.lsq_max_nfev = sp(10, 10000, 500)
        self.lsq_tighten_all = QCheckBox("--lsq-tighten-all")
        self.lsq_tighten_all.stateChanged.connect(self._update_preview)
        self.lsq_window_all = dbl2(0.5)

        lay.addWidget(self.lsq_init,       0, 0, 1, 2)
        lay.addWidget(self.lsq_smart_init, 1, 0, 1, 2)
        lay.addWidget(self.lsq_only,       2, 0, 1, 2)
        lay.addWidget(_hsep(),             3, 0, 1, 2)

        sub_rows = [
            ("nstarts",  self.lsq_nstarts),
            ("nbatches", self.lsq_nbatches),
            ("seed",     self.lsq_seed),
            ("max-nfev", self.lsq_max_nfev),
        ]
        self._lsq_sub_widgets = []
        for i, (lbl, w) in enumerate(sub_rows):
            r = i + 4
            ll = _label(lbl); lay.addWidget(ll, r, 0); lay.addWidget(w, r, 1)
            self._lsq_sub_widgets.extend([ll, w])

        lay.addWidget(self.lsq_tighten_all, 8, 0, 1, 2)
        ll2 = _label("window-all"); lay.addWidget(ll2, 9, 0)
        lay.addWidget(self.lsq_window_all, 9, 1)
        self._lsq_sub_widgets.extend([self.lsq_tighten_all, ll2, self.lsq_window_all])

        self._toggle_lsq_sub()
        return box

    def _toggle_lsq_sub(self):
        enabled = self.lsq_init.isChecked() or self.lsq_smart_init.isChecked() or self.lsq_only.isChecked()
        for w in self._lsq_sub_widgets:
            w.setEnabled(enabled)

    # ── Gaussian Priors ──
    def _group_priors(self):
        box = QGroupBox("Gaussian Priors")
        lay = QGridLayout(box)
        lay.setSpacing(6)

        self.gaussian_prior = QCheckBox("--gaussian-prior  (requires LSQ init)")
        self.gaussian_prior.stateChanged.connect(self._update_preview)
        self.gaussian_prior.stateChanged.connect(self._toggle_prior_sub)

        def dbl3(val, decs=2, lo=0, hi=100):
            w = _DoubleSpinBox(); w.setDecimals(decs); w.setRange(lo, hi); w.setValue(val)
            w.valueChanged.connect(self._update_preview)
            return w

        self.gp_rchi2_tol    = dbl3(1.5)
        self.gp_scale        = dbl3(0.3, 3)
        self.gp_max_frac_bnd = dbl3(0.25, 3)

        lay.addWidget(self.gaussian_prior, 0, 0, 1, 2)
        self._prior_sub = []
        rows = [
            ("rchi2 tolerance", self.gp_rchi2_tol),
            ("prior scale",     self.gp_scale),
            ("max frac bound",  self.gp_max_frac_bnd),
        ]
        for i, (lbl, w) in enumerate(rows):
            ll = _label(lbl)
            lay.addWidget(ll, i+1, 0); lay.addWidget(w, i+1, 1)
            self._prior_sub.extend([ll, w])

        self._toggle_prior_sub()
        return box

    def _toggle_prior_sub(self):
        enabled = self.gaussian_prior.isChecked()
        for w in self._prior_sub:
            w.setEnabled(enabled)

    # ── Model Options ──
    def _group_model(self):
        box = QGroupBox("Model Options")
        lay = QGridLayout(box)
        lay.setSpacing(6)

        self.fit_bkg          = QCheckBox("--fit-bkg  (background as free parameter)")
        self.full_vikhlinin   = QCheckBox("--full-vikhlinin-em  (second β component)")
        self.fit_bkg.stateChanged.connect(self._update_preview)
        self.full_vikhlinin.stateChanged.connect(self._update_preview)

        self.fix_eps = _DoubleSpinBox()
        self.fix_eps.setDecimals(4); self.fix_eps.setRange(-1e6, 1e6); self.fix_eps.setValue(0)
        self.fix_eps_cb = QCheckBox("--fix-eps")
        self.fix_eps_cb.stateChanged.connect(self._update_preview)
        self.fix_eps_cb.stateChanged.connect(lambda s: self.fix_eps.setEnabled(bool(s)))
        self.fix_eps.setEnabled(False)
        self.fix_eps.valueChanged.connect(self._update_preview)

        self.fix_after_lsq = QLineEdit()
        self.fix_after_lsq.setPlaceholderText("e.g. rc,rs,beta2")
        self.fix_after_lsq.textChanged.connect(self._update_preview)

        lay.addWidget(self.fit_bkg,        0, 0, 1, 2)
        lay.addWidget(self.full_vikhlinin, 1, 0, 1, 2)
        lay.addWidget(self.fix_eps_cb,     2, 0)
        lay.addWidget(self.fix_eps,        2, 1)
        lay.addWidget(_label("fix-after-lsq"), 3, 0)
        lay.addWidget(self.fix_after_lsq,  3, 1)
        return box

    # ── Preset bar ──
    def _make_preset_bar(self):
        bar = QWidget()
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(0, 4, 0, 4)
        lay.setSpacing(6)
        lbl = QLabel("PRESETS")
        lbl.setObjectName("section_label")
        lay.addWidget(lbl)

        self.preset_combo = QComboBox()
        self.preset_combo.setMinimumWidth(160)
        self.preset_combo.currentTextChanged.connect(self._load_selected_preset)
        lay.addWidget(self.preset_combo)

        save_btn = QPushButton("Save")
        save_btn.setFixedWidth(70)
        save_btn.clicked.connect(self._save_preset)
        del_btn = QPushButton("Delete")
        del_btn.setFixedWidth(75)
        del_btn.clicked.connect(self._delete_preset)
        lay.addWidget(save_btn)
        lay.addWidget(del_btn)
        lay.addStretch()
        return bar

    # ── RIGHT PANEL ──────────────────────────────────────────────────────────
    def _build_right(self, lay: QVBoxLayout):
        # Command preview
        cmd_lbl = QLabel("COMMAND PREVIEW")
        cmd_lbl.setObjectName("section_label")
        lay.addWidget(cmd_lbl)

        self.cmd_preview = QTextEdit()
        self.cmd_preview.setObjectName("cmd_preview")
        self.cmd_preview.setMaximumHeight(80)
        self.cmd_preview.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.cmd_preview.setToolTip("Paste a command here to auto-populate all fields")
        self.cmd_preview.textChanged.connect(self._on_preview_edited)
        lay.addWidget(self.cmd_preview)

        # Validation label
        self.validation_lbl = QLabel("")
        self.validation_lbl.setObjectName("status_ok")
        lay.addWidget(self.validation_lbl)

        # ── Terminal tabs ─────────────────────────────────────────────────
        self.terminal_tabs = QTabWidget()
        self.terminal_tabs.setDocumentMode(True)
        self.terminal_tabs.setTabsClosable(True)
        self.terminal_tabs.tabCloseRequested.connect(self._close_terminal_tab)
        self.terminal_tabs.currentChanged.connect(self._on_tab_changed)

        add_tab_btn = QPushButton("＋")
        add_tab_btn.setFixedSize(28, 28)
        add_tab_btn.setToolTip("Open a new terminal tab")
        add_tab_btn.setFont(QFont("JetBrains Mono", 14, QFont.Weight.Light))
        add_tab_btn.setStyleSheet(
            f"QPushButton {{"
            f"  background: transparent;"
            f"  border: 1px solid {DARK['border']};"
            f"  border-radius: 6px;"
            f"  color: {DARK['text_dim']};"
            f"  padding: 0;"
            f"}}"
            f"QPushButton:hover {{"
            f"  background: {DARK['highlight']};"
            f"  border-color: {DARK['accent']};"
            f"  color: {DARK['accent']};"
            f"}}"
            f"QPushButton:pressed {{"
            f"  background: {DARK['accent']};"
            f"  color: #fff;"
            f"}}"
        )
        add_tab_btn.clicked.connect(self._add_terminal_tab)

        corner_wrap = QWidget()
        corner_lay = QHBoxLayout(corner_wrap)
        corner_lay.setContentsMargins(0, 2, 6, 0)
        corner_lay.addWidget(add_tab_btn)
        self.terminal_tabs.setCornerWidget(corner_wrap, Qt.Corner.TopRightCorner)

        self._add_terminal_tab()   # first terminal

        lay.addWidget(self.terminal_tabs, stretch=1)

        # Controls bar
        ctrl = QHBoxLayout()
        ctrl.setSpacing(8)

        put_btn = QPushButton("⌨  Put in terminal")
        put_btn.setToolTip("Insert the built command into the active terminal (without executing)")
        put_btn.clicked.connect(self._put_in_terminal)

        copy_btn = QPushButton("Copy command")
        copy_btn.clicked.connect(self._copy_cmd)

        self.status_lbl = QLabel("")
        self.status_lbl.setObjectName("status_ok")

        ctrl.addWidget(put_btn)
        ctrl.addWidget(copy_btn)
        ctrl.addStretch()
        ctrl.addWidget(self.status_lbl)
        lay.addLayout(ctrl)

    def _add_terminal_tab(self):
        # Save current state onto the active terminal before switching
        if self._active_terminal is not None:
            self._active_terminal._state = self._collect_state()

        term = TerminalWidget()
        term._state = self._collect_state()   # new tab inherits current parameters
        self._terminal_counter += 1
        idx = self.terminal_tabs.addTab(term, f"Terminal {self._terminal_counter}")
        self.terminal_tabs.setCurrentIndex(idx)   # fires _on_tab_changed

    def _close_terminal_tab(self, idx: int):
        if self.terminal_tabs.count() <= 1:
            return   # always keep at least one terminal
        widget = self.terminal_tabs.widget(idx)
        if isinstance(widget, TerminalWidget):
            widget.stop()
        self.terminal_tabs.removeTab(idx)

    def _current_terminal(self) -> "TerminalWidget | None":
        w = self.terminal_tabs.currentWidget()
        return w if isinstance(w, TerminalWidget) else None

    def _on_tab_changed(self, new_idx: int):
        # Save current parameters to the terminal we're leaving
        if self._active_terminal is not None:
            self._active_terminal._state = self._collect_state()

        # Restore parameters for the terminal we're switching to
        new_term = self.terminal_tabs.widget(new_idx)
        if isinstance(new_term, TerminalWidget):
            self._active_terminal = new_term
            self._updating_preview = True
            try:
                self._apply_state(new_term._state)
            finally:
                self._updating_preview = False
            self._update_preview()

    # ── COMMAND BUILDER ──────────────────────────────────────────────────────
    def _build_cmd(self):
        py   = self.python_exe.text().strip() or "python3"
        scr  = self.script_path.text().strip()
        cmd  = [py, scr, str(self.num_cores.value())]

        def add(flag, val=None):
            cmd.append(flag)
            if val is not None:
                cmd.append(str(val))

        cluster = self.cluster.text().strip()
        if cluster != "J023218.3-442048":
            add("--cluster", cluster)

        add("--nh",   f"{self.nh.value():.9g}")
        add("--kT",   f"{self.kT.value():.4g}")
        add("--z",    f"{self.z.value():.4g}")
        add("--ra",   f"{self.ra.value():.9g}")
        add("--dec",  f"{self.dec.value():.9g}")
        add("--r500", f"{self.r500.value():.9g}")
        add("--nsteps",   self.nsteps.value())
        add("--nwalkers", self.nwalkers.value())
        if self.nburn.value() > 0:
            add("--nburn", self.nburn.value())
        if self.fit_bkg.isChecked():
            add("--fit-bkg")
        if self.full_vikhlinin.isChecked():
            add("--full-vikhlinin-em")

        if self.lsq_init.isChecked():
            add("--lsq-init")
        if self.lsq_smart_init.isChecked():
            add("--lsq-smart-init")
        if self.lsq_only.isChecked():
            add("--lsq-only")

        if any([self.lsq_init.isChecked(), self.lsq_smart_init.isChecked(), self.lsq_only.isChecked()]):
            add("--lsq-nstarts",  self.lsq_nstarts.value())
            add("--lsq-nbatches", self.lsq_nbatches.value())
            add("--lsq-seed",     self.lsq_seed.value())
            add("--lsq-max-nfev", self.lsq_max_nfev.value())
            if self.lsq_tighten_all.isChecked():
                add("--lsq-tighten-all")
                add("--lsq-window-all", f"{self.lsq_window_all.value():.2f}")

        if self.gaussian_prior.isChecked():
            add("--gaussian-prior")
            add("--gaussian-prior-rchi2-tol",    f"{self.gp_rchi2_tol.value():.2f}")
            add("--gaussian-prior-scale",         f"{self.gp_scale.value():.3f}")
            add("--gaussian-prior-max-frac-bound",f"{self.gp_max_frac_bnd.value():.3f}")

        if self.fix_eps_cb.isChecked():
            add("--fix-eps", f"{self.fix_eps.value():.4g}")

        fix_str = self.fix_after_lsq.text().strip()
        if fix_str:
            add("--fix-after-lsq", fix_str)

        return cmd

    def _update_preview(self):
        self._updating_preview = True
        try:
            cmd = self._build_cmd()
            self.cmd_preview.setPlainText(" ".join(shlex.quote(c) for c in cmd))
            self._validate()
        finally:
            self._updating_preview = False

    # ── PARSE PASTED COMMAND ─────────────────────────────────────────────────
    def _on_preview_edited(self):
        if self._updating_preview:
            return
        text = self.cmd_preview.toPlainText().strip()
        if not text:
            return
        try:
            tokens = shlex.split(text)
        except ValueError:
            return
        if len(tokens) < 3:
            return
        self._parse_cmd_tokens(tokens)

    def _parse_cmd_tokens(self, tokens):
        """Parse a command token list and apply values to all widgets."""
        # Block recursive updates while we apply state
        self._updating_preview = True
        try:
            self.python_exe.setText(tokens[0])
            self.script_path.setText(tokens[1])
            try:
                self.num_cores.setValue(int(tokens[2]))
            except (ValueError, IndexError):
                pass

            # Build a simple flag→value map
            flags = {}
            i = 3
            while i < len(tokens):
                tok = tokens[i]
                if tok.startswith("--"):
                    # peek ahead: if next token is not a flag, it's the value
                    if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                        flags[tok] = tokens[i + 1]
                        i += 2
                    else:
                        flags[tok] = True
                        i += 1
                else:
                    i += 1

            def flt(key, default=None):
                v = flags.get(key, default)
                try:
                    return float(v)
                except (TypeError, ValueError):
                    return default

            def intt(key, default=None):
                v = flags.get(key, default)
                try:
                    return int(v)
                except (TypeError, ValueError):
                    return default

            def checked(key):
                return flags.get(key, False) is True

            # cluster
            if "--cluster" in flags:
                self.cluster.setText(str(flags["--cluster"]))

            # physics
            if "--nh"   in flags: self.nh.setValue(flt("--nh",   self.nh.value()))
            if "--kT"   in flags: self.kT.setValue(flt("--kT",   self.kT.value()))
            if "--z"    in flags: self.z.setValue(flt("--z",     self.z.value()))
            if "--ra"   in flags: self.ra.setValue(flt("--ra",   self.ra.value()))
            if "--dec"  in flags: self.dec.setValue(flt("--dec", self.dec.value()))
            if "--r500" in flags: self.r500.setValue(flt("--r500", self.r500.value()))

            # MCMC
            if "--nsteps"   in flags: self.nsteps.setValue(intt("--nsteps",   self.nsteps.value()))
            if "--nwalkers" in flags: self.nwalkers.setValue(intt("--nwalkers", self.nwalkers.value()))
            if "--nburn"    in flags: self.nburn.setValue(intt("--nburn",      self.nburn.value()))

            # Model options
            self.fit_bkg.setChecked(checked("--fit-bkg"))
            self.full_vikhlinin.setChecked(checked("--full-vikhlinin-em"))

            if "--fix-eps" in flags:
                self.fix_eps_cb.setChecked(True)
                self.fix_eps.setValue(flt("--fix-eps", 0.0))
            else:
                self.fix_eps_cb.setChecked(False)

            if "--fix-after-lsq" in flags:
                self.fix_after_lsq.setText(str(flags["--fix-after-lsq"]))
            else:
                self.fix_after_lsq.setText("")

            # LSQ
            self.lsq_init.setChecked(checked("--lsq-init"))
            self.lsq_smart_init.setChecked(checked("--lsq-smart-init"))
            self.lsq_only.setChecked(checked("--lsq-only"))
            if "--lsq-nstarts"  in flags: self.lsq_nstarts.setValue(intt("--lsq-nstarts",  self.lsq_nstarts.value()))
            if "--lsq-nbatches" in flags: self.lsq_nbatches.setValue(intt("--lsq-nbatches", self.lsq_nbatches.value()))
            if "--lsq-seed"     in flags: self.lsq_seed.setValue(intt("--lsq-seed",         self.lsq_seed.value()))
            if "--lsq-max-nfev" in flags: self.lsq_max_nfev.setValue(intt("--lsq-max-nfev", self.lsq_max_nfev.value()))
            self.lsq_tighten_all.setChecked(checked("--lsq-tighten-all"))
            if "--lsq-window-all" in flags: self.lsq_window_all.setValue(flt("--lsq-window-all", self.lsq_window_all.value()))

            # Gaussian priors
            self.gaussian_prior.setChecked(checked("--gaussian-prior"))
            if "--gaussian-prior-rchi2-tol"     in flags: self.gp_rchi2_tol.setValue(flt("--gaussian-prior-rchi2-tol",     self.gp_rchi2_tol.value()))
            if "--gaussian-prior-scale"          in flags: self.gp_scale.setValue(flt("--gaussian-prior-scale",              self.gp_scale.value()))
            if "--gaussian-prior-max-frac-bound" in flags: self.gp_max_frac_bnd.setValue(flt("--gaussian-prior-max-frac-bound", self.gp_max_frac_bnd.value()))

            self._toggle_lsq_sub()
            self._toggle_prior_sub()
            self._validate()
        finally:
            self._updating_preview = False

    # ── VALIDATION ───────────────────────────────────────────────────────────
    def _validate(self) -> bool:
        errors = []
        scr = self.script_path.text().strip()
        if not scr:
            errors.append("script path not set")
        elif not Path(scr).exists():
            errors.append("script file not found")

        nw = self.nwalkers.value()
        # ndim ≈ 6 standard, 9 full-em
        ndim = 9 if self.full_vikhlinin.isChecked() else 6
        if nw < 2 * ndim:
            errors.append(f"nwalkers ({nw}) < 2×ndim ({2*ndim})")

        if self.gaussian_prior.isChecked() and not (self.lsq_init.isChecked() or self.lsq_smart_init.isChecked()):
            errors.append("gaussian-prior requires lsq-init or lsq-smart-init")

        if errors:
            self.validation_lbl.setObjectName("status_err")
            self.validation_lbl.setText("⚠  " + "   ·   ".join(errors))
        else:
            self.validation_lbl.setObjectName("status_ok")
            self.validation_lbl.setText("✓  ready")

        # force style refresh
        self.validation_lbl.style().unpolish(self.validation_lbl)
        self.validation_lbl.style().polish(self.validation_lbl)
        return not errors

    # ── PUT IN TERMINAL ───────────────────────────────────────────────────────
    def _put_in_terminal(self):
        cmd = " ".join(shlex.quote(c) for c in self._build_cmd())
        term = self._current_terminal()
        if term:
            term.put_text(cmd)

    # ── COPY ─────────────────────────────────────────────────────────────────
    def _copy_cmd(self):
        cmd = " ".join(shlex.quote(c) for c in self._build_cmd())
        QApplication.clipboard().setText(cmd)
        self.status_lbl.setObjectName("status_ok")
        self.status_lbl.setText("copied!")
        self._refresh_status()

    # ── BROWSE ───────────────────────────────────────────────────────────────
    def _browse_script(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select script", "", "Python (*.py);;All (*)")
        if path:
            self.script_path.setText(path)

    # ── PRESETS ──────────────────────────────────────────────────────────────
    def _collect_state(self) -> dict:
        return {
            "python_exe":    self.python_exe.text(),
            "script_path":   self.script_path.text(),
            "num_cores":     self.num_cores.value(),
            "cluster":       self.cluster.text(),
            "nh":            self.nh.value(),
            "kT":            self.kT.value(),
            "z":             self.z.value(),
            "ra":            self.ra.value(),
            "dec":           self.dec.value(),
            "r500":          self.r500.value(),
            "nsteps":        self.nsteps.value(),
            "nwalkers":      self.nwalkers.value(),
            "nburn":         self.nburn.value(),
            "fit_bkg":       self.fit_bkg.isChecked(),
            "full_vikhlinin":self.full_vikhlinin.isChecked(),
            "lsq_init":      self.lsq_init.isChecked(),
            "lsq_smart_init":self.lsq_smart_init.isChecked(),
            "lsq_only":      self.lsq_only.isChecked(),
            "lsq_nstarts":   self.lsq_nstarts.value(),
            "lsq_nbatches":  self.lsq_nbatches.value(),
            "lsq_seed":      self.lsq_seed.value(),
            "lsq_max_nfev":  self.lsq_max_nfev.value(),
            "lsq_tighten_all":self.lsq_tighten_all.isChecked(),
            "lsq_window_all":self.lsq_window_all.value(),
            "gaussian_prior":self.gaussian_prior.isChecked(),
            "gp_rchi2_tol":  self.gp_rchi2_tol.value(),
            "gp_scale":      self.gp_scale.value(),
            "gp_max_frac_bnd":self.gp_max_frac_bnd.value(),
            "fix_eps_cb":    self.fix_eps_cb.isChecked(),
            "fix_eps":       self.fix_eps.value(),
            "fix_after_lsq": self.fix_after_lsq.text(),
        }

    def _apply_state(self, s: dict):
        self.python_exe.setText(s.get("python_exe", "python3"))
        self.script_path.setText(s.get("script_path", ""))
        self.num_cores.setValue(s.get("num_cores", 8))
        self.cluster.setText(s.get("cluster", "J023218.3-442048"))
        self.nh.setValue(s.get("nh", 0.017261))
        self.kT.setValue(s.get("kT", 7.19))
        self.z.setValue(s.get("z", 0.292))
        self.ra.setValue(s.get("ra", 38.076336))
        self.dec.setValue(s.get("dec", -44.346873))
        self.r500.setValue(s.get("r500", 5.449646))
        self.nsteps.setValue(s.get("nsteps", 1000))
        self.nwalkers.setValue(s.get("nwalkers", 40))
        self.nburn.setValue(s.get("nburn", 0))
        self.fit_bkg.setChecked(s.get("fit_bkg", False))
        self.full_vikhlinin.setChecked(s.get("full_vikhlinin", False))
        self.lsq_init.setChecked(s.get("lsq_init", False))
        self.lsq_smart_init.setChecked(s.get("lsq_smart_init", False))
        self.lsq_only.setChecked(s.get("lsq_only", False))
        self.lsq_nstarts.setValue(s.get("lsq_nstarts", 10))
        self.lsq_nbatches.setValue(s.get("lsq_nbatches", 5))
        self.lsq_seed.setValue(s.get("lsq_seed", 42))
        self.lsq_max_nfev.setValue(s.get("lsq_max_nfev", 500))
        self.lsq_tighten_all.setChecked(s.get("lsq_tighten_all", False))
        self.lsq_window_all.setValue(s.get("lsq_window_all", 0.5))
        self.gaussian_prior.setChecked(s.get("gaussian_prior", False))
        self.gp_rchi2_tol.setValue(s.get("gp_rchi2_tol", 1.5))
        self.gp_scale.setValue(s.get("gp_scale", 0.3))
        self.gp_max_frac_bnd.setValue(s.get("gp_max_frac_bnd", 0.25))
        self.fix_eps_cb.setChecked(s.get("fix_eps_cb", False))
        self.fix_eps.setValue(s.get("fix_eps", 0.0))
        self.fix_after_lsq.setText(s.get("fix_after_lsq", ""))

    def _load_presets_file(self):
        self._presets: dict = {}
        if self.PRESETS_FILE.exists():
            try:
                self._presets = json.loads(self.PRESETS_FILE.read_text())
            except Exception:
                pass
        self._refresh_preset_combo()

    def _refresh_preset_combo(self):
        self.preset_combo.blockSignals(True)
        self.preset_combo.clear()
        self.preset_combo.addItem("— select preset —")
        for name in sorted(self._presets):
            self.preset_combo.addItem(name)
        self.preset_combo.blockSignals(False)

    def _load_selected_preset(self, name: str):
        if name in self._presets:
            self._apply_state(self._presets[name])
            self._update_preview()

    def _save_preset(self):
        name, ok = QInputDialog.getText(self, "Save preset", "Preset name:")
        if ok and name.strip():
            self._presets[name.strip()] = self._collect_state()
            self.PRESETS_FILE.write_text(json.dumps(self._presets, indent=2))
            self._refresh_preset_combo()

    def _delete_preset(self):
        name = self.preset_combo.currentText()
        if name in self._presets:
            del self._presets[name]
            self.PRESETS_FILE.write_text(json.dumps(self._presets, indent=2))
            self._refresh_preset_combo()

    def closeEvent(self, e):
        term = self._current_terminal()
        if term:
            term.stop()
        super().closeEvent(e)


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)
    win = DensityGUI()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
