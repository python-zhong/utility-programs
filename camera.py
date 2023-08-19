import sys
sys.OpenCV_LOADER_DEBUG = True
import cv2
import cv2.data
import os
import functools
import tkinter
import tkinter.messagebox
import tkinter.filedialog
try:
    import ctypes; ctypes.oledll.shcore.SetProcessDpiAwareness(1)
except: pass
FILE_FORMATS = [
    # Portable Network Graphics Files
    '.png',
    # Windows Bitmap
    '.bmp', '.dib',
    # JPEG Files
    '.jpg', '.jpeg', '.jpe',
    # TIFF Files
    '.tiff', '.tif',
    # WebP Files
    '.webp',
    # Portable Image Format
    '.pbm', '.pgm', '.ppm', '.pxm', '.pnm',
    # OpenEXR Image Files
    '.exr',
    # Radiance HDR
    '.hdr', '.pic',
    # Sun Raster Files
    '.sr', '.ras'
]
VIDEO_FORMATS = [
    '.3g2', '.3gp', '.3gp2', '.3gpp',
    '.asf', '.asx', '.avi',
    '.dvr-ms',
    '.m1v', '.m2t', '.m2ts',
    '.m2v', '.m4v', '.mkv',
    '.mod', '.mov', '.mp2v',
    '.mp4', '.mp4v',
    '.mpe', '.mpeg', '.mpg', '.mpv2',
    '.ogm', '.ogv', '.ogx',
    '.tod', '.tts', '.uvu',
    'webm', '.wm', '.wmv', '.wmx', '.wvx']
FILE_FORMATS_NOTE = {
    'Portable Network Graphics Files': ['.png'],
    'Windows Bitmap': ['.bmp', '.dib'],
    'JPEG Files': ['.jpg', '.jpeg', '.jpe'],
    'TIFF Files': ['.tiff', '.tif'],
    'Webp Files': ['.webp'],
    'Portavle Image Format': ['.pbm', '.pgm', '.ppm', '.pxm', '.pnm'],
    'OpenEXR Image Files': ['.exr'],
    'Radiance HDR': ['.hdr', '.pic'],
    'Sun Raster Files': ['.sr', '.ras']
}
tk = tkinter.Tk(className='Camera.FileChooser')
tk.withdraw()
capture = cv2.VideoCapture(0)
writer = cv2.VideoWriter()
video_mode = False
video = None
cv2.putText = functools.partial(
    cv2.putText,
    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale=0.8,
    color=(255, 255, 255)
)
classifier = cv2.CascadeClassifier(
    os.path.join(
        cv2.data.haarcascades,
        'haarcascade_frontalface_default.xml'
    )
)
capture.setExceptionMode(True)
while True:
    try:
        result,  img = capture.read()
        if not capture.isOpened() or img is None or not bool(result):
            raise RuntimeError('')
    except Exception as e:
        tkinter.messagebox.showerror('ERROR', f'Failed to read from the camera:\n{"".join(e.args)}')
        break
    modified_img = img.copy()
    if not video_mode:
        detected = classifier.detectMultiScale(
            modified_img,
            minNeighbors=10,
            minSize=(150, 150),
            maxSize=(600, 600)
        )
        for x, y, w, h in detected:
            cv2.rectangle(modified_img, (x, y), (x+w, y+h), (0, 200, 200))
        cv2.rectangle(modified_img, (0, 0), (460, 95), (200, 0, 0), thickness=cv2.FILLED)
        cv2.putText(modified_img, "Press 'c' to capture.", (0, 25))
        cv2.putText(modified_img, "Press 'e' or 'q' to exit.", (0, 55))
        cv2.putText(modified_img, "Press 'v' to start recording a video.", (0, 85))
    else:
        cv2.rectangle(modified_img, (0, 0), (230, 60), (200, 0, 0), thickness=cv2.FILLED)
        cv2.putText(modified_img, "Recording ...", (0, 25))
        cv2.putText(modified_img, "Press 'f' to finish.", (0, 55))
        video.write(img)
    cv2.imshow('Image', modified_img)
    k = cv2.waitKey(1) & 0xFF
    if not video_mode:
        if k == ord('c'):
            while True:
                modified_img = img.copy()
                cv2.rectangle(modified_img, (0, 0), (250, 60), (200, 0, 0), thickness=cv2.FILLED)
                cv2.putText(modified_img, "Press 's' to save.", (0, 25))
                cv2.putText(modified_img, "Press 'c' to cancel.", (0, 55))
                cv2.imshow('Image', modified_img)
                k = cv2.waitKey(1) & 0xFF
                if k == ord('s'):
                    f = tkinter.filedialog.asksaveasfilename(
                        filetypes=[
                            ('All Supported Image Formats', FILE_FORMATS),
                            *tuple(FILE_FORMATS_NOTE.items())
                        ],
                        title='Save As ...'
                    )
                    if f:
                        cv2.imwrite(f, img)
                    if f:
                        break
                elif k == ord('c'):
                    break
        elif k == ord('q') or k == ord('e'):
            break
        elif k == ord('v'):
            f = tkinter.filedialog.asksaveasfilename(
                filetypes=[('All Supported Video Formats', VIDEO_FORMATS)],
                title='Save As ...'
            )
            if f:
                video = cv2.VideoWriter(
                    f,
                    -1,
                    int(capture.get(cv2.CAP_PROP_FPS)),
                    (
                        int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    ),
                    True
                )
                if not video.isOpened():
                    tkinter.messagebox.showerror('ERROR', 'Failed to create new video writer.')
                    video.release()
                    continue
                video_mode = True
    else:
        if k == ord('f'):
            video.release()
            video_mode = False
capture.release()
tk.destroy()
cv2.destroyAllWindows()