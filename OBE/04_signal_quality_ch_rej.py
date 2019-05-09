def findSNR(input,spec):
    import numpy as np
    '''
    설명 : Calculate SNR map (t sec x n ch)
    args* = input(d780 || d850), spec
    result = [z]
    example:
    '''
    # first. BPF
    filtered_raw = bpf(input, spec)
    win_size = round(10 * spec.FS)  #10초
    (num_ch,num_frame) = input.shape
    # second. calculate SNR
    out_mat = np.zeros(num_ch,num_frame)
    for i in range(num_ch): ## for each channel0.00000000000000000000000000000000000000000000
        for j in range(1, win_size, num_frame): ## moving window : 너무 느려서 띄엄띄엄하게 하도록 함
            if j <= num_frame-win_size:
                sig = filtered_raw[i, j:j+win_size]
                out_mat[i,j:j+winsize-1] = np.real(20*np.exp(sig.mean/sig.std ) )
            else:
                # 끝부분은 그냥 패딩
                out_mat[i,j:] = out_mat[i,num_frame-win_size]
    z = outmat
    return z

class MDOD:
    def findMDOD(self, MAR_dOD, filt_ang_x, filt_ang_z, ths_motion_xyz, spec):
        '''
        설명 : calculate motion corrected dOD from normal dOD
        args* = input(d780 || d850), spec
        result = [mdOD]
        example:
        '''
        import numpy as np

        # Motion corrected dOD
        mdoD = []
        Xcorr_Thre = spec.dOD.Xcorrthr
        spline_window = spec.dOD.Spkwin
        ch_num = spec.NCH
        ch_reject = spec.chrej
        nCh = spec.NCHJ

        [Cos_angle_Rx,Cos_angle_Lx,Cos_angle_z] = featuresFromIMU(filt_ang_x, filt_ang_z, spec)
        [env_Rx_filt, env_Lx_filt, env_z_filt] = env_det_gyro(Cos_angle_Rx, Cos_angle_Lx, Cos_angle_z, spec)
        MAR_OD_R_flag = XcorrOD_Motion_sensor(env_z_filt, env_Lx_filt, env_Rx_filt, MAR_dOD, spec)
        MAR_OD_R_flag = MAR_OD_R_flag > Xcorr_Thre

        MAR_OD_GLM = np.zeros(size(MAR_dOD))

        for i in range(ch_num):
            if ch_reject[i] == 0:
                if MAR_OD_R_flag[i] == 1:
                    GLM_X = np.concate((env_z_filt, env_Lx_filt, env_Rx_filt), axis = None)
                    mdl_GLM = fit_glm(GLM_X, MAR_dOD[i,:])
                    MAR_OD_GLM[i,:] = mdl_GLM.Residuals.Raw
                else:
                    MAR_OD_GLM[i,:] = MAR_dOD[i,:]
            else:
                MAR_OD_GLM[i,:] = MAR_dOD[i,:]

        dODspline = GyroMotionCorrectSpline(MAR_OD_GLM, ths_motion_xyz, spline_window, 0.1, spec).dODspline
        dODspline[:,1] = 0
        baselines = spec.dOD.sBase
        baselinef = spec.dOD.eBase

        dODspline_ini = np.zeros(nCh,1)
        for i in range(nCh):
            dODspline_ini[i] = mean(dODspline[i, round(baselines * spec.FS)+1 : round(baselinef * spec.FS)])

        dOD = np.zeros(size(MAR_dOD))
        for i in range(nCh):
            dOD[i,:] = dODspline[i,:]-dODspline_ini[i]
        mdOD = dOD
        return mdOD 


function [dOD_Spline_SG] = deleteSpike(input,spec)
## spike removal
dod = input
fs = spec.Fs

iqr = 1.5
SNR_Thre = zeros(1,size(dod,2))
FrameSize_sec = 10
wd =10
sp_factor = 0.1

for ww = 1:size(dod,2)
    clearvars -except ww d ml fs t dod tMotion SD dodorg p iqr SNR_Thre SNR_Thre2 FrameSize_sec dataSet wd sp_factor
    s1 =  dod(:,ww) 
    [s1,~] = hmrBandpassFilt( s1, fs, 0, 2)
    [s2,~] = hmrBandpassFilt( s1, fs, 0, 0.5)
    
    ## detecting outliers in std variations of the signal
    tMotion=1
    Win_Size=round(fs*tMotion)
    Sigstd = zeros(length(s1)-(Win_Size),1)
    for ilent=1:length(s1)-(Win_Size)
        Sigstd(ilent,1)=std(s2(ilent:ilent+(Win_Size),:))
    end
    iqr2 = 2
    quants_std = quantile(Sigstd,[.25 .50 .75])  # compute quantiles
    IQR_std = quants_std(3)-quants_std(1)  # compute interquartile range
    High_std = quants_std(3)+IQR_std*iqr2
    Low_std = quants_std(1)-IQR_std*iqr2
    
    ## detecting outliers in gradient of the signal
    grad = conv(s1,[-1,0,1]) # Sobel mask
    quants = quantile(grad,[.25 .50 .75])  # compute quantiles
    IQR1 = quants(3)-quants(1)  # compute interquartile range
    High = quants(3)+IQR1*iqr
    Low = quants(1)-IQR1*iqr
    
    
    z_std=0
    M_std = zeros(length(dod)-(Win_Size),1)
    for i=1:length(dod)-(Win_Size)
        if ((Sigstd(i)>High_std) || (Sigstd(i)<Low_std))
            z_std=z_std+1 M_std(z_std)=i
        end
    end
    M_std(z_std+1:end,:)=[]
    
    if exist('M_std','var')
        M_std=round(Win_Size/2)+M_std
    end
    
    z=0
    M_sobel = zeros(length(dod),1)
    for i=1:length(dod)
        if ((grad(i)>High) || (grad(i)<Low))
            z=z+1 M_sobel(z)=i
        end
    end
    M_sobel(z+1:end,:)=[]
    
    if exist('M_sobel','var') && exist('M_std','var')
        M=union(M_sobel,M_std)
    else
        if exist('M_sobel','var')
            M=M_sobel
        else
            if exist('M_std','var')
                M=M_std
            end
        end
    end
    extend = round(12*fs)
    s11=repmat(s1(1,:),extend,1)s12=repmat(s1(end,:),extend,1)
    s1temp=[s11s1s12] # extending signal for motion detection purpose (12 sec from each edge)
    s1=s1temp
    
    t=(0:(1/fs):(length(s1)/fs))'
    t=t(1:length(s1),1)
    if ww==1
        #prelocation
        tInc = zeros(length(t),size(dod,2))
    end
    
    if exist('M','var')
        M=M+extend
        sig=ones(length(s1),1)
        for i=1:length(M)
            sig(M(i),:)=0
        end
        
        ### finding the location of the spikes or baseline shifts
        temp = (diff(sig))
        
        c=0
        meanpL = zeros(length(s1)-1,1)
        meanpH = zeros(length(s1)-1,1)
        for i=1:length(s1)-1
            if (temp(i)==1)
                c=c+1
                meanpL(c)=mean(s1(i),1)
                meanpH(c)=mean(s1(i),1)
            end
        end
        meanpL(c+1:end,:)=[]
        meanpH(c+1:end,:)=[]
        motionkind=abs(meanpH-meanpL)
        
        ## finding the baseline shifts by comparing motion amplitudes with heart rate amplitude
        stemp=s1
        [s1,~] = hmrBandpassFilt( stemp, fs, 0, 2 )
        snoise2=stemp
        zz=0tt=1
        sigtemp = cell(1,length(s1)-1)
        sigtempnoise = cell(1,length(s1)-1)
        for i=1:length(s1)-1
            if (sig(i)==1)
                zz=zz+1
                sigtemp{1,tt}(1,zz)=s1(i)
                sigtempnoise{1,tt}(1,zz)=snoise2(i)
                if ((sig(i)==1) && (sig(i+1)==0))
                    tt=tt+1
                    zz=0
                end
            end
        end
        
        Nthre=round(0.5*fs)ssttdd=0
        for i=1:tt
            tempo=sigtemp{1,i}
            if length(tempo)>Nthre
                tempo2 = zeros(1,length(tempo)-Nthre)
                for l=1:length(tempo)-Nthre
                    tempo2(l)=(abs(tempo(l+Nthre)-tempo(l)))
                end
            end
            ssttdd=[ssttdd tempo2]
            clear tempo2
            tempo2=[]
        end
        
        thrshld = quantile(ssttdd,0.5)
        pointS = (find(temp<0))
        pointE = (find(temp>0))
        countnoise = 0
        SNR_Thresh = zeros(length(sigtempnoise),1)
        for ks=1:length(sigtempnoise)
            if (length(sigtempnoise{1,ks})>3*fs)
                countnoise = countnoise+1
                dmean = mean(sigtempnoise{1,ks},2)
                dstd = std(sigtempnoise{1,ks},[],2)
                SNR_Thresh(countnoise,1) = abs(dmean)./(dstd+eps)
            end
        end
        SNR_Thresh(countnoise+1:end,:)=[]
        SNR_Thre(1,ww)=mean(SNR_Thresh(2:end-1,1))
        
        sig2=ones(length(s1),1)
        for i=1:length(pointS)
            if motionkind(i)>thrshld
                sig2(pointS(i):pointE(i),:)=0
            end
            # # # # # # # # # # # # # # # # # #
            # spline on long duration spikes  #
            # # # # # # # # # # # # # # # # # #
            
            if (((pointE(i)-pointS(i))> (0.1*fs))&&((pointE(i)-pointS(i))< (0.49999*fs)))
                sig2(pointS(i):pointE(i),:)=0
            end
            if (pointE(i)-pointS(i))> (fs)
                sig2(pointS(i):pointE(i),:)=0
            end
        end
        clear pointS
        clear pointE
        clear sig
        clear temp
        
        tInc(:,ww)=sig2
    else
        tInc(:,ww)=ones(length(t),1)
    end
end

## Extracting the noisy channels from baseline-shift motion correction precedure
for w=1:(size(SNR_Thre,2))
    if isnan(SNR_Thre(1,w)) || isempty(SNR_Thre(1,w)) || (SNR_Thre(1,w)==0)
        dmean = mean(dod(:,w))
        dstd = std(dod(:,w))
        SNR_Thre(1,w)=abs(dmean)./dstd
    end
end

SNRvalue=3
for i = 1:size(SNR_Thre,2)
    if SNR_Thre(i) < SNRvalue || isnan(SNR_Thre(i))
        tInc(:,i) = ones(size(tInc,1),1)
    end
end
tIncCh=tInc(extend+1:end-extend,:)

extend = round(12*fs)

tIncCh1=repmat(tIncCh(1,:),extend,1)
tIncCh2=repmat(tIncCh(end,:),extend,1)
tIncCh=[tIncCh1tIncChtIncCh2]

d1=repmat(dod(1,:),extend,1)
d2=repmat(dod(end,:),extend,1)
dod=[d1dodd2]



[dodLP,~] = hmrBandpassFilt( dod, fs, 0, 2 )

## Spline Interpolation


n_data = length(dodLP)
dODspline = zeros(size(dod,2),n_data)
for k = 1:size(dod,2)
    MA_segment= zeros(1,n_data)
    dOD = dodLP(:,k)'
    Thrs_MA = tIncCh(:,k)
    for i = 1:n_data-2*wd
        if Thrs_MA(i) == 0
            MA_segment(i:i+2*wd) = 1
        end
        MA_segment(1) = 0
        MA_segment(end) = 0
    end
    
    Gyro_MA_sf = diff(MA_segment)
    if isempty(find(Gyro_MA_sf, 1)) == 0
        s_pt = find(Gyro_MA_sf ==1)
        f_pt = find(Gyro_MA_sf == -1)
        for i = 1:length(s_pt)
            spline = csaps(1:(f_pt(i)-s_pt(i)+1),dOD(1,s_pt(i):f_pt(i)),sp_factor,1:(f_pt(i)-s_pt(i)+1))
            Offset_spline = [zeros(1,s_pt(i)-1) (spline-spline(1)) ones(1,n_data - f_pt(i))*(spline(end)-spline(1))]
            dOD(1,:) = dOD(1,:) - Offset_spline
        end
        dODspline(k,:) = dOD
    else
        dODspline(k,:) = dOD
    end
    
end

dODspline = dODspline'
dod=dODspline(extend+1:end-extend,:) # removing the extention

## Savitzky_Golay filter
K = 3 # polynomial order
FrameSize_sec = round(FrameSize_sec * fs)
if mod(FrameSize_sec,2)==0
    FrameSize_sec = FrameSize_sec  + 1
end

dod2=sgolayfilt(dod,K,FrameSize_sec)

dOD_Spline_SG = dod2'
end


def baselinefit(signal, spec=[]):   # by SJ
    '''
    설명: 특정 시점에 다시 baseline 잡아주는 기능
    args*=
        signal, spec
    return=
        [sigout]
    example:

    '''
    sigout = []
    nb = round(spec.dOD.nBase * spec.FS)
    nch = spec.NCH

    for i in range(len(nch)):
        signal[i] = signal[i] - signal[i,nb]
    sigout = signal
    return sigout


def ChRejection(inputRAW, inputSNR, inputMBLL, spec):
    '''
    설명: SNR-based Channel rejection
    args*= inputRAW, inputSNR, inputMBLL, spec
    result= [RejectedCh]
    example:
    '''
    RejectedCh = []
    nch = spec.NCH
    ndata = spec.ndata

    start = round(spec.dOD.nBase * spec.FS)

    rd7 = inputRAW.d780[1:nch,:]
    rd8 = inputRAW.d850[1:nch,:]
    sd7 = inputSNR.d780[1:nch,:]
    sd8 = inputSNR.d850[1:nch,:]
    hbo = inputMBLL.HbO[1:nch,start+1:-1]
    hbr = inputMBLL.HbR[1:nch,start+1:-1]

    # 다 0인경우
    reject1 = rd7.sum(axis=1)==0 or rd8.sum(axis=1)==0
    # raw에서 한번이라도 음수로 떨어지는 경우
    reject2 = rd7.sum(axis=1)<0 or rd8.sum(axis=1)<0
    # SNR threshold 값과
    SNRthd = spec.SNRthd
    ZSCRthd = spec.ZSCRthd
    zscore_780 = np.zeros(nch,1)
    zscore_850 = np.zeros(nch,1)

    for i in range(nch):
        zscore_780[i] = sum((sd7[i,]<=SNRthd)*abs(sd7[i,] - mean(sd7,1))/std(sd7,1))/ndata
        zscore_850[i] = sum((sd7[i,]<=SNRthd)*abs(sd8[i,] - mean(sd8,1))/std(sd8,1))/ndata
    reject3 = zscore_780 > ZSCRthd | zscore_850 > ZSCRthd
    # 다 nan인경우
    reject4 = isnan(rd7.sum(axis=1)) | isnan(rd7.sum(axis=1))

    # MBLL이 차이가 심한 경우
    ZSCRthd2 = spec.ZSCRthd2
    zscore_hbo = np.zeros(nch)
    zscore_hbr = np.zeros(nch)

    for i in range(nch):
        zscore_hbo[i] = sum( abs(hbo[i,] - mean(hbo,1))/std(hbo,1) )/ndata
        zscore_hbr[i] = sum( abs(hbr[i,] - mean(hbr,1))/std(hbr,1) )/ndata
    reject5 = zscore_hbo > ZSCRthd2 | zscore_hbr > ZSCRthd2

    # MBLL이 다 0으로 나온 경우
    reject6 = hbo,sum(axis=1)==0 | hbr.sum(axis=1)==0

    # rejection all
    RejectedCh = reject1 | reject2 | reject3 | reject4 | reject5 | reject6
    return RejectedCh


def ApplyChRej(sig, ch_rej):
    '''
    설명: Channel Rejection 적용 하는 부분
    args*= sig, ch_rej
    result= [HbO, HbR, HbT]
    example:
    '''
    HbO = sig.HbO
    HbR = sig.HbR
    HbT = sig.HbT

    for i in range(ch_rej.size):
        if ch_rej(i):
            HbO[i,]=0
            HbR[i,]=0
            HbT[i,]=0
    return HbO, HbR, HbT


function [HbO2, HbR, HbT, RejectCh] = paddingCh3(siginput, RejectCh)
## Padding : 중앙 부분만 
HbO2 = siginput.HbO
HbR = siginput.HbR

couplech = [1,0 2,0 3,0 4,0 5,0 6,49 7,50 8,51 9,0 10,0 ...
    11,52 12,53 13,54 14,0 15,0 16,0 17,0 18,0 19,0 20,0 ...
    21,55 22,56 23,57 24,58 25,59 26,60 27,61 28,62 29,0 30,0 ...
    31,0 32,0 33,0 34,0 35,0 36,63 37,64 38,65 39,0 40,0 ...
    41,66 42,67 43,68 44,0 45,0 46,0 47,0 48,0]

for i = 1 : 48
    if RejectCh(i,1) == 1
        if couplech(i,2) ~= 0
            if RejectCh(couplech(i,2),1) == 0
                HbO2(i,:) = HbO2(couplech(i,2),:)
                HbR(i,:) = HbR(couplech(i,2),:)
                RejectCh(i,1) = 0
                RejectCh(couplech(i,2),1) = 1
            end
        end
    end
end
HbT = HbO2 + HbR
end


