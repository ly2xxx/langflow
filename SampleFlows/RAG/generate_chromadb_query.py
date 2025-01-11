import json
import re

def generate_chromadb_query(file_list, user_question):
    # Preprocess the user question to extract relevant keywords
    relevant_keywords = re.findall(r'\b\w+\b', user_question.lower())
    
    # Initialize a dictionary to store file information
    files_info = {}
    
    # Populate the files_info dictionary with file metadata
    for file in file_list:
        with open(file, 'r') as f:
            content = f.read()
            if re.search(r'\d{8}', content) and 'funds' in content.lower():
                files_info[file] = {'date': re.search(r'\d{8}', content).group()}
    
    # Determine the most relevant file based on user question
    relevant_files = [file for file, info in files_info.items() if any(keyword in file or keyword in info['date'] for keyword in relevant_keywords)]
    
    # Generate Chromadb query with filter clause if a relevant file is found
    if relevant_files:
        query_text = f"What is fund {relevant_files[0].split('_')[-1]} launch date?"
        query_filter = {"file_path": relevant_files[0]}
        return json.dumps({"query_text": query_text, "filter": query_filter})
    
    # Generate Chromadb query without filter clause if no relevant file is found
    else:
        return json.dumps({"query_text": user_question})

# Example usage
file_list = ["6_B0O3_Fact-Sheet_UK-Smaller-Companies-Index-Fund-LG-PMC-UK-Smaller-Companies-Index-Fund-3_31-10-2024.md"]
user_question = "What's the fund's Launch date?"
print(generate_chromadb_query(file_list, user_question))