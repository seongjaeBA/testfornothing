import expyriment

n_trials_block = 4
n_blocks = 6
durations = 2000

flanker_stimuli = ['<<<<<', '>>>>>', '<<><<', '>><>>']

instructions = "press key for victory!!!"

experiment = expyriment.design.Experiment(name='flanker task')

expyriment.control.initialize(experiment)

for block in range(n_blocks):
    temp_block = expyriment.design.Block(name=str(block + 1))

    for trial in range(n_trials_block):
        curr_stim = flanker_stimuli[trial]
        temp_stim = expyriment.stimuli.TextLine(text = curr_stim, text_size = 40)
        temp_trial = expyriment.design.Trial()
        temp_trial.add_stimulus(temp_stim)

        if flanker_stimuli[trial].count(curr_stim[0]) == len(curr_stim):
            trialtype = 'congruent'
        else:
            trialtype = 'Incongruent'

        if curr_stim[2] == '<':
            correctresponse = 120
        elif curr_stim[2] == '>':
            correctresponse = 109

        temp_trial.set_factor('trialtype',trialtype)
        temp_trial.set_factor('correctresponse', correctresponse)

    temp_block.add_trial(temp_trial)
    
    temp_block.shuffle_trials()
    experiment.add_block(temp_block)

experiment.data_variable_names = ['block', 'correctresp', 'response', 'trial', 'RT', 'accuracy', 'trialtype']

flaxtion_cross = expyriment.stimuli.FixCross()
# fixation_cross.preload()

expyriment.control.start(skip_ready_screen=True)

expyriment.stimuli.TextScreen('flanker task', instructions).present()
experiment.keyboard.wait(expyriment.misc.constants.K_SPACE)

for block in experiment.blocks:
    for trial in block.trials:
        
        trial.stimuli[0].preload()
        flaxtion_cross.present()
        experiment.clock.wait(durations)
        trial.stimuli[0].present()
        experiment.clock.reset_stopwatch()

        key, rt = experiment.keyboard.wait(keys = [expyriment.misc.constants.K_x, expyriment.misc.constants.K_m], duration = durations)

        experiment.clock.wait(durations - experiment.clock.stopwatch_time)

        if key == trial.get_factor('correctresponse'):
            acc = 1
        else:
            acc = 0
        
        experiment.data.add([block.name, trial.get_factor('correctresponse'), key, trial.id, rt, acc, trial.get_factor('trialtype')])

        if block.name !='6':
            expyriment.stimuli.TextScreen('short break', 'that was block: ' + block.name + '. \n next block will soon start', ).present()

        experiment.clock.wait(3000)
    experiment.clock.wait(3000)
