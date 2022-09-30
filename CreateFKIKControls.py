from gettext import translation
import maya.cmds as cmds
#intended operation: user selects any number of joint(s) in Maya, and runs the below script.
#Authot: Yukti Gupte
#global dictionary with format - jointName : jointCtrlName
controlDict = {}
#argument needed: selected joint(s)
selectedJoint = cmds.ls(sl=True, type='joint')
print(selectedJoint)
# FIRST PART: CREATING AND POSITIONING THE CONTROL CURVE
def CreateControlCurve():
    for eachJoint in selectedJoint:
        #create NURBS circle and assign the same name as the selected joint, but replace _j with _ctrl
        ctrlName = eachJoint.replace("_j","_ctrl")
        newCtrl = cmds.circle(name= ctrlName)
        #group the control transform node once, name the group "_ctrl" + "_auto"
        ctrlAuto_grp = cmds.group(newCtrl, name=ctrlName+ '_auto')
        #group the group node created above, name the group "_ctrl" + "_offset"
        ctrlOffset_grp = cmds.group(ctrlAuto_grp, name=ctrlName+ '_offset')
        #parent "_offset" group under the joint
        cmds.parent(ctrlOffset_grp, eachJoint)
        #set translate and rotate channels of _offset group to 0
        cmds.xform(ctrlOffset_grp, translation = (0,0,0), rotation = (0,0,0))
        #un-parent offset group from under joint
        cmds.parent(ctrlOffset_grp, world=True)
        #controlDict[eachJoint] = newCtrl[0]
        controlDict.update({eachJoint : ctrlName})
    print(controlDict)


#SECOND PART: SETTING UP CONSTRAINTS FOR FK AND IK JOINTS
#this function can loop through all selected joints
def CreateConstraint():
    cmds.select(selectedJoint)
    print(selectedJoint)
    if bool(selectedJoint):
    #controlDict[jointName : jointCtrlName]
        for eachJoint in selectedJoint:
            #check if selected joint is mapped to the controls dictionary or not
            if eachJoint in controlDict:
                if '_fk_j' in eachJoint:
                    #if fk joint, create a point and an orient constraint from _ctrl to _j
                    cmds.pointConstraint(controlDict.get(eachJoint), eachJoint, maintainOffset=True)
                    cmds.orientConstraint(controlDict.get(eachJoint), eachJoint, maintainOffset=True)
                    #if ik joint, create a point constraint from _ctrl to _j
                elif '_ik_j' in eachJoint:
                    cmds.pointConstraint(controlDict.get(eachJoint), eachJoint, maintainOffset=True)
                    #if it's neither then create a parent constraint from _ctrl to _j
                else:
                    cmds.parentConstraint(controlDict.get(eachJoint), eachJoint, maintainOffset=True)
                    
            
            else:
                print('No controller was created for this joint')
                            
    else:
        print('No joints were selected')


#THIRD PART: CLEANING UP
#this function can loop through all selected joints
#:D
def ControlsCleanUp():
    cmds.select(selectedJoint)
    print(selectedJoint)
    if bool(selectedJoint):
    #check if selected joint is mapped to a controller or not
        for eachJoint in selectedJoint:
            if eachJoint in controlDict:
                #enable drawing overrides
                cmds.setAttr(controlDict.get(eachJoint) + '.overrideEnabled', 1)
                #lock and hide scale xyz channels
                cmds.setAttr(controlDict.get(eachJoint) + '.scaleX', keyable=False, cb=False, lock=True)
                cmds.setAttr(controlDict.get(eachJoint) + '.scaleY', keyable=False, cb=False, lock=True)
                cmds.setAttr(controlDict.get(eachJoint) + '.scaleZ', keyable=False, cb=False, lock=True)
                #if fk control: 
                if '_fk_ctrl' in controlDict.get(eachJoint): 
                    #set colour to "light blue"
                    cmds.setAttr(controlDict.get(eachJoint) + '.overrideColor', 18)
                #else if ik control: 
                elif '_ik_ctrl' in controlDict.get(eachJoint):
                    #lock and hide rotate xyz channels
                    cmds.setAttr(controlDict.get(eachJoint) + '.rotateX', keyable=False, cb=False, lock=True)
                    cmds.setAttr(controlDict.get(eachJoint) + '.rotateY', keyable=False, cb=False, lock=True)
                    cmds.setAttr(controlDict.get(eachJoint) + '.rotateZ', keyable=False, cb=False, lock=True)
                    #set colour to "yellow" 
                    cmds.setAttr(controlDict.get(eachJoint) + '.overrideColor',17)
                #else lock visibility channel for all other controls
                else:
                    cmds.setAttr(controlDict.get(eachJoint) + '.visibility', keyable=False, cb=False, lock=True)

            else:
                print('No controller was created for this joint')
    else:
        print('No joints were selected')

#Calling all the functions in order
CreateControlCurve()
CreateConstraint()
ControlsCleanUp()