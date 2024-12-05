import uiautomator2 as u2
d = u2.connect('emulator-5554')
import time
d(description='Location list').click()
time.sleep(1)
d(text='United States, Santa Clara').click()
time.sleep(1)
d(description='Edit this location').click()
time.sleep(1)
d(text='Delete').click()
time.sleep(1)
d(text='Confirm').click()
time.sleep(1)
