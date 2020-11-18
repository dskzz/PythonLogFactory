import inspect
import datetime
from classtools import AttrDisplay

class skzz_log_control(  AttrDisplay ):
	log_list = {}
	log_location = ''
	
	
	def __init__( self , file_loc = None, custom=False ):
		if file_loc is not None:
			self.log_location = file_loc
	
		if custom is not True:
			self.create_default( )
	
	
	def create_default( self ):
		self.create_log( 'debug', log_level = 4, log_prompt = '', log_number_prompt_delim='', log_save_file_loc=self.log_location, log_number_prompt_on= True)
		print (" ")
		self.create_log( 'screen', log_level = 2, log_prompt = 'CM', log_number_prompt_on= True)
		print (" ")
		self.create_log( 'error', log_level = 5, log_prompt = '!!', log_number_prompt_on= True, log_save_file_loc=self.log_location )
		print (" ")
	
	def create_log( self, name, **kwargs ):
		self.log_list[name] = skzzlogger2( **kwargs )
	
	def show_log( self, name ):
		if self._check_log_name( name ) is False:
			return
			
		print( log_list[name] )
		
	def set_log_attr( self, name, **kwargs ):
		if self._check_log_name( name ) is False:
			return
			
		self.log_list[name].set_attr( **kwargs )
	
	def _check_log_name( self, name ):
		if name in self.log_list.keys():
			return True
		else:
			return False
		
	
	def mark( self, name = 'debug' ):
		self.log_list[name].mark(  )
	
	def mark( self, name = 'debug' ):
		self.log_list[name].omark(  )
	
	def log( self, txt, lvl=None, name = 'debug' ):
		if self._check_log_name( name ) is False:
			return
		
		print ("SCREEN LOG")
		print ("screen log level " + str(self.log_list[name].log_level))
		self.log_list[name].log( txt, lvl )
		
	
	def out( self, txt, lvl=None, name = 'screen' ):
		if self._check_log_name( name ) is False:
			return
		
		self.log_list[name].out(txt,lvl)
	
	def m( self ):
		for name in self.log_list:
			self.log_list[name].mark( )

	def om( self ):
		for name in self.log_list:
			self.log_list[name].omark( )
			
	
	def o( self, txt, lvl ):
		for name in self.log_list:
			self.log_list[name].out( txt, lvl )
			
	def l( self, txt, lvl ): 
		for name in self.log_list:
			self.log_list[name].out( txt, lvl )
	
	def ol( self, txt, lvl ): 
		for name in self.log_list:
			self.log_list[name].out( txt, lvl )
			self.log_list[name].log( txt, lvl )
	
	def err( self, txt, lvl=None , name = 'error' ):
		if self._check_log_name( name ) is False:
			return
		
		if lvl is None:
			lvl = self.log_list[name].get_err_lvl( )
			
		self.log_list[name].out( txt, lvl )
		
		
	

class skzzlogger2( AttrDisplay ):
	log_on = True
	log_level = None        # Log level, 
	log_prompt = None             # This goes into prompts as such [x].  useful to set this module as different than main module.
	log_timestamp_format = "%Y-%m-%d::%H:%M:%S"          # On or off - true or false, Put a timetamp in before prompt
	log_save_file_loc = ''           # The location to write out the log if needed.
	log_number_prompt_on = False      # Add number to the prompt, use with smart prompt
	log_prompt_format = "{log_timestamp}{log_prompt} {log_caller} {log_text}"
	log_caller = True
	
	_default_level = 2
    
	log_timestamp_delim = '-'
	log_number_prompt_delim = ':'
	
	MIN_LEVEL = 0
	MAX_LEVEL = 5
	MAX_ERR_LEVEL = 3
	
	LOG_FILE_HANDLE = None
	
	def __init__( self,  **kwargs ):
		if __class__.log_save_file_loc is not None and __class__.log_save_file_loc is not "":
			self.set_save_file_loc( __class__.log_save_file_loc )
				
		self.set_attr( **kwargs )
		
		if self.log_level is None:
			self.log_level = self._default_level
	
	def get_err_lvl( self ):
		return self.MAX_LEVEL + 1
	
	def set_on_off( self, turn_on = True ):
		if turn_on is False:
			self.log_on = False
		else:
			self.log_on = True
			
	
	def validate_level( self,  level ):
		if level > self.MAX_LEVEL + self.MAX_ERR_LEVEL:
			level = self.MAX_LEVEL + self.MAX_ERR_LEVEL
		
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
		
		print ('save at :' +self.log_save_file_loc)
		
		if len(attrib) > 2:
			print ("Warning: Attribute " + attrib + " seems to be too long." )
			
		if( attrib[0] not in 'aw+'):
			print ("Warning: Attribute " + attrib[0] + " in invalid; defaulting to append." )
			attrib = 'a+'
			
		self.log_save_file_attrib = attrib
		self.init_file( )

		
	def init_file( self ):
		try:
			__class__.LOG_FILE_HANDLE = open( self.log_save_file_loc, self.log_save_file_attrib )
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
			print ("SAVE FILE" )
			self.set_save_file_loc( kwargs.pop('log_save_file_loc', None ) )
		
		for key in kwargs:
			if key in dir( __class__ ):
				setattr( self, key, kwargs[key] )
				print (key + "->" + str(kwargs[key]) )
	

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
			return "[" + prompt_bracket +   "]"
		else:
			return ""
			
	
	def set_default_level( self, lvl ):
			self._default_level = self.validate_level( lvl )
	
	def set_level( self, lvl ):
			self.log_level = self.validate_level( lvl )
	
	
	
	
	def out( self,  txt, level = None, tmp_prompt = None , caller = None):
		self.test(  txt,  level , tmp_prompt , caller )
		line = self.prep_line( txt,  level, tmp_prompt, caller )
		
		if line is not None and line != "":
			print ( line )
	
	
	
	def log( self,  txt, caller = None, level = None, tmp_prompt = None ):
		line = self.prep_line( txt, level, tmp_prompt , caller)
		
		if line is not None and line != "" and __class__.LOG_FILE_HANDLE is not None:
			__class__.LOG_FILE_HANDLE.write( line +"\n") 
	
	
	
	def olog( self,  txt, caller = None, level = None, tmp_prompt = None ):
		self.log( txt, caller, level, tmp_prompt )
		self.out( txt, caller, level, tmp_prompt )
		
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
	
	
	
	def prep_line( self, txt,  level = None, tmp_prompt = None , caller = None):
		if level is None:
			level = self._default_level
		else:
			level = self.validate_level( level )
		
		if self.log_on is not True:
			return
			
		#print ( "level " + str(level ) + "  vs log_level " + str(self.log_level ))
		if level < self.log_level:
			return
			
		log_caller = ''
		if self.log_caller is not False and caller is not False:
			log_caller = "("+self.caller_name( )+")"
		
			
		log_timestamp = self.get_timestamp( )
		log_prompt = self._generate_prompt( tmp_prompt )
		log_text = txt
		log_txt = txt
		log_level = level
		
		#print ( 'ts: ' + log_timestamp  )
		#print ( 'prompt: ' + log_prompt )
		#print ( 'text: ' + log_text )
		#print ( 'lvel: ' + str(log_level ))
		
		# log_prompt_format = "{log_timestamp}{log_prompt}{caller}{log_text}"
		line = self.log_prompt_format
		final_line = line.format_map( vars() )
		final_line = final_line.format_map( vars() )
		return final_line 
	
	def caller_name(self, skip=4):
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
	
	
	