import requests

def download_image(image_url, name, max_retries=3):
    for attempt in range(max_retries):
        print(image_url)
        response = requests.get(image_url, stream=True)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            if content_type.startswith('image/'):
                image_format = content_type.split('/')[1]
                filename = f'CERT/img/{name}.{image_format}'
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f'Image downloaded successfully: {filename}')
                return image_format
            else:
                print('Invalid image format')
                return False
        else:
            print(f'Failed to download user\'s photo from Google Drive. Retrying...')
            

    print(f'Failed after {max_retries} attempts. Unable to download user\'s photo.')
    return False