# markshust/gptchain

`gptchain` is a Python library designed to facilitate the creation of a sequence of GPT prompts that build upon each other's responses. This tool allows users to generate complex, multistep conversations or processes with AI models by linking prompts into a cohesive chain.

It differs from tools such as [`langchain`](https://github.com/langchain-ai/langchain) in that it's far easier to use. It lacks many of the features of langchain, as it simply interacts with GPT by executing a list of prompts in sequential order.

## Features

- Easy installation and setup.
- Customizable prompt chains for complex AI-driven workflows.
- Support for custom command-line arguments to tailor the AI's output.
- Ability to override default OpenAI configuration for model specifications.

## Installation

Install the `gptchain` library using pip with the following command in your terminal:

```bash
pip install gptchain
```

This command will download and install `gptchain` along with any necessary dependencies.

## Usage

To use `gptchain`, you'll need to write a Python script that imports the library and defines the prompt chain and any custom arguments.

### OpenAI Setup

Be sure to expose your OpenAI API Key as an environment variable by adding the following to your `~/.bash_profile` or `~/.zshrc` file:

```
export OPENAI_API_KEY="your-key"
```

### Defining Custom Arguments

Custom arguments allow you to pass dynamic content to the AI prompts. These arguments are defined as a list of dictionaries, where each dictionary represents a command-line flag.

```python
custom_args = [
    {'flag': '--idea', 'help': 'The name of the idea to discuss', 'required': True},
    {'flag': '--timeframe', 'help': 'The timeframe for the business concept', 'required': True},
    # Add more custom arguments as needed
]
```

### Creating a Message Chain

The message chain is a list of prompt stages, where each stage is a list of system and user messages. The chain defines the flow of conversation or analysis.

Custom arguments may be included in messages by using the `{argName}` format as shown below:

```python
message_chain = [
    [
        {"role": "system", "content": "You are a business analyst."},
        {"role": "user", "content": "Create 5 potential business initiatives for the idea: {idea}"}
    ],
    [
        {"role": "system", "content": "You are a technical architect."},
        {"role": "user", "content": "Pick the best idea from the previous list, and list out any potential technical limitations that could come up for it."}
    ],
    [
        {"role": "system", "content": "You are a product manager."},
        {"role": "user", "content": "List out any potential impediments for this idea that would prevent it from launching in {timeframe}."}
    ]
]
```

When the script is executed, the first array in the message chain is sent to GPT and the result is returned. The response is merged with the second message in the chain as an "assistant" response, like so:

```python
[
    {"role": "system", "content": "You are a technical architect."},
    {"role": "assistant", "content": "These are the 5 business initiatives for the idea..."},
    {"role": "user", "content": "Pick the best idea from the previous list, and list out any potential technical limitations that could come up for it."}
]
```

And this process continues with each subsequent prompt. The previous results are included in order to create a cohesive chain of prompts. This allows you to automate a chain of prompts in a successive order without any human intervention.

### Execute the Chain

Once you have defined your custom arguments and message chain, use the `gptchain` function to execute the chain. 

```python
from gptchain import gptchain
    gptchain(custom_args, message_chain)
```

## Configuration

You can also customize the default OpenAI configuration by providing additional parameters such as the model, temperature, and max tokens.

```python
# Define custom OpenAI configuration values
model = 'gpt-4-1106-preview'  # Replace with the model you want to use
temperature = 0.7  # Set the temperature for the conversation
max_tokens = 1000  # Set the maximum number of tokens per response

# Call the main function with the custom configuration values
gptchain(custom_args, message_chain, model, temperature, max_tokens)
```

## Example of a Complete Script

Below is an example of a completed script that defines custom arguments, defines a message chain, and executes the chain with custom configuration values.

```python
from gptchain import gptchain

# Define your custom arguments
custom_args = [
    {'flag': '--idea', 'help': 'The name of the idea to discuss', 'required': True},
    {'flag': '--timeframe', 'help': 'The timeframe for the business concept', 'required': True},
    # Add more custom arguments as needed
]

# Define your chain of messages
message_chain = [
    [
        {"role": "system", "content": "You are a business analyst."},
        {"role": "user", "content": "Create 5 potential business initiatives for the idea: {idea}"}
    ],
    [
        {"role": "system", "content": "You are a technical architect."},
        {"role": "user", "content": "Pick the best idea from the previous list, and list out any potential technical limitations that could come up for it."}
    ],
    [
        {"role": "system", "content": "You are a product manager."},
        {"role": "user", "content": "List out any potential impediments for this idea that would prevent it from launching in {timeframe}."}
    ]
]

if __name__ == '__main__':
    # Define custom OpenAI configuration values
    model = 'gpt-4-1106-preview'  # Replace with the model you want to use
    temperature = 0.7  # Set the temperature for the conversation
    max_tokens = 1000  # Set the maximum number of tokens per response

    # Call the main function with the custom configuration values
    gptchain(custom_args, message_chain, model, temperature, max_tokens)
```

## Command-Line Interface (CLI) Execution

When you execute your script from command line, be sure to pass in any custom arguments that were defined. In the example above, `idea` and `timeframe` were defined arguments, and you can pass in values with quoted strings, like so:

```bash
python usage.py --idea "deploy drones to feed the poor" --timeframe "1 month"
```

This command will start the `gptchain` process using the provided idea and timeframe, executing the linked prompts in sequence.

## Output

Each message chain is output to the terminal as it is executed, along with the response after it has been executed. When the script has completed in its entirety, it is written to a CSV file using the naming convention:

```
conversation-{arg1value}-{arg2value}-{etc}.csv
```

In the above example, this file will be named:

```
conversation-deploy drones to feed the poor-1 month.csv
```

## License

[MIT](https://opensource.org/licenses/MIT)
