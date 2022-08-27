import requests
import sys

def Progress_Download(*args, **kwargs):
    response = requests.get(*args,stream=True,**kwargs)
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
