"""

.. module:: particleCreator
    :platform: Win
    :synopsis: to attach particles around the given mesh to be able to apply dynamics

.. moduleauthor:: ananya

"""

# ============================================
# Imports
# ============================================

import maya.api.OpenMaya as om
import maya.OpenMaya as om1
import maya.OpenMayaFX as omFx
import sys

# =============================================
# Global Variables
# =============================================
commandName = 'particleCreator'
kHelpFlag = '-h'
kHelpLongFlag = '-help'
kSparseFlag = '-s'
kSparseLongFlag = '-sparse'


def maya_useNewAPI():
    pass


class particleCreator(om.MPxCommand):
    """Particle simulator"""

    sparse = None

    def __init__(self):
        """Class Initializer """
        super(particleCreator, self).__init__()

    def doIt(self, args):
        """ particle creation """
        print("DO IT")
        self.argumentParser(args=args)
        if self.sparse != None:
            self.redoIt()

    def isUndoable(self):
        """Determines if the operation is undoable. For the time being its kept to always return true 
        but can be changed as per requirement
        """
        return True
    
    def undoIt(self):
        """Undo operation"""
        mFnDagNode = om.MFnDagNode(self.mobjParticle)
        mDagModifier = om.MDagModifier()
        mDagModifier.deleteNode(mFnDagNode.parent(0))
        mDagModifier.doIt()

    def argumentParser(self, args):
        """Argument Parser to parse the argList in the doIt method
        
        :param args: argument list of doIt
        """
        syntax = self.syntax()
        parsedArguments = om.MArgDatabase(syntax, args)
        
        if parsedArguments.isFlagSet(kSparseFlag):
            self.sparse = parsedArguments.flagArgumentDouble(kSparseFlag, 0)
        if parsedArguments.isFlagSet(kSparseLongFlag):
            self.sparse = parsedArguments.flagArgumentDouble(kSparseLongFlag, 0)
        if parsedArguments.isFlagSet(kHelpFlag):
            self.setResult('Help Message for particle simulator')
        if parsedArguments.isFlagSet(kHelpLongFlag):
            self.setResult('Help Message for particle simulator')
        
    def redoIt(self):
        """Redo function"""
        mSel = om.MSelectionList()
        mFnMesh = om.MFnMesh()
        mPointArray2 = om.MPointArray()
        mPointArray1 = om1.MPointArray()
        mFnParticle = omFx.MFnParticleSystem()
        mSel = om.MGlobal.getActiveSelectionList()

        if mSel.length() >= 1:
            try:
                dag = mSel.getDagPath(0)
                mFnMesh.setObject(dag)
            except RuntimeError as e:
                om.MGlobal.displayError("Select a poly mesh")
                
        else:
            om.MGlobal.displayError("Select at least one object")
        
        mPointArray2 = mFnMesh.getPoints(om.MSpace.kObject)
        self.mobjParticle = mFnParticle.create()
       
        # Done to fix the maya crash
        mFnParticle = omFx.MFnParticleSystem(self.mobjParticle)

        counter = 0
        # convertion of OpenMaya.api.MPointArray to OpenMaya.MPointArray
        for i in range(len(mPointArray2)):
            mPointArray1.append(om1.MPoint(mPointArray2[i].x, mPointArray2[i].y, mPointArray2[i].z))
        
        for j in range(mPointArray1.length()):
            if j % self.sparse == 0:
                mFnParticle.emit(mPointArray1[j])
                counter+=1

        print("Total Points: {}".format(counter))
        mFnParticle.saveInitialState() # To save initial state after dynamics are applied


def cmdCreator():
    """To attach the pointer to instance of class
    
    :rtype: MPx Pointer
    """
    return particleCreator()

def syntaxCreator():
    """Helper for maya to accept args in the collection of flags 
    
    :rtype: OpenMaya.MSyntax
    """
    syntax = om.MSyntax()
    syntax.addFlag(kHelpFlag, kHelpLongFlag)
    syntax.addFlag(kSparseFlag, kSparseLongFlag, om.MSyntax.kDouble)

    return syntax

def initializePlugin(mObject):
    """Plugin register"""

    mPlugin = om.MFnPlugin(mObject)
    try:
        mPlugin.registerCommand(commandName, cmdCreator, syntaxCreator)
    except:
        om.MGlobal.displayError("Failed to Register Command: {commandName}".format(commandName=commandName))

def uninitializePlugin(mObject):
    """Plugin deregister"""

    mPlugin = om.MFnPlugin(mObject)
    try:
        mPlugin.deregisterCommand(commandName)
    except:
        om.MGlobal.displayError("Failed to Deregister Command: {commandName}".format(commandName=commandName))

