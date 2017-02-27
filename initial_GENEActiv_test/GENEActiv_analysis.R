Encoding("UTF-8")
# GENEActiv_analysis.R
# 
# Script to analyze output CSV files from GENEActive wearable devices.
# Built in R 3.3.2 (Sincere Pumpkin Patch)
# 
# Author:
#   – Jon Clucas, 2017 <jon.clucas@childmind.org>
#   
# © 2017, Child Mind Institute, Apache v2.0 License
#   
# Depends on:
#   Package 'GENEAread' v 1.1.1
#     Maintainer:
#       Joss Langford <Joss at activinsights.co.uk>
#     Author:
#       – Zhou Fang
#   Published: 2013-04-23
#   License: GPL-2 | GPL-3
#   Documentation:
#     https://cran.r-project.org/web/packages/GENEAread/GENEAread.pdf
#       
#   Package 'GGIR' v 1.4
#     Author:
#       – Vincent T van Hees <vincentvanhees@gmail.com>
#     Contributors:
#       – Zhou Fang
#       – Jing Hua Zhao
#       – Joe Heywood
#       – Severine Sabia
#     Date/Publication: 2017-01-22 17:02:09
#     License: LGPL (≥ 2.0, < 3)
#     Documentation:
#       https://cran.r-project.org/web/packages/GGIR/GGIR.pdf

# our GENEActive data
setwd("/Volumes/Data/Research/ITL/GENEActiv/Data/")
# exclude the partial data CSVs; include only full-data binaries
g_files <- list.files()[endsWith(list.files(), '.bin')]
# subset the recordings captured 2017 Feb 20-22,
# offloaded Feb 22 & Feb 24
g_files <- g_files[grepl('02-22', g_files) | grepl('02-24', g_files)]

# GENEActiv analysis libraries
require(GENEAread)
require(GGIR)

# dependencies
require(mmap)

# GENEAread function `read.bin` returns an AccData object
# AccData factors for the device we are testing are:
#   timestamp
#   x
#   y
#   z
#   light
#   button
#   temperature
arno_foot_l <- read.bin(g_files[1])
arno_foot_r <- read.bin(g_files[2])
arno_hand <- read.bin(g_files[3])
curt_hand <- read.bin(g_files[4])
jon_hand <- read.bin(g_files[5])

AccDatas <- c('arno_foot_l', 'arno_foot_r', 'arno_hand', 'curt_hand', 'jon_hand')
processing_times <- c(2.219 * 60, 3.077 * 60, 3.916, 12.753 * 60, 3.57)
pt2 <- c(39.367, 25.765, 3.652, 9.103*60, 3.991)
record_frames <- c(14803200, 10368000, 2009100, 33276000, 1728000)
record_RAM <- c(829, 581, 113, 1863, 97)
fq <- c(85.7, 60, 20, 100, 10)
dur <- c(48, 48, 168, 168, 48)
meta <- data.frame(g_files, AccDatas, fq, dur, processing_times, pt2, record_frames, record_RAM)
remove(AccDatas, processing_times, pt2, record_frames, record_RAM, fq, dur)
