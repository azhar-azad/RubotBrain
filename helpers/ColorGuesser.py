from __future__ import print_function
from PIL import Image

class ColorGuesser(object):
    
    colors = {
        'w' : {'r': {'min': 200, 'max': 255}, 'g': {'min': 200, 'max': 255}, 'b': {'min': 200, 'max': 255}},
        'y' : {'r': {'min': 200, 'max': 255}, 'g': {'min': 200, 'max': 255}, 'b': {'min':   0, 'max': 150}},
        'r' : {'r': {'min': 200, 'max': 255}, 'g': {'min':   0, 'max': 100}, 'b': {'min':   0, 'max': 100}},
        'b' : {'r': {'min':   0, 'max': 100}, 'g': {'min':   0, 'max': 100}, 'b': {'min': 200, 'max': 255}},
        'g' : {'r': {'min':   0, 'max': 100}, 'g': {'min': 200, 'max': 255}, 'b': {'min':   0, 'max': 150}},
        'o' : {'r': {'min':   0, 'max': 100}, 'g': {'min':   0, 'max': 100}, 'b': {'min':   0, 'max': 100}}    
        }

    def guess(self, regim, enhance = True):
        
        width, height = regim.size
        wxh = width * height    

        R, G, B = 0, 1, 2
        source = regim.split()    

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
        
        #print(rgb)
         
        
        #enhance
        if enhance:
            #print("Actual: " + str(rgb))
            contrast = 1.5           
            
            rgb[R] = ((rgb[R]-128) * contrast) + 128
            rgb[G] = ((rgb[G]-128) * contrast) + 128
            rgb[B] = ((rgb[B]-128) * contrast) + 128
            
            brightness=1.0
            mrgb = max(rgb)
            if mrgb > 0:
                brightness = 255.0 / mrgb
                if brightness > 5:
                    brightness = 5            
                
            rgb[R] = rgb[R] * brightness
            rgb[G] = rgb[G] * brightness
            rgb[B] = rgb[B] * brightness
            
            if rgb[R] < 0:
                rgb[R] = 0
            if rgb[R] > 255:
                rgb[R] = 255
                
            if rgb[G] < 0:
                rgb[G] = 0
            if rgb[G] > 255:
                rgb[G] = 255
                
            if rgb[B] < 0:
                rgb[B] = 0
            if rgb[B] > 255:
                rgb[B] = 255
            
            #print("Enhanced" + str(rgb)

        guess = ''
        
        for c, p in ColorGuesser.colors.items():
            
            if rgb[R] >= p['r']['min'] and rgb [R] <= p['r']['max'] and rgb[G] >= p['g']['min'] and rgb[G] <= p['g']['max'] and rgb[B] >= p['b']['min'] and rgb[B] <= p['b']['max']:
                guess = c
                #print('Guess for the region is ' + guess)
                break;
            
        #if guess == '':
        #    print('No guess for the region ')
            
        return guess

    def get_contrasted_color(self, color):
        
        cc = (255, 255, 255, 255)
        if color == 'w':
            cc = (0,0,0,255)
        elif color == 'y':
            cc = (0,0,255, 255)
        elif color == 'r':
            cc = (0, 255, 255, 255)
        elif color == 'g':
            cc = (255, 0, 255, 255)
        elif color == 'b':
            cc = (255, 255, 0, 255)
        elif color == 'o':
            c = (0, 0, 0, 255)
        
        
        return cc;


    