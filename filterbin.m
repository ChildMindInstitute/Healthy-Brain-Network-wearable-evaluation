function [Filtered_data] = filterbin(xyz, time)

%change sampling frequency here:
freq=75;

x=xyz(:,1);
y=xyz(:,2);
z=xyz(:,3);

[bx,ax]=butter(4,[.2,15]/(freq/2));
filtx=filter(bx,ax,x);

[by,ay]=butter(4,[.2,15]/(freq/2));
filty=filter(by,ay,y);

[bz,az]=butter(4,[.2,15]/(freq/2));
filtz=filter(bz,az,z);

filtered=[filtx,filty,filtz];
Filtered_data=[time,filtered];
