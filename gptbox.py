import sys
import subprocess
import pathlib
import re
import ollama

model = "qwen2.5-coder:7b"
prompt_base = '''
Write a Python program that implements the "{command}" POSIX command. Include help text functionality and various flags. Make the behavior as similar as possible to the real command. Write only the code, with no explanation.
'''.strip()

help_text = '''
GPTBox

Usage: gptbox [function [arguments]]
'''.strip()

python_bin = sys.executable

if __name__ == "__main__":
  if len(sys.argv) == 1:
    print(help_text)
    sys.exit(1)
  
  command = sys.argv[1]
  prompt = prompt_base.format(command=command)
  arguments = sys.argv[2:]

  response = ollama.chat(model=model, stream=True, messages=[
    {"role": "user", "content": prompt}
  ])
  response_text = ""
  for chunk in response:
    print(chunk.message.content, end="", flush=True)
    response_text += chunk.message.content

  code_regex = r"```.*?\n(.+?)```"
  generated_code = re.findall(code_regex, response_text, flags=re.S)[0]
  print("\n\n")

  script_path = "/tmp/generated.py"
  script_file = pathlib.Path(script_path)
  script_file.write_text(generated_code)
  
  subprocess.run([python_bin, script_path, *arguments])