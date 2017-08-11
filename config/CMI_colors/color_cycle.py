from cycler import cycler
import json
import os
with open(os.path.abspath(os.path.join(__file__, os.pardir,
     'Color_palette.json'))) as color_palette:
    color_key = json.load(color_palette)

def CMI_color_palette():

    color_list = list()
    for palette in ["Primary", "Secondary", "Tertiary"]:
        color_key[palette].reverse()
    while(len(color_key)):
        for palette in ["Primary", "Secondary", "Tertiary"]:
            if(palette in color_key):
                color_list.append(color_key[palette].pop())
                if(not len(color_key[palette])):
                    del(color_key[palette])
                
    return(cycler(c=color_list))
