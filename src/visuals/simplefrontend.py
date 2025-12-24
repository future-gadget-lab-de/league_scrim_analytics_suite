import logging
logger = logging.getLogger(__name__)

import sys

from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SimpleFrontend(QMainWindow):
    def __init__(self, f) -> None:
        super().__init__()
        self.setWindowTitle("LSAS - Einstieg")
        self.setMinimumSize(480, 320)
        self.custom_function = f
        self._build_ui()

    def _build_ui(self) -> None:
        """Create a minimal entry window with a short welcome and two actions."""
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(18)

        headline = QLabel("Willkommen bei der League Scrim Analytics Suite")
        headline.setWordWrap(True)

        subtext = QLabel(
            "Dieses einfache Fenster dient als Einstiegspunkt. "
            "Von hier aus kann spaeter die Datenauslese oder Visualisierung gestartet werden."
        )
        subtext.setWordWrap(True)

        import_button = QPushButton("Import starten")
        import_button.clicked.connect(self._show_placeholder)

        start_button = QPushButton("Starten")
        start_button.clicked.connect(self.custom_function)

        quit_button = QPushButton("Beenden")
        quit_button.clicked.connect(self.close)

        layout.addWidget(headline)
        layout.addWidget(subtext)
        layout.addStretch(1)
        layout.addWidget(import_button)
        layout.addWidget(start_button)
        layout.addWidget(quit_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _show_placeholder(self) -> None:
        """Placeholder hook for later import logic."""
        QMessageBox.information(
            self,
            "In Arbeit",
            "Hier kann spaeter der Importprozess angebunden werden.",
        )





