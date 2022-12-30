"""

.. module:: particleCreator
    :platform: Win
    :synopsis: to attach particles around the given mesh to be able to apply dynamics

.. moduleauthor:: ananya

"""

# ==================================================================================
# Python Imports
# ==================================================================================
import sys

# ==================================================================================
# Other Imports
# ==================================================================================
import maya.OpenMaya as om
import maya.OpenMayaFX as omFx
import maya.OpenMayaMPx as omMpx

# ==================================================================================
# Variables
# ==================================================================================
commandName = 'particleCreator'
kHelpFlag = '-h'
kHelpLongFlag = '-help'
kSparseFlag = '-s'
kSparseLongFlag = '-sparse'


class particleCreator(omMpx.MPxCommand):
    """Particle simulator"""

    sparse = None

    def __init__(self):
        """Class Initializer """
        super(particleCreator, self).__init__()

    def doIt(self, argList):
        """ particle creation """
        #print("DO IT")
        self.argumentParser(argList=argList)
        if self.sparse != None:
            self.redoIt
        return om.MStatus.kSuccess

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
        return om.MStatus.kSuccess

    def argumentParser(self, argList):
        """Argument Parser to parse the argList in the doIt method
        
        :param argList: argument list of doIt
        """
        syntax = self.syntax()
        parsedArguments = om.MArgDatabase(syntax, argList)
        
        if parsedArguments.isFlagSet(kSparseFlag):
            self.sparse = parsedArguments.flagArgumentDouble(kSparseFlag, 0)
            return om.Mstatus.kSuccess
        if parsedArguments.isFlagSet(kSparseLongFlag):
            self.sparse = parsedArguments.flagArgumentDouble(kSparseLongFlag, 0)
            return om.Mstatus.kSuccess
        if parsedArguments.isFlagSet(kHelpFlag):
            self.setResult('Help Message for particle simulator')
            return om.Mstatus.kSuccess
        if parsedArguments.isFlagSet(kHelpLongFlag):
            self.setResult('Help Message for particle simulator')
            return om.Mstatus.kSuccess
        
    def redoIt(self):
        """Redo function"""
        mSel = om.MSelectionList()
        mDagPath = om.MDagPath()
        mFnMesh = om.MFnMesh()
        om.MGlobal.getActiveSelectionList(mSel)

        if mSel.length() >= 1:
            try:
                mSel.getDagPath(0, mDagPath)
                mFnMesh.setObject(mDagPath)
            except:
                print("Select a poly mesh")
                return om.MStatus.kUnknownParameter
        else:
            print("Select a poly mesh")
            return om.MStatus.kUnknownParameter
        mPointArray = om.MPointArray()
        mFnMesh.getPoints(mPointArray, om.MSpace.kWorld)

        mFnParticle = omFx.MFnParticleSystem()
        self.mobjParticle = mFnParticle.create()

        # Done to fix the maya bug 
        mFnParticle = omFx.MFnParticleSystem(self.mobjParticle)
        counter = 0

        for i in range(mPointArray.length()):
            if i % self.sparse == 0:
                mFnParticle.emit(mPointArray[i])
                counter+=1
        
        # print("Total Points: {}".format(counter))
        mFnParticle.saveInitialState() # To save initial state after dynamics are applied

        return om.MStatus.kSuccess



def cmdCreator():
    """To attach the pointer to instance of class
    
    :rtype: MPx Pointer
    """
    return omMpx.asMPxPtr(particleCreator())

def initializePlugin(mObject):
    """Plugin register"""
    mPlugin = omMpx.MFnPlugin(mObject)
    try:
        mPlugin.registerCommand(commandName, cmdCreator, syntaxCreator)
    except:
        sys.stderr.write("Failed to Register Command: {commandName}".format(commandName=commandName))

def uninitializePlugin(mObject):
    """Plugin deregister"""
    mPlugin = omMpx.MFnPlugin(mObject)
    try:
        mPlugin.deregisterCommand(commandName)
    except:
        sys.stderr.write("Failed to Deregister Command: {commandName}".format(commandName=commandName))

def syntaxCreator():
    """Helper for maya to accept args in the collection of flags 
    
    :rtype: OpenMaya.MSyntax
    """
    syntax = om.MSyntax()
    syntax.addFlag(kHelpFlag, kHelpLongFlag)
    syntax.addFlag(kSparseFlag, kSparseLongFlag, om.MSynatx.kDouble)

    return syntax