import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        command = ["python", target_file]
        if args:
             command.extend(args)

        completed_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        output_string = ""
        if completed_process.returncode != 0:
            output_string += f"Process exited with code {completed_process.returncode}\n"
        
        if completed_process.stdout == None:
            output_string += "No output produced\n"
        else:
            output_string += f"STDOUT:\n{completed_process.stdout}"
            output_string += f"STDERR:\n{completed_process.stderr}"
        
        return output_string
    
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified python file relative to the working directory, using args if provided",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description='File path to run the file, relative to the working directory (default is the working directory itself represented as ".")',
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments (It's optional, default is None)",
                items=types.Schema(
                    type=types.Type.STRING
                )
            ),
        },
        required=["file_path"],
    ),
)