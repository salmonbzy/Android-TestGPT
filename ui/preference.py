import uiautomator2 as u2
d = u2.connect('emulator-5554')
import time
d(description='Edit this location').click()
time.sleep(1)
d(text='Location preferences').click()
time.sleep(1)
d(text='Best match').click()
time.sleep(1)
d(className='android.view.View').click()
time.sleep(1)
d(text='Confirm').click()
time.sleep(1)
