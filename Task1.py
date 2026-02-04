# Exploring Pseduo-Randomness and Collision Resistance
from Crypto.Random import get_random_bytes
from hashlib import sha256
import time
import matplotlib.pyplot as plt
import csv

# part a)
def hash_input(s):
    # turn the str into bytes for sha 256
    b = s.encode("utf-8")

    # hash and output to hex
    hash_sha = sha256(b).hexdigest()

    return hash_sha

# part b)

# to count how many bytes differ between two digests

def byte_diff_count(hex1, hex2):
    d1 = bytes.fromhex(hex1)
    d2 = bytes.fromhex(hex2)
    return sum(x != y for x, y in zip(d1, d2))

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
        print("difference in bytes between,", byte_diff_count(hash_1, hash_2))

    else:
        raise ValueError("Hamming distance is not 1!")

    return (hash_1, hash_2)

# part c)

# truncate first n bits to make collisions more likely to happen
def trunc_sha256_bits(data, n):
    d = sha256(data).digest()
    x = int.from_bytes(d, "big")
    return x >> (256 - n) # keep top n bits

# weak collision
def find_collision(m0, nbits, msg_len):
    start = time.time()

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
            end = time.time()
            return m0, m1, tries, target, (end - start)
        
# birthday problem
def birthday_collision(nbits, msg_len):
    start = time.time()
    tries = 1
    m0 = get_random_bytes(msg_len)
    seen = {}

    first = trunc_sha256_bits(m0, nbits)
    seen[first] = m0

    while True:
        m1 = get_random_bytes(msg_len)
        h1 = trunc_sha256_bits(m1, nbits)
        tries += 1

        prev = seen.get(h1)
        if prev is not None and prev != m1:
            end = time.time()
            return prev, m1, tries, h1, (end - start)
        else:
            seen[h1] = m1



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

    # # weak collision
    # m0, m1, tries, target, elapsed = find_collision(get_random_bytes(16), 20, 16)
    # print("m0 is: ",m0)
    # print("m0 sha256:", sha256(m0).hexdigest())
    # print("m1 is: ",m1)
    # print("m1 sha256:", sha256(m1).hexdigest())
    # print("target hash: ",target)
    # print("found hash:", trunc_sha256_bits(m1, 15))
    # print("amount of tries: ",tries)
    # print("time taken: ",elapsed)

    # # birthday collision
    # m0, m1, tries, hash_1, elapsed = birthday_collision(15, 16)
    # print("m0 is: ",m0)
    # print("m0 sha256:", sha256(m0).hexdigest())
    # print("m1 is: ",m1)
    # print("m1 sha256:", sha256(m1).hexdigest())
    # print("amount of tries: ",tries)
    # print("hash found matching", hash_1)
    # print("time taken: ",elapsed)

    # # graphs
    #     # graphs (birthday method): bits -> time and bits -> inputs
    # bit_sizes = list(range(8, 51, 2))  # 8, 10, ..., 50
    # times = []
    # inputs = []

    # for nbits in bit_sizes:
    #     print(f"\nRunning birthday collision for {nbits} bits...")
    #     m0, m1, tries, h, elapsed = birthday_collision(nbits, 16)  # msg_len=16
    #     inputs.append(tries)
    #     times.append(elapsed)
    #     print(f"  tries={tries}, time={elapsed:.4f}s, truncated_hash={h}")

    # # Graph 1: digest size vs collision time
    # plt.figure()
    # plt.plot(bit_sizes, times, marker="o")
    # plt.xlabel("Digest size (bits)")
    # plt.ylabel("Collision time (seconds)")
    # plt.title("Digest size vs collision time (Birthday attack)")
    # plt.grid(True)
    # plt.show()

    # # Graph 2: digest size vs number of inputs
    # plt.figure()
    # plt.plot(bit_sizes, inputs, marker="o")
    # plt.xlabel("Digest size (bits)")
    # plt.ylabel("Inputs until collision")
    # plt.title("Digest size vs inputs until collision (Birthday attack)")
    # plt.grid(True)
    # plt.show()


    return None


if __name__ == "__main__":
    main()