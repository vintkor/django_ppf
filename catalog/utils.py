class FileUtil(object):

    def __init__(self, obj):
        self.obj = obj

    def get_file_type(self):
        """
        Возврашает HTML изображение соответствующее типу файла
        :return: string
        """
        ext = self.obj.file.__str__().split('.')[1].lower()
        template = '<img class="file-icon" src="{}">'

        if ext == 'xls' or ext == 'xlsx':
            return template.format('//image.flaticon.com/icons/svg/136/136532.svg')

        if ext == 'pdf':
            return template.format('//image.flaticon.com/icons/svg/136/136522.svg')

        if ext == 'png':
            return template.format('//image.flaticon.com/icons/svg/136/136523.svg')

        if ext == 'jpg' or ext == 'jpeg':
            return template.format('//image.flaticon.com/icons/svg/136/136524.svg')

        if ext == 'svg':
            return template.format('//image.flaticon.com/icons/svg/136/136537.svg')

        if ext == 'zip':
            return template.format('//image.flaticon.com/icons/svg/136/136544.svg')

        if ext == 'ppt':
            return template.format('//image.flaticon.com/icons/svg/136/136543.svg')

        if ext == 'doc' or ext == 'docx' or ext == 'rtf':
            return template.format('//image.flaticon.com/icons/svg/136/136521.svg')

        if ext == 'mp3':
            return template.format('//image.flaticon.com/icons/svg/136/136548.svg')

        return template.format('//image.flaticon.com/icons/svg/136/136549.svg')