# Task ID [] -- Object Detecion -- Diff0 & Diff1 -- Target Startreck
from ethopy.behaviors.multi_port import *
from ethopy.experiments.match_port import *
from ethopy.stimuli.panda import *
from scipy import interpolate
import time 


# Define session parameters
session_params = {
    'max_reward'        : 1200,
    'min_reward'        : 700,
    'setup_conf_idx'    : 0,
}

exp = Experiment()
exp.setup(logger, MultiPort, session_params)

exp.interface.give_liquid(1, 300)
time.sleep(2)
exp.interface.give_liquid(2, 300)


conditions = []

env_key = {
    "init_ready"            : 100,
    "trial_ready"           : 200,
    "intertrial_duration"   : 500,
    "trial_duration"        : 9000,
    "reward_duration"       : 5000,
    "punish_duration"       : 10000,
    "abort_duration"        : 500,
}

print(env_key)

panda_obj = Panda()
panda_obj.fill_colors.set({
    'background'   : (0, 0, 0),
    'start'        : (0.2, 0.2, 0.2),
    'reward'       : (0.6, 0.6, 0.6),
    'punish'       : (0, 0, 0)
})



interp = lambda x: interpolate.splev(np.linspace(0, len(x), 100),
                                     interpolate.splrep(np.linspace(0, len(x), len(x)), x)) if len(x) > 3 else x 


# Diff0

resp_obj = [2, 2]
rew_prob = [1, 2]
x_pos = [-0.3, 0.3]

rot_f = lambda: interp((np.random.rand(20)-.5) * 100)
rots = rot_f()

block = exp.Block(difficulty=0, 
                  next_up=1,
                  next_down=0,
                  staircase_window=20,
                  trial_selection='staircase',
                  stair_up=0.75,
                  stair_down=0.55,
                  )

for idx, obj_comb in enumerate(resp_obj):
    conditions += exp.make_conditions(stim_class=panda_obj, conditions={**env_key, **block.dict(), 
            'obj_id'            : resp_obj[idx],
            'obj_dur'           : 9000,
            'obj_pos_x'         : x_pos[idx],
            'obj_pos_y'         : 0,
            'obj_mag'           : 0.5,
            'obj_rot'           : (rots, rots),
            'obj_tilt'          : (0, 0),
            'obj_yaw'           : (0, 0),
            'reward_port'       : rew_prob[idx],
            'response_port'     : rew_prob[idx],
            'reward_amount'     : 6
            })
     

# Diff1

resp_obj = [(2, 1), (1, 2)]
rew_prob = [1, 2]
x_pos =[(-0.3, 0.3), (-0.3, 0.3)]

rot_f = lambda: interp((np.random.rand(20)-.5) * 100)
rots = rot_f()

block = exp.Block(difficulty=1, 
                  next_up=1,
                  next_down=1,
                  staircase_window=30,
                  trial_selection='staircase',
                  stair_up=0.75,
                  stair_down=0.55,
                  )

for idx, obj_comb in enumerate(resp_obj):
    conditions += exp.make_conditions(stim_class=panda_obj, conditions={**env_key, **block.dict(),
            'obj_id'            : resp_obj[idx],
            'obj_dur'           : 9000,
            'obj_pos_x'         : x_pos[idx],
            'obj_pos_y'         : 0.05,
            'obj_mag'           : 0.5,
            'obj_rot'           : (rots, rots),
            'obj_tilt'          : (0, 0),
            'reward_port'       : rew_prob[idx],
            'response_port'     : rew_prob[idx],
            'reward_amount'     : 6
            })
    
# Run Exeperiment
exp.push_conditions(conditions)
exp.start()