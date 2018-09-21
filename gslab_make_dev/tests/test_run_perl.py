# #! /usr/bin/env python

# import unittest, sys, os, shutil, contextlib
# from gslab_make_dev.write_logs import start_makelog
# from gslab_make_dev.dir_mod import clear_dir
# from gslab_make_dev.run_program import run_perl
# from nostderrout import nostderrout
# import gslab_make_dev.private.metadata as metadata
# from gslab_make_dev.private.exceptionclasses import CritError
    

# class testRunPerl(unittest.TestCase):

#     def setUp(self):
#         with nostderrout():
#             clear_dir(['../output/', '../log'])

#     def test_default_log(self):
#     	default_makelog = metadata.settings['makelog']
#         with nostderrout():
#             start_makelog(default_makelog)
#             run_perl(program = 'gslab_make_dev/tests/input/perl_test_script.pl')
#         self.assertIn('Test script complete', open(default_makelog).read())
#         self.assertTrue(os.path.isfile('output.txt'))
        
#     def test_custom_log(self):
#         makelog_file = '../log/custom_make.log'
#         with nostderrout():
#             start_makelog(makelog_file)
#             run_perl(program = 'gslab_make_dev/tests/input/perl_test_script.pl', makelog = makelog_file)
#         self.assertIn('Test script complete', open(makelog_file).read())
#         self.assertTrue(os.path.isfile('output.txt'))
        
#     def test_independent_log(self):
#     	default_makelog = metadata.settings['makelog']
#     	independent_log = '../log/perl.log'
#         with nostderrout():
#             start_makelog(default_makelog)
#             run_perl(program = 'gslab_make_dev/tests/input/perl_test_script.pl', log = independent_log)
#         self.assertIn('Test script complete', open(default_makelog).read())
#         self.assertIn('Test script complete', open(independent_log).read())        
#         self.assertTrue(os.path.isfile('output.txt'))
        
#     def test_executable(self):
#     	default_makelog = metadata.settings['makelog']
#         with nostderrout():
#             start_makelog(default_makelog)
#             run_perl(program = 'gslab_make_dev/tests/input/perl_test_script.pl', executable = metadata.default_executables[os.name]['perl']) 
#         self.assertIn('Test script complete', open(default_makelog).read())
#         self.assertTrue(os.path.isfile('output.txt'))
        
#     def test_bad_executable(self):
#     	default_makelog = metadata.settings['makelog']
#         with nostderrout():
#             start_makelog(default_makelog)
#         with self.assertRaises(CritError):
#             run_perl(program = 'gslab_make_dev/tests/input/perl_test_script.pl', executable = 'nonexistent_perl_executable')
#         self.assertNotIn('Test script complete', open(default_makelog).read())

#     def test_no_program(self):
#     	default_makelog = metadata.settings['makelog']
#         with nostderrout():
#             start_makelog(default_makelog)
#         with self.assertRaises(Exception):
#             run_perl(program = 'gslab_make_dev/tests/input/nonexistent_perl_script.pl')
#         self.assertNotIn('Test script complete', open(default_makelog).read())
    
#     def tearDown(self):
#         if os.path.isdir('../output/'):
#             shutil.rmtree('../output/')
#         if os.path.isdir('../log/'):
#             shutil.rmtree('../log/')
#         if os.path.isfile('output.txt'):
#             os.remove('output.txt')
                
# if __name__ == '__main__':
#     os.getcwd()
#     unittest.main()
