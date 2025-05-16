import sys
import re
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QPushButton, QLineEdit, QHBoxLayout, QTextEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard, QIcon, QPixmap

class HexUuidApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UUID Format Converter")
        self.setGeometry(100, 100, 600, 400)
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'app_icon_256.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create input area with icon
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add icon on the left
        icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'app_icon_64.png')
        if os.path.exists(icon_path):
            icon_label = QLabel()
            icon_label.setPixmap(QIcon(icon_path).pixmap(48, 48))  # Slightly smaller icon
            icon_label.setAlignment(Qt.AlignCenter)
            input_layout.addWidget(icon_label)

        # Create input field
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Paste UUIDs, URLs, or Python byte strings (one per line)")
        self.input_field.setMinimumHeight(60)
        input_layout.addWidget(self.input_field)
        
        layout.addWidget(input_container)

        # Create convert button
        convert_button = QPushButton("Convert")
        convert_button.clicked.connect(self.convert_uuid)
        layout.addWidget(convert_button)

        # Create output displays
        self.output_fields = {}
        self.formats = [
            "Original (with hyphens)",
            "Uppercase (no hyphens)",
            "Hex format (0x)",
            "Python bytes"
        ]
        
        for format_name in self.formats:
            group = QWidget()
            group_layout = QVBoxLayout(group)
            group_layout.setContentsMargins(0, 10, 0, 0)
            
            header = QWidget()
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(0, 0, 0, 0)
            
            # Label
            label = QLabel(format_name + ":")
            header_layout.addWidget(label)
            
            # Toggle format button
            toggle_btn = QPushButton("Toggle Commas")
            toggle_btn.setCheckable(True)
            header_layout.addWidget(toggle_btn)
            
            # Copy button
            copy_btn = QPushButton("Copy All")
            header_layout.addWidget(copy_btn)
            
            group_layout.addWidget(header)
            
            # Text field
            text_field = QTextEdit()
            text_field.setReadOnly(True)
            text_field.setMinimumHeight(60)
            group_layout.addWidget(text_field)
            
            copy_btn.clicked.connect(lambda checked, tf=text_field: self.copy_to_clipboard(tf.toPlainText()))
            
            layout.addWidget(group)
            self.output_fields[format_name] = {
                'field': text_field,
                'toggle': toggle_btn,
                'values': [],
                'connected': False
            }
            
    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        
    def toggle_format(self, field_data, use_commas):
        if field_data['values']:
            separator = ', ' if use_commas else '\n'
            field_data['field'].setText(separator.join(field_data['values']))

    def extract_uuids(self, text):
        # First check if it's a Python bytes literal
        if text.startswith("b'") or text.startswith('b"'):
            try:
                # Convert the string representation of bytes back to actual bytes
                byte_val = eval(text)
                # Convert bytes to hex string
                hex_str = byte_val.hex()
                # If the byte string is 16 bytes (UUID length), treat it as a UUID
                if len(byte_val) == 16:
                    return [re.match(r'.*', hex_str)]  # Return as a match object
            except:
                pass

        # UUID pattern that matches both with and without hyphens
        uuid_pattern = r'[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{12}'
        return re.finditer(uuid_pattern, text)

    def normalize_input(self, input_str):
        # Handle Python bytes format (b'\x90L...')
        if input_str.startswith("b'") or input_str.startswith('b"'):
            try:
                # Convert the string representation of bytes back to actual bytes
                byte_val = eval(input_str)
                if len(byte_val) == 16:  # Check if it's the correct length for a UUID
                    return byte_val.hex()
                return None
            except:
                return None

        # Remove any whitespace and make uppercase
        clean = input_str.strip().upper()
        
        # Handle 0x format
        if clean.startswith('0X'):
            clean = clean[2:]
        
        # Remove hyphens if present
        clean = clean.replace('-', '')
        
        # Validate if it's a valid 32-character hex string
        if len(clean) == 32 and all(c in '0123456789ABCDEF' for c in clean):
            return clean
        return None

    def convert_uuid(self):
        # Get input text
        text_input = self.input_field.toPlainText().strip()
        
        # Extract all UUIDs from the text
        uuid_matches = list(self.extract_uuids(text_input))
        uuid_list = [match.group(0) for match in uuid_matches]
        
        if not uuid_list:
            for field_data in self.output_fields.values():
                field_data['field'].setText("")
                field_data['values'] = []
            return
        
        # Process each UUID
        results = {fmt: [] for fmt in self.formats}
        
        for uuid_input in uuid_list:
            clean_uuid = self.normalize_input(uuid_input)
            if clean_uuid:
                # Format with hyphens
                with_hyphens = f"{clean_uuid[:8]}-{clean_uuid[8:12]}-{clean_uuid[12:16]}-{clean_uuid[16:20]}-{clean_uuid[20:]}"
                
                # Add to results
                results["Original (with hyphens)"].append(with_hyphens.lower())
                results["Uppercase (no hyphens)"].append(clean_uuid)
                results["Hex format (0x)"].append(f"0x{clean_uuid}")
                results["Python bytes"].append(repr(bytes.fromhex(clean_uuid)))
        
        # Store and display results in respective fields
        for format_name, values in results.items():
            field_data = self.output_fields[format_name]
            field_data['values'] = values
            
            if values:
                separator = ', ' if field_data['toggle'].isChecked() else '\n'
                field_data['field'].setText(separator.join(values))
            else:
                field_data['field'].setText("No valid UUIDs found")
                field_data['values'] = []
            
            # Connect toggle button (only if not already connected)
            if not field_data['connected']:
                field_data['toggle'].toggled.connect(
                    lambda checked, fd=field_data: self.toggle_format(fd, checked)
                )
                field_data['connected'] = True

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("UUID Format Converter")
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'app_icon_256.png')
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
    
    window = HexUuidApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
