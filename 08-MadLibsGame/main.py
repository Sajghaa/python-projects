def minimal_madlibs():
    print("Simple Mad Libs")

    adjective = input("Adjective: ")
    noun1 = input("Noun: ")
    verb = input("Verb: ")
    noun2 = input("Noun: ")
    adverb = input("Adverb: ")

    story =f"""
one day, a {adjective} {noun1} decided to {verb} to the {noun2}. 
It {verb}ed very{adverb} and had a great adventure!"""
    
    print("\n Your Story: ")
    print(story)

if __name__ == "__main__":
    minimal_madlibs()