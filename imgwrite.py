from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import textwrap

FONT = 'verdanab.ttf'

def wallpaper(filename, title, text):
	im = Image.open(filename).convert('RGBA')
	
	lines = text.splitlines()
	title_font = ImageFont.truetype(FONT, 32)
	text_font = ImageFont.truetype(FONT, 18)
	buff = 10
	Xshift = 100
	Yshift = 60
	
	ybuff = buff/2
	(xmax, ymax) = (0,0)
	for line in lines:
		(xtext, ytext) = text_font.getsize(line)
		xmax = max(xmax, xtext)
		ymax = max(ymax, ytext)

	txt = Image.new('RGBA', im.size, (255, 255, 255, 0))

	draw = ImageDraw.Draw(txt)
	(xim, yim) = im.size

	#xcoord = xim - xtext - 2*buff - Xshift
	ycoord = yim - 3*ytext - 2*buff - Yshift
	
	
	# Draw text
	for line in reversed(lines):
		(xtext, ytext) = text_font.getsize(line)
		xcoord = xim - xtext - 2*buff - Xshift
		draw.rectangle([xcoord - buff, ycoord-buff, 
					xcoord + xtext + buff, ycoord+ytext+2*ybuff], (255, 255, 255, 140))
		draw.text((xcoord,ycoord),line, fill=(0, 0, 0, 255), font = text_font)
		
		ycoord-=(ymax+3*ybuff)
		
	# Draw title
	(xtitle, ytitle) = title_font.getsize(title)
	xct = xim - xtitle - 2*buff - Xshift
	yct = ycoord - ytitle + ymax - 2*ybuff
	draw.rectangle([xct - buff, yct, xct + xtitle + buff, yct+ytitle+ybuff], 
					(255, 255, 255, 140))
	draw.text((xct,yct),title, fill=(0, 0, 0, 255), font = title_font)
	
	draw = ImageDraw.Draw(im)
	
	out = Image.alpha_composite(im, txt)
	outfile = filename[:len(filename)-4] + '.jpg'
	out.save(outfile, quality=100)
	return outfile
