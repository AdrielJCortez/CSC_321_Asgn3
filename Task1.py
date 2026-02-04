# Exploring Pseduo-Randomness and Collision Resistance
from Crypto.Random import get_random_bytes
from hashlib import sha256

# part a)
def hash_input(s):
    # turn the str into bytes for sha 256
    b = s.encode("utf-8")

    # hash and output to hex
    hash_sha = sha256(b).hexdigest()

    return hash_sha

# part b)

# flip a bit to get a guarnteed change of hamming distance of 1
def flip_one_bit_at(b, bit_index):
    ba = bytearray(b)
    byte_i = bit_index // 8
    print("byte_i: ", byte_i)
    bit_i = bit_index % 8
    print("bit i: ", bit_i)
    ba[byte_i] ^= (1 << bit_i)
    return bytes(ba)

# calculate the hamming distance
def hamming_d(b1, b2):
    if len(b1) != len(b2):
        raise ValueError("Inputs must be same len")
    
    distance = 0
    for x, y in zip(b1, b2):
        distance += bin(x ^ y).count("1")

    return distance

# need to hash two strings w hamming distance being exactly one
def hash_two(str1, i):
    b1 = str1.encode("utf-8")
    b2 = flip_one_bit_at(b1, i)

    bits1 = ''.join(f'{byte:08b}' for byte in b1)
    bits2 = ''.join(f'{byte:08b}' for byte in b2)

    print(bits1)
    print(bits2)

    ham_d = hamming_d(b1, b2)
    print("hamming distance", ham_d)

    if ham_d == 1:
        hash_1 = sha256(b1).hexdigest()
        hash_2 = sha256(b2).hexdigest()

    else:
        raise ValueError("Hamming distance is not 1!")

    
    return (hash_1, hash_2)

# part c)

# truncate first n bits to make collisions more likely to happen
def trunc_sha256_bits(data, n):
    d = sha256(data).digest()
    x = int.from_bytes(d, "big")
    return x >> (256 - n) # keep top n bits

def find_collision(str1, nbits, msg_len):
    m0 = str1.encode("utf-8")

    # hash then truncate
    target = trunc_sha256_bits(m0, nbits)
    
    tries = 0
    while True:
        m1 = get_random_bytes(msg_len)
        tries += 1
        if m1 == m0:
            continue
        attempt = trunc_sha256_bits(m1, nbits)

        if attempt == target:
            return m0, m1, tries, target

def main():
    # Part a)
    # Hash a single user input
    user_input = input("Enter a string (Part a): ")
    h = hash_input(user_input)
    print(h)

    # Part b)

    # Hash two strings whose hamming distance is exactly 1
    string1 = input("Please enter str1 (Part b): ")
    for i in range(3):
        print(f"take {i + 1} of hash two:")
        h1, h2 = hash_two(string1, i)
        print("hash1: ", h1)
        print("hash2: ", h2)


    # part c)
    stringc = input("Please enter string (part c): ")
    max_num_bits = int(input("enter a max number of bits: "))
    m0, m1, target, tries = find_collision(stringc, max_num_bits, 16)
    print("m0 is: ",m0)
    print("m0 sha256:", sha256(m0).hexdigest())
    print("m1 is: ",m1)
    print("m1 sha256:", sha256(m1).hexdigest())
    print("target hash: ",target)
    print("found hash:", trunc_sha256_bits(m1, max_num_bits))
    print("amount of tries: ",tries)

    return None


if __name__ == "__main__":
    main()