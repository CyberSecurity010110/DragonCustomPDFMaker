import os

# Disable MTDev and other unnecessary input providers
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_METRICS_DENSITY"] = "1"
os.environ["KIVY_NO_MTDEV"] = "1"

from kivy.config import Config
Config.set('input', 'mtdev', 'none')  # Disable MTDev input provider

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from fpdf import FPDF
import platform

class PDFCreatorApp(App):
    def build(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)

        # Set default directory dynamically
        self.default_dir = self.get_default_directory()

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Text input for adding text to the PDF
        self.text_input = TextInput(multiline=True, hint_text='Enter text here')
        layout.add_widget(self.text_input)

        # File chooser for selecting images
        self.file_chooser = FileChooserListView(path=self.default_dir)
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
        text = self.text_input.text.strip()
        if text:
            self.pdf.multi_cell(0, 10, text)
            self.text_input.text = ''  # Clear the input box

    def add_image(self, selection):
        """Add an image to the PDF from the selected file."""
        if selection:
            image_path = selection[0]
            if os.path.exists(image_path):
                try:
                    self.pdf.add_page()
                    self.pdf.image(image_path, x=10, y=None, w=190)  # Adjust width as needed
                except Exception as e:
                    print(f"Failed to add image: {e}")

    def save_pdf(self, instance):
        """Save the PDF to the default directory."""
        output_file = os.path.join(self.default_dir, "custom_document.pdf")
        try:
            self.pdf.output(output_file)
            print(f"PDF saved as {output_file}")
        except Exception as e:
            print(f"Failed to save PDF: {e}")

if __name__ == '__main__':
    PDFCreatorApp().run()
    Exception as e:
            print(f"Failed to save PDF: {e}")

if __name__ == '__main__':
    PDFCreatorApp().run()
