import sys
import re
import os
import ctypes

def read_write_heap(pid, search_string, replace_string):
    # Open the process's memory map
    mem_file = open('/proc/{}/maps'.format(pid), 'r')
    
    for line in mem_file:
        if 'heap' in line:
            # Extract the start and end addresses of the heap
            start, end = line.split()[0].split('-')
            start = int(start, 16)
            end = int(end, 16)
            
            # Open the process's memory
            mem_fd = open('/proc/{}/mem'.format(pid), 'rb+')
            
            # Seek to the start of the heap
            mem_fd.seek(start)
            
            # Read the heap contents
            heap_data = mem_fd.read(end - start)
            
            # Find the search string in the heap data
            offset = heap_data.find(search_string.encode())
            if offset != -1:
                # Calculate the address in the process memory
                address = start + offset
                
                # Seek to the address in the memory file
                mem_fd.seek(address)
                
                # Replace the string with the replace string
                mem_fd.write(replace_string.encode())
                
                print('Successfully replaced the string at address 0x{:x}'.format(address))
                
            mem_fd.close()
    
    mem_file.close()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        print('Usage: read_write_heap.py pid search_string replace_string')
        sys.exit(1)
    
    pid = int(sys.argv[1])
    search_string = sys.argv[2]
    replace_string = sys.argv[3]
    
    # Call the function to find and replace the string
    read_write_heap(pid, search_string, replace_string)
