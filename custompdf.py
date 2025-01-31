import os
import platform
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser, Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from fpdf import FPDF
from PIL import Image, ImageTk, ImageOps
import enchant
from enchant.checker import SpellChecker

class PDFCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Creator")
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.default_dir = self.get_default_directory()
        self.recent_files = []
        self.create_widgets()
        self.dark_mode = False
        self.current_page = 1

    def create_widgets(self):
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.title_input = tk.Entry(self.frame, width=50)
        self.title_input.insert(0, "Enter title here")
        self.title_input.pack(pady=5)

        self.text_input = ScrolledText(self.frame, width=50, height=10, undo=True)
        self.text_input.insert(tk.END, "Enter text here")
        self.text_input.pack(pady=5)
        self.create_context_menu()

        self.file_chooser_btn = tk.Button(self.frame, text="Choose Image", command=self.choose_image, bg="aqua")
        self.file_chooser_btn.pack(pady=5)

        self.image_label = tk.Label(self.frame)
        self.image_label.pack(pady=5)

        self.image_options_frame = tk.Frame(self.frame)
        self.image_options_frame.pack(pady=5)

        self.rotate_left_btn = tk.Button(self.image_options_frame, text="Rotate Left", command=self.rotate_image_left, bg="aqua")
        self.rotate_left_btn.pack(side=tk.LEFT, padx=5)

        self.rotate_right_btn = tk.Button(self.image_options_frame, text="Rotate Right", command=self.rotate_image_right, bg="aqua")
        self.rotate_right_btn.pack(side=tk.LEFT, padx=5)

        self.resize_btn = tk.Button(self.image_options_frame, text="Resize Image", command=self.resize_image, bg="aqua")
        self.resize_btn.pack(side=tk.LEFT, padx=5)

        self.add_text_btn = tk.Button(self.frame, text="Add Text", command=self.add_text, bg="aqua")
        self.add_text_btn.pack(pady=5)

        self.add_image_btn = tk.Button(self.frame, text="Add Image", command=self.add_image, bg="aqua")
        self.add_image_btn.pack(pady=5)

        self.save_btn = tk.Button(self.frame, text="Save PDF", command=self.save_pdf, bg="aqua")
        self.save_btn.pack(pady=5)

        self.spell_check_btn = tk.Button(self.frame, text="Check Spelling", command=self.check_spelling, bg="aqua")
        self.spell_check_btn.pack(pady=5)

        self.edit_pages_btn = tk.Button(self.frame, text="Edit Pages", command=self.edit_pages, bg="aqua")
        self.edit_pages_btn.pack(pady=5)

        self.preview_btn = tk.Button(self.frame, text="Preview PDF", command=self.preview_pdf, bg="aqua")
        self.preview_btn.pack(pady=5)

        self.toggle_mode_btn = tk.Button(self.frame, text="Toggle Dark/Light Mode", command=self.toggle_mode, bg="aqua")
        self.toggle_mode_btn.pack(pady=5)

        self.text_format_frame = tk.Frame(self.frame)
        self.text_format_frame.pack(pady=5)

        self.bold_btn = tk.Button(self.text_format_frame, text="Bold", command=lambda: self.format_text("bold"), bg="aqua")
        self.bold_btn.pack(side=tk.LEFT, padx=5)

        self.italic_btn = tk.Button(self.text_format_frame, text="Italic", command=lambda: self.format_text("italic"), bg="aqua")
        self.italic_btn.pack(side=tk.LEFT, padx=5)

        self.underline_btn = tk.Button(self.text_format_frame, text="Underline", command=lambda: self.format_text("underline"), bg="aqua")
        self.underline_btn.pack(side=tk.LEFT, padx=5)

        self.color_btn = tk.Button(self.text_format_frame, text="Text Color", command=self.choose_text_color, bg="aqua")
        self.color_btn.pack(side=tk.LEFT, padx=5)

        self.progress_bar = ttk.Progressbar(self.frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=5)

        self.root.bind("<Control-s>", lambda event: self.save_pdf())
        self.root.bind("<Control-o>", lambda event: self.open_pdf())
        self.root.bind("<Control-z>", lambda event: self.text_input.edit_undo())
        self.root.bind("<Control-y>", lambda event: self.text_input.edit_redo())

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Cut", command=lambda: self.text_input.event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Copy", command=lambda: self.text_input.event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Paste", command=lambda: self.text_input.event_generate("<<Paste>>"))
        self.text_input.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def get_default_directory(self):
        if platform.system() == "Linux" and "ANDROID_ROOT" in os.environ:
            return "/sdcard/Download"
        elif platform.system() == "Windows":
            return os.path.join(os.environ["USERPROFILE"], "Downloads")
        elif platform.system() == "Darwin":
            return os.path.expanduser("~/Downloads")
        else:
            return os.getcwd()

    def add_text(self):
        title = self.title_input.get().strip()
        text = self.text_input.get("1.0", tk.END).strip()
        if title:
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(0, 10, title, ln=True)
            self.title_input.delete(0, tk.END)
        if text:
            self.pdf.set_font("Arial", size=12)
            self.pdf.multi_cell(0, 10, text)
            self.text_input.delete("1.0", tk.END)
        self.current_page = self.pdf.page_no()

    def choose_image(self):
        self.image_path = filedialog.askopenfilename(initialdir=self.default_dir, title="Select Image",
                                                     filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")))
        if self.image_path:
            self.img = Image.open(self.image_path)
            self.display_image(self.img)

    def display_image(self, img):
        img.thumbnail((200, 200))
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img

    def rotate_image_left(self):
        if hasattr(self, 'img'):
            self.img = self.img.rotate(90, expand=True)
            self.display_image(self.img)

    def rotate_image_right(self):
        if hasattr(self, 'img'):
            self.img = self.img.rotate(-90, expand=True)
            self.display_image(self.img)

    def resize_image(self):
        if hasattr(self, 'img'):
            size_options = [
                (16, 16), (32, 32), (64, 64), (128, 128), (256, 256),
                (512, 512), (1024, 1024), (2048, 2048), (3840, 2160)
            ]
            size_str = "\n".join([f"{i+1}. {size[0]}x{size[1]}" for i, size in enumerate(size_options)])
            choice = simpledialog.askinteger("Resize Image", f"Choose size:\n{size_str}")
            if choice and 1 <= choice <= len(size_options):
                width, height = size_options[choice - 1]
                self.img = self.img.resize((width, height), Image.LANCZOS)
                self.display_image(self.img)

    def add_image(self):
        if hasattr(self, 'img'):
            try:
                self.pdf.add_page()
                self.img.save("temp_image.png")
                self.pdf.image("temp_image.png", x=10, y=None, w=190)
                os.remove("temp_image.png")
                self.current_page = self.pdf.page_no()
                messagebox.showinfo("Success", "Image added to PDF.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add image: {e}")

    def save_pdf(self):
        file_name = simpledialog.askstring("Save PDF", "Enter file name")
        if file_name:
            output_file = os.path.join(self.default_dir, f"{file_name}.pdf")
            try:
                self.pdf.output(output_file)
                messagebox.showinfo("Success", f"PDF saved as {output_file}")
                self.recent_files.append(output_file)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save PDF: {e}")

    def check_spelling(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if text:
            chkr = SpellChecker("en_US")
            chkr.set_text(text)
            for err in chkr:
                messagebox.showinfo("Spelling Error", f"Misspelled word: {err.word}\nSuggestions: {', '.join(err.suggest())}")

    def edit_pages(self):
        edit_text = simpledialog.askstring("Edit Pages", "Edit text here")
        if edit_text:
            self.pdf.add_page()
            self.pdf.set_font("Arial", size=12)
            self.pdf.multi_cell(0, 10, edit_text)
        self.current_page = self.pdf.page_no()

    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.root.config(bg="#2E2E2E")
            self.frame.config(bg="#2E2E2E")
            self.title_input.config(bg="#3E3E3E", fg="white")
            self.text_input.config(bg="#3E3E3E", fg="white")
            self.toggle_mode_btn.config(bg="#3E3E3E", fg="white")
        else:
            self.root.config(bg="white")
            self.frame.config(bg="white")
            self.title_input.config(bg="white", fg="black")
            self.text_input.config(bg="white", fg="black")
            self.toggle_mode_btn.config(bg="white", fg="black")

    def format_text(self, tag):
        current_tags = self.text_input.tag_names("sel.first")
        if tag in current_tags:
            self.text_input.tag_remove(tag, "sel.first", "sel.last")
        else:
            self.text_input.tag_add(tag, "sel.first", "sel.last")
        self.text_input.tag_configure("bold", font=("Arial", 12, "bold"))
        self.text_input.tag_configure("italic", font=("Arial", 12, "italic"))
        self.text_input.tag_configure("underline", font=("Arial", 12, "underline"))

    def choose_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_input.tag_add("color", "sel.first", "sel.last")
            self.text_input.tag_configure("color", foreground=color)

    def open_pdf(self):
        file_path = filedialog.askopenfilename(initialdir=self.default_dir, title="Open PDF",
                                               filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))
        if file_path:
            # Implement PDF opening functionality here
            pass

    def browse_text_file(self):
        file_path = filedialog.askopenfilename(initialdir=self.default_dir, title="Open Text File",
                                               filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert(tk.END, text)

    def preview_pdf(self):
        preview_window = Toplevel(self.root)
        preview_window.title("PDF Preview")
        preview_text = ScrolledText(preview_window, width=50, height=20)
        preview_text.pack(pady=10)
        preview_text.insert(tk.END, self.get_pdf_text())
        preview_text.config(state=tk.DISABLED)

    def get_pdf_text(self):
        # This is a placeholder function. You would need to implement a way to extract text from the PDF.
        # For now, it just returns the text from the text_input widget.
        return self.text_input.get("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCreatorApp(root)
    root.mainloop()
