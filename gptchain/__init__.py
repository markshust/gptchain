import csv
import argparse
from openai import OpenAI

class OpenAIChat:
    def __init__(self, model='gpt-4-1106-preview', temperature=0.7, max_tokens=1000):
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def save_to_csv(self, conversation, csv_filename):
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['role', 'content'])
            for message in conversation:
                writer.writerow([message['role'], message['content']])

    def chat_with_openai(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        return response.choices[0].message.content

    def run_chat(self, message_chain, args, csv_filename):
        conversation = []
        args_dict = vars(args)  # Convert the Namespace to a dictionary

        for messages in message_chain:
            system_prompt, user_prompt = messages

            # Format the user prompt with the actual argument values dynamically
            user_prompt['content'] = user_prompt['content'].format_map(args_dict)

            # Always start with the current system prompt
            current_conversation = [system_prompt]

            # Add all previous user prompts and assistant responses
            current_conversation.extend(conversation)

            # Append the current user prompt
            current_conversation.append(user_prompt)

            # Send the current conversation state to OpenAI and get the completion
            assistant_response_content = self.chat_with_openai(current_conversation)

            # Append the OpenAI (assistant) response to the conversation
            assistant_response = {'role': 'assistant', 'content': assistant_response_content}
            print(assistant_response)

            # Add only the user prompt and assistant response to the main conversation state
            conversation.append(user_prompt)
            conversation.append(assistant_response)

        # Save the conversation to a CSV file
        self.save_to_csv(conversation, csv_filename)

        # Print the conversation
        for message in conversation:
            print(f"{message['role']}: {message['content']}")

def create_parser(custom_args):
    parser = argparse.ArgumentParser(description="Chat with OpenAI using custom roles and messages.")
    for arg in custom_args:
        parser.add_argument(arg['flag'], help=arg['help'], required=arg['required'])
    return parser

def generate_csv_filename(args):
    # Generate a CSV filename based on all the defined arguments
    filename_parts = ['conversation']
    for arg, value in vars(args).items():
        # Skip if the argument value is None
        if value is not None:
            filename_parts.append(str(value))
    return '-'.join(filename_parts) + '.csv'

def gptchain(custom_args, message_chain, model='gpt-4-1106-preview', temperature=0.7, max_tokens=1000):
    parser = create_parser(custom_args)
    args = parser.parse_args()
    csv_filename = generate_csv_filename(args)
    chat = OpenAIChat(model=model, temperature=temperature, max_tokens=max_tokens)
    chat.run_chat(message_chain, args, csv_filename)
