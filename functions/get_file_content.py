import os
from config import MAX_CHARS
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" is not a file'
        
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1) != "":
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string

    except:
        return "Error: something went wrong"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns a string with the contents of a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description='File path to read the file from, relative to the working directory (default is the working directory itself represented as ".")',
            ),
        },
        required=["file_path"],
    ),
)