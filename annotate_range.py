#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def annotation_line(ax, xmin, xmax, text, y=-1.5, ytext=0, linecolor='black',
                    linewidth=1, fontsize=12):
    ax.annotate('', xy=(xmin, y), xytext=(xmax, y), xycoords='data',
                textcoords='data', arrowprops={'arrowstyle': '|-|', 'color':
                linecolor, 'linewidth':linewidth})
    ax.annotate('', xy=(xmin, y), xytext=(xmax, y), xycoords='data',
                textcoords='data', arrowprops={'arrowstyle': '<->', 'color':
                linecolor, 'linewidth':linewidth})

    xcenter = xmin + (xmax - xmin) / 2
    if ytext == 0:
        ytext = y + (ax.get_ylim()[1] - ax.get_ylim()[0]) / 20

    if text in ['charging (after)', 'charging (before)']:
        text = 'charging'

    ax.annotate(text, xy=(xcenter,ytext), ha='center', va='center',
                fontsize=fontsize)