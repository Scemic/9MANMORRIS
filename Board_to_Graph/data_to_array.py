from dataprocessing import State, load_dataset
import numpy as np

# Set filename to load and load states and moves
def convert_file(filename='../datasets/DATASET.short.txt'):
    states_ini, moves = load_dataset(filename)

    states_ini_arr = []
    states_res_arr = []
    # Create result array

    for i in range(len(moves)):
        TO, has_FROM, FROM, has_REMOVE, REMOVE = moves[i]
        state = states_ini[i]

        # only select states when in phase 2
        if state.my_phase != 2:
            continue
        if not has_FROM:
            continue
        if has_REMOVE:
            continue

        # Convert to array
        arr = []
        for pos in state.positions:
            if pos == 'O':
                arr.append(0)
            if pos == 'M':
                arr.append(1)
            if pos == 'E':
                arr.append(2)
        states_ini_arr.append(arr)

        # create result array
        res_arr = np.copy(arr)
        res_arr[TO-1],res_arr[FROM-1] = res_arr[FROM-1],res_arr[TO-1]
        states_res_arr.append(res_arr)
    states_ini_arr = np.array(states_ini_arr)
    states_res_arr = np.array(states_res_arr)
    return states_ini_arr, states_res_arr

if __name__ == '__main__':
    print('+++ data_to_array.py - TESTING +++ ')
    states_ini_arr,states_res_arr = convert_file
