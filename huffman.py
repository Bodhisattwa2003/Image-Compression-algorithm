import re
import os
import numpy as np
from PIL import Image

def rgb_image(input_path, output_path, quality=85):
    try:
        
        with Image.open(input_path) as img:
            if img.mode == 'RGBA':               
                r, g, b, a = img.split()
                img = Image.merge('RGB', (r, g, b))
            img.save(output_path, 'JPEG', quality=quality)

    except Exception as e:
        print(f"Error: {e}")
        
print("Image compression Tool")
print("=================================================================")
filex = input("Enter the filename: ")
file = ("rgb.png")
rgb_image(filex, file, quality=85)
my_string = np.asarray(Image.open(file), np.uint8)
shape = my_string.shape
a = my_string

my_string = str(my_string.tolist())


letters = []                            #This block stores the charachters and their frequencies in letters list
only_letters = []                       #only_letters stores the unique charachters to keep track of all the symbols
for letter in my_string:
    if letter not in letters:
        frequency = my_string.count(letter)
        letters.append(frequency)
        letters.append(letter)
        only_letters.append(letter)

nodes = []                                  #this block creates a list nodes to store the charachters 
while len(letters) > 0:                     #the while loop basically appends the first and 2nd charachter ie char and their frequency
    nodes.append(letters[0:2])              #in nodes list. Then the letters is eddited by removing the first two charachters. 
    letters = letters[2:]                   #this is repeated until letters list is empty

nodes.sort()
huffman_tree = []
huffman_tree.append(nodes)

def combine_nodes(nodes):
    pos = 0
    newnode = []
    if len(nodes) > 1:
        nodes.sort()
        nodes[pos].append("1")
        nodes[pos + 1].append("0")
        combined_node1 = (nodes[pos][0] + nodes[pos + 1][0])                #combined_node1  stores the addition of the frequencies of the combined charachter
        combined_node2 = (nodes[pos][1] + nodes[pos + 1][1])                #combined_node2 stores the concatenation of the two charachters
        newnode.append(combined_node1)                                      #newnode gets stored with the value of combined frequency and the concaten char
        newnode.append(combined_node2)
        newnodes = []
        newnodes.append(newnode)                                            #adds the new node to the newnodes list
        newnodes = newnodes + nodes[2:] #                                        appends newnodes by concatenating all nodes after index 2
        nodes = newnodes                                                        #updates nodes with content of newnodes list
        huffman_tree.append(nodes)                                              # adds nodes to the huffman tree
        combine_nodes(nodes)                                                   #calls the function recursively
    return huffman_tree

newnodes = combine_nodes(nodes)

huffman_tree.sort(reverse=True)

checklist = []                                                              #makes sure all nodes are visited only once
for level in huffman_tree:
    for node in level:
        if node not in checklist:
            checklist.append(node)
        else:
            level.remove(node)


letter_binary = []
if len(only_letters) == 1:
    lettercode = [only_letters[0], "0"]
    letter_binary.append(*len(my_string))
else:
    for letter in only_letters:
        code = ""
        for node in checklist:
            if len(node) > 2 and letter in node[1]: #             checks if the node is a leaf node
                code = code + node[2]                           #appends the 3rd letter of the node list to the code
        lettercode = [letter, code]                         #contains every unique letter and its huffman code
        letter_binary.append(lettercode)                        #adds the lettercode to the letter_binary



bitstring = ""                              #this block converts all symbols to binary
for character in my_string:
    for item in letter_binary:
        if character in item:
            bitstring = bitstring + item[1]  #searches for unique char and appends the binary bit to the bitstring

binary = "0b" + bitstring

output = open("compressed.txt", "w+")
print("Compressed file generated as compressed.txt")
output = open("compressed.txt", "w+")
print("Compressing Final Image.......")
output.write(bitstring)

bitstring = str(binary[2:])
uncompressed_string = ""
code = ""
for digit in bitstring:
    code = code + digit           #appends every digit to code for every digit
    pos = 0
    for letter in letter_binary:
        if code == letter[1]:                                                  #checks if code matches with each letter in letter_binary
            uncompressed_string = uncompressed_string + letter_binary[pos][0]   #appends uncompressed_string with  decoded symbols. This slowly forms the entire decoded string 
            code = ""
        pos += 1


temp = re.findall(r'\d+', uncompressed_string)
res = list(map(int, temp))                                          #maps every charachter in temp as integer and stores in re list
res = np.array(res)                                           #stores res as a numpy array into res
res = res.astype(np.uint8)                          #converts res to unsigned 8 bit char
res = np.reshape(res, shape)                 #reshaes res to the shape of original file (check line 29 )
data = Image.fromarray(res)                   # uses PIL to create image from res and stores to data
output_image_path = 'decompressed_image.jpg'
data.save(output_image_path)
if a.all() == res.all():
        print("Success")
os.remove("rgb.png")
