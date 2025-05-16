from PySide6.QtGui import QPainter, QColor, QFont, QIcon, QPixmap, QPainterPath
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtWidgets import QApplication
import sys

def create_icon():
    app = QApplication.instance() or QApplication(sys.argv)
    # Create base pixmap
    size = 512
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Define colors
    bg_color = QColor("#4a90e2")  # Blue
    fg_color = QColor("#ffffff")   # White
    
    # Create background circle
    painter.setPen(Qt.NoPen)
    painter.setBrush(bg_color)
    painter.drawEllipse(0, 0, size, size)
    
    # Draw UUID-like pattern
    painter.setPen(fg_color)
    painter.setBrush(fg_color)
    font = QFont("Courier", size // 8)
    font.setBold(True)
    painter.setFont(font)
    
    # Draw stylized "UUID" text
    text_rect = QRect(0, size//3, size, size//3)
    painter.drawText(text_rect, Qt.AlignCenter, "UUID")
    
    # Draw some decorative hex-like elements
    small_size = size // 16
    positions = [
        (size//4, size//6),
        (3*size//4, size//6),
        (size//4, 5*size//6),
        (3*size//4, 5*size//6)
    ]
    
    for x, y in positions:
        painter.drawRect(x - small_size//2, y - small_size//2, small_size, small_size)
    
    painter.end()
    
    # Save in multiple sizes
    icon = QIcon(pixmap)
    sizes = [16, 32, 64, 128, 256, 512]
    for size in sizes:
        pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation).save(
            f"hex_uuid_tool/icons/app_icon_{size}.png"
        )
    
    # Save ICO format for Windows
    pixmap.save("hex_uuid_tool/icons/app_icon.ico")

if __name__ == "__main__":
    create_icon()
