# How to Run the Code

Follow the steps below to set up and run the project:

## Steps

1. **Clone the Repository from terminal**
   ```bash
   git clone <repository_url>

2. **Move to the pulled folder from terminal**
   ```bash
   cd valis_kodune

3. **Activate your desired conda environment from terminal, where you want to use the tool**
   ```bash
   conda activate your_environment_name

4. **Install the requirements needed to run the tool from terminal**
   ```bash
   pip install -r requirements.txt

# User Guide

1. **Run the Script**
   ```bash
   doc_query_tool

2. **Choose an Optionl**
After running, the program will prompt you to choose from three options:

* Option 1: Query the indexed documents.
* Option 2: Index PDF documents.
* Option 3: Index manually entered text.
  
Enter the corresponding number (1, 2, or 3) to proceed.

# How to Use Each Option
1. **Query the Index**
* If you’ve already indexed documents, choose this option to ask questions.
* Enter your question (in English) when prompted.
* Set a similarity threshold (default: 1.0, range: 0.0 - 2.0). A lower threshold gives broader matches, while a higher threshold gives stricter matches.
* View the results with relevant snippets and metadata.
2. **Add Documents to the Index**
* Select PDF files to index via a file dialog.
* The program extracts and processes the content for efficient searching.
* Once complete, you can start querying the index.
3. **Input Text Manually**
* Type or paste text into the console, pressing "Enter" twice to finish input.
* The entered text is indexed and made available for querying.

# Interpreting the Output

When querying, the program returns results in the following format:

1. Score

* Indicates how closely the result matches your query. Higher scores signify better matches.
2. Snippet

* A contextual portion of the document or text where your query matches.
* The relevant section is highlighted for clarity (e.g., ** matched text **).
3. Metadata

* Provides additional information about the document, such as its origin or section.

# Example Output
   ```bash
Result 1 (Score: 1.85):
Snippet: The **quick brown fox** jumps over the lazy dog...
Metadata: No metadata provided.

Result 2 (Score: 1.50):
Snippet: In the story, the **quick fox** symbolizes agility and cunning...
Metadata: Chapter 2, Page 15. 
```

If no results meet the threshold, you’ll see:
   ```bash
No satisfactory results found. Try rephrasing your question or using more specific terms.
```
