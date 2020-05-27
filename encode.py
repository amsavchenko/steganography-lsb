from PIL import Image



def encode_bits_in_carrier_image(image, message):
    message_with_len = format(len(message), '024b') + message
    image_max_capacity = (image.size[0] * image.size[1]) * 3
    if len(message_with_len) > image_max_capacity:
        raise ValueError('Изображение-переносчик недостаточно большое для такого количества информации')
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


def encode_string(string):
    res = ''.join(format(i, '08b') for i in bytearray(string, 'ascii'))
    res = '0' * (3 - (len(res) % 3)) + res
    return res


def encode():
    print('Введите путь до изображения в формате PNG:')
    path_to_carrier_image = input()
    while path_to_carrier_image.find('.png') == -1:
        print('Неправильный формат!\nВведите путь до изображения в формате PNG:')
        path_to_carrier_image = input()

    while True:
        try:
            carrier_image = Image.open(path_to_carrier_image).convert('RGB')
        except FileNotFoundError:
            print('Файл не найден!\nВведите путь до изображения в формате PNG:')
            path_to_carrier_image = input()
        else:
            break

    print('Введите текст сообщения:')
    secret_string = input()

    secret_message = encode_string(secret_string)
    try:
        carrier_image = encode_bits_in_carrier_image(carrier_image, secret_message)
    except ValueError as err:
        print(err)
        return

    path_to_encoded_image = f'{path_to_carrier_image[:-4]}_encoded.png'
    carrier_image.save(path_to_encoded_image)
    print(f'Успешно! Изображение сохранено в {path_to_encoded_image}')


if __name__ == "__main__":
    encode()