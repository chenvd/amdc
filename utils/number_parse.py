import re

from meta.number import NumberMeta

extensions = ['mp4', 'avi', 'rmvb', 'mkv']


def parse(file_name):
    file_name = file_name.replace('_', '-').lower()
    pattern = re.compile(r"([a-z]{3,})-?(\d{3,})((-uncensored|-leak)*)-?(ch|uc|c|u|)?-?\w*\.(\w+)")
    matched = pattern.search(file_name)
    if matched:
        groups = matched.groups()
        number = f'{groups[0]}-{groups[1]}'.upper()
        extension = groups[5]

        if extension not in extensions:
            return None

        meta = NumberMeta(number, extension)

        if groups[3]:
            parts = groups[3].split("-")
            if 'leak' in parts:
                meta.is_leak = True
            if 'uncensored' in parts:
                meta.is_uncensored = True

        if groups[4]:
            if groups[4] == 'ch' or groups[4] == 'c':
                meta.is_ch = True
            if groups[4] == 'uc':
                meta.is_ch = True
                meta.is_uncensored = True
            if groups[4] == 'u':
                meta.is_uncensored = True

        meta.file_name = meta.num + ("-C" if meta.is_ch else "")

        return meta


if __name__ == '__main__':
    pass
