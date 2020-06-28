

def get_n_instructions_data(filename,destination,n):
    with open(filename,"r") as f:
        lines = f.readlines()
        output = []
        for line in lines:
            info = line.split("-") # We split into state and instruction
            #print(info)
            if len(info[1].strip()) == n: # We check if the instructions take 6 characters
                output.append(line)
        
    with open(destination,"w+") as g:
        for line in output:
            g.write(line)
    
    print("Data successfully extracted from " + filename + " to " + destination +".")
    
if __name__ == "__main__":
    
    get_n_instructions_data("..\\datasets\\DATASET.complete.txt", "to_1_instructions.txt",2)
        