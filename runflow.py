from langflow.load import load_flow_from_json, run_flow_from_json

# flow = load_flow_from_json("SampleFlows\Ollama Code Generator.json")
# result = flow("Write me the python code using python-pptx libraries to (1) Take content from input_ppt, (2) Take the slide shapes format from template_ppt, (3) Create output_ppt based on content from input_ppt in slide shapes format defined in template_ppt")
# Use the build and execute methods
# result = flow.execute({
#     "input": "Write me the python code using python-pptx libraries to (1) Take content from input_ppt, (2) Take the slide shapes format from template_ppt, (3) Create output_ppt based on content from input_ppt in slide shapes format defined in template_ppt"
# })
# result = run_flow_from_json(flow, "Write me the python code using python-pptx libraries to (1) Take content from input_ppt, (2) Take the slide shapes format from template_ppt, (3) Create output_ppt based on content from input_ppt in slide shapes format defined in template_ppt")
# pass the JSON file path directly
result = run_flow_from_json(
    "SampleFlows/Ollama Code Generator.json",  # Direct path to JSON file
    "Write me the python code using python-pptx libraries to (1) Take content from input_ppt, (2) Take the slide shapes format from template_ppt, (3) Create output_ppt based on content from input_ppt in slide shapes format defined in template_ppt"
)
print(result)