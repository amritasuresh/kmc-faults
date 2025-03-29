import re
import sys

def split_blocks(file_path):
    """
    Splits a file into blocks based on occurrences of ".outputs".
    
    :param file_path: Path to the input file
    :return: A list of blocks
    """
    with open(file_path, 'r') as file:
        content = file.read()
        #print(content)
    # Split by occurrences of ".outputs"
    blocks = content.split(".outputs")
    
    # Add back ".outputs" to each block (except the first which would be empty if the file starts with .outputs)
    blocks = [f".outputs{block.strip()}" for block in blocks if block.strip()]
    return blocks[1:]

def count_unique_patterns(block):
    """
    Counts unique words starting with 'q', following '!', and following '?' in a block.
    Also stores lines between ".state graph" and ".marking" as transitions and categorizes them into sendtrans and rectrans.
    
    Extracts tuples from sendtrans into a set called sendt and from rectrans into a set called rect.
    
    For tuples in sendt, generates new tuples of the form (q, n, b, r) for all b in outgoing, excluding the current letter.
    
    :param block: The block of text to process
    :return: A dictionary containing counts, sets, transitions, sendtrans, rectrans, sendt, and rect
    """
    
    # Extract transitions between ".state graph" and ".marking"
    transitions_match = re.search(r'\.state graph(.*?)\.marking', block, re.DOTALL)
    transitions = set()
    sendt = set()
    rect = set()
    chanset = set()
    outgoing = set()
    incoming = set()
    stateset = set()
    
    if transitions_match:
        # Split into individual lines and remove empty lines
        lines = transitions_match.group(1).strip().split("\n")
        transitions = set(line.strip() for line in lines if line.strip())

        #Extract transitions
        for trans in transitions:
            parts = trans.split()
            if len(parts) >= 5:
                sendstate, channel, act, letter, recstate = parts[:5]
                stateset.add(sendstate)
                stateset.add(recstate)
                chanset.add(channel)
                if act == '!':
                    sendt.add((sendstate, channel, letter, recstate))
                    outgoing.add(letter)
                elif act == '?':
                    rect.add((sendstate, channel, letter, recstate))
                    incoming.add(letter)

        # Extract the marking line
        marking_line_match = re.search(r'\.marking.*', block)
        marking_word = marking_line_match.group(0).split()[1] if marking_line_match else "q1"
        initial = marking_word
        #marking_line = marking_line_match.group(0) if marking_line_match else ".marking q1"

        # Convert states to integers
        state_to_int = {state: idx for idx, state in enumerate(sorted(set(stateset)))}
        initial_int = state_to_int[initial]
        #print(state_to_int)

        #Make every state associated to the other states by transitions

        state_associations = {i: [] for i in range(len(state_to_int))}
        #print(state_associations)

        for trans in transitions:
            parts = trans.split()
            if len(parts) >= 5:
                sendstate, channel, act, letter, recstate = parts[:5]
                state = state_to_int[sendstate]
                #print(state)
                state_associations[state].append((channel, act, letter, state_to_int[recstate]))

        #print(state_associations)
        
        # Corruption: Generate new tuples for sendt
        #new_tuples = set()
        #for q, n, a, r in sendt:
        #    for b in outgoing:
        #        if b != a:
        #            new_tuples.add((q, n, b, r))
        #sendt.update(new_tuples)
    
    return {
        "outgoing": outgoing,
        "incoming": incoming,
        "channels": chanset,
        "states": stateset,
        "transitions": transitions,
        "sendt": sendt,
        "rect": rect,
        "initial": initial_int,
        "tranlist": state_associations,
        "stateset": state_to_int
    }

def format_and_print_blocks(file_path):
    """
    Reads a file, processes each block, and prints the output in the specified format:
    - ".outputs"
    - ".state graphs"
    - For each tuple in sendt, prints "q n ! a r"
    - For each tuple in rect, prints "q n ? a r"
    - Prints the line starting with ".marking"
    - Prints ".end"
    
    :param file_path: Path to the input file
    """
    # Extract the filename from the file path
    filename = file_path.split('/')[-1]
    filename = filename.split('.')[0]

    blocks = split_blocks(file_path)
    
    print("scm " + filename + " :")

    all_sendt = set()
    all_rect = set()
    all_chans = set()
    all_letters = set()

    for i, block in enumerate(blocks):
        results = count_unique_patterns(block)
        sendt = results["sendt"]
        rect = results["rect"]
        chans = results["channels"]
        all_chans.update(chans)
       
        all_letters.update(results["outgoing"])
        
        # Print the formatted output

        #print("initial" + " = " + results["initial"] + " ;")
       
        #print(".outputs")
        #print(".state graph")
        
        # Print send transitions
        #for q, n, a, r in sorted(sendt):
        #    print(f"{q} {n} ! {a} {r}")
        
        # Print receive transitions
        #for q, n, a, r in sorted(rect):
        #    print(f"{q} {n} ? {a} {r}")
        
        # Print marking and end lines
        #print(marking_line)
        #print(".end")
        #print()  # Blank line between blocks
    
    print("nb_channels = " + str(len(all_chans)) + " ;")
    print ("parameters:")
    for l in all_letters:
        print("real " + l + " ;")
    
    for i, block in enumerate(blocks):
        results = count_unique_patterns(block)
        print ("automaton A" + str(i) + " :")

        print ("initial : " + str(results["initial"]))

        for i in results["stateset"]:
            print ("state " + str(results["stateset"][i]) + " :")
            for a,b,c,d in results["tranlist"][results["stateset"][i]]:
                #print(t)
                print("to " + str(d) + " : " + "when true, " + a + " " + b + " " + c + ";")

    


if __name__ == "__main__":
    # Check for command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
    
    # Get the input file from arguments
    input_file = sys.argv[1]
    
    # Process and print blocks
    format_and_print_blocks(input_file)
