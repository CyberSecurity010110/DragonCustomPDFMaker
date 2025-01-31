import os
import traceback
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
from kivy.uix.progressbar import ProgressBar
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from fpdf import FPDF
import platform
import enchant
from enchant.checker import SpellChecker

class CustomTextInput(TextInput):
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'v' and 'ctrl' in modifiers:
            self.insert_text(Clipboard.paste())
        else:
            super(CustomTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

class PDFCreatorApp(App):
    def build(self):
        try:
            self.pdf = FPDF()
            self.pdf.set_auto_page_break(auto=True, margin=15)
            self.pdf.add_page()
            self.pdf.set_font("Arial", size=12)

            # Set default directory dynamically
            self.default_dir = self.get_default_directory()

            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

            # Title input for adding titles to the PDF
            self.title_input = CustomTextInput(multiline=False, hint_text='Enter title here', size_hint_y=None, height=40)
            layout.add_widget(self.title_input)

            # Text input for adding text to the PDF
            self.text_input = CustomTextInput(multiline=True, hint_text='Enter text here', size_hint_y=0.4)
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

            # Progress bar for large file operations
            self.progress_bar = ProgressBar(max=100, value=0, size_hint_y=None, height=20)
            layout.add_widget(self.progress_bar)

            # Color picker for text color
            color_picker_btn = Button(text='Choose Text Color', size_hint_y=None, height=40)
            color_picker_btn.bind(on_press=self.choose_text_color)
            layout.add_widget(color_picker_btn)

            return layout

        except Exception as e:
            print(f"An error occurred: {e}")
            print(traceback.format_exc())

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
        try:
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
        except Exception as e:
            print(f"An error occurred while adding text: {e}")
            print(traceback.format_exc())

    def add_image(self, selection):
        """Add an image to the PDF from the selected file."""
        try:
            if selection:
                image_path = selection[0]
                if os.path.exists(image_path):
                    try:
                        self.pdf.add_page()
                        self.pdf.image(image_path, x=10, y=None, w=190)  # Adjust width as needed
                        self.update_pdf_size()
                    except Exception as e:
                        print(f"Failed to add image: {e}")
                        print(traceback.format_exc())
        except Exception as e:
            print(f"An error occurred while adding image: {e}")
            print(traceback.format_exc())

    def save_pdf(self, instance):
        """Save the PDF to the default directory."""
        try:
            content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            file_name_input = TextInput(hint_text='Enter file name', multiline=False)
            content.add_widget(file_name_input)
            save_btn = Button(text='Save', size_hint_y=None, height=40)
            content.add_widget(save_btn)

            popup = Popup(title='Save PDF', content=content, size_hint=(0.9, 0.5))
            save_btn.bind(on_press=lambda x: self.save_pdf_to_location(file_name_input.text, popup))
            popup.open()
        except Exception as e:
            print(f"An error occurred while saving PDF: {e}")
            print(traceback.format_exc())

    def save_pdf_to_location(self, file_name, popup):
        try:
            if not file_name:
                file_name = "custom_document"
            output_file = os.path.join(self.default_dir, f"{file_name}.pdf")
            try:
                self.pdf.output(output_file)
                print(f"PDF saved as {output_file}")
                popup.dismiss()
            except Exception as e:
                print(f"Failed to save PDF: {e}")
                print(traceback.format_exc())
        except Exception as e:
            print(f"An error occurred while saving PDF to location: {e}")
            print(traceback.format_exc())

    def toggle_mode(self, instance, value):
        try:
            if value:
                self.root_window.background_color = (1, 1, 1, 1)  # Light mode
                self.update_ui_mode('light')
            else:
                self.root_window.background_color = (0, 0, 0, 1)  # Dark mode
                self.update_ui_mode('dark')
        except Exception as e:
            print(f"An error occurred while toggling mode: {e}")
            print(traceback.format_exc())

    def update_ui_mode(self, mode):
        """Update the UI elements to match the selected mode."""
        try:
            if mode == 'light':
                self.title_input.background_color = (1, 1, 1, 1)
                self.title_input.foreground_color = (0, 0, 0, 1)
                self.text_input.background_color = (1, 1, 1, 1)
                self.text_input.foreground_color = (0, 0, 0, 1)
            else:
                self.title_input.background_color = (0, 0, 0, 1)
                self.title_input.foreground_color = (1, 1, 1, 1)
                self.text_input.background_color = (0, 0, 0, 1)
                self.text_input.foreground_color = (1, 1, 1, 1)
        except Exception as e:
            print(f"An error occurred while updating UI mode: {e}")
            print(traceback.format_exc())

    def update_pdf_size(self):
        try:
            # Estimate PDF size (this is a rough estimation)
            size_kb = len(self.pdf.buffer) / 1024
            self.size_label.text = f'Estimated PDF size: {size_kb:.2f} KB'
        except Exception as e:
            print(f"An error occurred while updating PDF size: {e}")
            print(traceback.format_exc())

    def check_spelling(self, instance):
        """Check spelling in the text input."""
        try:
            text = self.text_input.text.strip()
            if text:
                chkr = SpellChecker("en_US")
                chkr.set_text(text)
                for err in chkr:
                    print(f"Misspelled word: {err.word}")
                    suggestions = ", ".join(err.suggest())
                    print(f"Suggestions: {suggestions}")
        except Exception as e:
            print(f"An error occurred while checking spelling: {e}")
            print(traceback.format_exc())

    def edit_pages(self, instance):
        """Edit pages after they are created."""
        try:
            content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            edit_text_input = CustomTextInput(multiline=True, hint_text='Edit text here')
            content.add_widget(edit_text_input)
            save_btn = Button(text='Save Changes', size_hint_y=None, height=40)
            content.add_widget(save_btn)

            popup = Popup(title='Edit Pages', content=content, size_hint=(0.9, 0.9))
            save_btn.bind(on_press=lambda x: self.save_page_edits(edit_text_input.text, popup))
            popup.open()
        except Exception as e:
            print(f"An error occurred while editing pages: {e}")
            print(traceback.format_exc())

    def save_page_edits(self, text, popup):
        """Save page edits."""
        try:
            if text:
                self.pdf.add_page()
                self.pdf.set_font("Arial", size=12)
                self.pdf.multi_cell(0, 10, text)
                self.update_pdf_size()
                popup.dismiss()
        except Exception as e:
            print(f"An error occurred while saving page edits: {e}")
            print(traceback.format_exc())

    def choose_text_color(self, instance):
        """Open a color picker to choose text color."""
        try:
            content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            color_picker = ColorPicker()
            content.add_widget(color_picker)
            select_btn = Button(text='Select', size_hint_y=None, height=40)
            content.add_widget(select_btn)

            popup = Popup(title='Choose Text Color', content=content, size_hint=(0.9, 0.9))
            select_btn.bind(on_press=lambda x: self.set_text_color(color_picker.color, popup))
            popup.open()
        except Exception as e:
            print(f"An error occurred while choosing text color: {e}")
            print(traceback.format_exc())

    def set_text_color(self, color, popup):
        """Set the selected text color."""
        try:
            self.text_color = color
            popup.dismiss()
        except Exception as e:
            print(f"An error occurred while setting text color: {e}")
            print(traceback.format_exc())

if __name__ == '__main__':
    PDFCreatorApp().run()
