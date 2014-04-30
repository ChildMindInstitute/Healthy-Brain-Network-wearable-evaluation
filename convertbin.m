clear all
clc

disp('Sampling Frequency is set at 75 hz')
disp(' ')
disp('File being processed:')

direc=dir('*.bin');
fnames={direc.name};
numfiles=length(fnames);


All_Data=[];
for t=1:numfiles
    filename=fnames {t};
    Name_1=filename;
    disp(Name_1);

    [hdr, time, xyz, light, but] = binread(filename); %Read in the bin file


[Name]=textscan(Name_1, '%s %s', 'delimiter','.'); %Seperates ID number from .xls extension
ID=Name{1,1}; %Selects the ID number
Extension1='_filtered.csv';
New_Name1=char(strcat(ID,Extension1));




    [Filtered_data] = filterbin(xyz, time);%Apply Bandpass filter and calculate signal vector magnitude

    dlmwrite(New_Name1,Filtered_data,'delimiter',',','precision',15);


clear xyz
clear time
clear Filtered_data


end
disp(' ')
disp('Columns 1:4 of the .csv are:[time, filt x, filt y, filt z]');
