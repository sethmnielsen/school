"""
mavSimPy
    - Chapter 2 assignment for Beard & McLain, PUP, 2012
    - Update history:
        1/10/2019 - RWB
"""
import sys
sys.path.append('..')

# import viewers and video writer
# from chap2.spacecraft_viewer import spacecraft_viewer
from chap2.mav_viewer import mav_viewer
# from chap2.video_writer import video_writer

# import parameters
import parameters.simulation_parameters as SIM
# import message types
from message_types.msg_state import msg_state

# initialize messages
state = msg_state()  # instantiate state message

# initialize viewers and video
VIDEO = False  # True==write video, False==don't write video
# mav_view = spacecraft_viewer()
mav_view = mav_viewer()
if VIDEO == True:
    video = video_writer(video_name="chap2_video.avi",
                         bounding_box=(0, 0, 1000, 1000),
                         output_rate=SIM.ts_video)

# initialize the simulation time
sim_time = SIM.start_time
print("SIM.end_time/6:", SIM.end_time/6)
def trans_rot(sim_time):
    if sim_time < SIM.end_time/6:
        # print(SIM.end_time/6)
        print(sim_time)
        state.pn += 10*SIM.ts_simulation
    elif sim_time < 2*SIM.end_time/6:
        # print(1)
        state.pe += 10*SIM.ts_simulation
    elif sim_time < 3*SIM.end_time/6:
        # print(2)
        state.h += 10*SIM.ts_simulation
    elif sim_time < 4*SIM.end_time/6:
        # print(3)
        state.phi += 0.1*SIM.ts_simulation
    elif sim_time < 5*SIM.end_time/6:
        # print(4)
        state.theta += 0.1*SIM.ts_simulation
    else:
        # print(5)
        state.psi += 0.1*SIM.ts_simulation

def rot_trans(sim_time):
    if sim_time < SIM.end_time/6:
        state.phi += 0.1*SIM.ts_simulation
    elif sim_time < 2*SIM.end_time/6:
        state.theta += 0.1*SIM.ts_simulation
    elif sim_time < 3*SIM.end_time/6:
        state.psi += 0.1*SIM.ts_simulation
    elif sim_time < 4*SIM.end_time/6:
        state.pn += 10*SIM.ts_simulation
    elif sim_time < 5*SIM.end_time/6:
        state.pe += 10*SIM.ts_simulation
    else:
        state.h += 10*SIM.ts_simulation


# main simulation loop
T = 2.5
while sim_time < SIM.end_time:
    #-------vary states to check viewer-------------
    # print(sim_time)
    trans_rot(sim_time)
    # rot_trans(sim_time)

    #-------update viewer and video-------------
    mav_view.update(state)
    if VIDEO == True: video.update(sim_time)

    #-------increment time-------------
    sim_time += SIM.ts_simulation

print("Press Ctrl-Q to exit...")
if VIDEO == True: video.close()
