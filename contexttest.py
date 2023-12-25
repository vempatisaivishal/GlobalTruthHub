import spacy
import re
from gingerit.gingerit import GingerIt
from subjectivemodel import subjective


class context:
    def __init__(self, text):
        self.text = text
        self.corrected_text = text
        self.own_corrections = {'iam': "i'm", 'im': "i'm"}

    def lower_case(self):
        pattern = re.compile("<.*?>")
        text = self.text
        text = pattern.sub(r'', text)
        pattern = re.compile(r'https?://\S+|www\.\S+')
        text = pattern.sub(r'', text)
        exclude = "[!\#\$%\&\(\)\*\+,\.\"/:;<=>\?@\[\\\\]\^_`\{\|\}\~0123456789]"
        return text.translate(str.maketrans('', '', exclude))

    def spelling_mistakes(self):
        text = self.text
        text = self.lower_case()

        nlp = spacy.load('en_core_web_lg')
        doc = nlp(text)
        misspelled_words = []
        parser = GingerIt()
        words = []

        named_entities = []
        [named_entities.extend(x) for x in [ent.text.lower().split(" ") for ent in doc.ents if ent.label_ == 'PERSON']]
        for token in doc:
            if token.is_alpha and token.text.lower() in self.own_corrections:
                words.append(self.own_corrections[token.text.lower()])
                misspelled_words.append(token.text)
            elif token.is_alpha and not token.text.lower() == parser.parse(token.text.lower())['result'].lower() and token.text.lower() not in named_entities:
                misspelled_words.append(token.text)
                words.append(parser.parse(token.text.lower())['result'])
            else:
                words.append(token.text.lower())

        if len(misspelled_words) == 0:
            return 0

        self.corrected_text = ' '.join(words)
        return len(set(misspelled_words)) / len(self.text.split(" "))

    def subjective_test(self):
        subjective_obj = subjective()
        answer = subjective_obj.send_request(self.corrected_text)
        return answer

    def run(self):
        print(self.spelling_mistakes())
        print(self.subjective_test())

