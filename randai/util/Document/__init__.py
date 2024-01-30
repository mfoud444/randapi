import subprocess
from .WordTool import WordTool
class PandocConverter:
    def __init__(self, input_text, output_file, options=None):
        self.input_text = input_text
        self.output_file = output_file
        self.options = options if options else []

    def convert(self):
        try:
            # Construct the pandoc command with input text
            command = ["pandoc", "--from=markdown", "--to=pdf", "-o", self.output_file] + self.options
            subprocess.run(command, input=self.input_text, text=True, check=True)

            print("Conversion successful!")
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")
            raise