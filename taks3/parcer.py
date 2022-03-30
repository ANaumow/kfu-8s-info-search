import re
import string

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

    def eval(self, index, html_file):
        if self.word in index:
            return html_file in index[self.word]
        else:
            return False


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
    if tokens[0] in string.ascii_lowercase:
        a = re.findall(r'(\w+)', ''.join(tokens))

        for x in range(len(a[0])):
            tokens.pop(0)

        return WordNode(a[0])

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
