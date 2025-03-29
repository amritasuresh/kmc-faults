import os
import subprocess

def run_script_on_folder(script_path, input_folder, output_folder):
    """
    Runs a script on all files in the input folder and saves results to the output folder.

    Parameters:
        script_path (str): Path to the Python script (e.g., xyz.py).
        input_folder (str): Path to the folder containing input files.
        output_folder (str): Path to the folder to store output files.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, filename)

        # Skip if it's not a file
        if not os.path.isfile(input_file_path):
            continue

        # Define the output file path
        output_file_path = os.path.join(output_folder, filename)

        # Run the script on the current file
        try:
            result = subprocess.run(
                ["python3", script_path, input_file_path],
                capture_output=True,
                text=True,
                check=True,
            )

            # Save the output of the script to the output file
            with open(output_file_path, "w") as output_file:
                output_file.write(result.stdout)
            
            print(f"Processed {filename} -> {output_file_path}")

        except subprocess.CalledProcessError as e:
            print(f"Error processing {filename}: {e.stderr}")

# Define paths
script_path = "fsmtoscm.py"          # Path to your Python script
input_folder = "tests/benchmarks/"            # Path to the folder with input files
output_folder = "tests/RSCbenchmarks/"           # Path to the folder for output files

# Run the script on all files in the input folder
run_script_on_folder(script_path, input_folder, output_folder)
