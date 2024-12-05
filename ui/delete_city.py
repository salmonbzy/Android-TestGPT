import uiautomator2 as u2
d = u2.connect('emulator-5554')
import time
d(description='Edit this location').click()
time.sleep(1)
d(text='Delete').click()
time.sleep(1)
d(text='Confirm').click()
time.sleep(1)
