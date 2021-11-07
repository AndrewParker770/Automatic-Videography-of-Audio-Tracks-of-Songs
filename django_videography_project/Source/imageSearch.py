from google_images_search import GoogleImagesSearch


gis = GoogleImagesSearch('AIzaSyCdPQbeNMEt5SQFbcngbWHfwo2f5FsS2MY', '343f3550ca7267d54')

if __name__ == "__main__":
    imageSearch = sys.argv[1]

    _search_params = {
    'q': '{fname}'.format(fname=imageSearch),
    'num': 2,
    'safe': 'high',
    'fileType': 'png',
    }

    gis.search(search_params=_search_params, path_to_dir='ImageFiles/')
    