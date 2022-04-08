import re

class Node:
    def eval(self, index, current_item) -> bool:
        pass


class AndNode(Node):

    def __init__(self, left: Node, right: Node):
        super().__init__()
        self.left = left
        self.right = right

    def eval(self, index, current_item):
        return self.left.eval(index, current_item) and self.right.eval(index, current_item)


class OrNode(Node):

    def __init__(self, left: Node, right: Node):
        super().__init__()
        self.left = left
        self.right = right

    def eval(self, index, current_item):
        return self.left.eval(index, current_item) or self.right.eval(index, current_item)


class WordNode(Node):

    def __init__(self, word):
        super().__init__()
        self.word = word

    def eval(self, index, article_to_check):
        # это лемма из запроса
        lemma = self.word

        if lemma in index:
            articles_with_lemma = index[lemma]
            # проверям - отсеевать ли эту статью
            return article_to_check in articles_with_lemma
        else:
            return False

class NotNode(Node):

    def __init__(self, nested: Node):
        super().__init__()
        self.nested = nested

    def eval(self, index, current_item) -> bool:
        return not self.nested.eval(index, current_item)


def __parse_lvl_1(tokens):
    left_node = __parse_lvl_2(tokens)

    if len(tokens) > 0:

        if tokens[0] == '|':
            tokens.pop(0)
            right_node = __parse_lvl_1(tokens)
            return OrNode(left_node, right_node)

    return left_node


def __parse_lvl_2(tokens):
    left_node = __parse_lvl_3(tokens)

    if len(tokens) > 0:
        if tokens[0] == '&':
            tokens.pop(0)
            right_node = __parse_lvl_2(tokens)
            return AndNode(left_node, right_node)


    return left_node

def __parse_lvl_3(tokens) -> Node:
    if tokens[0] in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
        a = re.findall(r'([а-я]+)', ''.join(tokens))

        for x in range(len(a[0])):
            tokens.pop(0)

        return WordNode(a[0])

    if tokens[0] == '!':
        tokens.pop(0)
        return NotNode(__parse_lvl_1(tokens))

    if tokens[0] == '(':
        tokens.pop(0)

    node = __parse_lvl_1(tokens)

    if tokens[0] == ')':
        tokens.pop(0)

    return node

def parse(query: str) -> Node:
    return __parse_lvl_1([x for x in query.replace(" ", "")])


# if __name__ == '__main__':
#     index = []
#     current_item = ''
#
#     root_node = __parse_lvl_1([x for x in "(asdfas&sdfsd)|asdfsdf"])
#
#     print(root_node)
