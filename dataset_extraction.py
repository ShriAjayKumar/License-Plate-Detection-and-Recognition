import json # For handling JSON Files
import wget # For Downloading images 

# File Path for image and json file
filename = "C:\\Users\\Aj\\Desktop\\HumanAI\\vehicle-number-plate-detection Datasets\\Indian_Number_plates.json"
path = "C:\\Users\\Aj\\Desktop\\HumanAI\\vehicle-number-plate-detection Datasets\\data\\"

# For reading each line as input and read JSON data
def json_readr(f):
    for line in open(f, mode="r"):
        yield json.loads(line)

# For reading JSON data file
with open(filename,'r') as obj:
    dataset = list(json_readr(filename)) 

# for Loading URL from dictionary and storing images and  annotations of respective images
count = 1
for it in range(len(dataset)):
    url = dataset[it]['content']
    wget.download(url,path + "image%d.png"%count)
    width = dataset[it]['annotation'][0]['imageWidth']
    height = dataset[it]['annotation'][0]['imageHeight']
    top_left_x = dataset[it]['annotation'][0]['points'][0]['x']
    top_left_y = dataset[it]['annotation'][0]['points'][0]['y']
    bottom_right_x = dataset[it]['annotation'][0]['points'][1]['x']
    bottom_right_y = dataset[it]['annotation'][0]['points'][1]['y']
    count += 1
    # for debugging purpose
    
    # print(url)
    # print(width)
    # print(height)
    # print(top_left_x)
    # print(top_left_y)
    # print(bottom_right_x)
    # print(bottom_right_y)    