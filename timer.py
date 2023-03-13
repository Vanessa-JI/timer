import time as time
import threading as threading
import sys

# instantiating a lock to prevent concurrent modification of the same variable
# makes sure that all threads are in sync with the variable value
lock = threading.Lock()


class Timer():

    def __init__(self, callback):

        # stop_thread variable identifies whether the timer is to be stopped or not
        self.stop_thread = False
        self.callback = callback
        self.timeout = int(input('\nEnter a time in seconds to start timer: '))
        self.start_timer(self.timeout, self.stop_thread)

        return

    # stop_timer exits the thread it is called from
    def stop_timer(self):
        sys.exit()

    # function controlling the timer countdown
    def countdown(self, stop_thread, timeout):
        for _ in range(timeout):

            # variables within lock.acquire and lock.release cannot be changed elsewhere
            lock.acquire()
            if self.stop_thread == True:
                self.stop_timer()
            lock.release()

            timeout -= 1
            time.sleep(1)

        # once the timer has elapsed, call the callback function and exit the thread
        self.callback()
        self.stop_timer()

    # function starts the countdown thread so timer can run in the background
    def start_timer(self, timeout, stop_thread):
        countdown_thread = threading.Thread(target=self.countdown, kwargs={
                                            'stop_thread': stop_thread, 'timeout': timeout})

        countdown_thread.start()

        while True:
            inp = input(
                "\na: Check if timer is running \nb: Stop timer/exit \n\nSelect a or b: ")
            if inp == 'a':
                self.is_running(countdown_thread)

            if inp == 'b':
                print('\nExited/Timer stopped.\n')

                lock.acquire()
                self.stop_thread = True
                lock.release()

                self.stop_timer()

    # function to see if timer is running
    def is_running(self, countdown_thread):

        if countdown_thread.is_alive():
            return print('\nTimer is running...')

        else:
            return print('\nTimer is not running.')


# instantiating timer object and specifying callback function
t = Timer(lambda: print("\nTimer has ended.\n"))
