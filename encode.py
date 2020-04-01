from PIL import Image

secret_message = '101101010101010110001111111'
path_to_carrier_image = 'carrier.png'
path_to_secret_image = 'secret_message.png'


def encode_bits_in_carrier_image(image, message):
    message_with_len = format(len(message), '024b') + message
    image_max_capacity = (image.size[0] * image.size[1]) * 3
    if len(message_with_len) > image_max_capacity:
        raise ValueError('Изображение-переносчик недостаточно большое для такого кол-ва информации')
    return change_bits(image, message_with_len)


def change_bits(image, message):
    pixels = image.load()
    counter_of_encoded_bits = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b = pixels[i, j]

            r_byte = format(r, '08b')
            r_byte = int(r_byte[:-1] + message[counter_of_encoded_bits], 2)
            counter_of_encoded_bits += 1

            g_byte = format(g, '08b')
            g_byte = int(g_byte[:-1] + message[counter_of_encoded_bits], 2)
            counter_of_encoded_bits += 1

            b_byte = format(b, '08b')
            b_byte = int(b_byte[:-1] + message[counter_of_encoded_bits], 2)
            counter_of_encoded_bits += 1

            pixels[i, j] = (r_byte, g_byte, b_byte)
            if counter_of_encoded_bits == len(message):
                return image


def transfer_image_to_bits(image):
    result = ''
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b = pixels[i, j]
            result += format(r, '08b') + format(g, '08b') + format(b, '08b')
    return result


def encode_string(string):
    res = ''.join(format(i, '08b') for i in bytearray(string, 'ascii'))
    res = '0' * (3 - (len(res) % 3)) + res
    return res


def encode():
    carrier_image = Image.open(path_to_carrier_image).convert('RGB')
    secret_string = 'Hello! It is test of stegonography algorithm Least Significant Bit by ' \
                    'students Rudik Maxim and Savchenko Anton of b17-505 study group'
    secret_message = encode_string(secret_string)
    carrier_image = encode_bits_in_carrier_image(carrier_image, secret_message)
    carrier_image.save('encoded_image.png')


if __name__ == "__main__":
    encode()