import json
import time
import pyperclip
from rich.console import Console 
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import print

console = Console()

# A list to store saved prompts
saved_prompts = []

# Function to save prompts to a JSON file
def save_to_json(filename='saved_prompts.json'):
    with open(filename, 'w') as json_file:
        json.dump(saved_prompts, json_file, indent=4)
    console.print(f"[bold green]Prompts saved to {filename} successfully![/bold green]")

# Function to load prompts from a JSON file
def load_from_json(filename='saved_prompts.json'):
    global saved_prompts
    try:
        with open(filename, 'r') as json_file:
            saved_prompts = json.load(json_file)
        console.print(f"[bold green]Prompts loaded from {filename} successfully![/bold green]")
    except FileNotFoundError:
        console.print(f"[bold red]No saved prompts file found. Starting fresh.[/bold red]")

# Function to create a new prompt
def create_prompt():
    console.clear()
    console.print("[bold cyan]Creating a New Prompt for AI Chatbot:[/bold cyan]")

    base_question = Prompt.ask("Base Question: ")
    character_role = Prompt.ask("Relative Character/Role: ")
    
    describe_steps = Confirm.ask("Can you describe the Question in Steps? ")
    steps = []
    if describe_steps:
        step = Prompt.ask("Enter a step: ")
        steps.append(step)
        while True:
            step = Prompt.ask("Enter next step (leave blank to finish): ")
            if step == "":
                break
            steps.append(step)

    example_output = Prompt.ask("Provide Example Output: ")
    
    has_structure = Confirm.ask("Does the output consist of any structure/format/language? ")
    structure_format = ""
    if has_structure:
        structure_format = Prompt.ask("Select Structure/Format (e.g., Python, English, JSON, XML, Markdown): ")

    additional_notes = Prompt.ask("Any further notes/rules: ")
    output_preference = Prompt.ask("Output Preference (brief/summarize) (default: brief): ")

    # Save the prompt as a dictionary, excluding empty fields
    prompt = {
        "base_question": base_question if base_question else None,
        "character_role": character_role if character_role else None,
        "steps": steps if steps else None,
        "example_output": example_output if example_output else None,
        "structure_format": structure_format if structure_format else None,
        "additional_notes": additional_notes if additional_notes else None,
        "output_preference": output_preference if output_preference else "brief"
    }

    # Remove None values from the dictionary
    prompt = {k: v for k, v in prompt.items() if v is not None}

    saved_prompts.append(prompt)
    console.print("[bold green]Prompt saved successfully![/bold green]")
    save_to_json()  # Save to JSON after creating a prompt

# Function to view saved prompts
def view_saved_prompts():
    console.clear()
    if not saved_prompts:
        console.print("[bold red]No saved prompts found.[/bold red]")
        time.sleep(5)
        return

    table = Table(title="Saved Prompts")
    table.add_column("ID", justify="center")
    table.add_column("Base Question", justify="left")

    for idx, prompt in enumerate(saved_prompts):
        table.add_row(str(idx + 1), prompt.get("base_question", "N/A"))

    console.print(table)

    prompt_id = Prompt.ask("Select a prompt by ID to view, edit, or delete")
    try:
        prompt_id = int(prompt_id) - 1
        if 0 <= prompt_id < len(saved_prompts):
            prompt = saved_prompts[prompt_id]
            console.print("[bold cyan]Selected Prompt Details:[/bold cyan]")
            for key, value in prompt.items():
                console.print(f"[bold]{key}:[/bold] {value}")

            # Copy prompt to clipboard
            pyperclip.copy(json.dumps(prompt, indent=4))
            console.print("[bold green]Prompt copied to clipboard![/bold green]")

            action = Prompt.ask("Would you like to (E)dit, (D)elete, or (V)iew again? (E/D/V)")
            if action.upper() == "E":
                edit_prompt(prompt_id)
            elif action.upper() == "D":
                delete_prompt(prompt_id)
            time.sleep(5)
        else:
            console.print("[bold red]Invalid ID selected.[/bold red]")
    except ValueError:
        console.print("[bold red]Please enter a valid number.[/bold red]")

# Function to edit an existing prompt
def edit_prompt(prompt_id):
    console.clear()
    console.print("[bold cyan]Editing Prompt:[/bold cyan]")
    prompt = saved_prompts[prompt_id]

    for key in prompt.keys():
        new_value = Prompt.ask(f"Edit {key} (leave blank to keep current value: {prompt[key]}): ", default=prompt[key])
        if new_value:
            prompt[key] = new_value

    console.print("[bold green]Prompt updated successfully![/bold green]")
    save_to_json()  # Save changes to JSON

# Function to delete a prompt
def delete_prompt(prompt_id):
    console.clear()
    console.print("[bold red]Deleting Prompt:[/bold red]")
    confirm = Confirm.ask("Are you sure you want to delete this prompt?")
    if confirm:
        del saved_prompts[prompt_id]
        console.print("[bold green]Prompt deleted successfully![/bold green]")
        save_to_json()  # Save changes to JSON

# Main function to run the application
def main():
    load_from_json()  # Load saved prompts at the start
    while True:
        console.clear()
        console.print("[bold magenta]Welcome to the AI Chatbot Prompt Generator![/bold magenta]")
        console.print("Please choose an option:")
        console.print("1. Create New Prompt")
        console.print("2. View Saved Prompts")
        console.print("3. Exit Application")

        choice = Prompt.ask("Enter your choice (1/2/3)")

        if choice == "1":
            create_prompt()
        elif choice == "2":
            view_saved_prompts()
        elif choice == "3":
            console.print("[bold yellow]Exiting the application. Goodbye![/bold yellow]")
            break
        else:
            console.print("[bold red]Invalid choice. Please select 1, 2, or 3.[/bold red]")

if __name__ == "__main__":
    main()
