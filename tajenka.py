#!/bin/python3

import os
from sys import argv
import re
import cairo

if not argv[1]:
  raise 'missing infile'

def generate_pdf(filename, title, crosswords, clues, show_solution):
  # get the height and width of crosswords
  crossh = 0
  crossw = 0
  for l in crosswords:
    crossh += 1
    if len(l) > crossw:
      crossw = len(l)

  cluesw = 0
  for c in clues:
    if len(c) > cluesw:
      cluesw = len(c)

  font_size = 22
  px = 34
  py = 34
  # height = space line + title + spaceline + crossword + spaceline + line
  height = (crossh + 5) * py
  # width = space collum + crossword + space collum + clues
  width = (2 + crossw + cluesw) * px
  
  surface = cairo.PDFSurface(filename, 1240, 1754)
  ctx = cairo.Context(surface)

  ctx.set_source_rgb(0, 0, 0)
  ctx.select_font_face("FreeSerif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
  ctx.set_font_size(font_size)
  ctx.move_to(font_size, font_size)
  ctx.show_text(title)
  ctx.move_to(font_size, 2 * font_size)
  ctx.set_line_width(1)

  y = 4 * font_size
  for i, l in enumerate(crosswords):
    x = px
    for c in l:
      x += px
      if c == '':
         ctx.move_to(x, y)
      elif c.islower():
         ctx.set_line_width(1)
         ctx.rectangle(x, y, px , py )
         ctx.stroke()
         if show_solution:
           ctx.move_to(x + 1, y + py - 2)
           ctx.show_text(c)
      elif c.isupper():
         ctx.set_line_width(1)
         ctx.rectangle(x, y, px, py)
         ctx.set_source_rgb(1, 1, 0)
         ctx.fill()
         ctx.set_source_rgb(0, 0, 0)
         ctx.rectangle(x, y, px, py)
         ctx.stroke()
         if show_solution:
           ctx.move_to(x + 1, y + py - 2)
           ctx.show_text(c)
    # write clue
    ctx.move_to((crossw + 4) * px, y + py -2)
    ctx.show_text(clues[i])
    y += py
  ctx.move_to(0, y + 3 * py)
  ctx.set_line_width(1)
  ctx.line_to(1240, y + 3 * py)
  ctx.stroke()
  ctx.show_page()

title = None
crosswords = []
clues = []
with open(argv[1]) as infile:
  reading_crosswords = False
  reading_clues = False
  reading_title = False
  for line in infile:
    line = line.rstrip()
    if len(line) == 0 or re.match(r'^#', line):
      next
    elif re.match(r'title:', line):
      reading_title = True
      reading_crosswords = False
      reading_clues = False
      next
    elif re.match(r'tajenka:', line):
      reading_title = False
      reading_crosswords = True
      reading_clues = False
      next
    elif re.match(r'napovedy:', line):
      reading_title = False
      reading_crosswords = False
      reading_clues = True
      next
    else:
      if reading_title:
        title = line
      elif reading_crosswords:
        crosswords.append(line)
      elif reading_clues:
        clues.append(line)

# one doc generate full
filename_private = title.replace(' ', '_') + '_private.pdf'
generate_pdf(filename_private, title, crosswords, clues, True)
# one doc generate empty
filename_pub = title.replace(' ', '_') + '_public.pdf'
generate_pdf(filename_pub, title, crosswords, clues, False)

print("Generated files {} and {}\n".format(filename_private, filename_pub))
