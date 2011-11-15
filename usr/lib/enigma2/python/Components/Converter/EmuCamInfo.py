# v0.02 , 15 Nov 2011
# ambrosa

from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config

"""
OSCAM /tmp/ecm.info example :

caid: 0x0919
pid: 0x0626
prov: 0x000000
reader: remote_camd35
from: 192.168.1.100
protocol: 16
hops: 0
ecm time: 0.172
cw0: 55 6C 95 56 4C 25 99 0A
cw1: F9 DF 6F 47 59 EB 57 9B



CCCAM /tmp/ecm.info example :

system: Videoguard (News Datacom)
caid: 0x919
provider: SKY Italia (13E)
provid: 0x000
pid: 0x654
using: newcamd
address: 192.168.1.100:10000
hops: 1
ecm time: 0.186
"""

class EmuCamInfo(Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)

		self.calledTypeParam = type


	def caName(self,caid):
		if ((caid>="0100") and (caid<="01FF")):
			return "SECA"
		elif ((caid>="0500") and (caid<="05FF")):
			return "VIACCESS"
		elif ((caid>="0600") and (caid<="06FF")):
			return "IRDETO"
		elif ((caid>="0900") and (caid<="09FF")):
			return "NDS"
		elif ((caid>="0B00") and (caid<="0BFF")):
			return "CONAX"
		elif ((caid>="0D00") and (caid<="0DFF")):
			return "CWORKS"
		elif ((caid>="1700") and (caid<="17FF")):
			return "BETA"
		elif ((caid>="1800") and (caid<="18FF")):
			return "NAGRA"
		else:
			return "unknown"


	@cached
	def getText(self):

		txt_cam = '[NO INFO]'

		try:
			f = open('/tmp/ecm.info', 'r')
			flines = f.readlines()
			f.close()
		except:
			txt_cam = '[no /tmp/ecm.info file]'
		else:
			camInfo = {}
			for line in flines:
				r = line.split(':', 1)
				if len(r) > 1 :
					camInfo[r[0].strip('\n\r\t ')] = r[1].strip('\n\r\t ')

			cam_active = ''

			if 'system' in camInfo :
				cam_active = 'CCcam'
				cam_caid = camInfo.get('caid','')
				cam_ecmtime = camInfo.get('ecm time','')
				cam_info1 = camInfo.get('using','')
				cam_info2 = camInfo.get('address','')

			elif 'reader' in camInfo :
				cam_active = 'OSCam'
				cam_caid = camInfo.get('caid','')
				cam_ecmtime = camInfo.get('ecm time','')
				cam_info1 = camInfo.get('reader','')
				cam_info2 = camInfo.get('from','')

			else:
				cam_active = 'CAM unknown'
				cam_caid = ''
				cam_ecmtime = ''
				cam_info1 = ''
				cam_info2 = ''
				

			txt_cam = "%s     %s %s     %s     %s  %s" % (cam_active, self.caName(cam_caid[2:]), cam_caid, cam_ecmtime, cam_info1, cam_info2)



		if self.calledTypeParam == 'CAMINFO' :
			return txt_cam

		return 'generic error EmuCamInfo.getText()'

	text = property(getText)


