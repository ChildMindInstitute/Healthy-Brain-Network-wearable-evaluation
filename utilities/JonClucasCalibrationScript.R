#### Calibration function for Jon Clucas ####
#' Notes: 
#'       This script will calibrate GENEActiv .bin files to a new output folder.
#' 
#### Install and load libraries ####

if(!require(GGIR)) install.packages("GGIR")
if(!require(GENEAread)) install.packages("GENEAread")
library(GGIR)
library(GENEAread)
# library(GENEAclassify)

#### Calibrating files ####
# Run the following lines to create new directories containing the recalibrated files.
# This should take all the .bin files in your data directory, create an output directory and place all the 
# new calibrated files into this folder

ReCalibrate = function(datadir ,outputdir,...){
  # Create new folder if there isnt an outputdirectory
  if (length(datadir) == 0) {
    if (length(datadir) == 0) {
      print("Variable datadir is not defined")
    }
    if (missing(outputdir)) {
      print("Variable outputdir is not specified")
    }
  }
  
  filelist = FALSE
  
  # List all the files 
  fnames=list.files(path = datadir)
  if (length(fnames)==0){stop("There are no files in the data directory")}
  
  ####list of all bin files
  if (filelist == FALSE) {
    fnames = c(dir(datadir,recursive=TRUE,pattern="[.]bin"))
  } 
  
  else {
    fnames = datadir
  }
  # create output directory if it does not exist
  
  # If the outputdirectory is not specified create a defaulft
  if (missing(outputdir)) {
    outputfolder = paste(datadir,".Calibrated",sep="")
    dir.create(file.path(outputfolder))
  }
  
  for (i in 1:length(fnames)){
    
    Binfile = fnames[i]
    setwd(datadir)
    
    # Find the calibration values of the data.
    C=g.calibrate(Binfile, use.temp = TRUE, spherecrit = 0.3, minloadcrit = 72, 
                  printsummary = TRUE,chunksize=c(0.5),windowsizes=c(60,900,3600))
    
    # Read in the current values - 
    Lines=readLines(Binfile,-1) # Reads the bin file to the point where the calibration data is.
    XOffset=Lines[49];  XGain=Lines[48]
    YOffset=Lines[51];  YGain=Lines[50]
    ZOffset=Lines[53];  ZGain=Lines[52]
    
    # Extracting just the numerical value. - Offset
    XOffsetN=as.numeric(unlist(strsplit(XOffset,"x offset:"))[2])
    YOffsetN=as.numeric(unlist(strsplit(YOffset,"y offset:"))[2])
    ZOffsetN=as.numeric(unlist(strsplit(ZOffset,"z offset:"))[2])
    
    # Extracting just the numerical value for the Gain
    XGainN=as.numeric(unlist(strsplit(XGain,"x gain:"))[2])
    YGainN=as.numeric(unlist(strsplit(YGain,"y gain:"))[2])
    ZGainN=as.numeric(unlist(strsplit(ZGain,"z gain:"))[2])
    
    # Calculating the New values using the calibration values- Rounding to whole numbers
    if (C$offset[1] != 0){
      XOffsetNew=round((C$offset[1]* -25600) + XOffsetN)
      Lines[49]=paste("x offset:",sep="", XOffsetNew)
    }
    
    if (C$offset[2] != 0){
      YOffsetNew=round((C$offset[2] * -25600) + YOffsetN)
      Lines[51]=paste("y offset:",sep="", YOffsetNew)
    }
    
    if (C$offset[2] != 0){
      ZOffsetNew=round((C$offset[3] * -25600) + ZOffsetN)
      Lines[53]=paste("z offset:",sep="", ZOffsetNew)
    }
    
    if (C$scale[1] != 0){
      XGainNew=round(XGainN / C$scale[1])
      Lines[48]=paste("x gain:",sep="", XGainNew)
    }
    
    if (C$scale[2] != 0){
      YGainNew=round(YGainN / C$scale[2])
      Lines[50]=paste("y gain:",sep="", YGainNew)
    }
    if (C$scale[3] != 0){
      ZGainNew=round(ZGainN / C$scale[3])
      Lines[52]=paste("z gain:",sep="", ZGainNew)
    }
    # Set the correct path to the outputfolder
    setwd(outputfolder)
    
    # Creating the correct file name
    filename = fnames[i]
    names=strsplit(filename,".bin")
    writeLines(Lines,paste0(names,"_Recalibrate.bin"))
  }
}

# Change the data Directory to the location of your GENEActiv .bin files. 
# Please note that nothing else should be in the folder apart from the .bin files.
setwd(dirname(parent.frame(2)$ofile))
DataDirectory = "../raw"
ReCalibrate(DataDirectory)



