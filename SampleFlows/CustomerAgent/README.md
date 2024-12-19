###This is a simplified adaption of https://github.com/techwithtim/Langflow-Customer-Support-Agent
to work on langflow==1.1.1

In order for this to work, 
-first do all steps in the top level README.md to host langflow
-then import "Ollama Customer FAQ flow.json" & "Customer Support Demo-Ollama.json"
-then from "Ollama Customer FAQ flow" in langflow, run the part to import Company_FAQ.pdf
-lastly, install requirements.txt using pip and run command "streamlit run .\main.py"