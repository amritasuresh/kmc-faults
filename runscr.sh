TEST_FOLDER="tests/corruptbenchmarks"  # Adjust the relative path to the test folder if needed

# Loop through all .scm files in the test folder
for file in "$TEST_FOLDER"/*.txt; do
    # Run the rescu command on each file
    # for file in *; do mv "$file" "${file%.*}.scm"; done
    echo "$file"
    cabal run KMC -- "$file" --fsm
done
