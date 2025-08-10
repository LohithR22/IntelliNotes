# 🧠 IntelliNotes: AI-Powered PDF Note Generator

**Transform your lecture PDFs into expert-level study notes with the power of Large Language Models.**

This project automates the tedious process of note-taking by extracting text from your PDF lectures and using the Google Gemini API to generate detailed, well-structured notes. The real power lies in its customizable prompts, allowing you to command the AI to act as an expert in any field, providing insights, examples, and even practice problems.

---

## ✨ Features

- **Automated PDF Processing**: Batch processes all PDF files in a specified folder.
- **Powered by Google Gemini**: Leverages a powerful LLM for high-quality content generation.
- **Customizable AI Personas**: Easily modify the prompt to change the AI's expertise and the style of notes it generates (e.g., from a simple summary to an expert analysis).
- **Robust & Resilient**: Includes error handling and exponential backoff to manage API rate limits and transient network issues.
- **Consolidated Output**: Compiles notes from all PDFs into a single, clean, and portable Markdown (`.md`) file.

---

## 🔧 How It Works

The process is simple yet powerful:

1.  **Scan & Sort**: The script scans a designated folder for PDF files (`lec1.pdf`, `lec2.pdf`, etc.) and sorts them numerically.
2.  **Extract Text**: It reads each PDF and extracts its raw text content.
3.  **Prompt the AI**: The extracted text is inserted into a carefully crafted prompt. This prompt instructs the AI on its persona, the desired format, and the level of detail required.
4.  **Generate Notes**: The complete prompt is sent to the Google Gemini API, which generates the expert-level notes.
5.  **Compile**: The generated notes for each PDF are appended to a single Markdown file, creating your complete study guide.



---

## ⚙️ Setup & Installation

Follow these steps to get IntelliNotes up and running on your local machine.

### 1. Prerequisites

- Python 3.8 or higher.

### 2. Clone the Repository

```bash
git clone [https://github.com/LohithR22/IntelliNotes.git](https://github.com/LohithR22/IntelliNotes.git)
cd IntelliNotes
```

### 3\. Install Dependencies

Create a `requirements.txt` file with the following content:

```txt
google-generativeai
pypdf2
```

Then, install the required packages:

```bash
pip install -r requirements.txt
```

### 4\. Get Your Google Gemini API Key

  - Go to the [Google AI Studio](https://aistudio.google.com/app/apikey).
  - Click **"Create API key"** and copy your key.
  - **Important**: For security, it's best to set this key as an environment variable. However, for simplicity in this project, you will add it directly to the script. **Do not commit your API key to a public repository\!**

-----

## 🏃‍♂️ How to Use

1.  **Add Your PDFs**: Create a folder (e.g., `MyLectures`) and place your lecture PDFs inside. Make sure they are named sequentially (e.g., `lec1.pdf`, `lec2.pdf`, `lec10.pdf`) for correct ordering.

2.  **Configure the Script**: Open your main Python script and update the following variables at the top:

      - `GOOGLE_API_KEY`: Paste your Gemini API key here.
      - `PDF_FOLDER_PATH`: Set the path to the folder containing your PDFs.
      - `OUTPUT_FILE_NAME`: Choose a name for your final notes file.

3.  **Customize the Prompt (Optional but Recommended)**: Navigate to the `get_gemini_summary` function and modify the `prompt` variable to suit your needs. See the section below for powerful examples.

4.  **Run the Script**:

    ```bash
    python your_script_name.py
    ```

5.  **Get Your Notes**: Once the script finishes, a new Markdown file (e.g., `My_Course_Notes.md`) will appear in your project directory. You can open this file with any text editor or Markdown viewer like VS Code, Obsidian, or Typora.

-----

## 🧠 Customizing the AI Persona (The Magic Sauce)

This is where IntelliNotes truly shines. By changing the `prompt` variable, you can fundamentally alter the output. Don't just ask for a summary; command the AI to be the expert you need.

Simply replace the `prompt` string in the `get_gemini_summary` function with one of the examples below or create your own\!

### Example 1: The Entrepreneurship & IP Strategy Expert

Use this when you want business-oriented notes with strategic insights and real-world applications.

```python
prompt = f"""You are a seasoned expert in entrepreneurship and intellectual property (IP) strategy. Your task is to analyze the following lecture content and transform it into a set of comprehensive, expert-level notes.

Do not simply summarize the provided text. Instead, your goal is to add significant value by elaborating on the key concepts with detailed explanations and strategic insights.

For each core topic or definition mentioned in the lecture, you must:
- **Provide In-Depth Explanations**: Clearly explain each concept as if you were mentoring a new entrepreneur.
- **Include Practical Examples**: Illustrate every major point with real-world examples relevant to startups.
- **Discuss Strategic Implications**: Analyze why each concept is critical for a new venture.

Present the final output in a well-structured Markdown format.

Lecture Content:
{text_content}"""
```

### Example 2: The Distributed Systems Expert

Use this for technical subjects where you need deep explanations, architectural examples, and even practice problems.

```python
prompt = f"""You are a distinguished expert and author in the field of distributed systems. Your task is to analyze the following lecture material and expand it into a comprehensive study guide.

Do not merely summarize the text. For each major concept, you must:

- **Provide Expert Explanations**: Deconstruct complex topics (e.g., CAP Theorem, Paxos/Raft) into clear, intuitive explanations.
- **Cite Real-World Examples**: Illustrate with specific examples from large-scale systems (e.g., Google's Spanner, Amazon's DynamoDB).
- **Create Numerical Problems**: For key concepts (like availability, latency, or consensus), you must create and solve a relevant numerical problem.
- **Analyze Trade-offs**: Discuss the inherent trade-offs associated with each concept.

Structure the final output as a professional study guide using Markdown.

Lecture Content:
{text_content}"""
```

-----

## 📜 License

This project is distributed under the MIT License. See `LICENSE` for more information.

```
```