import requests
import sys
import TOR.tor

def Progress_Download(*args, **kwargs):
    response = Plain_Get(*args,stream=True,**kwargs,verify=False)
    length = response.headers.get('content-length')
    if length == None:
        return None
    else:
        download_length = 0
        total_length = int(length)
        file = b""
        for data in response.iter_content(chunk_size=4096):
            download_length += len(data)
            file += data
            done = int(50 * download_length / total_length)
            sys.stdout.write(f"\r{total_length} [{'=' * done}{' '*(50 - done)}]")
            sys.stdout.flush()
        print("")
    return file

def Plain_Get(*args, **kwargs):
    """Wrapper to force get requests"""
    request_worked = False
    # You will download!
    while request_worked == False:
        try:
            response = requests.get(*args,**kwargs)
            request_worked = True
        except Exception as e:
            print(f"Error performing Get request: {e}")
            print("Changing TOR Node")
            TOR.tor.main()
    return response

def Plain_Head(*args, **kwargs):
    """Wrapper to force head requests"""
    request_worked = False
    # You will download!
    while request_worked == False:
        try:
            response = requests.get(*args,**kwargs)
            request_worked = True
        except Exception as e:
            print(f"Error performing Head request: {e}")
            print("Changing TOR Node")
            TOR.tor.main()
    return response

def Plain_Post(*args, **kwargs):
    """Wrapper to force post requests"""
    request_worked = False
    # You will download!
    while request_worked == False:
        try:
            response = requests.get(*args,**kwargs)
            request_worked = True
        except Exception as e:
            print(f"Error performing Post request: {e}")
            print("Changing TOR Node")
            TOR.tor.main()
    return response

        
