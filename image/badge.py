import cv2 as cv


def tags(fan_art, meta):
    thumb = fan_art.copy()

    index = 0
    if meta.is_ch:
        tag = cv.imread("./image/ch.png")
        thumb = add_badges(thumb, tag, index)
        index += 1

    if meta.is_leak:
        tag = cv.imread("./image/leak.png")
        thumb = add_badges(thumb, tag, index)
        index += 1

    if meta.is_uncensored:
        tag = cv.imread("./image/uncensored.png")
        thumb = add_badges(thumb, tag, index)
        index += 1

    return thumb


def add_badges(thumb, tag, index):
    thumb_size = thumb.shape

    badge_height = int((35 / 538) * thumb_size[0])
    badge_width = int(badge_height * 2)

    tag = cv.resize(tag, (badge_width, badge_height))

    badge_step = int((5 / 538) * thumb_size[0])

    top = badge_step + (badge_step + badge_height) * index
    bottom = top + badge_height

    left = badge_step
    right = left + badge_width

    dest = thumb[top:bottom, left:right]
    result = cv.addWeighted(tag, 1, dest, 0, 0)
    thumb[top:bottom, left:right] = result

    return thumb
