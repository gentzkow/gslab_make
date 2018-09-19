#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import subprocess
import shutil
import traceback

from gslab_make_dev.private.exceptionclasses import CritError
import gslab_make_dev.private.messages as messages
import gslab_make_dev.private.metadata as metadata
from gslab_make_dev.private.utility import norm_path, format_error


class Directive(object):
    """
    Directive.
    
    Notes
    -----
    Contains instructions on how to run shell commands.

    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to False.
    makelog : str, optional
        Path of make log.
    log : str, optional
        Path of directive log. Directive log is only written if specified.  

    Returns
    -------
    None
    """
    
    def __init__(self, 
                 makelog, 
                 osname = os.name,
                 shell = False,
                 log = ''):

        self.makelog  = makelog
        self.osname   = osname
        self.shell    = shell
        self.log      = log  
        self.check_os()
        self.get_paths()

    def check_os(self):
        """ Check OS is either POSIX or NT. 
        
        Returns
        -------
        None
        """    
        
        if (self.osname != 'posix') & (self.osname != 'nt'):
            raise CritError(messages.crit_error_unknown_system % self.osname)

    def get_paths(self):   
        """ Normalize paths.   
        
        Returns
        -------
        None  
        """
        self.makelog  = norm_path(self.makelog)
        self.log      = norm_path(self.log) if self.log != '' else self.log        

    def execute_command(self, command):   
        """ Execute shell command.
        
        Parameters
        ----------
        command : str
            Shell command to execute.
        
        Returns
        -------
        exit : tuple
            (Exit code, error message).
        """
        
        self.output = 'Executing: "%s"' % command
        print(self.output)

        try:   
             command = command.split()
             p = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = self.shell)
             stdout, stderr = p.communicate()
             exit = (p.returncode, stderr)

             if stdout:
                self.output += '\n' + stdout
             if stderr:
                self.output += '\n' + stderr
        except:
             error = messages.crit_error_bad_command % ' '.join(command) + '\n' + traceback.format_exc()
             error = format_error(error)
             exit = (1, error)

             self.output += '\n' + error
             
        return(exit)

    def write_log(self):
        """ Write logs for shell command.
        
        Returns
        -------
        None
        """
        
        if self.makelog: 
            if not (metadata.makelog_started and os.path.isfile(self.makelog)):
                raise CritError(messages.crit_error_no_makelog % self.makelog)
            with open(self.makelog, 'a') as f:
                f.write(self.output)

        if self.log:
            with open(self.log, 'w') as f:
                f.write(self.output)


class ProgramDirective(Directive):
    """
    Program directive.
    
    Notes
    -----
    Contains instructions on how to run a program through shell command.

    Parameters
    ----------
    See `Directive`.
    
    application : str
        Name of application to run program.
    program : str
        Path of program to run.
    executable : str, optional
        Executable to use for shell command. Defaults to executable specified in metadata.
    option : str, optional
        Options for shell command. Defaults to options specified in metadata.
    args : str, optional
        Arguments for shell command. Defaults to no arguments.
        
    Attributes
    ----------
    program_dir : str
        Directory of program parsed from program.
    program_base : str
        `program_name.program_ext` of program parsed from program.
    program_name : str
        Name of program parsed from program.
    program_ext : str
        Extension of program parsed from program.
        
    Returns
    -------
    None
    """
    
    def __init__(self, 
                 application, 
                 program,
                 executable = '', 
                 option = '',
                 args = '', 
                 **kwargs):

        super(ProgramDirective, self).__init__(**kwargs)
        self.application = application
        self.program     = program
        self.executable  = executable
        self.option      = option
        self.args        = args      
        self.parse_program()
        self.check_program()
        self.get_executable()
        self.get_option()

    def parse_program(self):
        """ Parse program for directory, name, and extension.
        
        Returns
        -------
        None
        """
    
        self.program = norm_path(self.program)
        self.program_dir = os.path.dirname(self.program)
        self.program_base = os.path.basename(self.program)
        self.program_name, self.program_ext = os.path.splitext(self.program_base)

    def check_program(self):
        """ Check program exists and has correct extension given application.
        
        Returns
        -------
        None
        """  
    
        if not os.path.isfile(self.program):
            raise CritError(messages.crit_error_no_file % self.program)
            
        if self.program_ext != metadata.extensions[self.application]:
            raise CritError(messages.crit_error_extension % self.program)

    def get_executable(self):
        """ Set executable to default from metadata if unspecified.
        
        Returns
        -------
        None
        """
        
        if not self.executable:
            self.executable = metadata.default_executables[self.osname][self.application]

    def get_option(self):
        """ Set options to default from metadata if unspecified.
        
        Returns
        -------
        None
        """

        if not self.option:
            self.option = metadata.default_options[self.osname][self.application]

    def move_program_output(self, program_output, log_file = ''):
        """ Move program outputs.
        
        Notes
        -----
        Certain applications create program outputs that need to be moved to 
        appropriate logging files.
        
        Parameters
        ----------
        program_output : str
             Path of program output.
        log_file : str, optional
             Path of log file. Log file is only written if specified.  
        """
    
        try:
            program_output = norm_path(program_output)
            with open(program_output, 'r') as f:
                out = f.read()
        except:
            raise CritError(messages.crit_error_no_file % program_output)

        if self.makelog: 
            if not (metadata.makelog_started and os.path.isfile(self.makelog)):
                raise CritError(messages.crit_error_no_makelog % self.makelog)
            with open(self.makelog, 'a') as f:
                f.write(out)

        if log_file: 
            if program_output != log_file:
                shutil.copy2(program_output, log_file)
                os.remove(program_output)
        else: 
            os.remove(program_output)


class SASDirective(ProgramDirective):    
    """
    SAS directive.
    
    Notes
    -----
    Contains instructions on how to run a SAS program through shell command.

    Parameters
    ----------
    See `ProgramDirective`.
    
    lst : str, optional
        Path of directive lst. Directive lst is only written if specified.  
    """
    def __init__(self, 
                 lst = '', 
                 **kwargs):

        super(SASDirective, self).__init__(**kwargs)
        self.lst = lst  


class LyxDirective(ProgramDirective):    
    """
    Lyx directive.
    
    Notes
    -----
    Contains instructions on how to run a Lyx program through shell command.

    Parameters
    ----------
    See `ProgramDirective`.
    
    doctype : str, optional
        Type of LyX document. Takes either `handout` and `comments`. 
        Defaults to no special document type.
    pdfout : str, optional
        Directory to write PDF. Defaults to directory specified in metadata.
    """
    
    def __init__(self, 
                 doctype = '',
                 pdfout = metadata.settings['output_dir'],
                 **kwargs):

        super(LyxDirective, self).__init__(**kwargs)
        self.doctype = doctype
        self.pdfout  = pdfout
        self.check_doctype()
        self.get_pdfout()

    def check_doctype(self):
        """ Check document type is valid.
        
        Returns
        -------
        None
        """
    
        if self.doctype not in ['handout', 'comments', '']:
            print('Document type "%s" unrecognized. Reverting to default' % self.doctype)
            self.doctype = ''
            
    def get_pdfout(self):
        """ Get PDF output directory.
        
        Returns
        -------
        None
        """
        
        if self.doctype:
            self.pdfout = metadata.settings['temp_dir']

        self.pdfout = norm_path(self.pdfout)