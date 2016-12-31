"""maya.py"""
from maya import cmds


def match(obj=None, attrs=None, selection=True):
    """
    This first section is to make sure something is selected and to define
    attrs and selection.
    """

    # If nothing is selected warn the user
    if obj is None and selection is None:
        raise ValueError("Nothing is selected")
    # If object is not specified get it from the first selection
    if obj is None:
        obj = cmds.ls(selection=True)[0]

    if attrs is None:
        attrs = cmds.listAttr(obj, keyable=True)

    # This gives us the current time of the playback slider
    c_time = cmds.currentTime(q=True)

    # Now we have everything to start, lets loop through all the attributes
    for attr in attrs:
        # It's common to need the object and attribute together like
        # pCube1.translateX so we prepare the full name before hand
        attr_full = '{}.{}'.format(obj, attr)

        # We query what keyframes exist for that attribute
        keyframes = cmds.keyframe(attr_full, q=True)

        # If there are no keyframes, then it isn't keyed so we skip it
        if keyframes:
            # This section let's us know what the value of the current and next
            # keys are
            # It says add every frame from keyframes if the frame is greater
            # than the current time
            later_keyframes = [frame for frame in keyframes if frame > c_time]

            # This goes back to the top of the code if there are no keyframes
            # after the current time
            if later_keyframes:
                # This finds the next keyframe after the current time
                next_frame = min(later_keyframes)

                # Now we query the values on the respective frames for this
                # attribute
                # Because we prepared the attr_full variable above, we can
                # reuse it here
                next_val = cmds.getAttr(attr_full, time=next_frame)
                curr_val = cmds.getAttr(attr_full, time=c_time)

                # find the difference between the current value and next frame
                # value and return the absolute of it
                diff = abs(curr_val - next_val)

                if curr_val > next_val:
                    cmds.setAttr(attr_full, v=(-diff), t=int(next_frame))
                else:
                    cmds.setAttr(attr_full, v=(diff), t=int(next_frame))

                # Below is code that I am not sure if I need or not
                cmds.setKeyframe(attr_full, time=c_time, value=curr_val)

                # Selects keyframes after current time
                sel = cmds.ls(sl=True)
                ct = cmds.currntTime(q=True)  # Unused variable
                keys = cmds.selectKey(sel, time=(20, 110))  # Unused variable

                # Not sure what this line is supposed to do
                cmds.selectKey(time=("10:",))
