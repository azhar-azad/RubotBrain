from __future__ import print_function
from PIL import Image

im = Image.open("snap.jpg")

print(im.format, im.size, im.mode)

colors = {
    'w' : {'r': {'min': 150, 'max': 255}, 'g': {'min': 150, 'max': 255}, 'b': {'min': 150, 'max': 255}},
    'y' : {'r': {'min': 150, 'max': 255}, 'g': {'min': 150, 'max': 255}, 'b': {'min':   0, 'max': 100}},
    'r' : {'r': {'min': 200, 'max': 255}, 'g': {'min':   0, 'max': 100}, 'b': {'min':   0, 'max': 100}},
    'b' : {'r': {'min':   0, 'max': 100}, 'g': {'min':   0, 'max': 100}, 'b': {'min': 200, 'max': 255}},
    'g' : {'r': {'min':   0, 'max': 150}, 'g': {'min': 200, 'max': 255}, 'b': {'min':   0, 'max': 100}},
    'o' : {'r': {'min': 150, 'max': 255}, 'g': {'min':   0, 'max':  80}, 'b': {'min': 120, 'max': 255}}    
    }

points = [(950, 120), (950, 420), (950, 750), (1170, 120), (1170, 420), (1170, 750)]
size_x = 50
size_y = 50

regions = {}
for i in range(6):
    regions[i+1] = (points[i][0], points[i][1], points[i][0] + size_x, points[i][1] + size_y)

for regi in range(1, 7):
    reg = regions[regi]
    regim = im.crop(reg)
    #enhance
    #regim = regim.point(lambda i: i*1.5)
    
    width, height = regim.size
    wxh = width * height    

    R, G, B = 0, 1, 2
    source = regim.split()
    
    regim_marked = regim.point(lambda i: i*1.5)
    im.paste(regim_marked, reg) 

    total = [0,0,0]
    rgb = [0,0,0]

    for h in range(height):
        for w in range(width):
            total[R] += source[R].getpixel((w,h))
            total[G] += source[G].getpixel((w,h))
            total[B] += source[B].getpixel((w,h))

    rgb[R] = total[R] / wxh;
    rgb[G] = total[G] / wxh;
    rgb[B] = total[B] / wxh;
    
    print(rgb)
    scale = 255 / max(rgb)   
    
    #enhance
    rgb[R] = rgb[R] * scale
    rgb[G] = rgb[G] * scale
    rgb[B] = rgb[B] * scale
    
    print(rgb)

    guess = ''
    
    for c, p in colors.items():
        
        if rgb[R] >= p['r']['min'] and rgb [R] <= p['r']['max'] and rgb[G] >= p['g']['min'] and rgb[G] <= p['g']['max'] and rgb[B] >= p['b']['min'] and rgb[B] <= p['b']['max']:
            guess = c
            print('Guess for region ' + str(regi) + ' is ' + guess)
            break;
        
    if guess == '':
        print('No guess for region ' + str(regi))
        
im.save('snap_marked.jpg')
