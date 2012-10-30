from hd44780 import HD44780
from socket import gethostname, gethostbyname_ex
from psutil import cpu_percent, phymem_usage
from time import sleep

lcd = HD44780()
#lcd.clear()
lcd.message("Hello World!!!")

while 1:
    sleep(2)
    cpu = round(cpu_percent(),0)
    mem = round(phymem_usage()[3],0)
    ip = "127.0.0.1" #[ip for ip in gethostbyname_ex(gethostname())[2] if not ip.startswith("127.")][:1][0]
    lcd.clear()
    lcd.message('CPU %.0f%% MEM %.0f%%\nIP %s' % (cpu,mem,ip))