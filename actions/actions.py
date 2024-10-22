# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

# Import the necessary RASA and PDF libraries
import rasa_sdk 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import fitz  # PyMuPDF for reading the PDF


# Function to extract all text from the PDF
def extract_comparison_data(pdf_path="C:\Sooryakrishna M\Samhitha\IPC-BNS_Table.pdf"):
    doc = fitz.open(pdf_path="C:\Sooryakrishna M\Samhitha\IPC-BNS_Table.pdf")
    text = ""

    # Extract text from each page
    for page in doc:
        text += page.get_text()

    return text

# Function to search for a specific section in the extracted text
def get_law_section(comparison_text, section_number):
    # Check if the section number exists in the text
    if section_number in comparison_text:
        # Extract relevant section info, adjust range as needed
        section_data = comparison_text[comparison_text.find(section_number):].split("\n")[0:10]
        return "\n".join(section_data)
    else:
        return "Section not found in the comparison."

# Custom action to retrieve law section comparison
class ActionCompareLaw(Action):

    def name(self) -> str:
        return "action_compare_law"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        section_number = tracker.get_slot("section_number")  # Retrieve section number slot from user input
        pdf_path = "/path/to/your/IPC-BNS_Table.pdf"  # Path to your PDF file

        # Extract comparison text from PDF
        comparison_text = extract_comparison_data(pdf_path)

        # Retrieve the comparison result for the given section number
        comparison_result = get_law_section(comparison_text, section_number)

        # Send the result back to the user
        dispatcher.utter_message(text=f"The comparison for section {section_number} is:\n{comparison_result}")

        return []
