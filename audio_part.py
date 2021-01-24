import speech_recognition as sr
# import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def convert():
    r = sr.Recognizer()

    with sr.AudioFile("G:\\third.wav") as source:
        r.adjust_for_ambient_noise(source)
        print("Converting Audio To Text and saving to file..... ")
        audio = r.listen(source)
    try:
        value = r.recognize_google(audio)
        # os.remove("record.wav")
        if str is bytes:
            result = u"{}".format(value).encode("utf-8")
        else:
            result = "{}".format(value)

        with open("test.txt", "a") as f:
            f.write(result)
            f.write(" ")
            f.close()

    except sr.UnknownValueError:
        print("")
    except sr.RequestError as e:
        print("{0}".format(e))
    except KeyboardInterrupt:
        pass


def common_member(a, b):
    a_set = set(a)
    b_set = set(b)

    if len(a_set.intersection(b_set)) > 0:
        return a_set.intersection(b_set)
    else:
        return[]


def record_audio(status):

    convert()

    with open("test.txt", 'r') as file:
        data = file.read()

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(data)
    filtered_sentence = [
        w for w in word_tokens if w not in stop_words
    ]

    with open('final.txt', 'w') as f:
        for word in filtered_sentence:
            f.write(word + ' ')

    with open("paper.txt", 'r') as file:
        data = file.read()
    word_tokens = word_tokenize(data)
    filtered_questions = [
        w for w in word_tokens if w not in stop_words
    ]

    comm = common_member(filtered_questions, filtered_sentence)
    print('Number of common elements:', len(comm))

    with open("common_words.txt", 'r') as file:
        data = file.read()

    common_word = [w for w in word_tokenize(data)]

    if len(common_word) > 0:
        with open("common_words.txt", 'a') as file:
            union = comm.union(set(common_word))
            for w in list(union):
                file.write(w + ' ')
    else:
        with open("common_words.txt", 'a') as file:
            for w in list(comm):
                file.write(w + ' ')

    status.value = 1
