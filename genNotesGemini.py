import os
import re
from google.colab import drive
import PyPDF2
import google.generativeai as genai
import time

# --- 1. Mount Google Drive (if your PDFs are in Drive) ---
# # This will open a new tab/window for authentication. Follow the instructions.
# print("Mounting Google Drive...")
# drive.mount('/content/drive')
# print("Google Drive mounted successfully!")

# --- 2. Configure your Gemini API Key ---
# IMPORTANT: Replace 'YOUR_GEMINI_API_KEY' with your actual API key.
# You can get one from Google AI Studio: https://makersuite.google.com/
# It's recommended to store this as a Colab secret for security.
# Go to the 'Secrets' tab (lock icon on the left sidebar), add a new secret named API_KEY, and paste your Gemini API key there.
# Then, uncomment the line below:
# from google.colab import userdata
# API_KEY = userdata.get('API_KEY')
API_KEY = os.getenv("GEMINI_API_KEY") # Replace this or use Colab secrets
genai.configure(api_key=API_KEY)

# --- 3. Define your PDF folder path and output file name ---
# Adjust 'YOUR_LECTURE_FOLDER_PATH' to the actual path in your Google Drive or Colab environment.
# Example for Google Drive: '/content/drive/MyDrive/MyLectures/PDFs'
# Example for Colab session storage: '/content/my_pdfs' (if you upload directly)
PDF_FOLDER_PATH = '/content/drive/MyDrive/Distributed_systems_nptel' # <--- IMPORTANT: SET YOUR FOLDER PATH HERE
OUTPUT_FILE_NAME = 'DS_notes_nptel.md'

# --- Function to extract text from a PDF ---
def extract_text_from_pdf(pdf_path):
    """
    Extracts all text content from a given PDF file.
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or '' # Use .extract_text() and handle None
            return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return None

# --- Function to get summary from Gemini API with exponential backoff ---
def get_gemini_summary(text_content, max_retries=5, initial_delay=5):
    """
    Sends text content to Gemini API for summarization with exponential backoff.
    """
    # CORRECTED: Updated to a valid and current model name.
    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = f"""You are a distinguished expert and author in the field of distributed systems, with deep knowledge of system architecture, concurrency, consensus, and fault tolerance. Your task is to analyze the following lecture material and expand it into a comprehensive study guide.

Your goal is to add significant value and clarity. Do not merely summarize the text. Instead, for each major concept presented, you must:

- **Provide Expert Explanations**: Deconstruct complex topics (e.g., CAP Theorem, Paxos/Raft, replication, sharding) into clear, intuitive explanations. Use analogies to make them easier to understand for a software engineer new to the field.

- **Cite Real-World Examples**: Illustrate the concepts with specific, practical examples from well-known, large-scale systems. Reference systems like Google's Spanner, Amazon's DynamoDB, LinkedIn's Kafka deployments, or Facebook's Cassandra usage where appropriate.

- **Create Numerical Problems**: For key performance or theoretical concepts (like availability, latency, or consensus), you must **create and solve a relevant numerical problem** or quantitative example. For instance:
    - If discussing **availability**, calculate system uptime for "five nines" vs. "three nines."
    - If discussing **latency**, create a problem calculating round-trip time in a geo-distributed setting.
    - If discussing **consensus algorithms** like Raft, calculate the quorum size needed for a cluster of a given size.

- **Analyze Trade-offs**: Discuss the inherent trade-offs associated with each concept. For example, explain the consistency vs. availability trade-off in the CAP theorem or the performance implications of different consistency models.

Structure the final output as a professional study guide using Markdown. Use headings, bullet points, bold text for key terms, and code blocks for configuration snippets or pseudo-code.

Lecture Content:
{text_content}"""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    # CORRECTED: Changed response_mime_type to 'text/plain' as 'text/markdown' is not supported.
                    # The prompt already instructs the model to generate Markdown content.
                    response_mime_type="text/plain"
                )
            )
            # Access the text from the response candidate
            return response.text
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                sleep_time = initial_delay * (2 ** attempt)
                print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print("Max retries reached. Skipping this summary.")
                return f"**[Error: Could not summarize due to API issue after multiple retries.]**"


# --- Main script execution ---
def main():
    if not os.path.exists(PDF_FOLDER_PATH):
        print(f"Error: Folder '{PDF_FOLDER_PATH}' not found. Please check the path and ensure Google Drive is mounted correctly.")
        return

    pdf_files = [f for f in os.listdir(PDF_FOLDER_PATH) if f.endswith('.pdf')]

    # Sort files numerically based on the number in "lecX"
    def get_lecture_number(filename):
        match = re.search(r'lec(\d+)\.pdf', filename, re.IGNORECASE)
        return int(match.group(1)) if match else 0 # Return 0 if no number found, ensuring it's sorted first

    # Filter out files that don't match the 'lecX.pdf' pattern reliably for sorting
    processable_pdfs = [f for f in pdf_files if re.search(r'lec(\d+)\.pdf', f, re.IGNORECASE)]
    processable_pdfs.sort(key=get_lecture_number)

    if not processable_pdfs:
        print(f"No PDF files matching 'lecX.pdf' found in '{PDF_FOLDER_PATH}'.")
        return

    all_summaries_content = []
    print(f"Found {len(processable_pdfs)} PDF files. Starting summarization...")

    for i, filename in enumerate(processable_pdfs):
        pdf_path = os.path.join(PDF_FOLDER_PATH, filename)
        print(f"\n--- Processing Lecture {i + 1}/{len(processable_pdfs)}: {filename} ---")

        pdf_text = extract_text_from_pdf(pdf_path)

        if pdf_text:
            if len(pdf_text.strip()) < 50: # Basic check for very short/empty extraction
                summary = "*Could not extract sufficient text from this PDF or PDF is empty.*"
                print(f"  Warning: Extracted text from {filename} is very short or empty. Skipping summarization.")
            else:
                summary = get_gemini_summary(pdf_text)
                print("  Summary generated.")
        else:
            summary = "**[Error: Failed to extract text from PDF.]**"
            print(f"  Error: Failed to extract text from {filename}. Skipping summarization.")

        all_summaries_content.append(f"# Lecture {get_lecture_number(filename)}: {filename.replace('.pdf', '')}\n\n{summary}\n\n---\n\n")

    # Write all summaries to a single Markdown file
    output_path = os.path.join('/content/', OUTPUT_FILE_NAME) # Save in Colab content folder
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write("--- Lecture Notes Summary ---\n\n")
        outfile.write("This document contains summaries of all lectures, generated by the Gemini API.\n\n")
        outfile.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        outfile.write("---\n\n")
        outfile.write("".join(all_summaries_content))

    print(f"\nAll summaries compiled into '{output_path}'")
    print("You can download this file from the Colab file browser (left sidebar) or copy its content.")

if __name__ == '__main__':
    main()