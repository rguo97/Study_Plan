import threading
import time
def thread_A(dict={}):
    print("Thread A start!")
    for i in range(5):
        dict["message"] = "Thread A is doing"
        time.sleep(5)
        print(i)

    dict["result"]=2
    dict["message"]="Thread B has done"
    print("Thread A stop!")
def thread_B(dict={}):
    print("Thread B start!")
    while(dict["result"]!=2):
        time.sleep(1)
        print(dict["message"])
    print("Thread B stop!")


dict={"result":1,"message":None}
threadA=threading.Thread(target=thread_A,args=(dict,))
threadB=threading.Thread(target=thread_B,args=(dict,))

threadA.start()
threadB.start()
