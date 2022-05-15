
from ccgp_cq import main_hub,main_artcle
import sys
input = sys.argv[1]
if input == 'hub':
	main_hub()
elif input == 'article':
	main_artcle()
else:
	exit()
