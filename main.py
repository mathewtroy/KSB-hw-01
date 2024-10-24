# 1. Caesar Cipher
def caesar_cipher(text, shift=-3):
    """
        Decrypts a text encrypted using Caesar Cipher with a given shift.

        Parameters:
        - text: The encrypted text
        - shift: The number of positions each letter is shifted (default is -3)

        Returns:
        - Decrypted text
    """
    decrypted = []
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.isupper():
                if shifted < ord('A'):
                    shifted += 26
                elif shifted > ord('Z'):
                    shifted -= 26
                decrypted.append(chr(shifted))
            else:
                decrypted.append(char)
        else:
            decrypted.append(char)
    return ''.join(decrypted)


# 2. Simple Shift Cipher
def simple_shift_cipher(text):
    """
        Attempts to decrypt a text using all possible shift values (1-26).

        Parameters:
        - text: The encrypted text

        Returns:
        - A list of tuples with (shift_value, decrypted_text) for each possible shift
    """
    decrypted_texts = []
    for shift in range(1, 27):
        decrypted = ''
        for char in text:
            if char.isalpha():
                if char.isupper():
                    shifted = (ord(char) - ord('A') + shift) % 26 + ord('A')
                    decrypted += chr(shifted)
                elif char.islower():
                    shifted = (ord(char) - ord('a') + shift) % 26 + ord('a')
                    decrypted += chr(shifted)
            else:
                decrypted += char
        decrypted_texts.append((shift, decrypted))
    return decrypted_texts


# 3. Affine Cipher
def affine_cipher_decrypt(text):
    """
        Attempts to decrypt a text using Affine Cipher by trying all possible values of 'a' and 'b'.

        Parameters:
        - text: The encrypted text

        Returns:
        - A list of tuples with (a_value, b_value, decrypted_text) for each possible combination of 'a' and 'b'
    """
    from math import gcd

    decrypted_texts = []

    # All possible values of 'a', coprime with 26
    valid_a = [a for a in range(1, 26) if gcd(a, 26) == 1]

    # Function to compute the multiplicative inverse modulo 26
    def modinv(a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None  # No inverse if a and m are not coprime

    # Iterate through all combinations of 'a' and 'b'
    for a in valid_a:
        a_inv = modinv(a, 26)
        for b in range(0, 26):
            decrypted = ''
            for char in text:
                if char.isalpha():
                    y = ord(char.upper()) - ord('A')
                    x = (a_inv * (y - b)) % 26
                    decrypted += chr(x + ord('A'))
                else:
                    decrypted += char
            decrypted_texts.append((a, b, decrypted))
    return decrypted_texts


# 4. Substitution Cipher with a keyword
def create_substitution_alphabet(keyword):
    """
        Creates a substitution alphabet based on a keyword.

        Parameters:
        - keyword: The keyword to build the substitution alphabet

        Returns:
        - A dictionary mapping original alphabet letters to substitution letters
    """
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    key_letters = []

    # Remove duplicates in the keyword and create the substitution list
    for char in keyword.upper():
        if char not in key_letters:
            key_letters.append(char)

    # Create substitution alphabet starting with the keyword letters
    substitution_alphabet = key_letters.copy()

    # Add remaining letters of the alphabet
    for char in alphabet:
        if char not in substitution_alphabet:
            substitution_alphabet.append(char)

    return dict(zip(alphabet, substitution_alphabet))


def decrypt_with_keyword(text, keyword):
    """
        Decrypts a text encrypted using a substitution cipher with a given keyword.

        Parameters:
        - text: The encrypted text
        - keyword: The keyword used to build the substitution alphabet

        Returns:
        - Decrypted text
    """
    substitution_alphabet = create_substitution_alphabet(keyword)

    # Invert the substitution dictionary for decryption
    inverse_substitution_alphabet = {v: k for k, v in substitution_alphabet.items()}

    decrypted = []
    for char in text:
        if char.isalpha() and char.isupper():
            decrypted.append(inverse_substitution_alphabet[char])
        else:
            decrypted.append(char)

    return ''.join(decrypted)


def try_decrypt_with_popular_words(text):
    """
        Attempts to decrypt a text using a list of popular keywords for a substitution cipher.

        Parameters:
        - text: The encrypted text

        Prints:
        - Possible decrypted texts that contain common words
    """
    # List of popular keywords for encryption
    popular_keywords = [
        "PASSWORD", "SECRET", "HELLO", "WORLD", "MYSTERY", "KEYWORD", "ENCRYPT", "DECRYPT", "HIDDEN", "LOCKED",
        "ACCESS", "ACCOUNT", "ACTION", "ADVENTURE", "AGENT", "ALERT", "ALPHA", "AMAZING", "ANSWER", "APPLE",
        "ARMOR", "ARROW", "ASSASSIN", "ATTACK", "AURORA", "AUTOMATIC", "AZURE", "BACKUP", "BANDIT", "BATTLE",
        "BEACON", "BEAUTY", "BEHIND", "BLACK", "BLADE", "BLAST", "BLAZE", "BLIND", "BLOCK", "BLOOD", "BLUE",
        "BRAIN", "BRAVE", "BREAK", "BRIDGE", "BULLET", "BURN", "CALIBER", "CAPTAIN", "CATCH", "CHAMPION",
        "CHARGE", "CHASE", "CIPHER", "CIRCLE", "CLASH", "CODE", "COLLISION", "COMMAND", "CONTROL", "CORE",
        "CRASH", "CRYPTO", "CYBER", "DANGER", "DARK", "DATA", "DEAD", "DELTA", "DESTROY", "DEVICE", "DIAL",
        "DIGITAL", "DINO", "DISCOVERY", "DISK", "DRAGON", "DRIVE", "EAGLE", "ECHO", "ELEMENT", "ELEVATE",
        "EMPIRE", "ENERGY", "ENGAGE", "ENTER", "EXCALIBUR", "EXPLORE", "EXPRESS", "FALCON", "FIRE", "FLASH",
        "FLUX", "FORCE", "FURY", "GALAXY", "GAMMA", "GENESIS", "GHOST", "GLASS", "GLOBAL", "GOLD", "GRAVITY",
        "GREEN", "GUARD", "HACKER", "HALO", "HAVOC", "HAWK", "HERO", "HORIZON", "HYDRA", "IMPACT", "INFINITY",
        "INSIGHT", "INVADER", "IRON", "JACKAL", "JAGUAR", "JET", "JUMP", "KILLER", "KING", "KNIGHT", "LASER",
        "LEGEND", "LIGHT", "LOCK", "LORD", "MAGIC", "MAJOR", "MATRIX", "MERCURY", "METAL", "MIRROR", "MONSTER",
        "MOON", "MOTION", "NANO", "NEXUS", "NIGHT", "NOVA", "NUTRON", "OMEGA", "ONYX", "ORBIT", "ORION",
        "PANIC", "PHANTOM", "PHOENIX", "PIRATE", "PLASMA", "PLUTO", "POWER", "PRIME", "PROTON", "PYTHON",
        "QUANTUM", "QUEST", "RAGE", "RAPTOR", "RED", "RELIC", "RIDER", "RIOT", "ROBOT", "ROCKET", "RUSH",
        "SATURN", "SAVAGE", "SCAR", "SCORPION", "SHADOW", "SHIELD", "SHOCK", "SIGNAL", "SILVER", "SLASH",
        "SNAP", "SPARK", "SPEED", "SPHERE", "SPIRIT", "STORM", "STRIKE", "SUN", "SUPER", "SURGE", "SWIFT",
        "SYSTEM", "TALON", "TANGO", "TANK", "TERRA", "TETRA", "TITAN", "TORCH", "TRACK", "TRAITOR", "TRIGGER",
        "TROJAN", "ULTRA", "VAMPIRE", "VECTOR", "VEGA", "VENGEANCE", "VENOM", "VIPER", "VIRUS", "VOID",
        "VOLCANO", "VORTEX", "WARRIOR", "WAVE", "WIDOW", "WILD", "WIND", "WING", "WOLF", "XENON", "YELLOW",
        "ZEBRA", "ZENITH", "ZERO", "ZODIAC", "ABILITY", "ACTION", "BALANCE", "BEAUTY", "BRIGHT", "CALM",
        "CHANCE", "CHARM", "CHIEF", "CHOICE", "CLEAN", "CLEAR", "CONTROL", "CREATE", "DARING", "DREAM",
        "DRIVE", "EARN", "EASY", "ENERGY", "ESCAPE", "EXCITE", "FINE", "FOCUS", "FORCE", "FORWARD", "FREE",
        "FRESH", "FRONT", "GAIN", "GATHER", "GENIUS", "GIFT", "GRACE", "GRAND", "GUIDE", "HEART", "HONOR",
        "HOPE", "IMPACT", "INSPIRE", "JOURNEY", "JOY", "LEAD", "LEARN", "LIMIT", "LOVE", "LUCK", "MASTER",
        "MOVE", "MYSTERY", "NATURAL", "NEED", "OPTIMISM", "PATH", "PEACE", "PERFECT", "PLAN", "POWERFUL",
        "PRECISE", "PROUD", "RAPID", "RARE", "REAL", "READY", "REASON", "REFLECT", "RESOLVE", "RESULT",
        "RICH", "SAFE", "SCALE", "SEARCH", "SHARE", "SHINE", "SKILL", "SMART", "SMILE", "SOLVE", "SOLID",
        "SPARK", "SPECIAL", "STAND", "STEADY", "STRONG", "SUCCESS", "SURE", "TALENT", "THRIVE", "TOP", "TRUE",
        "TRUST", "UNITY", "UPLIFT", "VALUE", "VICTORY", "VIVID", "VISION", "WARM", "WISE", "WORTH", "ZENITH",

        # password
        "SAZEB",
    ]

    # List of common words to help identify correct decryption
    common_words = ['THE', 'AND', 'THAT', 'WITH', 'THIS', 'HAVE', 'FROM', 'YOUR', 'NOT', 'BUT', 'ALL', 'FORM', 'TION',
                    'NION']

    for keyword in popular_keywords:
        decrypted_text = decrypt_with_keyword(text, keyword)

        # Check if the decrypted text contains common words
        if any(word in decrypted_text for word in common_words):
            print(f"Possible match with keyword '{keyword}':")
            print(decrypted_text)
            print("\n")


if __name__ == "__main__":
    caesar_text = "FUBSWRJUDSKLF NHBV DUH DQDORJRXV WR WKH KRXVH DQG FDU NHBV ZH FDUUB LQ RXU GDLOB OLYHV DQG VHUYH D VLPLODU SXUSRVH"
    simple_shift_text = "VEH IYCFBYSYJO DEHCQB CUIIQWU JUNJ IXQBB RU SQBBUT FBQYD JUNJ QDT JXU UDSHOFJUT VEHC SYFXUH JUNJ"
    affine_text = "ZFA KAQG ZI VA SGAH CNA IVZCYPAH TNIW C KAQ GISNOA EFYOF GADAOZG ZFAW BANFCBG NCPHIWDQ TNIW ZFA DCNMA GAZ IT CDD SGCVDA KAQG"
    substitution_text = "GLNTAJGZIBXQXQRBKQSQGLKMQRCMPKQMCZPXNRMDPSNFXSNGBZBMCGLCMPKSRGMLZSJJBESIBXGQTQBERMRPSLQCMPKKBQQSDBGLRMZPXNRGZCMPK"

    # Caesar Cipher
    print("\n----------------------------------------------------------------------")
    print("1) Caesar Cipher:")
    print(caesar_cipher(caesar_text))

    """
    Encrypted text:
    
    FUBSWRJUDSKLF NHBV DUH DQDORJRXV WR WKH KRXVH DQG FDU NHBV 
    ZH FDUUB LQ RXU GDLOB OLYHV DQG VHUYH D VLPLODU SXUSRVH
    
    ---------------------------------------------------------
    Decrypted text:
    
    CRYPTOGRAPHIC KEYS ARE ANALOGOUS TO THE HOUSE AND CAR KEYS 
    WE CARRY IN OUR DAILY LIVES AND SERVE A SIMILAR PURPOSE

    """

    # Simple Shift Cipher
    print("\n----------------------------------------------------------------------")
    print("2) Simple Shift Cipher:")
    decrypted_texts = simple_shift_cipher(simple_shift_text)
    common_words = ['THE', 'AND', 'THAT', 'WILL', 'THAN', 'WAS', 'ARE']

    for shift, decrypted in decrypted_texts:
        if any(word in decrypted for word in common_words):
            print(f"Shift {shift}:\n{decrypted}\n")

    """
    Encrypted text:

    VEH IYCFBYSYJO DEHCQB CUIIQWU JUNJ IXQBB RU SQBBUT FBQYD JUNJ QDT 
    JXU UDSHOFJUT VEHC SYFXUH JUNJ
    
    ---------------------------------------------------------
    Decrypted text:
    
    FOR SIMPLICITY NORMAL MESSAGE TEXT SHALL BE CALLED PLAIN TEXT AND 
    THE ENCRYPTED FORM CIPHER TEXT

    """

    # Affine Cipher
    print("\n----------------------------------------------------------------------")
    print("3) Affine Cipher:")
    decrypted_texts = affine_cipher_decrypt(affine_text)

    for a, b, decrypted in decrypted_texts:
        if any(word in decrypted for word in common_words):
            print(f"a = {a}, b = {b}:\n{decrypted}\n")

    """
    Encrypted text:
    
    ZFA KAQG ZI VA SGAH CNA IVZCYPAH TNIW C KAQ GISNOA EFYOF GADAOZG ZFAW 
    BANFCBG NCPHIWDQ TNIW ZFA DCNMA GAZ IT CDD SGCVDA KAQG
    
    ---------------------------------------------------------
    Decrypted text:
    
    THE KEYS TO BE USED ARE OBTAINED FROM A KEY SOURCE WHICH SELECTS THEM 
    PERHAPS RANDOMLY FROM THE LARGE SET OF ALL USABLE KEYS

    """


    # Substitution Cipher with keyword
    print("\n----------------------------------------------------------------------")
    print("4) Substitution Cipher with a keyword:")
    print("\nTrying to decrypt using popular keywords:")
    try_decrypt_with_popular_words(substitution_text)

    """
    Encrypted text:
    
    gl ntajgz ibx qxqrbkq sq
    gl kmqr cmpkq mc
    zpxnrmdpsnfx s
    ngbzb mc 
    glcmpksrml zsjjbe
    s ibx gqtqbe rm rpslqcmpk
    kbqqsdb glrm zpxnrgz cmpk
    
    ---------------------------------------------------------
    Decrypted text:
    
    in public key systems as
    in most forms of 
    cryptography a
    piece of
    informaton called
    a key isused to transform
    message into cryptic form
    
    """


    # known_mapping = {
    #     'Z': 'C',
    #     'P': 'R',
    #     'X': 'Y',
    #     'N': 'P',
    #     'R': 'T',
    #     'M': 'O',
    #     'D': 'G',
    #     'S': 'A',
    #     'F': 'H'
    # }
