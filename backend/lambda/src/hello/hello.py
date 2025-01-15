def handler(event, context):
    greeting = f"Hello!"
    print(greeting)
    return {"greeting" : greeting}
