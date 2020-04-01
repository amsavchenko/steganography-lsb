from PIL import Image

path_to_encoded_image = 'encoded_image.png'


def decode_bits_from_image(image):
    length = ''
    for j in range(8):
        r, g, b = image.getpixel((0, j))
        length += format(r, '08b')[-1] + format(g, '08b')[-1] + format(b, '08b')[-1]
    length = int(length, 2)
    secure_message = ''
    for j in range(8, image.size[1]):
        r, g, b = image.getpixel((0, j))
        secure_message += format(r, '08b')[-1] + format(g, '08b')[-1] + format(b, '08b')[-1]
        length -= 3
        if length == 0:
            return secure_message
    for i in range(1, image.size[0]):
        for j in range(image.size[1]):
            r, g, b = image.getpixel((i, j))
            secure_message += format(r, '08b')[-1] + format(g, '08b')[-1] + format(b, '08b')[-1]
            length -= 3
            if length == 0:
                return secure_message


def decode_string(string):
    if len(string) % 8 != 0:
        amount_of_nonleading_zeroes = len(string) - 8 * (len(string) // 8)
        string = string[amount_of_nonleading_zeroes:]
    result = ''
    for i in range(len(string) // 8):
        result += chr(int(string[8*i:8*(i+1)], 2))
    return result


def decode():
    encoded_image = Image.open(path_to_encoded_image).convert("RGB")
    secure_bits = decode_bits_from_image(encoded_image)
    secure_message = decode_string(secure_bits)
    print(secure_message)


if __name__ == "__main__":
    decode()