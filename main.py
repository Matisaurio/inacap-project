import threading
import time
from queue import SimpleQueue
import tkinter as tk
from PIL import Image, ImageTk
from vimba import Vimba

def camera_streaming():
    global is_streaming
    global camera
    is_streaming = True
    print("streaming started")
    with Vimba.get_instance() as vimba:
        with vimba.get_all_cameras()[0] as cam:
            c = 1
            for frame in cam.get_frame_generator(limit=10):
                im = Image.fromarray(frame.as_opencv_image()).resize((500, 400), Image.ANTIALIAS)
                im.save("ImagePy({}).png".format(c))
                c += 1
                image = ImageTk.PhotoImage(im)
                lblVideo.config(image=image)
                lblVideo.image = image
                time.sleep(0.05)
            print("streaming stopped")

def start_streaming():
    start_btn["state"] = "disabled" # disable start button to avoid running the threaded task more than once
    stop_btn["state"] = "normal"    # enable stop button to allow user to stop the threaded task
    threading.Thread(target=camera_streaming).start()

def stop_streaming():
    global is_streaming, after_id
    is_streaming = False  # terminate the streaming thread
    if after_id:
        lblVideo.after_cancel(after_id) # cancel the showing task
        after_id = None
    stop_btn["state"] = "disabled" # disable stop button
    start_btn["state"] = "normal"  # enable start button

# periodical task to show frames in queue

queue = SimpleQueue() # queue for video frames
after_id = None

root = tk.Tk()

lblVideo = tk.Label(root, image=tk.PhotoImage(), width=640, height=480)
lblVideo.grid(row=0, column=0, columnspan=2)

start_btn = tk.Button(root, text="Start", width=10, command=start_streaming)
start_btn.grid(row=1, column=0)

stop_btn = tk.Button(root, text="Stop", width=10, command=stop_streaming, state="disabled")
stop_btn.grid(row=1, column=1)


root.mainloop()
