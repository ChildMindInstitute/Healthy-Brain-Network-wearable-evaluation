Encoding("UTF-8")
# GENEActiv_analysis.R
# 
# Script to analyze output binary files from GENEActive wearable devices.
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
require(lubridate)

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

AccDatas <- c('arno_foot_l', 'arno_foot_r', 'arno_hand', 'curt_hand',
              'jon_hand')
processing_times <- c(2.219 * 60, 3.077 * 60, 3.916, 12.753 * 60, 3.57)
pt2 <- c(39.367, 25.765, 3.652, 9.103*60, 3.991)
record_frames <- c(14803200, 10368000, 2009100, 33276000, 1728000)
record_RAM <- c(829, 581, 113, 1863, 97)
fq <- c(85.7, 60, 20, 100, 10)
dur <- c(48, 48, 168, 168, 48)
meta <- data.frame(g_files, AccDatas, fq, dur, processing_times, pt2,
                   record_frames, record_RAM)
remove(AccDatas, processing_times, pt2, record_frames, record_RAM, fq, dur)

# put all of our data from the same time range into a single dataframe
acc_df <- function(df, acc, device, start_time, end_time){
  # function to bind acc data to a dataframe
  # 
  # Parameters
  # ----------
  # df : dataframe
  #   the dataframe we'll be binding to
  # 
  # acc : AccData
  #   the acc data we'll be binding
  #   
  # device : string
  #   the name we wnat in the "device" column for this acc data
  # 
  # start_time : double (lubridate ymd_hms), optional
  #   the start_time at which we cut off recording values
  #   defaults to `ymd_hms("2017-02-20 17:00:00 EST")`
  #   
  # end_time : double (lubridate ymd_hms), optional
  #   the end_time at which we cut off recording values
  #   defaults to `ymd_hms("2017-02-22 17:00:00 EST")`
  # 
  # Returns
  # -------
  # df : dataframe
  #   the original dataframe with the additional acc data appended
  if(missing(start_time)){
    start_time = ymd_hms("2017-02-20 17:00:00 EST")
  }
  if(missing(end_time)){
    end_time = ymd_hms("2017-02-22 17:00:00 EST")
  }
  accdf <- data.frame(ymd_hms(acc$page.timestamps[ymd_hms(
           acc$page.timestamps) <= end_time & ymd_hms(acc$page.timestamps) >= 
           start_time]), acc$x[ymd_hms(acc$page.timestamps) <= end_time & 
           ymd_hms(acc$page.timestamps) >= start_time], acc$y[ymd_hms(
           acc$page.timestamps) <= end_time & ymd_hms(acc$page.timestamps) >= 
           start_time], acc$z[ymd_hms(acc$page.timestamps) <= end_time &
           ymd_hms(acc$page.timestamps) >= start_time], acc$light[ymd_hms(
           acc$page.timestamps) <= end_time & ymd_hms(acc$page.timestamps) >= 
           start_time], acc$button[ymd_hms(acc$page.timestamps) <= end_time & 
           ymd_hms(acc$page.timestamps) >= start_time], acc$temperature[
           ymd_hms(acc$page.timestamps) <= end_time & ymd_hms(
           acc$page.timestamps) >= start_time], c(device))
  return(rbind(df, accdf))
}
# initialize dataframe
acc_data <- data.frame(timestamp=double(), x=double(), y=double(), z=double(), 
                       light=double(), button=double(), temperature=double(), device=
                         factor())
# append each acc data
acc_data <- acc_df(acc_data, arno_hand, "Arno hand")
acc_data <- acc_df(acc_data, arno_foot_l, "Arno left foot")
acc_data <- acc_df(acc_data, arno_foot_r, "Arno right foot")
acc_data <- acc_df(acc_data, curt_hand, "Curt hand")
acc_data <- acc_df(acc_data, jon_hand, "Jon hand")
names(acc_data) = c('timestamp', 'x', 'y', 'z', 'light', 'button', 'temperature', 'device')