import threading
import time
from datetime import datetime
from queue import SimpleQueue
from PIL import Image, ImageTk
import argparse
from vimba import Vimba# from vimba import Vimba


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--time", help="Tiempo en milisegundos tras cada captura de frame")
parser.add_argument("-s", "--sleep", help="Tiempo en segundos de descanso tras cada captura de frame", default=0)
parser.add_argument("-q", "--quantity", help="Cantidad de fotos a tomar")
parser.add_argument("-p", "--path", help="ruta donde se guardarán las fotografías")
parser.add_argument("-n", "--name", help="Nombre de las fotografías (<name>_number_hh:mm:ss_dd-mm-yy)")

args = parser.parse_args()
counter = 1

def timestamp():
    date = datetime.now().strftime("%d-%m-%y_%H:%M:%S")
    return date
if args.quantity:
    try:
        cantidad = int(args.quantity)
        error = False
    except:
        error = True
else:
    cantidad = None

if args.time and args.path and not(error):
    with Vimba.get_instance() as vimba:
        with vimba.get_all_cameras()[0] as camera:
            frames = camera.get_frame_generator(limit=cantidad, timeout_ms=int(args.time))
            for frame in frames:
                if not args.name:
                    filename = 'image_'+str(counter)+"_"+timestamp()
                else:
                    filename = str(args.name)+"_"+str(counter)+"_"+timestamp()
                counter += 1
                frame_array = frame.as_opencv_image()
                image = Image.fromarray(frame_array)
                image.save(str(args.path)+filename)
                time.sleep(int(args.time))
