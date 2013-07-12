

class ImageGalleryItem:
    """ A single item in an image gallery (or carousel)"""

    def __init__(self, image, title=None, description=None):
        self.image = image
        self.title = title
        self.description = description
