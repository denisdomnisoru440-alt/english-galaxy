import webbrowser, os, sys, http.server, socketserver, threading, json

if getattr(sys, 'frozen', False):
    base = sys._MEIPASS
else:
    base = os.path.dirname(os.path.abspath(__file__))

html_path = os.path.join(base, 'vocab.html')

# Try to open directly in browser (works with file://)
webbrowser.open('file://' + html_path)

# Keep process alive so the user knows it's running
print('English Galaxy opened in your browser.')
print('Press Ctrl+C to close.')
try:
    while True:
        import time
        time.sleep(1)
except KeyboardInterrupt:
    pass
