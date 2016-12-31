from maya import cmds


def match(obj=None, attrs= None, selection= True):

"""
This first section is to make sure something is selected and to define attrs and selection
"""

#If nothing is selected warn the user
if not obj and not selection:
raise ValueError ("Nothing is selected")
#If object is not specified get it from the first selection
if not obj:
obj = cmds.ls(selection=True) [0]

if not attrs:
attrs = cmds.listAttr(obj, keyable=True)


#This gives us the current time of the playback slider
ct = cmds.currentTime(q=True)


# Now we have everything to start, lets loop through all the attributes
    for attr in attrs:
        # It's common to need the object and attribute together like pCube1.translateX so we prepare the full name before hand
        attrFull = '%s.%s' % (obj, attr)

        # We query what keyframes exist for that attribute
        keyframes = cmds.keyframe(attrFull, q=True)

        # If there are no keyframes, then it isn't keyed so we skip it
        if not keyframes:
            # We continue on to the next item in the loop
            continue

  #This section let's us know what the value of the current and next keys are

  # It says add every frame from keyframes if the frame is greater than the current time
      laterKeyframes = [frame for frame in keyframes if frame > ct]

      #This goes back to the top of the code if there are no keyframes after the current time
      if not laterKeyframes:
            continue

        #This finds the next keyframe after the current time or just says there is none if it didn't find any
        nextFrame = min(laterKeyframes) if laterKeyframes else None

        # Now we query the values on the respective frames for this attribute
        # Because we prepared the attrFull variable above, we can reuse it here
        nextValue = cmds.getAttr(attrFull, time=nextFrame)
        currentValue = cmds.getAttr(attrFull, time=ct)

        #find the difference between the current value and next frame value and return the absolute of it
        diff = abs(currentValue - nextValue)

        if currentValue > nextValue:
        cmds.setAttr( 'attrFull', v=(-diff),t=(int("nextFrame:",) ))

        if currentValue < nextValue:
        cmds.setAttr('attrFull', v=(diff), t=(int('nextFrame',)))



      #Below is code that I am not sure if I need or not
        cmds.setKeyframe(attrFull, time=currentTime, value=currentValue)






keyFrames = []

laterKeyFrames = [frame for frame in keyframes if frame > currentTime]

#Selects keyframes after current time
sel = cmds.ls(sl=True)
ct = cmds.currntTime(q=True)
keys = cmds.selectKey(sel, time =(20,110))

cmds.selectKey(time=("10:",))

