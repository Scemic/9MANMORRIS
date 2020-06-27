

def get_3_instructions_data(filename,destination):
    with open(filename,"r") as f:
        lines = f.readlines()
        output = []
        for line in lines:
            info = line.split("-") # We split into state and instruction
            #print(info)
            if len(info[1].strip()) == 6: # We check if the instructions take 6 characters
                output.append(line)
        
    with open(destination,"w+") as g:
        for line in output:
            g.write(line)
    
    print("Data successfully extracted from " + filename + " to " + destination +".")
    

if __name__ == "__main__":
    
    get_3_instructions_data("..\\datasets\\DATASET.complete.txt", "remove_instructions.txt")
        