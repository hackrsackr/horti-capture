from picamera2 import Picamera2


# picam2: Picamera2 = Picamera2(tuning=Picamera2.load_tuning_file("imx477.json"))
picam2: Picamera2 = Picamera2(tuning=Picamera2.load_tuning_file("imx477_noir.json"))
# picam2: Picamera2 = Picamera2(tuning=Picamera2.load_tuning_file("imx477_scientific.json"))
config: dict = picam2.create_preview_configuration(main={"size": (800, 600)})
# preview: Preview = Preview.DRM


# picam2.start_preview(preview)
picam2.start(config=config, show_preview=False)

request = picam2.capture_request()
request.save("main", "image.jpg")
request.release()
