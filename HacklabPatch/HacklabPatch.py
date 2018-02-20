"""
Written by Misha @ Hacklab.to
add HacklabPatch.sendFileToCnc() to export_gcode() function in GCODETOOLS
Works for the engraver and the laser cutter, but not for the vinyl cutter (yet)
"""

class HacklabPatch:

	def sendFileToCnc(localpath, remotepath, filename):
		#EDIT HERE#
		cncDomain = None		#the domain name or IP address of the cnc cutter
		cncUsername = None
		cncPassword = None
		#EDIT HERE#

		if(not cncDomain or not cncUsername or not cncPassword):
			print_("After installing GCODETOOLS, please edit HacklabPatch.py with the login info for the cnc cutter")

		try:
			import telnetlib, time, traceback
			#install these first to py 2.7
			from paramiko import SSHClient
			from scp import SCPClient
		except ImportError as e:
			print_("Cannot import python libraries, did you install GCODETOOLS correctly?")

		try:
			try:
				#connect to cnc cutter
				client = SSHClient()
				client.load_system_host_keys()
				client.connect(cncDomain, username=cncUsername, password=cncPassword)
			except Exception as e:
				print_("Cannot connect to cnc, is the computer turned on?")

			#startup AXIS software
			#stdin, stdout, stderr = client.exec_command('linuxcnc -v hacklab-engraver3-server/hacklab-engraver3.ini')
			#f.write(stdout.read())

			#transfer the file to the cnc cutter
			scp = SCPClient(client.get_transport())
			scp.put(localpath+filename, remotepath+filename)
			scp.close()

			#fix the file
			stdin, stdout, stderr = client.exec_command('sh ./fix-file ' +remotepath+filename+ remotepath+'fixed-'+filename)

			try:
				#TELNET into the AXIS software
				comm_delay = 0.500 #delay between commands, just a guess
				tn = telnetlib.Telnet(cncDomain, port=5007)
				time.sleep(comm_delay)
				tn.write('hello EMC inkscapeuser 1.0\n')
				print_(("received data: ", tn.read_very_eager()))
				time.sleep(comm_delay)
				tn.write('set enable EMCTOO\n')
				print_(("received data: ", tn.read_very_eager()))
				time.sleep(comm_delay)
				tn.write('set verbose on\n')
				print_(("received data: ", tn.read_very_eager()))
				time.sleep(comm_delay)
				tn.write('set mode manual\n')
				print_(("received data: ", tn.read_very_eager()))
				time.sleep(comm_delay)
				tn.write('set estop off\n')
				print_(("received data: ", tn.read_very_eager()))
				time.sleep(comm_delay)
				tn.write('set machine on\n')
				print_(("received data: ", tn.read_very_eager()))
				time.sleep(comm_delay)
				tn.write('set home 1\n')
				print_(("received data: ", tn.read_very_eager()))
				time.sleep(4)
				tn.write('set home 0\n')
				print_(("received data: ", tn.read_very_eager()))
				time.sleep(4)
				tn.write('set mode auto\n')
				print_(("received data: ", tn.read_very_eager()))
				time.sleep(comm_delay)
				tn.write('set open ' + remotepath+'fixed-'+filename + '\n')
				print_(("received data: ", tn.read_very_eager()))
				time.sleep(comm_delay)
				tn.write('set run\n')
				print_(("received data: ", tn.read_very_eager()))
				time.sleep(6)
				tn.write('quit\n')
				print_(("received data: ", tn.read_very_eager()))
				time.sleep(comm_delay)
			except Exception as e:
				print_("Cannot communicate with AXIS software\n")
				raise e
		except Exception as e:
			print_("Cannot start CNC Cutter\nThe file will be saved locally\nError: %s" % e)
			traceback.print_exc()