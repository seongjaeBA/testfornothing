###  json writer ###
# 190225 : 웅진 분석을 위한 간이 table update를 위한 json 생성기
# 190226 : motion, spike removal 추가 및 raw > od > mbll 검증
# 190227 : spike removal code 정리 (BPF 마찬가지)
# ~190305 : json 생성(feature포함) 및 서버 전송 테스트 
# 190306 : 코드 정리 및 완성형 feature set 전송 테스트 + 분석을 위한 별도 csv 생성

def makejson(inputsignal,plotflag,dataTransflag):
    '''
    args* 
        inputsignal,plotflag,dataTransflag
    return = 
        server_result, output_mat
    example:
    '''
    
    '''
    matlab code
    function [server_result, output_mat] = makejson(inputsignal,plotflag,dataTransflag)
    ## function automation
    # inputsignal  # T frame (t seconds) x 68 ch

    [output] = signalprocessing(inputsignal,plotflag);
    [server_result] = serverTransmit(output,dataTransflag);
    # [output_mat]=makeAnalysis(output);  ### JY 
    [output_mat]=makeAnalysis2(output);  ### CM 

    end
    '''
    [output] = signalprocessing(inputsignal,plotflag)
    [server_result] = serverTransmit(output,dataTransflag)
    [output_mat]=makeAnalysis2(output)

    return output_mat, server_result

def signalprocessing(inputsignal,plotflag):
    ''' 
    args* 
        inputsignal,plotflag
    return = 
        inputsignal,plotflag
    example:

    '''
    '''
    function [output] = signalprocessing(inputsignal,plotflag)
    ## 입력에 대한 1차 데이터 출력 function

    ## 입력
    insig = inputsignal;

    ## extract data from input :: 각 항목 매칭필요.

    disp('------------------------------')
    disp('...OBELAB SIGNAL PROCESSING...')
    disp('------------------------------')
    disp('...start...')

    # constants
    Fs = 8.138;
    spec.Fs = Fs;
    spec.nch = 68;    # 204ch 중에서 68개만 씀

    BPFspec = [0.1 0.005];           ##
    spec.BPF = BPFspec;

    # MAR spec
    spec.dOD.sBase = 10;
    spec.dOD.eBase = 15;
    spec.dOD.nBase = 10;
    spec.dOD.Spkwin = 10;
    spec.dOD.Xcorrthr = 0.6;
    spec.dOD.Accthr = 1.8;
    spec.dOD.Gyrothr = 1.8;
    spec.dOD.Envwin = 100;
    spec.concunit = false; # 단위에 따른 처리
    spec.chrej = zeros(spec.nch,1); # channel rejections .. 일단 zero

    # 기기 정보 비교 필요 --> TODO:
    # r, dpf, inv_extinc params
    loadDetailParams = false;
    spec = findCoeff(loadDetailParams, spec);

    # Channel Rejection
    spec.SNRthd = 30;
    spec.ZSCRthd = 0.1;  # snr 기반 rejection threshold
    spec.ZSCRthd2 = 1;   # mbll 기반 rejection threshold

    # padding option
    spec.GSS = false;  # (Regional) global signal subtraction

    # Info:
    id = insig.ID;                  ## UID
    task_name = insig.TaskName;     ## Task종류
    date = insig.Date;              ## 측정날짜

    # Time-series data
    time_stp = insig.Timestamp;     ##
    spec.ndata = length(time_stp);      ##
    marker = insig.Marker;          ##
    TaskBlock = insig.TaskBlock;

    # IMU data
    [filt_ang_x, filt_ang_y, filt_ang_z, ths_motion_xyz, ~, ~] = ...
        degreeFromIMU(insig.Accel, insig.Gyro, spec);


    # raw signal
    tic
    disp('...Read d780/d850 raw signal')
    raw_sig.d780 = insig.Raw.d780';            ##
    raw_sig.d850 = insig.Raw.d850';            ##
    disp('...done')
    toc


    # calculate SNR (including BPF)
    tic
    disp('...Calculate SNR map')
    snr_sig.d780 = findSNR(raw_sig.d780, spec);  ## processing data
    snr_sig.d850 = findSNR(raw_sig.d850, spec);  ## processing data
    disp('...done')
    toc


    # calculate original MBLL (raw > BPF > dOD > MBLL) :: 검수완료. 추후 제거 요망
    tic
    disp('...Calculate MBLL without motion/spike removal')
    test_dod.d780 = findDOD(BPF(raw_sig.d780,spec),spec);
    test_dod.d850 = findDOD(BPF(raw_sig.d850,spec),spec);
    [orig_mbll_sig.HbO, orig_mbll_sig.HbR, orig_mbll_sig.HbT] = findMBLL(test_dod,spec);
    disp('...done')
    toc



    # calculate dOD
    tic
    disp('...Calculate dOD')
    dod_sig.d780 = findDOD(raw_sig.d780, spec);  ## dOD 850
    dod_sig.d850 = findDOD(raw_sig.d850, spec);  ## dOD 780
    disp('...done')
    toc


    # motion artifact
    tic
    disp('...Calculate motion artifact removal')
    mdod_sig.d780 = findMDOD(dod_sig.d780, filt_ang_x, filt_ang_z, ths_motion_xyz, spec);
    mdod_sig.d850 = findMDOD(dod_sig.d850, filt_ang_x, filt_ang_z, ths_motion_xyz, spec);
    disp('...done')
    toc


    # BPF
    tic
    disp('...Bandpass filter')
    mdod_sig.d780 = BPF(mdod_sig.d780,spec);
    mdod_sig.d850 = BPF(mdod_sig.d850,spec);
    disp('...done')
    toc


    # spike removal :: 외부 라이브러리임
    tic
    disp('...Calculate spike removal')
    sdod_sig.d780 = deleteSpike(mdod_sig.d780, spec);
    sdod_sig.d850 = deleteSpike(mdod_sig.d850, spec);
    disp('...done')
    toc


    # baseline fit 한번 더...
    tic
    disp('...Set new baseline')
    sdod_sig.d780 = BaselineFit(sdod_sig.d780, spec);
    sdod_sig.d850 = BaselineFit(sdod_sig.d850, spec);
    disp('...done')
    toc


    # MBLL
    tic
    disp('...Calculate MBLL')
    [mbll_sig.HbO, mbll_sig.HbR, mbll_sig.HbT] = findMBLL(sdod_sig, spec);
    disp('...done')
    toc


    # channel rejection decision
    tic
    disp('...Calculate Channel Rejection')
    ch_rej = ChRejection(raw_sig, snr_sig, mbll_sig, spec);
    disp('rejected channels are ... ')
    find(ch_rej==1)
    disp('...done')
    toc


    # MBLL + ch_rej + padding
    tic
    disp('...Apply Channel Rejection and Basic Padding')
    # [p_orig_mbll_sig.HbO, p_orig_mbll_sig.HbR, p_orig_mbll_sig.HbT] = ApplyChRej(orig_mbll_sig, ch_rej);
    # [p_orig_mbll_sig.HbO, p_orig_mbll_sig.HbR, p_orig_mbll_sig.HbT, ~] = paddingCh3(p_orig_mbll_sig, ch_rej, spec);
    [p_mbll_sig.HbO, p_mbll_sig.HbR, p_mbll_sig.HbT] = ApplyChRej(mbll_sig, ch_rej);
    [p_mbll_sig.HbO, p_mbll_sig.HbR, p_mbll_sig.HbT, ch_rej] = paddingCh3(p_mbll_sig, ch_rej);


    disp('...done')
    toc

    # plot output
    if plotflag
        showch = 1:1:48;    # 48개 채널을 보여줄거임
        figure('name','signal')
        m=5;
        n=2;
        mysubfigure(raw_sig.d780,'raw signal d780',m,n,1,showch)
        mysubfigure(raw_sig.d850,'raw signal d850',m,n,2,showch)
        mysubfigure(snr_sig.d780,'snr signal d780',m,n,3,showch)
        mysubfigure(snr_sig.d850,'snr signal d850',m,n,4,showch)
        mysubfigure(dod_sig.d780,'dod signal d780',m,n,5,showch)
        mysubfigure(dod_sig.d850,'dod signal d850',m,n,6,showch)
        mysubfigure(mdod_sig.d780,'mdod signal d780',m,n,7,showch)
        mysubfigure(mdod_sig.d850,'mdod signal d850',m,n,8,showch)
        mysubfigure(sdod_sig.d780,'sdod signal d780',m,n,9,showch)
        mysubfigure(sdod_sig.d850,'sdod signal d850',m,n,10,showch)

        figure('name','MBLL output')
        m=2;
        n=3;
        mysubfigure(orig_mbll_sig.HbO,'original mbll HbO2',m,n,1,showch)
        mysubfigure(orig_mbll_sig.HbR,'original mbll HbR',m,n,2,showch)
        mysubfigure(orig_mbll_sig.HbT,'original mbll HbT',m,n,3,showch)
        mysubfigure(mbll_sig.HbO,'Ch-rejected mbll HbO2',m,n,4,showch)
        mysubfigure(mbll_sig.HbR,'Ch-rejected mbll HbR',m,n,5,showch)
        mysubfigure(mbll_sig.HbT,'Ch-rejected mbll HbT',m,n,6,showch)

        figure('name','MBLL output with channel rejection and padding')
        m=2;
        n=3;
    #     mysubfigure(p_orig_mbll_sig.HbO,'original mbll HbO2',m,n,1,showch)
    #     mysubfigure(p_orig_mbll_sig.HbR,'original mbll HbR',m,n,2,showch)
    #     mysubfigure(p_orig_mbll_sig.HbT,'original mbll HbT',m,n,3,showch)
        mysubfigure(p_mbll_sig.HbO,'Ch-rejected mbll HbO2',m,n,4,showch)
        mysubfigure(p_mbll_sig.HbR,'Ch-rejected mbll HbR',m,n,5,showch)
        mysubfigure(p_mbll_sig.HbT,'Ch-rejected mbll HbT',m,n,6,showch)

        figure('name','Movement')
        plot(filt_ang_x); hold on;
        plot(filt_ang_y); hold on;
        plot(filt_ang_z); hold on;
        legend('X-axis','Y-axis','Z-axis')
        axis tight
    end


    # make output
    output.idnum = id;
    output.task = task_name;
    output.date = date;
    output.name = insig.name;
    output.sex = insig.sex;
    output.age = insig.age;
    output.inspector = insig.inspector;
    output.acc = insig.acc;
    output.rt = insig.rt;
    output.chrej = ch_rej;
    output.timestamp = time_stp;
    output.marker = marker;
    output.move = [filt_ang_x filt_ang_y filt_ang_z];
    output.raw = raw_sig;
    output.snr = snr_sig;
    output.mbll = p_mbll_sig;   # 68ch -> 48ch :: 기본 padding(중앙에 겹치는)만 해서 기본 output으로 내보내기로 함 
    output.orig_mbll = orig_mbll_sig;
    output.taskblock = TaskBlock;

    end
    '''

def serverTransmit(self, output, dataTrans):
    '''
        args* 
        inputsignal,plotflag
    return = 
        inputsignal,plotflag
    example:
    '''
    return server_result

    '''
    function [server_result]=serverTransmit(output,dataTrans)

    # make output
    sout=[];
    sout.idnum = output.idnum;
    sout.task = convertCharsToStrings(output.task);
    sout.date = convertCharsToStrings(num2str(output.date));
    sout.chrej = makestr_list(output.chrej,'#d');
    sout.timestamp = makestr_list(output.timestamp,'#f');
    sout.marker = makestr_list(output.marker,'#d');
    sout.move = makestr_matrix(output.move,'#f');
    sout.raw = makestr_matrices(output.raw,'#f');
    sout.snr = makestr_matrices(output.snr,'#f');
    # # output.dOD = dod_sig;
    # # output.mdOD = mdod_sig;
    # # output.sdOD = sdod_sig;
    sout.mbll = makestr_matrices(output.mbll,'#f');
    sout.orig_mbll = makestr_matrices(output.orig_mbll,'#f');

    if strcmp(output.task, 'REST')
        sout.taskblock = "empty";
    else

        sout.taskblock = makestr_matrix(output.taskblock,'#d');
    end

    sout.name = convertCharsToStrings(num2str(output.name));
    sout.sex = convertCharsToStrings(num2str(output.sex));
    sout.age = convertCharsToStrings(num2str(output.age));
    sout.inspector = convertCharsToStrings(num2str(output.inspector));


    sout.ACC = convertCharsToStrings(num2str(output.acc));
    sout.RT = convertCharsToStrings(num2str(output.rt));

    if dataTrans
        try
            ## RESTful API ==> POST
            URL = 'http://192.168.0.95:8080/api/v1/';
            URLdetail = 'wj/';  # 'tests' : 테스트
            URLall = [URL URLdetail];
            id_str = 'cmlee';
            pw_str = 'ckdals0315';
            # get_potions = weboptions('Username','cmlee','Password','ckdals0315',...
            #     'MediaType','application/json',...
            #     'RequestMethod','get');
            # get_result = webwrite(URLall,data, get_options); # 구조체 형식으로 던짐

            post_potions = weboptions('Username',id_str,'Password',pw_str, ...
                'MediaType','application/json', ...
                'RequestMethod','post');

    #         load exdatastr.mat

            datastr = sout;
    #         save exdatastr.mat datastr
            result = webwrite(URLall,datastr,post_potions);
            disp(result)

            server_result = result;
        catch
            server_result = 'fail';
        end
    else
        server_result = 'transmission is not allowed, change function input(dataTrans)';
    end
    end
    '''


def makestr_matrices(self, inputs, regexpstr):
    '''
    args* 
        inputsignal,plotflag
    return = 
        inputsignal,plotflag
    example:
    '''
    return strout

    '''
    function strout = makestr_matrices(inputs,regexpstr)
    # 필드 내 길이가 모두 같은경우 쓸 수있는 것 :: 안쓰고 싹다 모아서 json으로 넣어버리자 
    cell_inputs = struct2cell(inputs);
    # numElem = size(cell_inputs,1);
    [~,numData] = size(cell_inputs{1});
    mat_inputs = cell2mat(cell_inputs);


    regexpstr_mat = repmat([regexpstr ' '],1, numData);
    regexpstr_mat = regexpstr_mat(1:end-1);
    regexpstr = [regexpstr_mat ','];
    allOneString = sprintf(regexpstr , mat_inputs);
    allOneString = allOneString(1:end-1);   #마지막 ',' 제외
    strout = convertCharsToStrings(allOneString);
    end
    '''

    function strout = makestr_matrix(input,regexpstr)
    # nch x ndata data에 대하여 {#f_1 #f_2 #f_2 ..#f_ndata ,(행간구분자)}
    # d780 204개 먼저, 그다음 d850 204개를 쌓아서 1줄을 만드는 형식
    [~,numData]=size(input);
    regexpstr_mat = repmat([regexpstr ' '],1, numData);
    regexpstr_mat = regexpstr_mat(1:end-1);
    regexpstr = [regexpstr_mat ','];
    allOneString = sprintf(regexpstr , input);
    allOneString = allOneString(1:end-1);   #마지막 ',' 제외
    strout = convertCharsToStrings(allOneString);
    end

    function strout = makestr_list(input,regexpstr)
    # nch x 1 data에 대하여 {#f, ... ,#f} 형태로 나열
    allOneString = sprintf([regexpstr ','] , input);
    allOneString = allOneString(1:end-1);   #마지막 ',' 제외
    strout = convertCharsToStrings(allOneString);
    end



    function mysubfigure(signal,titlestr,m,n,k,showch)
    ## subfigure draw
    subplot(m,n,k)
    if isempty(showch)
        N = 1:1:48;     #size(signal,1);
    else
        N = showch;
    end
    for i= N
        plot(signal(i,:));hold on;
    end
    title(titlestr)
    axis tight
    end

    function [sigout]=BaselineFit(signal, spec)
    ## 특정 시점에 다시 baseline 잡아주는 기능
    nB = round(spec.dOD.nBase * spec.Fs);
    nCh = spec.nch;

    for i=1:1:nCh
        signal(i,:) = signal(i,:) - signal(i,nB);
    end
    sigout = signal;
    end


    function [HbO2, HbR, HbT, RejectCh] = paddingCh3(siginput, RejectCh)
    ## Padding : 중앙 부분만 
    HbO2 = siginput.HbO;
    HbR = siginput.HbR;

    couplech = [1,0; 2,0; 3,0; 4,0; 5,0; 6,49; 7,50; 8,51; 9,0; 10,0; ...
        11,52; 12,53; 13,54; 14,0; 15,0; 16,0; 17,0; 18,0; 19,0; 20,0; ...
        21,55; 22,56; 23,57; 24,58; 25,59; 26,60; 27,61; 28,62; 29,0; 30,0; ...
        31,0; 32,0; 33,0; 34,0; 35,0; 36,63; 37,64; 38,65; 39,0; 40,0; ...
        41,66; 42,67; 43,68; 44,0; 45,0; 46,0; 47,0; 48,0];

    for i = 1 : 48
        if RejectCh(i,1) == 1
            if couplech(i,2) ~= 0
                if RejectCh(couplech(i,2),1) == 0
                    HbO2(i,:) = HbO2(couplech(i,2),:);
                    HbR(i,:) = HbR(couplech(i,2),:);
                    RejectCh(i,1) = 0;
                    RejectCh(couplech(i,2),1) = 1;
                end
            end
        end
    end
    HbT = HbO2 + HbR;
    end

    function [HbO2, HbR, HbT] = paddingCh(siginput, RejectCh)
    ## (old) 최종적으로 rejection 된 채널이 있다면 구역 내 평균으로 처리 하는 것. 
    # 최하단에는 global signal substraction을 넣어두었음. 안쓰면 말고 
    HbO2 = siginput.HbO;
    HbR = siginput.HbR;

    couplech = [1,0; 2,0; 3,0; 4,0; 5,0; 6,49; 7,50; 8,51; 9,0; 10,0; ...
        11,52; 12,53; 13,54; 14,0; 15,0; 16,0; 17,0; 18,0; 19,0; 20,0; ...
        21,55; 22,56; 23,57; 24,58; 25,59; 26,60; 27,61; 28,62; 29,0; 30,0; ...
        31,0; 32,0; 33,0; 34,0; 35,0; 36,63; 37,64; 38,65; 39,0; 40,0; ...
        41,66; 42,67; 43,68; 44,0; 45,0; 46,0; 47,0; 48,0];

    for i = 1 : 48
        if RejectCh(i,1) == 1
            if couplech(i,2) ~= 0
                if RejectCh(couplech(i,2),1) == 0
                    HbO2(i,:) = HbO2(couplech(i,2),:);
                    HbR(i,:) = HbR(couplech(i,2),:);
                    RejectCh(i,1) = 0;
                    RejectCh(couplech(i,2),1) = 1;
                end
            end
        end
    end

    brodmannpadding{1,1} = [1, 2, 3, 5, 6, 11, 17, 18];
    brodmannpadding{2,1} = [4, 9, 10];
    brodmannpadding{3,1} = [7, 8, 12, 13, 21, 22, 25, 26];
    brodmannpadding{4,1} = [14, 15, 16, 29, 30];
    brodmannpadding{5,1} = [19, 20, 33, 34, 35, 38, 39, 43];
    brodmannpadding{6,1} = [40, 44, 45];
    brodmannpadding{7,1} = [23, 24, 27, 28, 36, 37, 41, 42];
    brodmannpadding{8,1} = [31, 32, 46, 47, 48];
    brodmannpadding{9,1} = [brodmannpadding{1,1} ...    
                            brodmannpadding{2,1} ...
                            brodmannpadding{3,1} ...
                            brodmannpadding{4,1}];
    brodmannpadding{10,1} = [brodmannpadding{1,1} ...
                            brodmannpadding{2,1} ...
                            brodmannpadding{3,1} ...
                            brodmannpadding{4,1}];
    brodmannpadding{11,1} = 1:48;


    avgHbO = zeros(size(HbO2));
    avgHbR = zeros(size(HbO2));
    outHbO = zeros(11,size(HbO2,2));
    outHbR = zeros(11,size(HbO2,2));
    for bp = 1 : 11
        t = 1;
        for i = brodmannpadding{bp,1}
            if RejectCh(i,1) == 0
                avgHbO(t,:) = HbO2(i,:);
                avgHbR(t,:) = HbR(i,:);
                t = t + 1;
            end
        end
        if t>1  # 없는 채널이 1개 이상일 경우
            if t==2
                avgHbOs = avgHbO(1,:);
                avgHbRs = avgHbR(1,:);
            else
                avgHbOs = mean(avgHbO(1:t-1,:),1);
                avgHbRs = mean(avgHbR(1:t-1,:),1);
            end
            outHbO(i,:) = avgHbOs;
            outHbR(i,:) = avgHbRs;
        else
            # 해당 영역에 통과하는 값이 하나도 없는 경우.. 
            # 일단 zeros 그대로 두자 
        end
    end



    # global signal substraction : GSS
    if spec.GSS
        BrodmanAvgHbO2 = cell(8,1);
        BrodmanAvgHbR = cell(8,1);
        t = 1;
        for bp = 1 : 8
            for i = brodmannpadding{bp,1}
                BrodmanAvgHbO2{bp,1}(t,:) = HbO2(i,:);
                BrodmanAvgHbR{bp,1}(t,:) = HbR(i,:);
                t = t + 1;
            end
            t = 1;
        end

        MeanHbO2 = zeros(size(HbO2));
        MeanHbR = zeros(size(HbR));
        for bp = 1 : 8
            MeanHbO2(bp,:) = mean(BrodmanAvgHbO2{bp,1}(:,:));
            MeanHbR(bp,:) = mean(BrodmanAvgHbR{bp,1}(:,:));
        end
        for bp = 1 : 8
            for i = brodmannpadding{bp,1}
                HbO2(i,:) = HbO2(i,:) - MeanHbO2(bp,:);
                HbR(i,:) = HbR(i,:) - MeanHbR(bp,:);
            end
        end
    end

    HbT = HbO2 + HbR;
    end

    function [HbO, HbR, HbT] = ApplyChRej(sig, ch_rej)
    ## Channel Rejection 적용 하는 부분
    HbO = sig.HbO;
    HbR = sig.HbR;
    HbT = sig.HbT;

    for i=1:1:size(ch_rej,1)
        if ch_rej(i)
            HbO(i,:)=0;
            HbR(i,:)=0;
            HbT(i,:)=0;
        end
    end
    end

    function [RejectedCh] = ChRejection(inputRAW, inputSNR, inputMBLL, spec)
    ## SNR-based Channel rejection : 빼야할 것 자동화
    nch = spec.nch;
    ndata = spec.ndata;

    start = round(spec.dOD.nBase * spec.Fs);

    rd7 = inputRAW.d780(1:nch,:);
    rd8 = inputRAW.d850(1:nch,:);
    sd7 = inputSNR.d780(1:nch,:);
    sd8 = inputSNR.d850(1:nch,:);
    hbo = inputMBLL.HbO(1:nch,start+1:end-1);
    hbr = inputMBLL.HbR(1:nch,start+1:end-1);


    # 다 0인경우
    reject1 = sum(rd7,2)==0 | sum(rd8,2)==0;


    # raw에서 한번이라도 음수로 떨어지는 경우
    reject2 = sum(rd7<0,2) | sum(rd8<0,2);


    # SNR threshold 값과
    SNRthd = spec.SNRthd;
    ZSCRthd = spec.ZSCRthd;
    zscore_780 = zeros(nch,1);
    zscore_850 = zeros(nch,1);
    for i=1:1:nch
        zscore_780(i) = sum((sd7(i,:)<=SNRthd).*abs(sd7(i,:) - mean(sd7,1))./std(sd7,1))/ndata;
        zscore_850(i) = sum((sd7(i,:)<=SNRthd).*abs(sd8(i,:) - mean(sd8,1))./std(sd8,1))/ndata;
    end
    reject3 = zscore_780 > ZSCRthd | zscore_850 > ZSCRthd;


    # 다 nan인경우
    reject4 = isnan(sum(rd7,2)) | isnan(sum(rd8,2));


    # MBLL이 차이가 심한 경우
    ZSCRthd2 = spec.ZSCRthd2;
    zscore_hbo = zeros(nch,1);
    zscore_hbr = zeros(nch,1);

    for i=1:1:nch
        zscore_hbo(i) = sum( abs(hbo(i,:) - mean(hbo,1))./std(hbo,1) )/ndata;
        zscore_hbr(i) = sum( abs(hbr(i,:) - mean(hbr,1))./std(hbr,1) )/ndata;
    end
    reject5 = zscore_hbo > ZSCRthd2 | zscore_hbr > ZSCRthd2;

    # MBLL이 다 0으로 나온 경우
    reject6 = sum(hbo,2)==0 | sum(hbr,2)==0;


    # rejection all
    RejectedCh = reject1 | reject2 | reject3 | reject4 | reject5 | reject6;
    end


    function [dOD_Spline_SG] = deleteSpike(input,spec)
    ## spike removal
    dod = input';
    fs = spec.Fs;

    iqr = 1.5;
    SNR_Thre = zeros(1,size(dod,2));
    FrameSize_sec = 10;
    wd =10;
    sp_factor = 0.1;

    for ww = 1:size(dod,2)
        clearvars -except ww d ml fs t dod tMotion SD dodorg p iqr SNR_Thre SNR_Thre2 FrameSize_sec dataSet wd sp_factor
        s1 =  dod(:,ww) ;
        [s1,~] = hmrBandpassFilt( s1, fs, 0, 2);
        [s2,~] = hmrBandpassFilt( s1, fs, 0, 0.5);

        ## detecting outliers in std variations of the signal
        tMotion=1;
        Win_Size=round(fs*tMotion);
        Sigstd = zeros(length(s1)-(Win_Size),1);
        for ilent=1:length(s1)-(Win_Size)
            Sigstd(ilent,1)=std(s2(ilent:ilent+(Win_Size),:));
        end
        iqr2 = 2;
        quants_std = quantile(Sigstd,[.25 .50 .75]);  # compute quantiles
        IQR_std = quants_std(3)-quants_std(1);  # compute interquartile range
        High_std = quants_std(3)+IQR_std*iqr2;
        Low_std = quants_std(1)-IQR_std*iqr2;

        ## detecting outliers in gradient of the signal
        grad = conv(s1,[-1,0,1]); # Sobel mask
        quants = quantile(grad,[.25 .50 .75]);  # compute quantiles
        IQR1 = quants(3)-quants(1);  # compute interquartile range
        High = quants(3)+IQR1*iqr;
        Low = quants(1)-IQR1*iqr;


        z_std=0;
        M_std = zeros(length(dod)-(Win_Size),1);
        for i=1:length(dod)-(Win_Size)
            if ((Sigstd(i)>High_std) || (Sigstd(i)<Low_std))
                z_std=z_std+1; M_std(z_std)=i;
            end
        end
        M_std(z_std+1:end,:)=[];

        if exist('M_std','var')
            M_std=round(Win_Size/2)+M_std;
        end

        z=0;
        M_sobel = zeros(length(dod),1);
        for i=1:length(dod)
            if ((grad(i)>High) || (grad(i)<Low))
                z=z+1; M_sobel(z)=i;
            end
        end
        M_sobel(z+1:end,:)=[];

        if exist('M_sobel','var') && exist('M_std','var')
            M=union(M_sobel,M_std);
        else
            if exist('M_sobel','var')
                M=M_sobel;
            else
                if exist('M_std','var')
                    M=M_std;
                end
            end
        end
        extend = round(12*fs);
        s11=repmat(s1(1,:),extend,1);s12=repmat(s1(end,:),extend,1);
        s1temp=[s11;s1;s12]; # extending signal for motion detection purpose (12 sec from each edge)
        s1=s1temp;

        t=(0:(1/fs):(length(s1)/fs))';
        t=t(1:length(s1),1);
        if ww==1
            #prelocation
            tInc = zeros(length(t),size(dod,2));
        end

        if exist('M','var')
            M=M+extend;
            sig=ones(length(s1),1);
            for i=1:length(M)
                sig(M(i),:)=0;
            end

            ### finding the location of the spikes or baseline shifts
            temp = (diff(sig));

            c=0;
            meanpL = zeros(length(s1)-1,1);
            meanpH = zeros(length(s1)-1,1);
            for i=1:length(s1)-1
                if (temp(i)==1)
                    c=c+1;
                    meanpL(c)=mean(s1(i),1);
                    meanpH(c)=mean(s1(i),1);
                end
            end
            meanpL(c+1:end,:)=[];
            meanpH(c+1:end,:)=[];
            motionkind=abs(meanpH-meanpL);

            ## finding the baseline shifts by comparing motion amplitudes with heart rate amplitude
            stemp=s1;
            [s1,~] = hmrBandpassFilt( stemp, fs, 0, 2 );
            snoise2=stemp;
            zz=0;tt=1;
            sigtemp = cell(1,length(s1)-1);
            sigtempnoise = cell(1,length(s1)-1);
            for i=1:length(s1)-1
                if (sig(i)==1)
                    zz=zz+1;
                    sigtemp{1,tt}(1,zz)=s1(i);
                    sigtempnoise{1,tt}(1,zz)=snoise2(i);
                    if ((sig(i)==1) && (sig(i+1)==0))
                        tt=tt+1;
                        zz=0;
                    end
                end
            end

            Nthre=round(0.5*fs);ssttdd=0;
            for i=1:tt
                tempo=sigtemp{1,i};
                if length(tempo)>Nthre
                    tempo2 = zeros(1,length(tempo)-Nthre);
                    for l=1:length(tempo)-Nthre
                        tempo2(l)=(abs(tempo(l+Nthre)-tempo(l)));
                    end
                end
                ssttdd=[ssttdd tempo2];
                clear tempo2
                tempo2=[];
            end

            thrshld = quantile(ssttdd,0.5);
            pointS = (find(temp<0));
            pointE = (find(temp>0));
            countnoise = 0;
            SNR_Thresh = zeros(length(sigtempnoise),1);
            for ks=1:length(sigtempnoise)
                if (length(sigtempnoise{1,ks})>3*fs)
                    countnoise = countnoise+1;
                    dmean = mean(sigtempnoise{1,ks},2);
                    dstd = std(sigtempnoise{1,ks},[],2);
                    SNR_Thresh(countnoise,1) = abs(dmean)./(dstd+eps);
                end
            end
            SNR_Thresh(countnoise+1:end,:)=[];
            SNR_Thre(1,ww)=mean(SNR_Thresh(2:end-1,1));

            sig2=ones(length(s1),1);
            for i=1:length(pointS)
                if motionkind(i)>thrshld
                    sig2(pointS(i):pointE(i),:)=0;
                end
                # # # # # # # # # # # # # # # # # #
                # spline on long duration spikes  #
                # # # # # # # # # # # # # # # # # #

                if (((pointE(i)-pointS(i))> (0.1*fs))&&((pointE(i)-pointS(i))< (0.49999*fs)))
                    sig2(pointS(i):pointE(i),:)=0;
                end
                if (pointE(i)-pointS(i))> (fs)
                    sig2(pointS(i):pointE(i),:)=0;
                end
            end
            clear pointS
            clear pointE
            clear sig
            clear temp

            tInc(:,ww)=sig2;
        else
            tInc(:,ww)=ones(length(t),1);
        end
    end

    ## Extracting the noisy channels from baseline-shift motion correction precedure
    for w=1:(size(SNR_Thre,2))
        if isnan(SNR_Thre(1,w)) || isempty(SNR_Thre(1,w)) || (SNR_Thre(1,w)==0)
            dmean = mean(dod(:,w));
            dstd = std(dod(:,w));
            SNR_Thre(1,w)=abs(dmean)./dstd;
        end
    end

    SNRvalue=3;
    for i = 1:size(SNR_Thre,2)
        if SNR_Thre(i) < SNRvalue || isnan(SNR_Thre(i))
            tInc(:,i) = ones(size(tInc,1),1);
        end
    end
    tIncCh=tInc(extend+1:end-extend,:);

    extend = round(12*fs);

    tIncCh1=repmat(tIncCh(1,:),extend,1);
    tIncCh2=repmat(tIncCh(end,:),extend,1);
    tIncCh=[tIncCh1;tIncCh;tIncCh2];

    d1=repmat(dod(1,:),extend,1);
    d2=repmat(dod(end,:),extend,1);
    dod=[d1;dod;d2];



    [dodLP,~] = hmrBandpassFilt( dod, fs, 0, 2 );

    ## Spline Interpolation


    n_data = length(dodLP);
    dODspline = zeros(size(dod,2),n_data);
    for k = 1:size(dod,2)
        MA_segment= zeros(1,n_data);
        dOD = dodLP(:,k)';
        Thrs_MA = tIncCh(:,k);
        for i = 1:n_data-2*wd
            if Thrs_MA(i) == 0
                MA_segment(i:i+2*wd) = 1;
            end
            MA_segment(1) = 0;
            MA_segment(end) = 0;
        end

        Gyro_MA_sf = diff(MA_segment);
        if isempty(find(Gyro_MA_sf, 1)) == 0
            s_pt = find(Gyro_MA_sf ==1);
            f_pt = find(Gyro_MA_sf == -1);
            for i = 1:length(s_pt)
                spline = csaps(1:(f_pt(i)-s_pt(i)+1),dOD(1,s_pt(i):f_pt(i)),sp_factor,1:(f_pt(i)-s_pt(i)+1));
                Offset_spline = [zeros(1,s_pt(i)-1) (spline-spline(1)) ones(1,n_data - f_pt(i))*(spline(end)-spline(1))];
                dOD(1,:) = dOD(1,:) - Offset_spline;
            end
            dODspline(k,:) = dOD;
        else
            dODspline(k,:) = dOD;
        end

    end

    dODspline = dODspline';
    dod=dODspline(extend+1:end-extend,:); # removing the extention

    ## Savitzky_Golay filter
    K = 3; # polynomial order
    FrameSize_sec = round(FrameSize_sec * fs);
    if mod(FrameSize_sec,2)==0
        FrameSize_sec = FrameSize_sec  + 1;
    end

    dod2=sgolayfilt(dod,K,FrameSize_sec);

    dOD_Spline_SG = dod2';
    end


    function [z]=findCoeff(loadDetailParams, spec)
    ## Coefficient decision
    # MBLL에 사용되는 각종 상수에 대한 결정.
    # 고정값을 사용하던가, 저장정보를 불러오던가

    # 파장별 coeff. search
    index_distance = [68; 120; 156; 204];

    r = [1.5 2.12 3 3.35];
    DPF_780 = 5.075;
    DPF_850 = 4.640;

    if ~loadDetailParams
        ## 고정된 세팅을 사용하는 경우
        Extinction_coef = 1/0.4343 *[0.763 1.066; 1.097 0.781];
        # mM^-1 * cm^-1 { -1.362 1.859 }, { 1.913, -1.330 }

        inv_extinc = inv(Extinction_coef);

        outmat3 = [ 1:204; repmat([inv_extinc(1,:)'; inv_extinc(2,:)'],1,204) ]';
    else
        ## 기기별 차이를 반영하여 필요한 경우 호출해서 사용하는 경우
        [filen, pathn] = uigetfile({'*.txt'}, 'Select the absorption parameter.','C:\Users\obelab\Documents\카카오톡 받은 파일');
        LD_wavelength = load(strcat(pathn,filen));

        LD_Channel = load('LD_Channel.mat','LD_Channel');
        Absorp = load('absorption_spectrum_HbO_HbR_V2.txt');
        Wavelength = cell(24,1);

        for i = 1 : 24
            for j = 1 : 151
                if mod(round(LD_wavelength(i,2)),2) == 0
                    wl_780 = round(LD_wavelength(i,2));
                else
                    wl_780 = round(LD_wavelength(i,2))+1;
                end
                if mod(round(LD_wavelength(i,3)),2) == 0
                    wl_850 = round(LD_wavelength(i,3));
                else
                    wl_850 = round(LD_wavelength(i,3))+1;
                end
                if Absorp(j,1) == wl_780
                    Wavelength{i,1}(1,1) = Absorp(j,2);
                    Wavelength{i,1}(2,1) = Absorp(j,3);
                end
                if Absorp(j,1) == wl_850
                    Wavelength{i,1}(1,2) = Absorp(j,2);
                    Wavelength{i,1}(2,2) = Absorp(j,3);
                end
            end
        end

        Extinction_coef = cell(24,1);
        for i = 1 : 24
            Extinction_coef{i,1} = 1/0.4343 * Wavelength{i,1};
        end

        inv_extin = cell(24,1);
        for i = 1 : 24
            inv_extin{i,1} = inv(Extinction_coef{i,1});
        end


        outmat=zeros(204,7);
        for m = 1 : 24
            for p = 1 : length(LD_Channel{m,1})
                k = LD_Channel{m,1}(p,1);
                outmat(i,:)=[m p k inv_extin{m,1}(1,:) inv_extin{m,1}(2,:)];
            end
        end

        outmat2 = outmat(:,3:end);
        [~,ind] = sort(outmat2(:,1),'ascend');
        outmat3 = outmat2(ind,:);
    end

    outmat3 = [outmat3 zeros(size(outmat3,1),3)];

    outmat3(1:index_distance(1),end-2:end) = repmat([r(3), DPF_780 DPF_850], index_distance(1), 1);
    outmat3(index_distance(1)+1:index_distance(2),end-2:end) = repmat([r(1), DPF_780 DPF_850], index_distance(2)-index_distance(1), 1);
    outmat3(index_distance(2)+1:index_distance(3),end-2:end) = repmat([r(2), DPF_780 DPF_850], index_distance(3)-index_distance(2), 1);
    outmat3(index_distance(3)+1:index_distance(4),end-2:end) = repmat([r(4), DPF_780 DPF_850], index_distance(4)-index_distance(3), 1);

    spec.chind = outmat3(:,1);
    spec.inv_extinc = [outmat3(:,2:3) outmat3(:,4:5)];
    spec.r = outmat3(:,6);
    spec.DPF_780 = outmat3(:,7);
    spec.DPF_850 = outmat3(:,8);

    z = spec;
    end


def findMBLL(self, input, spec):
    import math
    import numpy as np
    '''
    args*=
        input, spec
    return=
        [HbO2, HbR, HbT]
    '''
    bpf_D780 = input.d780;
    bpf_D850 = input.d850;

    # bpf_D780(:,1)=0;
    # bpf_D850(:,1)=0;

    bpf_D780.index[0]=0;
    bpf_D850.index[0]=0;

    ## get constants and calculate MBLL
    r = spec.r     ## 채널간 거리에 따라서 달라지는 ::
    DPF_780 = spec.DPF_780
    DPF_850 = spec.DPF_850
    inv_extinc = spec.inv_extinc
    nCh = spec.nch

    HbO2 = np.zeros(bpf_D780)
    HbR = np.zeros(bpf_D780)

    for i in range(nCh):
        bpf_D780[i] = np.divide(bpf_D780, (r[i] * DPF_780[i]))
        bpf_D850[i] = np.divide(bpf_D850, (r[i] * DPF_850[i]))

        HbO2 = inv_extinc*[bpf_D780; bpf_D850]
        HbR = inv_extinc*[bpf_D780; bpf_D850]

    # row가 nan인 줄을 없애기 위해
    math.isnan(HbO2)=0
    math.isnan(HbR)=0

    # calculate HbT
    HbT = HbO2 + HbR

    # unit에 따른 변화 필요시 적용
    if spec.concunit:
        HbO2 = HbO2 .* 1000
        HbR = HbR .* 1000
        HbT = HbT .* 1000

    return [HbO2, HbR, HbT]
'''
    function [HbO2, HbR, HbT] = findMBLL(input, spec)
    ## calculate MBLL
    # inputs must be after bandpassfilter
    bpf_D780 = input.d780;
    bpf_D850 = input.d850;

    bpf_D780(:,1)=0;
    bpf_D850(:,1)=0;

    ## get constants and calculate MBLL
    r = spec.r;     ## 채널간 거리에 따라서 달라지는 ::
    DPF_780 = spec.DPF_780;
    DPF_850 = spec.DPF_850;
    inv_extinc = spec.inv_extinc;
    nCh = spec.nch;

    HbO2 = zeros(size(bpf_D780));
    HbR = zeros(size(bpf_D780));

    for i = 1 : nCh
        bpf_D780(i,:) = bpf_D780(i,:)./(r(i) * DPF_780(i));
        bpf_D850(i,:) = bpf_D850(i,:)./(r(i) * DPF_850(i));

        HbO2(i,:) = inv_extinc(i,1:2)*[bpf_D780(i,:); bpf_D850(i,:)];
        HbR(i,:) = inv_extinc(i,3:4)*[bpf_D780(i,:); bpf_D850(i,:)];
    end

    # row가 nan인 줄을 없애기 위해
    HbO2(isnan(HbO2))=0;
    HbR(isnan(HbR))=0;

    # calculate HbT
    HbT = HbO2 + HbR;

    # unit에 따른 변화 필요시 적용
    if spec.concunit
        HbO2 = HbO2 .* 1000;
        HbR = HbR .* 1000;
        HbT = HbT .* 1000;
    end
    end
    '''

def funcname(self, input, spec):

    
    raise NotImplementedError
    function [dOD] = findDOD(input,spec)
    ## Calculate dOD
    Fs = spec.Fs
    # ndata = spec.ndata;
    nCh = spec.nch

    demod_data = input

    for i in range(nCh):
        if min(demod_data(i,:)) <= 0
            demod_data(i,:) = 0.1
        end
    end
    demod_data_ini = zeros(size(demod_data))
    dOD = zeros(size(demod_data))

    # baseline 연산
    baselines = spec.dOD.sBase
    baselinef = spec.dOD.eBase
    for i in range(nCh):
        demod_data_ini(i) = mean(demod_data(i, round(baselines * Fs)+1 : round(baselinef * Fs)));
    

    # dOD 연산
    for i in range(nCh):
        dOD(i,:) = -log(demod_data(i,:)/demod_data_ini(i));
    

    # take only real value
    dOD = real(dOD);
    return [dOD]

    '''
    function [dOD] = findDOD(input,spec)
    ## Calculate dOD
    Fs = spec.Fs;
    # ndata = spec.ndata;
    nCh = spec.nch;

    demod_data = input;
    for i = 1 : nCh
        if min(demod_data(i,:)) <= 0
            demod_data(i,:) = 0.1;
        end
    end
    demod_data_ini = zeros(size(demod_data));
    dOD = zeros(size(demod_data));

    # baseline 연산
    baselines = spec.dOD.sBase;
    baselinef = spec.dOD.eBase;
    for i = 1 : nCh
        demod_data_ini(i) = mean(demod_data(i, round(baselines * Fs)+1 : round(baselinef * Fs)));
    end

    # dOD 연산
    for i = 1 : nCh
        dOD(i,:) = -log(demod_data(i,:)/demod_data_ini(i));
    end

    # take only real value
    dOD = real(dOD);
    end
    '''

    function [mdOD] = findMDOD(MAR_dOD, filt_ang_x, filt_ang_z, ths_motion_xyz, spec)
    ## calculate motion corrected dOD from normal dOD
    # Motion corrected dOD
    Xcorr_Thre = spec.dOD.Xcorrthr;
    spline_window = spec.dOD.Spkwin;
    ch_num = spec.nch;
    ch_reject = spec.chrej;
    nCh = spec.nch;

    [Cos_angle_Rx,Cos_angle_Lx,Cos_angle_z] = featuresFromIMU(filt_ang_x, filt_ang_z, spec);
    [env_Rx_filt, env_Lx_filt, env_z_filt] = env_det_gyro(Cos_angle_Rx, Cos_angle_Lx, Cos_angle_z, spec);
    MAR_OD_R_flag = XcorrOD_Motion_sensor(env_z_filt, env_Lx_filt, env_Rx_filt, MAR_dOD, spec);
    MAR_OD_R_flag = MAR_OD_R_flag > Xcorr_Thre;

    MAR_OD_GLM = zeros(size(MAR_dOD));

    for i = 1: ch_num
        if ch_reject(i) == 0
            if MAR_OD_R_flag(i) == 1
                GLM_X = [env_z_filt; env_Lx_filt; env_Rx_filt];
                mdl_GLM = fitglm(GLM_X', MAR_dOD(i,:));
                MAR_OD_GLM(i,:) = mdl_GLM.Residuals.Raw';
            else
                MAR_OD_GLM(i,:) = MAR_dOD(i,:);
            end
        else
            MAR_OD_GLM(i,:) = MAR_dOD(i,:);
        end
    end

    [dODspline, ~] = GyroMotionCorrectSpline(MAR_OD_GLM, ths_motion_xyz, spline_window, 0.1, spec);
    dODspline(:,1) = 0;
    baselines = spec.dOD.sBase;
    baselinef = spec.dOD.eBase;

    dODspline_ini = zeros(nCh,1);
    for i = 1 : nCh
        dODspline_ini(i) = mean(dODspline(i, round(baselines * spec.Fs)+1 : round(baselinef * spec.Fs)));
    end

    dOD = zeros(size(MAR_dOD));
    for i = 1 : nCh
        dOD(i,:) = dODspline(i,:)-dODspline_ini(i);
    end
    mdOD = dOD;
    end

    function [z] = findSNR(input,spec)
    ## Calculate SNR map (t sec x n ch)
    # first. BPF
    filtered_raw = BPF(input, spec);

    winsize = round(10 * spec.Fs);  #10초
    [numch,numframe] = size(input);

    # second. calculate SNR
    outmat = zeros(size(input));
    for i = 1:numch     ## for each channel
        for ii = 1:winsize:numframe  ## moving window : 너무 느려서 띄엄띄엄하게 하도록 함
            if ii <= numframe-winsize
                sig = filtered_raw(i, ii:ii+winsize);
                outmat(i,ii:ii+winsize-1) = real( 20 * log10( mean(sig)/std(sig) ) );
            else
                # 끝부분은 그냥 패딩
                outmat(i,ii:end) = outmat(i,numframe-winsize);
            end
        end
    end

    z = outmat;
    end


    function [z] = BPF(input,spec)
    ## band-pass filter
    n_length = spec.ndata;
    fs = spec.Fs;

    # LPF setting
    Target_h = spec.BPF(1);
    cut_index_h = round(Target_h/(1/(2*n_length*1/fs)));
    zero_padding_h = zeros(1,(n_length - cut_index_h));

    # HPF setting
    Target_f = spec.BPF(2);
    cut_index = round(Target_f/(1/(2*n_length*1/fs)));
    zero_padding = zeros(1, cut_index);

    # ch별 BPF
    for i = 1 : size(input,1)
        #LPF
        X_value = dct(input(i,:));
        Y_value = idct([X_value(1, 1:cut_index_h) zero_padding_h]);

        # HPF
        avg_value = mean(Y_value);
        X_value = dct(Y_value);
        Z_value = idct([zero_padding X_value(cut_index+1:n_length)]);

        input(i,:) = (Z_value  + avg_value);
    end

    ### GLM에서 내가 쓴 코드
    # f2 = spec.BPF(1);
    # f1 = spec.BPF(2);
    # fs = spec.Fs;
    # size(input)
    # [b,a] = butter(4,[f1/(fs/2) f2/(fs/2)]); # Butterworth filter of order 6
    # for k=1:1:size(input,1)      ## for each channel
    #     inputGLM_channel = input(k,:)';
    #     filteredOne = filter(b,a,inputGLM_channel); # Will be the filtered signal
    #     input(k,:) = filteredOne(:);
    # end

    z = input;
    end



    function [z1,z2,z3,z4,z5,z6] = degreeFromIMU(Accel,Gyro,spec)
    ## Degree angle & MAR windowing
    Fs = spec.Fs;
    n_data = spec.ndata;
    Thrs_gyro = spec.dOD.Gyrothr;
    Thrs_accel = spec.dOD.Accthr;
    FS_SEL = 131;
    alpha = 0.96;

    if Accel(1,1) == 0 || Gyro(1,1) == 0
        Accel(1,:) = Accel(2,:);
        Gyro(1,:) = Gyro(2,:);
    end
    Accel_conv = 16384;

    accel_x = Accel(:,1)/Accel_conv;
    accel_y = Accel(:,2)/Accel_conv;
    accel_z = Accel(:,3)/Accel_conv;

    gyro_x = Gyro(:,1);
    gyro_y = Gyro(:,2);
    gyro_z = Gyro(:,3);

    ## gyro processing
    base_accel_x = 0;
    base_accel_y = 0;
    base_accel_z = 0;
    for i = 1:10
        base_accel_x = base_accel_x + atand(accel_z(i) / accel_y(i));
        base_accel_y = base_accel_y + atand((((accel_x(i)^2 + accel_y(i)^2))^(1/2)) / accel_z(i));
        base_accel_z = base_accel_z + atand(accel_x(i) / ((accel_y(i)^2 + accel_z(i)^2)^(1/2)));
    end

    base_gyro_x = sum(gyro_x(1:10))/10;
    base_gyro_y = sum(gyro_y(1:10))/10;
    base_gyro_z = sum(gyro_z(1:10))/10;

    base_accel_x = base_accel_x/10;
    base_accel_y = base_accel_y/10;
    base_accel_z = base_accel_z/10;

    base_gyro_x = base_gyro_x/10;
    base_gyro_y = base_gyro_y/10;
    base_gyro_z = base_gyro_z/10;

    last_x_angle = 0;
    last_y_angle = 0;
    last_z_angle = 0;

    gyro_x_conv = zeros(n_data,1); accel_angle_x = gyro_x_conv; gyro_angle_x = gyro_x_conv; filtered_angle_x = gyro_x_conv;
    gyro_y_conv = zeros(n_data,1); accel_angle_y = gyro_y_conv; gyro_angle_y = gyro_y_conv; filtered_angle_y = gyro_y_conv;
    gyro_z_conv = zeros(n_data,1); accel_angle_z = gyro_z_conv; gyro_angle_z = gyro_z_conv; filtered_angle_z = gyro_z_conv;

    for i = 1 : n_data
        gyro_x_conv(i) = (gyro_x(i) - base_gyro_x) / FS_SEL;
        gyro_y_conv(i) = (gyro_y(i) - base_gyro_y) / FS_SEL;
        gyro_z_conv(i) = (gyro_z(i) - base_gyro_z) / FS_SEL;

        accel_angle_x(i) = -atand(accel_z(i) / accel_y(i))- base_accel_x;
        accel_angle_y(i) = atand((accel_x(i)^2 + accel_y(i)^2)^(1/2) / accel_z(i)) - base_accel_y;
        accel_angle_z(i) = atand(accel_x(i) / (accel_y(i)^2 + accel_z(i)^2)^(1/2)) - base_accel_z;

        gyro_angle_x(i) = gyro_x_conv(i) * 1/Fs + last_x_angle;
        gyro_angle_y(i) = gyro_y_conv(i) * 1/Fs + last_y_angle;
        gyro_angle_z(i) = gyro_z_conv(i) * 1/Fs + last_z_angle;

        filtered_angle_x(i) = alpha * gyro_angle_x(i) + (1.0 - alpha) * accel_angle_x(i);
        filtered_angle_y(i) = alpha * gyro_angle_y(i);
        filtered_angle_z(i) = alpha * gyro_angle_z(i) + (1.0 - alpha) * accel_angle_z(i);

        last_x_angle = filtered_angle_x(i);
        last_y_angle = filtered_angle_y(i);
        last_z_angle = filtered_angle_z(i);
    end

    rest_start = ceil(10/Fs);
    rest_stop = ceil(15/Fs);
    rest_mean_filtered_x = mean(filtered_angle_x(rest_start:rest_stop));
    rest_mean_filtered_y = mean(filtered_angle_y(rest_start:rest_stop));
    rest_mean_filtered_z = mean(filtered_angle_z(rest_start:rest_stop));

    cal_filtered_angle_x = filtered_angle_x - rest_mean_filtered_x;
    cal_filtered_angle_y = filtered_angle_y - rest_mean_filtered_y;
    cal_filtered_angle_z = filtered_angle_z - rest_mean_filtered_z;

    # normalization for calculate Thrs
    Accel_xyz =  [diff(sqrt(accel_x.^2+accel_y.^2+accel_z.^2)); 0];
    Accel_xyz = abs(Accel_xyz')/max(Accel_xyz);
    Gyro_xyz =  sqrt(gyro_x_conv.^2+gyro_y_conv.^2+gyro_z_conv.^2);
    Gyro_xyz = abs(Gyro_xyz)/max(Gyro_xyz);

    # calculate Thrs (Accel, Gyro, Motion)
    Thrs_Accel_xyz = exp(Accel_xyz) > Thrs_accel;
    Thrs_Gyro_xyz = exp(Gyro_xyz) > Thrs_gyro;
    Thrs_Motion_xyz = or(Thrs_Accel_xyz, Thrs_Gyro_xyz);

    # output
    z1=cal_filtered_angle_x;
    z2=cal_filtered_angle_y;
    z3=cal_filtered_angle_z;
    z4=Thrs_Motion_xyz;
    z5=Thrs_Gyro_xyz;
    z6=Thrs_Accel_xyz;
    end


    function [z1,z2,z3] = featuresFromIMU(angle_x, angle_z,spec)
    ## MAR feature processing
    # angle_x  = calc_filtered_angle_x
    # angle_z  = calc_filtered_angle_z

    # KJM 추가
    n_data = spec.ndata;
    movN = 8;

    angle_z = MovAvgFilter(movN,angle_z);
    angle_x = MovAvgFilter(movN,angle_x);

    Cos_angle_z=zeros(size(angle_z));
    Cos_angle_x=zeros(size(angle_x));

    for i = 1: length(angle_z)
        if angle_z(i) > 0
            Cos_angle_z(i) = -(1-cosd(angle_z(i)))';
        else
            Cos_angle_z(i) = (1-cosd(angle_z(i)))';
        end
    end
    for i = 1: length(angle_x)
        if angle_x(i) > 0
            Cos_angle_x(i) = -(1-cosd(angle_x(i)))';
        else
            Cos_angle_x(i) = (1-cosd(angle_x(i)))';
        end
    end

    Cos_angle_Rx=zeros(size(Cos_angle_x));
    Cos_angle_Lx=zeros(size(Cos_angle_x));

    for i = 1: n_data
        if Cos_angle_x(i) > 0
            Cos_angle_Rx(i) = Cos_angle_x(i);
            Cos_angle_Lx(i) = 0;
        else
            Cos_angle_Rx(i) = 0;
            Cos_angle_Lx(i) = Cos_angle_x(i);
        end
    end

    z1=Cos_angle_Rx;
    z2=Cos_angle_Lx;
    z3=Cos_angle_z;
    end


    function [z1,z2,z3] = env_det_gyro(Cos_angle_Rx, Cos_angle_Lx, Cos_angle_z,spec)
    ## Gyro envelope detection & LPF processing (GLM features) # KJM 추가
    env_n = spec.dOD.Envwin;
    env_Rx = env_det_Max(Cos_angle_Rx, env_n, env_n);
    env_Lx = env_det_Min(Cos_angle_Lx, env_n, env_n);
    env_z = env_det(Cos_angle_z, env_n, env_n);

    env_Rx_filt = Gyro_filter_GLM(env_Rx);
    env_Lx_filt = Gyro_filter_GLM(env_Lx);
    env_z_filt = Gyro_filter_GLM(env_z);

    z1=env_Rx_filt;
    z2=env_Lx_filt;
    z3=env_z_filt;
    end
    function [out] =env_det(X,n1, n2)
    xMin = movmin(X,[n1,n1]);
    out = movmax(xMin,[n2,n2]);
    end
    function [out] =env_det_Max(X,n1, n2)
    xMax = movmax(X,[n1,n1]);
    out = movmin(xMax,[n2,n2]);
    end
    function [out] =env_det_Min(X,n1, n2)
    xMin = movmin(X,[n1,n1]);
    out = movmax(xMin,[n2,n2]);
    end

    function avg = MovAvgFilter(n, x)

    xbuf = x(1) * ones(n, 1);
    avg = zeros(length(x),1);
    for i = 1 : length(x)
       for m = 1 : n-1
           xbuf(m) = xbuf(m+1);
       end
       xbuf(n) = x(i);

       avg(i) = sum(xbuf) / n;
    end
    end

    function [filt_gyro] = Gyro_filter_GLM(env_gyro)  # KJM 추가
    ## Gyro Env smoothing
    Tau = 5;
    Delay = 0;

    filt_a = -exp(-1/(Tau));
    filt_b = 1-filt_a;
    filt_gyro = zeros(1,length(env_gyro)-Delay-1);

    for i = 2:length(env_gyro)-Delay
        filt_gyro(1, i) = filt_b * env_gyro(i+Delay) - filt_a * filt_gyro(1,i-1);
    end
    end


    function MAR_OD_R_flag = XcorrOD_Motion_sensor(env_z_filt, env_Lx_filt, env_Rx_filt,MAR_dOD,spec)
    ## Xcorr result from MAR features & dOD
    nCh = spec.nch;
    MAR_OD_R_flag = zeros(1,nCh);



    MAR_OD_R_flag_temp = zeros(1,nCh);
    for i = 1:nCh
        MAR_OD_R_flag_temp(1,i) = max(abs(xcorr(MAR_dOD(i,:),env_z_filt,0,'coeff')));
    end
    MAR_OD_R_flag_temp(isnan(MAR_OD_R_flag_temp))=0;
    MAR_OD_R_flag = MAR_OD_R_flag + MAR_OD_R_flag_temp;

    MAR_OD_R_flag_temp = zeros(1,nCh);
    for i = 1:nCh
        MAR_OD_R_flag_temp(1,i) = max(abs(xcorr(MAR_dOD(i,:),env_Lx_filt,0,'coeff')));
    end
    MAR_OD_R_flag_temp(isnan(MAR_OD_R_flag_temp))=0;
    MAR_OD_R_flag = MAR_OD_R_flag + MAR_OD_R_flag_temp;

    MAR_OD_R_flag_temp = zeros(1,nCh);
    for i = 1:nCh
        MAR_OD_R_flag_temp(1,i) = max(abs(xcorr(MAR_dOD(i,:),env_Rx_filt,0,'coeff')));
    end
    MAR_OD_R_flag_temp(isnan(MAR_OD_R_flag_temp))=0;
    MAR_OD_R_flag = MAR_OD_R_flag + MAR_OD_R_flag_temp;

    end


    function [dODspline, Gyro_MA_segment] = GyroMotionCorrectSpline(dOD, Thrs_Gyro_xyz, wd, sp_factor, spec)
    ##
    nCh = spec.nch;
    n_data = spec.ndata;

    Gyro_MA_segment= zeros(1,n_data);

    for i = 1+wd:n_data-2*wd
        if Thrs_Gyro_xyz(i) == 1
            Gyro_MA_segment(i-wd:i+2*wd) = 1;
        end
        Gyro_MA_segment(1) = 0;
        Gyro_MA_segment(end) = 0;
    end

    if sum(Gyro_MA_segment) >= n_data / 2
        Gyro_MA_segment= zeros(1,n_data);
    end
    Gyro_MA_sf = diff(Gyro_MA_segment);
    for j = 1 : nCh
        if sum(isnan(dOD(j,:))) > 0
            dOD(j,:) = 0.1;
        end
    end
    # for j = 1 : nCh
    #     if sum(isinf(dOD(j,:))) > 0
    #         dOD(j,:) = 0.1;
    #     end
    # end

    if isempty(find(Gyro_MA_sf, 1)) == 0
        s_pt = find(Gyro_MA_sf ==1);
        f_pt = find(Gyro_MA_sf ==-1);
        for j = 1: nCh
            for i = 1:length(s_pt)
                spline = csaps(1:(f_pt(i)-s_pt(i)+1),dOD(j,s_pt(i):f_pt(i)),sp_factor,1:(f_pt(i)-s_pt(i)+1));
                Offset_spline = [zeros(1,s_pt(i)-1) (spline-spline(1)) ones(1,n_data - f_pt(i))*(spline(end)-spline(1))];
                dOD(j,:) = dOD(j,:) - Offset_spline;
            end
        end
        dODspline = dOD;
    else
        dODspline = dOD;
    end

    end



    '''

IIR BPF는 DCT가 안될 때 사용.
from scipy.signal import butter, lfilter


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import freqz

    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 5000.0
    lowcut = 500.0
    highcut = 1250.0

    # Plot the frequency response for a few different orders.
    plt.figure(1)
    plt.clf()
    for order in [3, 6, 9]:
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        w, h = freqz(b, a, worN=2000)
        plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)

    plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
             '--', label='sqrt(0.5)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.legend(loc='best')

    # Filter a noisy signal.
    T = 0.05
    nsamples = T * fs
    t = np.linspace(0, T, nsamples, endpoint=False)
    a = 0.02
    f0 = 600.0
    x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
    x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
    x += a * np.cos(2 * np.pi * f0 * t + .11)
    x += 0.03 * np.cos(2 * np.pi * 2000 * t)
    plt.figure(2)
    plt.clf()
    plt.plot(t, x, label='Noisy signal')

    y = butter_bandpass_filter(x, lowcut, highcut, fs, order=6)
    plt.plot(t, y, label='Filtered signal (%g Hz)' % f0)
    plt.xlabel('time (seconds)')
    plt.hlines([-a, a], 0, T, linestyles='--')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')

    plt.show()

    '''

    ''' # function [y2,ylpf] = hmrBandpassFilt( y, fs, hpf, lpf )
    ## 호머 bpf .. 교체하자
    # convert t to fs
    # assume fs is a time vector if length>1
    if len(fs) > 1:
        fs = 1/(fs(2)-fs(1));




    # low pass filter
    FilterType = 1;
    FilterOrder = 3;
    #[fa,fb]=butter(FilterOrder,lpf*2/fs);
    if FilterType==1 || FilterType==5
        [fb,fa] = MakeFilter(FilterType,FilterOrder,fs,lpf,'low');
    elseif FilterType==4
        #    [fb,fa] = MakeFilter(FilterType,FilterOrder,fs,lpf,'low',Filter_Rp,Filter_Rs);
    else
        #    [fb,fa] = MakeFilter(FilterType,FilterOrder,fs,lpf,'low',Filter_Rp);
    end
    ylpf=filtfilt(fb,fa,y);


    # high pass filter
    FilterType = 1;
    FilterOrder = 5;
    if FilterType==1 || FilterType==5
        [fb,fa] = MakeFilter(FilterType,FilterOrder,fs,hpf,'high');
    elseif FilterType==4
        #    [fb,fa] = MakeFilter(FilterType,FilterOrder,fs,hpf,'high',Filter_Rp,Filter_Rs);
    else
        #    [fb,fa] = MakeFilter(FilterType,FilterOrder,fs,hpf,'high',Filter_Rp);
    end

    if FilterType~=5
        y2=filtfilt(fb,fa,ylpf);
    else
        y2 = ylpf;
    end
    end
    

    function [fb,fa] = MakeFilter(FilterType,FilterOrder,fs,cutoff,highlow,Rp,Rs)
    #Types
    #    Butterworth
    #    Chebyshev Type I
    #    Chebyshev Type II
    #    Cauer (Elliptic)
    #    sliding average filter

    if ~exist('Rp','var')
        Rp=0.5;  #PassBand suppression (in dB)
    end

    if ~exist('Rs','var')
        Rs=30;   #SideBand suppression (in dB)
    end

    Wn=cutoff*2/fs;

    lst=find(Wn==0);
    Wn(lst)=[];
    if lst==2 & strcmp(highlow,'band')      # &가 맞음..
        highlow='high';
    end

    if any(Wn<0) || any(Wn>=1) || isempty(Wn)
        if ~isempty(Wn)
            h=warndlg('Filter parameters exceed Nyquist frequency');
            while ishandle(h)
                pause(0.1);
            end
        end
        fa=[1 0];  #This will effectively not do anything to the data
        fb=[1 0];
        return
    end

    switch(FilterType)
        case 1
            #Butterworth
            if strcmp(highlow,'band') && length(Wn)==2
                [fb,fa]=butter(FilterOrder,Wn);
            elseif strcmp(highlow,'high')
                [fb,fa]=butter(FilterOrder,Wn,'high');
            else
                #Low
                [fb,fa]=butter(FilterOrder,Wn);
            end
        case 2
            #Chebyshev Type I
            if strcmp(highlow,'band') && length(Wn)==2
                [fb,fa]=cheby1(FilterOrder,Rp,Wn);
            elseif strcmp(highlow,'high')
                [fb,fa]=cheby1(FilterOrder,Rp,Wn,'high');
            else
                #Low
                [fb,fa]=cheby1(FilterOrder,Rp,Wn);
            end

        case 3
            #Chebyshev Type II
            if strcmp(highlow,'band') && length(Wn)==2
                [fb,fa]=cheby2(FilterOrder,Rp,Wn);
            elseif strcmp(highlow,'high')
                [fb,fa]=cheby2(FilterOrder,Rp,Wn,'high');
            else
                #Low
                [fb,fa]=cheby2(FilterOrder,Rp,Wn);
            end
        case 4
            #Ellipic
            if strcmp(highlow,'band') && length(Wn)==2
                [fb,fa]=ellip(FilterOrder,Rp,Rs,Wn);
            elseif strcmp(highlow,'high')
                [fb,fa]=ellip(FilterOrder,Rp,Rs,Wn,'high');
            else
                #Low
                [fb,fa]=ellip(FilterOrder,Rp,Rs,Wn);
            end
        case 5
            #sliding average version
            fb=ones(floor(2/Wn),1)/floor(2/Wn);
            fa=1;
    end
    return
    end
    '''

    ##  Json structure  ##
    # Info
    # - Id
    # - Task name:?
    # - filtering_spec: BPF, Motion artifact,
    # ?
    # Time-series data
    # - Timestamp : t초 x 1?
    # - Marker : t초 x 1?
    # - Movement : t초 x 2개?
    # - RAW : 68ch x t초
    # - SNR = RAW?> BPF > calculate 20log10(mu/std)
    # - OD = RAW?> calculate OD W/O BPF
    # - Motion OD  = OD >? Calculate Motion artifact
    # - MBLL = Motion OD >?Calculate Spike removal(검증필요) >?BPF > Calculate MBLL
    #
    # Performance
    # - accuracy(1/0)
    # - response time
    #
    # Meta : 엄교수님
    # - Tscr
    # - Zscr?
    # - Sex
    # - Age, …?
    # - StatusCode :: 메세지 생성을 위한?
