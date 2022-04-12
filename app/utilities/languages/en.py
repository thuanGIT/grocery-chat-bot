import inflect

class EnglishUtil:

    # Static field for inflect engine
    __engine = inflect.engine()

    # Special cases of singlular ending with s
    __special_singular_suffix = {"is", "us", "ss"}

    @staticmethod
    def to_plurals(singular_noun: str):
        if singular_noun is None:
            raise TypeError("Parameter noun cannot be None!")
        elif EnglishUtil.is_plural(singular_noun):
            return singular_noun
        return EnglishUtil.__engine.plural_noun(singular_noun)

    @staticmethod
    def to_singular(plural_noun: str):
        if plural_noun is None:
            raise TypeError("Parameter noun cannot be None!")
        elif not EnglishUtil.is_plural(plural_noun):
            return EnglishUtil.__engine.singular_noun(plural_noun)
        return plural_noun
        
    @staticmethod
    def is_plural(noun):
        # Check if the noun is valid
        # Throw exception if not
        EnglishUtil.__check_valid_noun(noun) 
        suffix = noun[-2:] # Get the suffix (last 2 characters)
        if suffix[-1] == "s" and suffix not in EnglishUtil.__special_singular_suffix:
            return True
        return False

    @staticmethod
    def __check_valid_noun(noun):
        if noun is None:
            raise TypeError("Parameter noun cannot be None!")
        elif len(noun) < 2:
            raise TypeError("A character is not sufficient")