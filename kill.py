import psutil


def kill():
    print("clearing...")
    for proc in psutil.process_iter():
        if proc.name() == 'chrome.exe':
            proc.kill()
    print("chrome is killed!")