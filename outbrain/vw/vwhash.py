

def mmh2all(word, base):
    raise NotImplementedError
def mmh2str(word, base):
    raise NotImplementedError
def mmh3all(word, base):
    raise NotImplementedError
def mmh3str(word, base):
    raise NotImplementedError


def truncate_feature(feature, num_bits):
    return feature & ((1 << num_bits) - 1)


class VWHasher(object):
    '''
    Class for hashing feature names.
    Resulting hash values are identical to the ones obtained by vw.
    '''
    QUADRATIC_CONSTANT = 27942141
    HASH_BASE = 97562527

    def __init__(self, hash_type='str', num_bits=None, version='mmh2'):
        '''
        hash_type - all - hash all factors, str - hash non-digit factors
        num_bits - max number of bits, should be same as the value used for learning vw
        '''

        self._type = hash_type
        self._num_bits = num_bits
        self._mask = (1 << num_bits) - 1

        if version == 'mmh3':
            self.HASH_BASE = 0

        if self._type == 'all':
            self.hash_word = mmh3all if version == 'mmh3' else mmh2all
        elif self._type == 'str':
            self.hash_word = mmh3str if version == 'mmh3' else mmh2str
        else:
            raise ValueError('wrong hash type specified')

    def __call__(self, word, namespace=None, second_word=None, second_namespace=None):
        return self.hash_feature(word, namespace=namespace, second_word=second_word,
            second_namespace=second_namespace)

    def hash_feature(self, word, namespace=None, second_word=None, second_namespace=None):

        feature_hash = None
        if second_word is None:
            namespace_hash = 0
            if namespace:
                namespace_hash = self.hash_word(namespace, self.HASH_BASE)

            word_hash = self.hash_word(word, namespace_hash)
            feature_hash = word_hash & self._mask
        else:
            namespace_hash = self.hash_word(namespace, self.HASH_BASE)
            second_namespace_hash = self.hash_word(second_namespace, self.HASH_BASE)
            first_hash = self.hash_word(word, namespace_hash)
            second_hash = self.hash_word(second_word, second_namespace_hash)
            feature_hash = (first_hash * self.QUADRATIC_CONSTANT + second_hash) & self._mask

        return feature_hash
