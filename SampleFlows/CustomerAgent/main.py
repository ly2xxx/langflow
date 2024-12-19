# import argparse
# import json
# from argparse import RawTextHelpFormatter
import requests
import json
import streamlit as st
# from typing import Optional
# import warnings
# try:
#     from langflow.load import upload_file
# except ImportError:
#     warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
#     upload_file = None

BASE_API_URL = "http://127.0.0.1:7860"
FLOW_ID = "d7e58b5a-37fc-4353-8e56-ac9a81623a9c"
ENDPOINT = "Customer-Support-Demo-Ollama" # You can set a specific endpoint name in the flow settings

# # You can tweak the flow by adding a tweaks dictionary
# # e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
# TWEAKS = {
#   "FlowTool-dBmBp": {},
#   "ToolCallingAgent-qq4Ul": {},
#   "ChatInput-NaxBM": {},
#   "ChatOutput-jjgRF": {},
#   "OllamaModel-lMPYf": {}
# }

# def run_flow(message: str,
#   endpoint: str,
#   output_type: str = "chat",
#   input_type: str = "chat",
#   tweaks: Optional[dict] = None,
#   api_key: Optional[str] = None) -> dict:
def run_flow(message: str) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat", #output_type,
        "input_type": "chat",#input_type,
    }
    headers = None
    # if tweaks:
    #     payload["tweaks"] = tweaks
    # if api_key:
    #     headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# {'session_id': 'd7e58b5a-37fc-4353-8e56-ac9a81623a9c', 
# 'outputs': [{'inputs': {'input_value': 'What are the shipment times?'}, 
# 'outputs': [{'results': {'message': 
# {'timestamp': '2024-12-19T23:20:45', 'sender': 'Machine', 'sender_name': 'AI', 'session_id': 'd7e58b5a-37fc-4353-8e56-ac9a81623a9c', 
# 'text': "Based on the tool's output, I can tell you that the shipment times are:\n\n* 3-5 business days for domestic orders\n* 7-14 business days for international orders\n\nAdditionally, expedited shipping options are available at checkout. If you need more information or have specific questions about delivery times, our customer support team is happy to help!", 'files': [], 'error': False, 'edit': False, 'properties': {'text_color': '', 'background_color': '', 'edited': False, 'source': {'id': 'ToolCallingAgent-qq4Ul', 'display_name': 'Tool Calling Agent', 'source': 'Tool Calling Agent'}, 'icon': 'LangChain', 'allow_markdown': False, 'state': 'complete', 'targets': []}, 'category': 'message', 'content_blocks': [{'title': 'Agent Steps', 'contents': [{'type': 'text', 'duration': 79, 'header': {'title': 'Input', 'icon': 'MessageSquare'}, 'text': ''}, {'type': 'tool_use', 'duration': 49906, 'header': {'title': 'Executed **FAQ-Agent**', 'icon': 'Hammer'}, 'name': 'FAQ-Agent', 'tool_input': {'chat_input': 'What are the shipment times?'}, 'output': "Flow run output:\nAccording to our Frequently Asked Questions, our standard shipment times are:\n\n* 3-5 business days for domestic orders\n* 7-14 business days for international orders\n\nWe also offer expedited shipping options at checkout, which can help reduce the delivery time. If you're interested in knowing more about our specific shipping options and estimated delivery times, please feel free to reach out to our customer support team, who would be happy to assist you further!", 'error': None}, {'type': 'text', 'duration': 40500, 'header': {'title': 'Output', 'icon': 'MessageSquare'}, 'text': "Based on the tool's output, I can tell you that the shipment times are:\n\n* 3-5 business days for domestic orders\n* 7-14 business days for international orders\n\nAdditionally, expedited shipping options are available at checkout. If you need more information or have specific questions about delivery times, our customer support team is happy to help!"}], 'allow_markdown': True, 'media_url': None}], 'id': 'e86c50b8-bdfb-4a95-b5c5-1ec42b0fa67b', 'flow_id': 'd7e58b5a-37fc-4353-8e56-ac9a81623a9c'}}, 'artifacts': {'message': "Based on the tool's output, I can tell you that the shipment times are:\n\n* 3-5 business days for domestic orders\n\n* 7-14 business days for international orders\n\nAdditionally, expedited shipping options are available at checkout. If you need more information or have specific questions about delivery times, our customer support team is happy to help!", 'sender': 'Machine', 'sender_name': 'AI', 'files': [], 'type': 'object'}, 'outputs': {'message': {'message': {'timestamp': '2024-12-19 23:20:45 ', 'sender': 'Machine', 'sender_name': 'AI', 'session_id': 'd7e58b5a-37fc-4353-8e56-ac9a81623a9c', 'text': "Based on the tool's output, I can tell you that the shipment times are:\n\n* 3-5 business days for domestic orders\n* 7-14 business days for international orders\n\nAdditionally, expedited shipping options are available at checkout. If you need more information or have specific questions about delivery times, our customer support team is happy to help!", 'files': [], 'error': False, 'edit': False, 'properties': {'text_color': '', 'background_color': '', 'edited': False, 'source': {'id': 'ToolCallingAgent-qq4Ul', 'display_name': 'Tool Calling Agent', 'source': 'Tool Calling Agent'}, 'icon': 'LangChain', 'allow_markdown': False, 'state': 'complete', 'targets': []}, 'category': 'message', 'content_blocks': [{'title': 'Agent Steps', 'contents': [{'type': 'text', 'duration': 79, 'header': {'title': 'Input', 'icon': 'MessageSquare'}, 'text': ''}, {'type': 'tool_use', 'duration': 49906, 'header': {'title': 'Executed **FAQ-Agent**', 'icon': 'Hammer'}, 'name': 'FAQ-Agent', 'tool_input': {'chat_input': 'What are the shipment times?'}, 'output': "Flow run output:\nAccording to our Frequently Asked Questions, our standard shipment times are:\n\n* 3-5 business days for domestic orders\n* 7-14 business days for international orders\n\nWe also offer expedited shipping options at checkout, which can help reduce the delivery time. If you're interested in knowing more about our specific shipping options and estimated delivery times, please feel free to reach out to our customer support team, who would be happy to assist you further!", 'error': None}, {'type': 'text', 'duration': 40500, 'header': {'title': 'Output', 'icon': 'MessageSquare'}, 'text': "Based on the tool's output, I can tell you that the shipment times are:\n\n* 3-5 business days for domestic orders\n* 7-14 business days for international orders\n\nAdditionally, expedited shipping options are available at checkout. If you need more information or have specific questions about delivery times, our customer support team is happy to help!"}], 'allow_markdown': True, 'media_url': None}], 'id': 'e86c50b8-bdfb-4a95-b5c5-1ec42b0fa67b', 'flow_id': 'd7e58b5a-37fc-4353-8e56-ac9a81623a9c'}, 'type': 'object'}}, 'logs': {'message': []}, 'messages': [], 'component_display_name': 'Chat Output', 'component_id': 'ChatOutput-jjgRF', 'used_frozen_result': False}]}]}
def main():
    st.title("Chat Interface")
    
    message = st.text_area("Message", placeholder="Ask something...")
    
    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return
    
        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
            
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()

# result = run_flow("What are the shipment times?")
# print(result)

# def main():
#     parser = argparse.ArgumentParser(description="""Run a flow with a given message and optional tweaks.
# Run it like: python <your file>.py "your message here" --endpoint "your_endpoint" --tweaks '{"key": "value"}'""",
#         formatter_class=RawTextHelpFormatter)
#     parser.add_argument("message", type=str, help="The message to send to the flow")
#     parser.add_argument("--endpoint", type=str, default=ENDPOINT or FLOW_ID, help="The ID or the endpoint name of the flow")
#     parser.add_argument("--tweaks", type=str, help="JSON string representing the tweaks to customize the flow", default=json.dumps(TWEAKS))
#     parser.add_argument("--api_key", type=str, help="API key for authentication", default=None)
#     parser.add_argument("--output_type", type=str, default="chat", help="The output type")
#     parser.add_argument("--input_type", type=str, default="chat", help="The input type")
#     parser.add_argument("--upload_file", type=str, help="Path to the file to upload", default=None)
#     parser.add_argument("--components", type=str, help="Components to upload the file to", default=None)

#     args = parser.parse_args()
#     try:
#       tweaks = json.loads(args.tweaks)
#     except json.JSONDecodeError:
#       raise ValueError("Invalid tweaks JSON string")

#     if args.upload_file:
#         if not upload_file:
#             raise ImportError("Langflow is not installed. Please install it to use the upload_file function.")
#         elif not args.components:
#             raise ValueError("You need to provide the components to upload the file to.")
#         tweaks = upload_file(file_path=args.upload_file, host=BASE_API_URL, flow_id=args.endpoint, components=[args.components], tweaks=tweaks)

#     response = run_flow(
#         message=args.message,
#         endpoint=args.endpoint,
#         output_type=args.output_type,
#         input_type=args.input_type,
#         tweaks=tweaks,
#         api_key=args.api_key
#     )

#     print(json.dumps(response, indent=2))

# if __name__ == "__main__":
#     main()
