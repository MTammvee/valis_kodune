import os
from difflib import SequenceMatcher
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import tempfile
from tkinter import Tk, filedialog

def index_documents(input_folder, index_file):
    documents = []
    for file in os.listdir(input_folder):
        if file.endswith(".pdf"):
            pdf_loader = PyPDFLoader(os.path.join(input_folder, file))
            documents.extend(pdf_loader.load_and_split())
    
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local(index_file)
    print(f"Indexing complete. Index saved to {index_file}.")

def index_text(text, index_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(text.encode("utf-8"))
    
    text_loader = TextLoader(temp_file_path)
    documents = text_loader.load_and_split()

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local(index_file)
    print(f"Text indexing complete. Index saved to {index_file}.")

    os.remove(temp_file_path)

def get_contextual_snippet(text, query, snippet_length=200, highlight_start="**", highlight_end="**"):
    match = SequenceMatcher(None, text.lower(), query.lower()).find_longest_match(0, len(text), 0, len(query))
    if match.size == 0:
        return text[:snippet_length]

    start = max(0, match.a - snippet_length // 2)
    end = min(len(text), match.a + match.size + snippet_length // 2)
    snippet = text[start:end]

    match_start = match.a - start
    match_end = match_start + match.size
    highlighted_snippet = (
        snippet[:match_start] +
        highlight_start + snippet[match_start:match_end] + highlight_end +
        snippet[match_end:]
    )
    return highlighted_snippet.strip()

def query_index(index_file, question, threshold=1):
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vector_store = FAISS.load_local(index_file, embeddings, allow_dangerous_deserialization=True)
    results = vector_store.similarity_search_with_score(question, k=5)
    
    filtered_results = [(res, score) for res, score in results if score >= threshold]
    
    if not filtered_results:
        return "No satisfactory results found. Try rephrasing your question or using more specific terms. Question has to be a full sentence and in English."

    output = []
    for i, (result, score) in enumerate(filtered_results):
        contextual_snippet = get_contextual_snippet(result.page_content, question, highlight_start="**", highlight_end="**")
        metadata = result.metadata or "No metadata provided"
        output.append(f"Result {i + 1} (Score: {score:.2f}):\nSnippet: {contextual_snippet}...\nMetadata: {metadata}")
    
    return "\n\n".join(output)

def start_questioning(index_file):
    print("\nYou can now ask questions about the indexed documents.")
    while True:
        question = input("\nEnter your question (or type 'exit' to quit): ").strip()
        if question.lower() == 'exit':
            print("Exiting the questioning phase. Goodbye!")
            break
        threshold = float(input("Enter a similarity threshold (default is 1 | Range 0-2): ") or 1)
        answer = query_index(index_file, question, threshold=threshold)
        print(f"\n{answer}")

def main():
    print("Choose an option:")
    print("1. Query the index")
    print("2. Add documents to the index")
    print("3. Input text manually")
    choice = input("Enter your choice (1/2/3): ").strip()

    index_file = "doc_search/index/vector_store"

    if choice == "1":
        if not os.path.exists(index_file):
            print("Index file not found. Please index documents first.")
            return
        start_questioning(index_file)
    elif choice == "2":
        print("Select PDF files to index.")
        Tk().withdraw()
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if not file_paths:
            print("No files selected. Exiting.")
            return
        input_folder = "doc_search/data"
        os.makedirs(input_folder, exist_ok=True)
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            os.rename(file_path, os.path.join(input_folder, file_name))
        index_documents(input_folder, index_file)

        start_questioning(index_file)
    elif choice == "3":
        print("Enter your text below (press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        manual_text = "\n".join(lines)
        index_text(manual_text, index_file)

        start_questioning(index_file)
    else:
        print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
