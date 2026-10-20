"""
DPCM (Differential Pulse Code Modulation)

Implement the functions encode(), decode() and distortion().
Everything else is already given and does not need to be changed.

Run with:  python dpcm.py
"""

from pathlib import Path

# Input/output files are resolved relative to this script, so the program
# works regardless of the current working directory.
BASE_DIR = Path(__file__).resolve().parent
IN_FILE = BASE_DIR / "sequence.csv"
OUT_FILE = BASE_DIR / "dpcm_seq.csv"


def main():
    """Nothing needs to be changed here."""
    # parse input values
    input_values = parse_values(IN_FILE)
    print("Input:\t", end="")
    print_array(input_values)

    # encode values with DPCM
    output_values = encode(input_values)
    print("Encoded:", end="")
    print_array(output_values)

    # save encoded values as csv file
    save_to_file(OUT_FILE, output_values)

    # parse encoded values from csv file
    encoded_values = parse_values(OUT_FILE)

    # decode DPCM values
    reconstructed_values = decode(encoded_values)
    print("Decoded:", end="")
    print_array(reconstructed_values)

    # calculate distortion
    print("Distortion: {:.2f}".format(distortion(reconstructed_values, input_values)))


def parse_values(filename):
    """
    Parses integer values from a csv file.

    :param filename: the file to read from
    :return: list of parsed integer values
    """
    with open(filename, "r") as f:
        content = ",".join(line.strip() for line in f if line.strip())
    return [int(v) for v in content.split(",")]


def encode(values: list[int]) -> list[int]:
    """
    Encodes a sequence of input values with DPCM.

    Referring to the last exercise, the input sequence are the f_n values.
    The e~_n values should be returned.

    Attention: The first returned value has to be the original value from
    the input sequence.

    :param values: list of raw input values (int)
    :return: list of DPCM encoded values (int)
    """
    # 1. Calculate f^_n
    first_value = trunc(values[0])
    encoded: list[int] = [first_value]
    reconstructed_values: list[int] = [first_value]

    # The first value of the encoded sequence is the original value f1
    for i in range(1, len(values)):
        value = values[i]

        # simple case: i = 1 -> use the first value for f_n - 1 and f_n - 2
        prev_value = prev_prev_value = first_value
        if i > 1:
            prev_value = reconstructed_values[i - 1]
            prev_prev_value = reconstructed_values[i - 2]

        predicted_value = trunc(float(prev_value + prev_prev_value) / 2)
        error_value = value - predicted_value
        quantized_error = quantize_error(error_value)

        encoded.append(quantized_error)

        reconstructed_value = predicted_value + quantized_error
        reconstructed_values.append(reconstructed_value)

    # return list of quantized errors
    return encoded

    #Calculate the error e_n = f_n - f^_n

def trunc(value: float | int) -> int:
    return int(value)

def quantize_error(value: int) -> int:
    return 16 * trunc((255 + value) / 16) - 256 + 8

def save_to_file(out_file, output_values):
    """
    Saves integer values into a csv file.

    :param out_file: name of the file
    :param output_values: the values to store
    """
    with open(out_file, "w") as f:
        f.write(",".join(str(v) for v in output_values))


def decode(encoded_values: list[int]) -> list[int]:
    """
    Decodes DPCM-encoded values.

    This function should transform the encoded e~_n values to f~_n values.

    :param encoded_values: list of DPCM encoded values (int)
    :return: list of decoded values (int)
    """
    first_value = trunc(encoded_values[0])
    reconstructed_values: list[int] = [first_value]

    for i in range(1, len(encoded_values)):
        # simple case: i = 1 => use the first value for f(n-1) and f(n-2)
        prev_value = prev_prev_value = first_value
        if i > 1:
            prev_value = reconstructed_values[i - 1]
            prev_prev_value = reconstructed_values[i - 2]

        predicted_value = trunc((prev_value + prev_prev_value) / 2)
        error_value = encoded_values[i]

        reconstructed_value = predicted_value + error_value
        reconstructed_values.append(reconstructed_value)

    return reconstructed_values


def distortion(recon_values: list[int], orig_values: list[int]) -> float:
    """
    Calculates the distortion between the reconstructed and the original values.

    :param recon_values: list of decoded values
    :param orig_values: list of original values
    :return: the distortion (average squared error) as float
    """
    squared_error_sum: int = 0
    for i in range(len(recon_values)):
        squared_error_sum += (recon_values[i] - orig_values[i]) ** 2

    return float(squared_error_sum) / len(recon_values)


def print_array(arr):
    """
    Prints a list of integers to the console.

    :param arr: the list to print
    """
    print("".join("{:4d} ".format(v) for v in arr))


if __name__ == "__main__":
    main()
