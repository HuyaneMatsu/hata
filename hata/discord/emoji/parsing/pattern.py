__all__ = ('EMOJI_ALL_RP',)

from re import compile as re_compile, escape as re_escape, U as re_unicode

from scarletio import call

from ...utils import EMOJI_RP

from ..unicode.unicodes import UNICODES


def trie_node_sort_key(node):
    """
    Sort key for trie nodes.
    
    Parameters
    ----------
    node : ``TrieNode``
        The node to get sort key of.
    
    Returns
    -------
    sort_key : `str`
    """
    character = node.character
    if character is None:
        character = ''
    
    return character


def escaped_string_iterator(string):
    """
    Regex escapes each character in a string and iterates over them.
    
    Parameters
    ----------
    string : `str`
        The string to iterate over.
    
    Yields
    ------
    escaped : `str`
    """
    for character in string:
        yield re_escape(character)


class TrieNode:
    """
    Represents a pattern node when building a pattern.
    
    Attributes
    ----------
    character : `None`, `str`
        The represented character.
    end : `bool`
        Whether self is end of a node.
    nodes : `None`, `dict` of (`str`, ``PatternNode``) items
        The nodes inheriting from self.
    """
    __slots__ = ('character', 'end', 'nodes')
    
    def __new__(cls, character):
        """
        Creates a new trie node.
        
        Parameters
        ----------
        character : `None`, `str`
            The represented character,
        """
        self = object.__new__(cls)
        self.character = character
        self.end = False
        self.nodes = None
        return self
    
    def has_length_1(self):
        """
        Returns whether length of self is 1.
        
        Returns
        -------
        has_length_1 : `bool`
        """
        if self.character is None:
            return False
        
        if self.nodes is not None:
            return False
        
        return True
    
    
    def extend_with_raw_string(self, string):
        """
        Extends self with the given string.
        
        Parameters
        ----------
        string : `str`
            The string to add to self.
        """
        return self.extend_with_escaped_iterator(escaped_string_iterator(string))
    
    
    def extend_with_escaped_iterator(self, iterator):
        """
        Extends the pattern with the given string iterator.
        
        Parameters
        ----------
        iterator : `GeneratorType`
            The iterator to walk through.
        """
        character = next(iterator, None)
        if character is None:
            self.end = True
            return
        
        nodes = self.nodes
        if nodes is None:
            nodes = {}
            self.nodes = nodes
        
        try:
            node = nodes[character]
        except KeyError:
            node = type(self)(character)
            nodes[character] = node
        
        node.extend_with_escaped_iterator(iterator)
    
    
    def build_into(self, into):
        """
        Builds self into the given list.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to extend with the pattern's parents.
        
        Returns
        -------
        into : `list` of `str`
        """
        character = self.character
        if (character is not None):
            into.append(character)
        
        nodes = self.nodes
        if (nodes is not None):
            nodes = sorted(nodes.values(), key = trie_node_sort_key)
            
            node_count = len(nodes)
            if node_count == 1:
                node = nodes[0]
                
                if node.has_length_1():
                    into = node.build_into(into)
                    if self.end:
                        into.append('?')
                else:
                    if self.end:
                        into.append('(?:')
                    
                    into = node.build_into(into)
                    
                    if self.end:
                        into.append(')?')
            
            else:
                into.append('(?:')
                
                node_index = 0
                
                while True:
                    node = nodes[node_index]
                    node_index += 1
                    
                    into = node.build_into(into)
                    
                    if node_index == node_count:
                        break
                    
                    into.append('|')
                    continue
                
                into.append(')')
                
                if self.end:
                    into.append('?')
        
        return into


EMOJI_ALL_RP = EMOJI_RP

@call
def build_all_emoji_pattern():
    """
    Builds an emoji matching pattern which matches not only the custom, but the custom emojis as well.
    
    Returns
    -------
    pattern : `re.Pattern`
    """
    global EMOJI_ALL_RP
    
    into = []
    into.append('(?:(')
    
    pattern_core = TrieNode(None)
    for unicode in UNICODES:
        pattern_core.extend_with_raw_string(unicode.value)
    pattern_core.build_into(into)
    pattern_core = None
    
    into.append(')|(?<!\\\\)\:(')
    
    pattern_core = TrieNode(None)
    for unicode in UNICODES:
        pattern_core.extend_with_raw_string(unicode.name)
        for alias in unicode.iter_aliases():
            pattern_core.extend_with_raw_string(alias)
    
    pattern_core.build_into(into)
    pattern_core = None
    
    into.append(')\:|')
    into.append(EMOJI_RP.pattern)
    into.append(')')
    
    EMOJI_ALL_RP = re_compile(''.join(into), re_unicode)
