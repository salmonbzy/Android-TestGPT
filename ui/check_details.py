import uiautomator2 as u2
d = u2.connect('emulator-5554')
import time
d(className='android.widget.RelativeLayout').click()
time.sleep(1)
d(text='Temperature').click()
time.sleep(1)
d(text='Air quality').click()
time.sleep(1)
d(text='Wind').click()
time.sleep(1)
