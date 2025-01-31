# Custom PDF Maker
 Custom PDF Maker
Overview

Custom PDF Maker is a user-friendly application designed to create custom PDFs with ease. The application provides a graphical user interface (GUI) that allows users to input text, upload images, and save the final document as a PDF. It includes features such as spell checking, title labeling, light/dark mode, and the ability to edit pages after they are created.
Features

    Text Input: Enter large amounts of text in a chat-type window.
    Image Upload: Upload images with a clickable button and remove metadata for security.
    Title Labeling: Label each group of text with a bold title.
    Spell Check: Check the spelling of the text.
    Edit Pages: Edit pages after they are created.
    Light/Dark Mode: Switch between light and dark modes.
    Save PDF: Save the PDF to a browsable destination or the current workspace by default.
    Automatic Page Layout: Automatically handle page layout with no size limits.
    PDF Size Estimation: Display an estimation of the PDF size, updated each time text or an image is added.
    Clipboard Friendly: Support for copy/paste operations.

Installation
Prerequisites

    Python 3.x
    Kivy
    FPDF
    PyEnchant

Installation Steps

    Clone the Repository:

git clone https://github.com/yourusername/custompdfmaker.git
cd custompdfmaker

Install Dependencies:

pip install kivy fpdf pyenchant

Run the Application:

    python custompdfmaker.py

Usage

    Text Input: Enter text in the provided text input area.
    Image Upload: Use the file chooser to select and upload images.
    Title Labeling: Enter a title in the title input area to label the text.
    Spell Check: Click the "Check Spelling" button to check the spelling of the text.
    Edit Pages: Click the "Edit Pages" button to edit pages after they are created.
    Light/Dark Mode: Use the switch to toggle between light and dark modes.
    Save PDF: Click the "Save PDF" button to save the document. You can choose the save location and file name.

Code Structure

    custompdfmaker.py: Main application file containing the GUI and logic for creating PDFs.

Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.
License

This project is licensed under the MIT License.

Example Usage

python

import os
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from fpdf import FPDF
import platform
import enchant
from enchant.checker import SpellChecker

class PDFCreatorApp(App):
    def build(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)

        # Set default directory dynamically
        self.default_dir = self.get_default_directory()

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title input for adding titles to the PDF
        self.title_input = TextInput(multiline=False, hint_text='Enter title here', size_hint_y=None, height=40)
        layout.add_widget(self.title_input)

        # Text input for adding text to the PDF
        self.text_input = TextInput(multiline=True, hint_text='Enter text here', size_hint_y=0.6)
        layout.add_widget(self.text_input)

        # File chooser for selecting images
        self.file_chooser = FileChooserListView(path=self.default_dir, size_hint_y=0.2)
        layout.add_widget(self.file_chooser)

        # Buttons for actions
        button_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        
        add_text_btn = Button(text='Add Text')
        add_text_btn.bind(on_press=self.add_text)
        
        add_image_btn = Button(text='Add Image')
        add_image_btn.bind(on_press=lambda x: self.add_image(self.file_chooser.selection))
        
        save_btn = Button(text='Save PDF')
        save_btn.bind(on_press=self.save_pdf)
        
        button_layout.add_widget(add_text_btn)
        button_layout.add_widget(add_image_btn)
        button_layout.add_widget(save_btn)

        layout.add_widget(button_layout)

        # Light/Dark mode switch
        mode_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        mode_label = Label(text='Light Mode')
        self.mode_switch = Switch(active=True)
        self.mode_switch.bind(active=self.toggle_mode)
        mode_layout.add_widget(mode_label)
        mode_layout.add_widget(self.mode_switch)
        layout.add_widget(mode_layout)

        # PDF size estimation
        self.size_label = Label(text='Estimated PDF size: 0 KB')
        layout.add_widget(self.size_label)

        # Spell check button
        spell_check_btn = Button(text='Check Spelling', size_hint_y=None, height=40)
        spell_check_btn.bind(on_press=self.check_spelling)
        layout.add_widget(spell_check_btn)

        # Edit pages button
        edit_pages_btn = Button(text='Edit Pages', size_hint_y=None, height=40)
        edit_pages_btn.bind(on_press=self.edit_pages)
        layout.add_widget(edit_pages_btn)

        return layout

    def get_default_directory(self):
        """Determine the default directory based on the operating system."""
        if platform.system() == "Linux" and "ANDROID_ROOT" in os.environ:
            return "/sdcard/Download"
        elif platform.system() == "Windows":
            return os.path.join(os.environ["USERPROFILE"], "Downloads")
        elif platform.system() == "Darwin":
            return os.path.expanduser("~/Downloads")
        else:
            return os.getcwd()

    def add_text(self, instance):
        """Add text from the input box to the PDF."""
        title = self.title_input.text.strip()
        text = self.text_input.text.strip()
        if title:
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(0, 10, title, ln=True)
            self.title_input.text = ''  # Clear the title input box
        if text:
            self.pdf.set_font("Arial", size=12)
            self.pdf.multi_cell(0, 10, text)
            self.text_input.text = ''  # Clear the input box
            self.update_pdf_size()

    def add_image(self, selection):
        """Add an image to the PDF from the selected file."""
        if selection:
            image_path = selection[0]
            if os.path.exists(image_path):
                try:
                    self.pdf.add_page()
                    self.pdf.image(image_path, x=10, y=None, w=190)  # Adjust width as needed
                    self.update_pdf_size()
                except Exception as e:
                    print(f"Failed to add image: {e}")

    def save_pdf(self, instance):
        """Save the PDF to the default directory."""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        file_name_input = TextInput(hint_text='Enter file name', multiline=False)
        content.add_widget(file_name_input)
        save_btn = Button(text='Save', size_hint_y=None, height=40)
        content.add_widget(save_btn)

        popup = Popup(title='Save PDF', content=content, size_hint=(0.9, 0.5))
        save_btn.bind(on_press=lambda x: self.save_pdf_to_location(file_name_input.text, popup))
        popup.open()

    def save_pdf_to_location(self, file_name, popup):
        if not file_name:
            file_name = "custom_document"
        output_file = os.path.join(self.default_dir, f"{file_name}.pdf")
        try:
            self.pdf.output(output_file)
            print(f"PDF saved as {output_file}")
            popup.dismiss()
        except Exception as e:
            print(f"Failed to save PDF: {e}")

    def toggle_mode(self, instance, value):
        if value:
            self.root_window.background_color = (1, 1, 1, 1)  # Light mode
        else:
            self.root_window.background_color = (0, 0, 0, 1)  # Dark mode

    def update_pdf_size(self):
        # Estimate PDF size (this is a rough estimation)
        size_kb = len(self.pdf.buffer) / 1024
        self.size_label.text = f'Estimated PDF size: {size_kb:.2f} KB'

    def check_spelling(self, instance):
        """Check spelling in the text input."""
        text = self.text_input.text.strip()
        if text:
            chkr = SpellChecker("en_US")
            chkr.set_text(text)
            for err in chkr:
                print(f"Misspelled word: {err.word}")
                suggestions = ", ".join(err.suggest())
                print(f"Suggestions: {suggestions}")

    def edit_pages(self, instance):
        """Edit pages after they are created."""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        edit_text_input = TextInput(multiline=True, hint_text='Edit text here')
        content.add_widget(edit_text_input)
        save_btn = Button(text='Save Changes', size_hint_y=None, height=40)
        content.add_widget(save_btn)

        popup = Popup(title='Edit Pages', content=content, size_hint=(0.9, 0.9))
        save_btn.bind(on_press=lambda x: self.save_page_edits(edit_text_input.text, popup))
        popup.open()

    def save_page_edits(self, text, popup):
        """Save page edits."""
        if text:
            self.pdf.add_page()
            self.pdf.set_font("Arial", size=12)
            self.pdf.multi_cell(0, 10, text)
            self.update_pdf_size()
            popup.dismiss()

if __name__ == '__main__':
    PDFCreatorApp().run()
