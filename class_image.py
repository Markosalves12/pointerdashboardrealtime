class Image:
    def __init__(self, path_svg = str(), height=int(), width=int()):
        self.path_svg = path_svg
        self.height = height
        self.width = width

    def open_image(self):
        with open(self.path_svg, "r") as file:
            image_svg = file.read()
        return image_svg
