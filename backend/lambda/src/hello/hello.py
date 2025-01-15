import PIL.Image


def handler(event, _):
    greeting = f"Hello {event['name']}!"
    new_image = PIL.Image.new("RGB", (60, 30), color = "red")
    print(greeting)
    print(new_image.size)
    return {"greeting" : greeting}
