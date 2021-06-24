import inspect
import datetime
import format_map
import os
from classtools import AttrDisplay

#######
# TODO - For better logging
#	x	1. Implement Headers in controller and direct_print in logs.
#		2. Filter out format_map invalids
#		3. Mark and Blank line need work.  
#		4. Error level constants
#		5. Exit on error rules.  IE - error is level 3, then exit or Raise exception
#######

class skzz_log_control2( AttrDisplay ):
	log_list = {}
	log_location = ''
	log_restart = None
	log_mode = ''
	_log_mode = ''
	FILE_HANDLE = None

	MAX_STD = 5		# loop, mark, control, vital, always show
	MAX_WARN = 3	#  warning minor, warning major
	MAX_ERR = 3		#  error simple, error breaks flow, error breaks program.


	def __init__( self , file_loc = None, custom=False ):
		if file_loc is not None:
			self.set_master_save_loc( file_loc )
	
		if custom is not True:
			self.create_default( )

	def set_master_save_loc( self, file_loc , restart_once = True ):
		mode = 'a+'
		if self.check_file_exists( file_loc ) is False:
			mode = 'w+'

		if restart_once is True and skzz_log_control2.log_restart is None:
			mode = 'w+'
			skzz_log_control2.log_restart = True

		skzz_log_control2.log_location = file_loc
		skzz_log_control2._log_mode = mode
		
		try:
			skzz_log_control2.FILE_HANDLE = open( skzz_log_control2.log_location, mode )
#			print "File Opened: "+skzz_log_control2.log_location + " Mode: " + mode
		
		except Exception as e:
			print ( "Log Failed to open " + skzz_log_control2.log_location + "; Attrib: " + mode +"; " + str(e) )
			

	def check_file_exists( self, file ):
		if( os.path.isfile( file ) ):
			return True
		else:
			return False

	def create_default( self ):
		self.create_log( 'file', log_level = 4, log_prompt = '', log_number_prompt_delim=':', log_save_file_handle=skzz_log_control2.FILE_HANDLE, log_number_prompt_on= True, log_screen_write_on = False, log_file_write_on = True, log_keep_internal_on = False)
#		print (" ")
		
		self.create_log( 'screen', log_level = 2, log_prompt = 'CM', log_number_prompt_on= True, log_screen_write_on = True, log_file_write_on = False , log_keep_internal_on = False, log_timestamp_format = None, log_timestamp_delim='', log_indent=2)
#		print (" ")
		
		self.create_log( 'debug', log_level = 1, log_prompt = 'D',  log_number_prompt_delim=':',log_number_prompt_on= True, log_screen_write_on = False, log_file_write_on = False, log_keep_internal_on = True )
#		print (" ")

	def header( self, txt ):
		for logname in self.log_list:
			self.log_list[logname].direct_log( txt )     
			#self.log_list[logname].direct_push( txt )


	def _check_log_name( self, name ):
		if name in self.log_list.keys():
			return True
		else:
			return False

	def create_log( self, name, **kwargs ):
		self.log_list[name] = skzzlogger2( **kwargs )


	def set_log_attr_all_logs( self, **kwargs ):
		for logname in self.log_list:
			self.log_list[logname].set_attr( **kwargs ) 		

	def set_log_attr( self, name, **kwargs ):
		if self._check_log_name( name ) is False:
			return
		
		self.log_list[name].set_attr( **kwargs ) 

	def warn( self, txt, lvl =0, prmpt = None ):
		if lvl is None:
			lvl = 0

		# start warnings above the standard communications
		# so 0 = Level 6.  6 and 7 are error levels. 
		lvl = int(lvl) + self.MAX_STD + 1
 
		if lvl >= self.MAX_STD + self.MAX_WARN :
			lvl = self.MAX_STD + self.MAX_WARN 

		if prmpt is None:
			prmpt = "*"

		for logname in self.log_list:
			self.log_list[logname].olog( txt, None, lvl, prmpt )


	def err( self, txt, lvl=0, prmpt = None ):
		new_lvl = lvl + self.MAX_STD + 1 + self.MAX_WARN

		if new_lvl > self.MAX_STD + self.MAX_WARN + self.MAX_ERR:
			new_lvl = self.MAX_STD + self.MAX_WARN + self.MAX_ERR

		if prmpt is None:
			prmpt = "!"

		print "ERROR - ACTUAL LEVEL: " + str(new_lvl) + "  Threshold: " + str(self.MAX_STD + self.MAX_WARN) 
		for logname in self.log_list:
			self.log_list[logname].olog( txt, None, new_lvl, prmpt )
	
	def log( self, txt, lvl=0, prmpt = None ):
		
		if lvl > self.MAX_STD:
			lvl = self.MAX_STD

		for logname in self.log_list:
			self.log_list[logname].olog( txt, None, lvl, prmpt )                	

	def flush_log( self ):
		skzz_log_control2.FILE_HANDLE.flush()
		self.close_log()

	def mark( self ):
		self.log_list['file'].mark()

	def blank_mark( self ):
		print "\n"

	def close_log( self ):
		skzz_log_control2.FILE_HANDLE.close()

	def dump_logs( self ):
		print '{:^90}'.format( "Dumping all logs" )
		print "Master save location: " + skzz_log_control2.log_location + "   ---   Mode: " + self._log_mode
		for logname in self.log_list:
			print "** LOG NAME: " + str(logname).upper() + " ** "
			self.log_list[logname].dump_log_stats( )

	def get_internal( self , name = None):
		if name is None:
			if 'debug' in self.log_list:
				return self.log_list['debug'].get_internal( )
		else:
			if name in self.log_list:
				return self.log_list[name].get_internal( )
			else:
				return ""


class skzzlogger2( AttrDisplay ):
	log_on = True
	log_level = None        # Log level, 
	log_prompt = None             # This goes into prompts as such [x].  useful to set this module as different than main module.
	log_timestamp_format = "%Y-%m-%d::%H:%M:%S"          # On or off - true or false, Put a timetamp in before prompt
	log_save_file_loc = ''           # The location to write out the log if needed.
	log_save_file_handle = None
	log_number_prompt_on = False      # Add number to the prompt, use with smart prompt
	log_prompt_format = "{log_timestamp}{log_prompt} {log_caller} {log_text}"
	log_caller = True
	
	log_screen_write_on = True
	log_file_write_on = True
	log_keep_internal_on = False
	

	_log_internal = []
	_default_level = 2
    
	log_timestamp_delim = '-'
	log_number_prompt_delim = ':'

	log_indent = 0
	
	MIN_LEVEL = 0
	MAX_LEVEL = 5
	MAX_WARN_LEVEL = 3
	MAX_ERR_LEVEL = 3
	
	LOG_FILE_HANDLE = None
	
	def __init__( self,  **kwargs ):		
		self.set_attr( **kwargs )
		
		if self.log_level is None:
			self.log_level = self._default_level
	
	def dump_log_stats ( self ):
		print "______________ Log details ______________"
		print "log_on: " + str(self.log_on )
		print "log_level: " +  str(self.log_level )
		print "log_prompt: " +   self.log_prompt 
		if self.log_timestamp_format is not None: print "log_timestamp_format: " + self.log_timestamp_format
		print "log_save_file_loc: " +   str(skzzlogger2.log_save_file_loc )
		print "log_number_prompt_on: " +  str(self.log_number_prompt_on)
		print "log_prompt_format: " +    self.log_prompt_format 
		print "log_caller: " +    str( self.log_caller )
		print "\n\n"
		

	def get_err_lvl( self ):
		return self.MAX_LEVEL + 1
	
	def set_on_off( self, turn_on = True ):
		if turn_on is False:
			self.log_on = False
		else:
			self.log_on = True
			
	
	def validate_level( self,  level ):
		if level > self.MAX_LEVEL + self.MAX_ERR_LEVEL +self.MAX_WARN_LEVEL:
			level = self.MAX_LEVEL + self.MAX_ERR_LEVEL +self.MAX_WARN_LEVEL
		
		if level < self.MIN_LEVEL:
			level = self.MIN_LEVEL
			
		return level
			
	def set_prompt( self, prompt ):
		self.log_prompt = promt
	
	
	def set_number_prompt_on_off( self, turn_on = True ):
		if turn_on is False:
			self.log_number_prompt_on = False
		else:
			self.log_number_prompt_on = True
		
	
	def set_timestamp_format( self, fmt = "%Y-%m-%d %H:%M:%S" ):
		self.log_timestamp_format = self._validate_ts_format( fmt ) 
		
	
	def _validate_ts_format( self, fmt ):
		test = "{:%s}" %(fmt)

		try:
			test.format(datetime.datetime.now())
			return fmt
		except:
			print("Timestamp format invalid")
			return None
	
	
	def set_save_file_loc( self, loc , attrib='a+'):
		self.log_save_file_loc = loc
		
		if self.log_save_file_loc is None or self.log_save_file_loc != " ":
			return
		else:
			print "["+self.log_save_file_loc+"]"

		print ('Save at: ' +self.log_save_file_loc)
		 
		if len(attrib) > 2:
			print ("Warning: Attribute " + attrib + " seems to be too long." )
			
		if( attrib[0] not in 'aw+'):
			print ("Warning: Attribute " + attrib[0] + " in invalid; defaulting to append." )
			attrib = 'a+'
			
		self.log_save_file_attrib = attrib
		self.init_file( )

		
	def init_file( self ):
		if not self.__class__.LOG_FILE_HANDLE  :
			try:
				self.__class__.LOG_FILE_HANDLE = open( self.log_save_file_loc, self.log_save_file_attrib )
			except Exception as e:
				print ( "Failed to open " + self.log_save_file_loc + "; Attrib: " + self.log_save_file_attrib +"; " + str(e) )
				exit()
		
		
	
	def check_file_exists( self, file ):
		if( os.path.isfile( file ) ):
			return True
		else:
			return False

		
	def set_attr( self, **kwargs ):
		if 'log_timestamp_format' in kwargs.keys():
			self.set_timestamp_format( kwargs.pop('log_timestamp_format', None ) )
				
		if 'log_save_file_loc' in kwargs.keys():
			#print ("SAVE FILE" )
			self.set_save_file_loc( kwargs.pop('log_save_file_loc', None ) )
		
		for key in kwargs:
			if key in dir( self.__class__ ):
				setattr( self, key, kwargs[key] )
				#print (key + "->" + str(kwargs[key]) )
	

	def get_timestamp( self ):
		if self.log_timestamp_format is not None:
			self.log_timestamp_format = self._validate_ts_format ( self.log_timestamp_format )
			ts = "{:%s}" %( self.log_timestamp_format )
			ts_stamp = ts.format( datetime.datetime.now() )
			
			if self.log_timestamp_delim is not None: 
				ts_stamp += " " + self.log_timestamp_delim + " "
			else:
				ts_stamp += " "
				
			return ts_stamp
		else:
			return ""
	
	def _generate_prompt_number( self ):
		num_str = ''
		
		if self.log_number_prompt_on is not False:
			if self.log_number_prompt_delim is not None:
				num_str = self.log_number_prompt_delim
			else:
				num_str = ''
			
			num_str += '{log_level}'
		
		return num_str
	
	
	def _generate_prompt( self, tmp_prompt = None ):	
		prompt_final = ''
		prompt_bracket = ''
		
		if tmp_prompt == False:
			return ""
		
		if tmp_prompt is not None:
			prompt_bracket = tmp_prompt 
		
		else:
			if self.log_prompt is not None:
				prompt_bracket = self.log_prompt
			else:
				prompt_bracket = ""
		
		prompt_bracket = str(prompt_bracket) +  str(self._generate_prompt_number( ))
				
		if prompt_bracket is not None and prompt_bracket != "":
			return (" " * self.log_indent)  + "[" + prompt_bracket +   "]"
		else:
			return ""
			
	
	def set_default_level( self, lvl ):
			self._default_level = self.validate_level( lvl )
	
	def set_level( self, lvl ):
			self.log_level = self.validate_level( lvl )
	
	def direct_lp( self , txt ):
		self.direct_print( txt )
		self.direct_log( txt )

	def direct_print( self , line ):
		if line is not None and line != "":
			if self.log_screen_write_on is not False:
				print ( line )

	def direct_log( self , line ):
		if int(self.log_level) >=3:
			if self.log_save_file_handle is not None:
				if  line is not None and line is not "" :
					if not self.log_save_file_handle.closed:
						if self.log_file_write_on is not False:
							self.log_save_file_handle.write( str(line) +"\n") 

	def direct_push( self , line ):
		if self.log_keep_internal_on is True:
			if  line is not None and line is not "" :
				self.add_to_internal_list( line )


	# wrtie to screen and to file.
	def olog( self,  txt, caller = None, level = None, tmp_prompt = None ):
		self.log( txt, level, tmp_prompt )
		self.out( txt, level, tmp_prompt )
		self.internal( txt, level, tmp_prompt )
	
	# out writes to screen
	def out( self,  txt, level = None, tmp_prompt = None , caller = None ):
		line = self.prep_line( txt,  level, tmp_prompt, caller, 'out' )
		if line is not None and line != "":
			if self.log_screen_write_on is not False:
				print ( line )
	
	
	# log writes to file.
	def log( self,  txt, caller = None, level = None, tmp_prompt = None ):		
		line = self.prep_line( txt, level, tmp_prompt , caller , 'log' )
		if self.log_save_file_handle is not None:
			if  line is not None and line is not "" :
				if not self.log_save_file_handle.closed:
					if self.log_file_write_on is not False:
						self.log_save_file_handle.write( str(line) +"\n") 
	
	def internal( self, txt, level, tmp_prompt ):
		if self.log_keep_internal_on is True:
			line = self.prep_line( txt, level, tmp_prompt, True, 'internal')
			if  line is not None and line is not "" :
				self.add_to_internal_list( line )


	def mark( self ):
		self.log( ' -- MARK -- ',  10, False, False )
		
	
	def omark( self ):
		self.out( ' -- MARK -- ', 10, False, False )
		self.log( ' -- MARK -- ', 10, False, False )
	
	
	
	def test( self,  txt,  level = None, tmp_prompt = None , caller = None):
		return
		print ( txt )
		print (  level )
		print (  tmp_prompt )
		print (  caller )
	
	def flush_log( self ):
		if  self.log_save_file_handle is not None:
			if not self.log_save_file_handle.closed:
				self.log_save_file_handle.flush()
		
		tmp = self._log_internal
		self._log_internal = []
		return tmp
	
	def add_to_internal_list( self, txt ):
		self._log_internal.append( txt )

	def get_internal( self ):
		return self._log_internal

	def prep_line( self, txt,  level = None, tmp_prompt = None , caller = None, xtra = None):
		#self.dump_log_stats( )
		if level is None:
			level = self._default_level
		else:
			level = self.validate_level( level )

		if self.log_on is not True:
			return ""
		

#		print (  txt + "*** level: " + str( level ) + "  vs log_level " + str(self.log_level ))
		if int(level) < int(self.log_level):
#			print "        Returning"
			return None
			
		log_caller = ''
		if self.log_caller is not False and caller is not False:
			log_caller = "("+self.caller_name( )+")"
		
			
		log_timestamp = self.get_timestamp( )
		log_prompt = self._generate_prompt( tmp_prompt )
		log_text = txt
		log_txt = txt
		log_level = level
		
#		print ("who: " + str(xtra))
#		print ( 'ts: ' + log_timestamp  )
#		print ( 'prompt: ' + log_prompt )
#		print ( 'text: ' + log_text )
#		print ( 'lvel: ' + str(log_level ))
#		print ( 'caller: ' + str(log_caller ))
#		print (  "level: " + str(level ) + "  vs log_level " + str(self.log_level ))
		
		# log_prompt_format = "{log_timestamp}{log_prompt}{caller}{log_text}"
		line = self.log_prompt_format
		#print line
		#{log_timestamp}{log_prompt} {log_caller} {log_text}
		final_line = line.format_map( vars() )
		final_line = str(final_line).format_map( vars() )

		#print ("Final line: " + final_line )
		#print " "
		return final_line 
	
	def caller_name(self, skip=6):
          """Get a name of a caller in the format module.class.method

             `skip` specifies how many levels of stack to skip while getting caller
             name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

            

             An empty string is returned if skipped levels exceed stack height
          """
          stack = inspect.stack()
          start = 0 + skip
          if len(stack) < start + 1:
            return ''
          parentframe = stack[start][0]    

          name = []
          module = inspect.getmodule(parentframe)
          # `modname` can be None when frame is executed directly in console
          # TODO(techtonik): consider using __main__
          if module:
              name.append(module.__name__)
          # detect classname
          if 'self' in parentframe.f_locals:
              # I don't know any way to detect call from the object method
              # XXX: there seems to be no way to detect static method call - it will
              #      be just a function call
              name.append(parentframe.f_locals['self'].__class__.__name__)
          codename = parentframe.f_code.co_name
          if codename != '<module>':  # top level usually
              name.append( codename ) # function or a method

          ## Avoid circular refs and frame leaks
          #  https://docs.python.org/2.7/library/inspect.html#the-interpreter-stack
          del parentframe, stack

          return ".".join(name)

	
if __name__ == '__main__':
	mylog = skzzlogger2( log_prompt='+', hello='world', log_timestamp_format = "%y/%m/%d"   )
	mylog.set_save_file_loc( 'x.txt' )
	
	print( mylog )
	
	#mylog.out('test12')
	#mylog.log('testabc')
	#mylog.omark( )
	l = skzz_log_control( 'xx_debug_test.txt' )
	
	l.log("Hello")
	l.out("Hello")
	l.om( )
	#l.err("This is an error!!!" )
	#l.log("Hello", 8)
	
	
