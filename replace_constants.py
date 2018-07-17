import tokenizer
import utils
import re


vars = set()
new_def = []


def replace_constants(source):
    lines = tokenizer.tokenize_file(source)
    lines = replace_constant_var_num(lines)
    lines = replace_constant_while(lines)
    lines = replace_constant_for(lines)

    pattern = 'import\s+\w+\s*'
    for index, line in enumerate(lines):
        if re.search(pattern, line) is None:
            break

    for block in new_def:
        lines.insert(index, block)
        index += 1

    return lines


def replace_constant_var_num(lines):
    for index, line in enumerate(lines):
        line_tokenized = tokenizer.tokenize_line(line)
        if is_var_num(line):
            constant = get_constant(line_tokenized)
            if constant is not None:
                if constant <= 100000000000:
                    if is_prime(constant):
                        # inject factorization
                        random_function_name = utils.get_random_var(vars)
                        lines[index] = replace(line_tokenized, random_function_name, constant)
                        new_def.append(generate_factorization_function(random_function_name))

    return lines


def is_var_num(line):
    pattern = '\s*\w+\s*=\s*\d+'
    if re.search(pattern, line) is not None:
        return True
    return False


def replace_constant_while(lines):
    for index, line in enumerate(lines):
        line_tokenized = tokenizer.tokenize_line(line)
        if is_while(line):
            constant = get_constant(line_tokenized)
            if constant is not None and constant <= 100000000000:
                # inject factorization
                random_function_name = utils.get_random_var(vars)
                lines[index] = replace_while(line_tokenized, random_function_name, constant)
                new_def.append(generate_factorization_function(random_function_name))

    return lines


def is_while(line):
    pattern = '\s*while\s*\(\s*\w+[\<\>\!=]\w+\):'
    if re.search(pattern, line) is not None:
        return True
    return False


def get_constant(tokens):
    for token in tokens:
        try:
            i = int(token[1])
            return i
        except:
            continue
    return None


def replace_constant_for(lines):
    for index, line in enumerate(lines):
        line_tokenized = tokenizer.tokenize_line(line)
        if is_for(line):
            spec = get_for_spec(line_tokenized)
            if is_a_integer(spec['end']):
                if int(spec['end']) <= 100000000000:
                    # inject factorization
                    random_function_name = utils.get_random_var(vars)
                    lines[index] = replace_for(line_tokenized, spec, random_function_name)
                    new_def.append(generate_factorization_function(random_function_name))

    return lines


def is_for(line):
    pattern = '\s*for\s*\w+\s*in\s*range\(\d+,\d+\):'
    if re.search(pattern, line) is not None:
        return True
    return False


# for var in range(num,num):
def get_for_spec(tokens):
    spec = {}
    for i in range(0, len(tokens)):
        if tokens[i][1] == 'for':
            spec['var'] = tokens[i+1][1]
            spec['start'] = tokens[i + 5][1]
            spec['end'] = tokens[i + 7][1]
    return spec


def replace_for(tokens, spec, function_name):
    line = ' ' * get_indentation(tokens, 'for')
    line += 'for ' + spec['var'] + ' in range(' + spec['start'] + ','
    line += function_name + '(' + str(spec['end']) + ')):\n'

    return line


def replace(tokens, function_name, num):
    line = ''
    for token in tokens:
        line += token[1]
        if token[1] == '=':
            break

    line += ' ' + function_name + '(' + str(num) + ')\n'
    return line


def replace_while(tokens, function_name, num):
    line = ' ' * get_indentation(tokens, 'while')
    line += 'while('
    var_name, op = get_while_spec(tokens)
    line += var_name
    line += op
    line += function_name + '(' + str(num) + ')):\n'

    return line


def get_indentation(tokens, construct):
    if construct == 'while':
        for token in tokens:
            if token[1] == 'while':
                return token[2][1]
    if construct == 'for':
        for token in tokens:
            if token[1] == 'for':
                return token[2][1]
    return 0


def get_while_spec(tokens):
    for i in range(0, len(tokens)):
        if tokens[i][1] == '(':
            return (tokens[i+1][1], tokens[i+2][1])
    return None


def generate_factorization_function(function_name):
    random_var_while = utils.get_random_var(vars)
    vars.add(random_var_while)

    random_var_par = utils.get_random_var(vars)
    vars.add(random_var_par)
    random_var_for = utils.get_random_var(vars)
    vars.add(random_var_for)

    block = 'def ' + function_name + '(' + random_var_par + '):\n'

    res = utils.get_random_var(vars)
    vars.add(res)
    block += ' ' * utils.SPACE_NUM
    block += res
    block += '=1\n'

    block += ' ' * utils.SPACE_NUM
    block += 'while ' + random_var_par + '>1:\n'

    block += ' ' * (utils.SPACE_NUM * 2)
    block += 'for ' + random_var_for + ' in range(2,' + random_var_par + '+1):\n'

    block += ' ' * (utils.SPACE_NUM * 3)
    block += 'if ' + random_var_par + '%' + random_var_for + '==0:\n'

    block += ' ' * (utils.SPACE_NUM * 4)
    block += random_var_par + '//=' + random_var_for + '\n'

    block += ' ' * (utils.SPACE_NUM * 4)
    block += res + '*=' + random_var_for + '\n'

    block += ' ' * (utils.SPACE_NUM * 4)
    block += 'break\n'

    block += ' ' * (utils.SPACE_NUM * 1)
    block += 'return ' + res + '\n'

    return block


def is_a_integer(str):
    try:
        num = int(str)
        return True
    except:
        return False

def is_prime(n):
    '''check if integer n is a prime'''

    # make sure n is a positive integer
    n = abs(int(n))

    # 0 and 1 are not primes
    if n < 2:
        return False

    # 2 is the only even prime number
    if n == 2:
        return True

    # all other even numbers are not primes
    if not n & 1:
        return False

    # range starts with 3 and only needs to go up
    # the square root of n for all odd numbers
    for x in range(3, int(n**0.5) + 1, 2):
        if n % x == 0:
            return False

    return True











