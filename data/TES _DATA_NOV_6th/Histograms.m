
Files_name = dir('*.mat');
global Wigner Nsum
Channel_A = Files_name(77,1).name



%Channe_A([a:a+g, b:b+g, c:c+g])=[];
%Channel_B([a:a+g, b:b+g, c:c+g])=[];
%Channel_A(1:1.714e5)=[];
%Channel_B(1:1.714e5)=[];
Size_Channel_A_raw = length(Channel_A);

Raw_A = load(Channel_A);


Raw_A_Voltages = Raw_A.Y1; 
 
Raw_T1 = Raw_A.T1; 
 
L_small_trace = 1/3*length(Raw_T1);

%Ya = Raw_A_Voltages.*Raw_B_Voltages;
 Ya = Raw_A.Y1; 
 Ya = Ya(1:10000);


%Ya([1:3.237e5, 3.958e6:5.44e6, 8.876e6:1.027e7, 1.39e7:1.534e7])=[];
%Ya([3.525e6:4.977e6, 8.646e6:5.44e6, 8.876e6:1.027e7, 1.39e7:1.499e7])=[];

%Ya([1:1.277e6, 3.821e6:5.023e6, 7.56e6:8.674e6, 1.123e7 : 1.237e7])=[];

Ta = Raw_A.T1;
%Ta([1:1.277e6, 3.821e6:5.023e6, 7.56e6:8.674e6, 1.123e7 : 1.237e7])=[];
Ta([1:5.69e6, 5.237e6:5.023e6, 1.025e7:1.157e7, 1.5144e7 : length(Ta)])=[];
%Ta([[1:3.237e5, 3.958e6:5.44e6, 8.876e6:9.993e6, 1.363e7:1.124e7]]) = [];
%data = Raw_A_Voltages(1500000:1605000);
data = Ya;%%(10000:360000);
data = data-mean(data);
figure
subplot(2,1,1)
plot(Raw_A_Voltages)
subplot(2,1,2)
plot(Ya)

%data = Raw_A_Voltages;
%data = Raw_A_Voltages; 
noisethresh=-50; %threshold for noise mean to be 0...
datai=data>noisethresh;
datap=data-sum(data.*not(datai))/length(data.*not(datai));


%data(data<200) = 0;
numtosum = 9;
mat = (0:numtosum - 1)';

TimeBin = 4;

%%Filter the data SG works the best because it keeps the amplitude and 
% figure
% plot(data)
% hold on
% plot(Raw_B_Voltages)
noisethres = 7745;
thres = [50,180,317,513,630,900,1200];

%Diff_thres = 150; 
numdiff = 6;
d = zeros(numdiff+1, length(data)-1);
d(1,:) = diff(data);
dindex = d(1,:)>0;
for i  = 1:numdiff
   d(i+1,:)=diff([data(1+i:end) zeros(1,i)]).*dindex;
   dindex = d(i+1,:)>0;
end 
d = sum(d,1);
figure
phindex=find(diff(d>50)>0)+1; 
plot(datap)
hold on
plot(phindex, datap(phindex), '*')
hold off
 
sum(diff(phindex)<numtosum);
dataj = repmat(mat, size(phindex))+repmat(phindex, numtosum,1)+1;
size(dataj)
dataj(dataj>length(data)) = 1;
datat = data(dataj);
if size(dataj,2) ==1
    datat = datat';
end
phmax = max(datat,[],1)-max(0,min(datat,[],1)-100);
DataFinal=zeros(size(data));
DataFinal(phindex) = phmax;
%fid = fopen('Data_final.txt', 'w');
%fwrite(fid, DataFinal);
%fclose(fid);
figure 
[n,x]=hist((DataFinal),400);
stairs(x,n,'r');
set(gca,'yscale','log');







for k = 1:(size(thres,2)-1)
    DataFinal(DataFinal>thres(k) & DataFinal<=thres(k+1)) = k-1;
end


%if mod(length(DataFinal), TimeBin) == 0
 %   more = TimeBin -mod(length(DataFinal),TimeBin);
  %  DataFinal(end+(1:more)) = zeros([1,more]);
%end
%phxx = sum(reshape(DataFinal, TimeBin,[]),1);
%size(phxx);
%sum(phxx);
%N = zeros(1,100);
%for t =1:100
 %   N(t) = sum(phxx == (t-1));
%end

%Wig = -sum(diff(reshape(N,2,[])))/length(phxx)


    



%figure
%plot(Raw_T1(1:1000),Raw_A_Voltages_Cut(1:1000), 'r')

%figure 

%plot(Raw_T1(1:1000),Raw_A_Voltages(1:1000), 'r')

%%Define the threshold for all 1,2,3,4 photon peaks

%%Use the first for H ratio, its without displacement and others are for
%%different EOM voltages starting from 0.5-7.0, 15 sets of A and B
