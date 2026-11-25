import itertools
import json
import math
from fractions import Fraction


def multiply(left, right):
    size = len(left)
    return [[sum(left[row][inner] * right[inner][column] for inner in range(size))
             for column in range(size)] for row in range(size)]


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def transfer(adjacency, word):
    size = len(adjacency)
    result = [[int(row == column) for column in range(size)] for row in range(size)]
    backward = transpose(adjacency)
    for sign in word:
        result = multiply(result, adjacency if sign == '+' else backward)
    return result


def total(matrix):
    return sum(map(sum, matrix))


def flips(word):
    return sum(left != right for left, right in zip(word, word[1:]))


def reflected(word):
    return ''.join('-' if sign == '+' else '+' for sign in word[::-1])


def tournaments(size):
    pairs = list(itertools.combinations(range(size), 2))
    for bits in itertools.product([0, 1], repeat=len(pairs)):
        adjacency = [[0] * size for row in range(size)]
        for (left, right), bit in zip(pairs, bits):
            adjacency[left][right] = bit
            adjacency[right][left] = 1 - bit
        yield adjacency


def permutation_count(word):
    counts = [1]
    for sign in word:
        prefix = [0]
        for count in counts:
            prefix.append(prefix[-1] + count)
        counts = [prefix[rank] if sign == '+' else prefix[-1] - prefix[rank]
                  for rank in range(len(counts) + 1)]
    return sum(counts)


def descent_count(word):
    vertices = len(word) + 1
    descents = [index + 1 for index, sign in enumerate(word) if sign == '-']
    result = 0
    for mask in range(2 ** len(descents)):
        selected = [position for index, position in enumerate(descents) if mask & (1 << index)]
        boundaries = [0] + selected + [vertices]
        denominator = math.prod(math.factorial(right - left)
                                for left, right in zip(boundaries, boundaries[1:]))
        result += (-1) ** (len(descents) - len(selected)) * math.factorial(vertices) // denominator
    return result


def permutation_witness():
    prefix = '++--' * 4 + '++'
    count19 = permutation_count(prefix)
    count20 = permutation_count(prefix + '-')
    assert count19 == 908138776681
    assert count20 == 13194844482843
    word = prefix + '+'
    count = 20 * count19 - count20
    assert count == permutation_count(word) == descent_count(word) == 4967931050777
    assert permutation_count('++--++--++') == descent_count('++--++--++') == 45541
    assert flips(word) == 8 and len(word) == 19
    assert Fraction(flips(word) + 1, len(word)) == Fraction(9, 19)
    vertices = 4096
    injective = count * math.comb(vertices, 20)
    numerator = 2 ** len(word) * injective
    denominator = vertices ** 20
    assert numerator > denominator
    return {'word': word, 'edges': len(word), 'flips': flips(word),
            'periodic_prefix_counts': {'a(19)': count19, 'a(20)': count20},
            'signature_permutations': count, 'independent_methods': ['last-rank recurrence', 'descent inclusion-exclusion'],
            'continuous_scaled_numerator': 2 ** len(word) * count,
            'continuous_scaled_denominator': math.factorial(20),
            'host': 'transitive tournament', 'vertices': vertices,
            'injective_homomorphisms': injective,
            'scaled_density_lower_bound_numerator': numerator,
            'scaled_density_lower_bound_denominator': denominator,
            'positive_integer_gap': numerator - denominator, 'limit_upper_bound': '9/19'}


def main():
    finite_cases = 0
    direct_cases = 0
    tournament_count = 0
    for size in range(1, 5):
        for adjacency in tournaments(size):
            tournament_count += 1
            for length in range(0, 7):
                for signs in itertools.product('+-', repeat=length):
                    word = ''.join(signs)
                    matrix = transfer(adjacency, word)
                    reflected_matrix = transfer(adjacency, reflected(word))
                    assert reflected_matrix == transpose(matrix)
                    assert transfer(adjacency, word + reflected(word)) == multiply(matrix, transpose(matrix))
                    q = Fraction(2 ** length * total(matrix), size ** (length + 1))
                    doubled = multiply(matrix, transpose(matrix))
                    scaled_mass = Fraction(2 ** (2 * length) * total(doubled), size ** (2 * length + 1))
                    assert scaled_mass >= q * q
                    extensions = [transfer(adjacency, word + sign) for sign in '+-']
                    assert total(extensions[0]) + total(extensions[1]) == (size - 1) * total(matrix)
                    if length:
                        for repeats in range(1, 5):
                            assert flips((word + reflected(word)) * repeats) == 2 * repeats * (flips(word) + 1) - 1
                    if size <= 3 and length <= 4:
                        count = 0
                        for mapping in itertools.product(range(size), repeat=length + 1):
                            count += all(adjacency[mapping[index]][mapping[index + 1]]
                                         if sign == '+' else adjacency[mapping[index + 1]][mapping[index]]
                                         for index, sign in enumerate(word))
                        assert count == total(matrix)
                        direct_cases += 1
                    finite_cases += 1
    size = 128
    word = '++--++--++'
    counts = [1] * size
    totals = [sum(counts)]
    for sign in word:
        prefix = [0]
        for count in counts:
            prefix.append(prefix[-1] + count)
        counts = [prefix[column] if sign == '+' else prefix[-1] - prefix[column + 1]
                  for column in range(size)]
        totals.append(sum(counts))
    homomorphisms = sum(counts)
    adjacency = [[int(row < column) for column in range(size)] for row in range(size)]
    assert homomorphisms == total(transfer(adjacency, word))
    assert homomorphisms == 158125066372222954176
    gap = 2 ** len(word) * homomorphisms - size ** (len(word) + 1)
    assert gap == 10804340513327658237952
    assert gap > 0 and flips(word) == 4
    result = {
        'arithmetic': 'exact integers and rational numbers',
        'finite_identities': {'tournament_orders': [1, 2, 3, 4], 'labelled_tournaments': tournament_count,
                              'word_lengths': [0, 6], 'cases': finite_cases,
                              'reflected_word_repetition_counts': [1, 4],
                              'direct_map_comparison_orders': [1, 2, 3],
                              'direct_map_word_lengths': [0, 4], 'direct_map_cases': direct_cases,
                              'identities': ['reflection', 'reflected-pair transfer', 'Cauchy lower bound',
                                             'one-edge extension sum', 'repeated reflected-word flip count']},
        'non_TAS_witness': {'host': 'transitive tournament', 'vertices': size, 'word': word,
                            'flips': flips(word), 'homomorphisms': homomorphisms,
                            'prefix_homomorphism_totals': totals,
                            'scaled_density_numerator': 2 ** len(word) * homomorphisms,
                            'scaled_density_denominator': size ** (len(word) + 1),
                            'positive_integer_gap': gap, 'limit_upper_bound': '1/2'},
        'permutation_witness': permutation_witness(),
        'coverage': 'Finite transfer identities, permutation counts and explicit witnesses; the all-length limit has a written proof.'
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
