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
