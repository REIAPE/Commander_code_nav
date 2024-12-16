import os
import threading

def callback_1():
    os.system('python3 /home/ap/commander/construction_inspection/src/pose_sub.py')
def callback_2():
    os.system('python3 /home/ap/commander/construction_inspection/src/camera_test.py')

if __name__ =="__main__":
    t1 = threading.Thread(target=callback_2(), args=(10,))
    t2 = threading.Thread(target=callback_1(), args=(10,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print("Done!")