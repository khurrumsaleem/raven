"""
Created on Jan 28, 2015

@author: alfoa
"""
from __future__ import division, print_function, unicode_literals, absolute_import
import warnings
warnings.simplefilter('default',DeprecationWarning)
#External Modules------------------------------------------------------------------------------------
import abc
import os
#External Modules End--------------------------------------------------------------------------------

#Internal Modules------------------------------------------------------------------------------------
import utils
#Internal Modules End--------------------------------------------------------------------------------

class CodeInterfaceBase(utils.metaclass_insert(abc.ABCMeta,object)):
  """
  Code Interface base class. This class should be the base class for all the code interfaces.
  In this way some methods are forced to be implemented and some automatic checking features
  are available (checking of the inputs if no executable is available), etc.
  NOTE: As said, this class SHOULD be the base class of the code interfaces. However, the developer
        of a newer code interface can decide to avoid to inherit from this class if he does not want
        to exploit the automatic checking of the code interface's functionalities
  """
  def __init__(self):
    """
      Constructor
      @ In, None
      @ Out, None
    """
    self.inputExtensions = []

  def genCommand(self,inputFiles,executable,flags=None, fileArgs=None, preExec=None):
    """
      This method is used to retrieve the command (in tuple format) needed to launch the Code.
      This method checks a bolean enviroment variable called 'RAVENinterfaceCheck':
      if true, the subcodeCommand is going to be overwritten with an empty string. In this way we can check the functionality of the interface without having an executable.
      See Driver.py to understand how this Env variable is set
      @ In, inputFiles, list, List of input files (lenght of the list depends on the number of inputs have been added in the Step is running this code)
      @ In, executable, string, executable name with absolute path (e.g. /home/path_to_executable/code.exe)
      @ In, flags, dict, optional, dictionary containing the command-line flags the user can specify in the input (e.g. under the node < Code >< clargstype =0 input0arg =0 i0extension =0 .inp0/ >< /Code >)
      @ In, fileArgs, dict, optional, a dictionary containing the axuiliary input file variables the user can specify in the input (e.g. under the node < Code >< clargstype =0 input0arg =0 aux0extension =0 .aux0/ >< /Code >)
      @ In, preExec, string, optional, a string the command that needs to be pre-executed before the actual command here defined
      @ Out, returnCommand, tuple, tuple containing the generated command. returnCommand[0] is the command to run the code (string), returnCommand[1] is the name of the output root
    """
    if preExec is None: subcodeCommand,outputfileroot = self.generateCommand(inputFiles,executable,clargs=flags,fargs=fileArgs)
    else: subcodeCommand,outputfileroot = self.generateCommand(inputFiles,executable,clargs=flags,fargs=fileArgs,preExec=preExec)
    if os.environ['RAVENinterfaceCheck'].lower() in utils.stringsThatMeanTrue(): return [('parallel','')],outputfileroot
    returnCommand = subcodeCommand,outputfileroot
    return returnCommand

  def readMoreXML(self,xmlNode):
    """
      Function to read the portion of the xml input that belongs to this class and
      initialize some members based on inputs.
      @ In, xmlNode, XML element node
      @ Out, None.
    """
    self._readMoreXML(xmlNode)

  def _readMoreXML(self,xmlNode):
    """
      Function to read the portion of the xml input that belongs to this specialized class and
      initialize some members based on inputs. This can be overloaded in specialized code interface in order
      to read specific flags
      @ In, xmlNode, XML element node
      @ Out, None.
    """
    pass #afaik, this is only used in GenericCodeInterface currently.

  @abc.abstractmethod
  def generateCommand(self,inputFiles,executable,clargs=None,fargs=None, preExec=None):
    """
      This method is used to retrieve the command (in tuple format) needed to launch the Code.
      @ In, inputFiles, list, List of input files (lenght of the list depends on the number of inputs have been added in the Step is running this code)
      @ In, executable, string, executable name with absolute path (e.g. /home/path_to_executable/code.exe)
      @ In, clargs, dict, optional, dictionary containing the command-line flags the user can specify in the input (e.g. under the node < Code >< clargstype =0 input0arg =0 i0extension =0 .inp0/ >< /Code >)
      @ In, fargs, dict, optional, a dictionary containing the axuiliary input file variables the user can specify in the input (e.g. under the node < Code >< clargstype =0 input0arg =0 aux0extension =0 .aux0/ >< /Code >)
      @ In, preExec, string, optional, a string the command that needs to be pre-executed before the actual command here defined
      @ Out, returnCommand, tuple, tuple containing the generated command. returnCommand[0] is the command to run the code (string), returnCommand[1] is the name of the output root
    """
    return

  @abc.abstractmethod
  def createNewInput(self,currentInputFiles,oriInputFiles,samplerType,**Kwargs):
    """
      This method is used to generate an input based on the information passed in.
      @ In, currentInputFiles, list,  list of current input files (input files from last this method call)
      @ In, oriInputFiles, list, list of the original input files
      @ In, samplerType, string, Sampler type (e.g. MonteCarlo, Adaptive, etc. see manual Samplers section)
      @ In, Kwargs, dictionary, kwarded dictionary of parameters. In this dictionary there is another dictionary called "SampledVars"
             where RAVEN stores the variables that got sampled (e.g. Kwargs['SampledVars'] => {'var1':10,'var2':40})
      @ Out, newInputFiles, list, list of newer input files, list of the new input files (modified and not)
    """
    pass

        ####################
  ####### OPTIONAL METHODS #######
        ####################

  def getInputExtension(self):
    """
      This method returns a list of extension the code interface accepts for the input file (the main one)
      @ In, None
      @ Out, tuple, tuple of strings containing accepted input extension (e.g.(".i",".inp"]) )
    """
    return tuple(self.inputExtensions)

  def setInputExtension(self,exts):
    """
      This method sets a list of extension the code interface accepts for the input files
      @ In, exts, list, list or other array containing accepted input extension (e.g.[".i",".inp"])
      @ Out, None
    """
    self.inputExtensions = exts[:]

  def addInputExtension(self,exts):
    """
      This method adds a list of extension the code interface accepts for the input files
      @ In, exts, list, list or other array containing accepted input extension (e.g.[".i",".inp"])
      @ Out, None
    """
    for e in exts:self.inputExtensions.append(e)

  def addDefaultExtension(self):
    """
      This method sets a list of default extensions a specific code interface accepts for the input files.
      This method should be overwritten if these are not acceptable defaults.
      @ In, None
      @ Out, None
    """
    self.addInputExtension(['i','inp','in'])

  def finalizeCodeOutput(self,command,output,workingDir):
    """
      this method is called by the RAVEN code at the end of each run (if the method is present).
      It can be used for those codes, that do not create CSV files to convert the whaterver output formato into a csv
      @ In, command, string, the command used to run the just ended job
      @ In, output, string, the Output name root
      @ In, workingDir, string, current working dir
      @ Out, output, string, optional, present in case the root of the output file gets changed in this method.
    """
    return output

  def checkForOutputFailure(self,output,workingDir):
    """
      This method is called by RAVEN at the end of each run if the return code is == 0.
      This method needs to be implemented by the codes that, if the run fails, return a return code that is 0
      This can happen in those codes that record the failure of the job (e.g. not converged, etc.) as normal termination (returncode == 0)
      This method can be used, for example, to parse the outputfile looking for a special keyword that testifies that a particular job got failed
      (e.g. in RELAP5 would be the keyword "********")
      @ In, output, string, the Output name root
      @ In, workingDir, string, current working dir
      @ Out, failure, bool, True if the job is failed, False otherwise
    """
    failure = False
    return failure

  def expandVarNames(self,**Kwargs):
    """
      This method will assure the full proper variable names are returned in a modificaton dictionary.
      It primarily expands aliases. I will admit I don't know what colons do.
      @ In, Kwargs, dict, keyworded dictionary. Arguments include:
          - alias, the alias -> TrueName dictionary
          - SampleVars, short name -> sampled value dictionary
      @ Out, listDict, list, list of dictionaries. The dictionaries contain:
               ['name'][path,to,name]
               [short varname][var value]
    """
    listDict=[]
    modifDict={}
    for var in Kwargs['SampledVars']:
      if 'alias' in Kwargs.keys() and var in Kwargs['alias'].keys():
        # for understending the alias system, plase check module Models.py (class Code)
        #if var in Kwargs['alias'].keys():
        key = Kwargs['alias'][var].split(':')
      else:
        key = var.split(':')
      modifDict = {}
      modifDict['name'] = key[0].split('|')[:-1]
      modifDict[key[0].split('|')[-1]] = Kwargs['SampledVars'][var]
      listDict.append(modifDict)
      del modifDict
    return listDict
