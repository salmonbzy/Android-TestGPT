import uiautomator2 as u2
d = u2.connect('emulator-5554')
import time
d(className='android.widget.FrameLayout').click()
time.sleep(1)
d(description='Edit this location').click()
time.sleep(1)
d(text='Weather sources').click()
time.sleep(1)
d(className='android.view.View').click()
time.sleep(1)
d(text='AccuWeather').click()
time.sleep(1)
d(text='Save').click()
time.sleep(1)
