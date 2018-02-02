from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.callbacks import ModelCheckpoint
import numpy as np
import sys


class RNNTextGeneration:

    learning_data_root = 'data/learning/'
    models_root = learning_data_root+'models/'

    # Same as in the RNN function, has to be changed afterwards
    filename = learning_data_root+"raw_review.txt"
    raw_text = open(filename, encoding='utf-8').read()
    chars = sorted(list(set(raw_text)))

    # Info to check if we loaded the right file
    n_chars = len(raw_text)
    n_vocab = len(chars)
    print("Total Characters: ", n_chars)
    print("Total Vocab: ", n_vocab)

    int_to_char = dict((i, c) for i, c in enumerate(chars))
    char_to_int = dict((c, i) for i, c in enumerate(chars))

    dropoutRate = 0.4
    hiddenDim = 256

    # load the network weights
    filename = models_root+"weights-improvement-04-2.8221.hdf5"
    model = Sequential()
    model.add(LSTM(hiddenDim, input_shape=(100, 1), return_sequences=True))
    model.add(Dropout(dropoutRate))
    model.add(LSTM(hiddenDim))
    model.add(Dropout(dropoutRate))                 
    model.add(Dense(191, activation='softmax'))
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    # Prediction text pieces
    predictionTextPieces = ["good for lunch good for lunch good for lunch great for lunch great for lunch great for lunch lunch  ",
                            "great for dinner great for dinner great for dinner great for dinner great for dinner good for dinner",
                            "takes reservations takes reservations takes reservations takes reservations takes reservations res  ",
                            "outdoor seating outdoor seating outdoor seating outdoor seating outdoor seating outdoor outdoor seat",
                            "Unfortunately expensive Unfortunately expensive Unfortunately expensive Unfortunately expensive exp ",
                            "drink alcohol drink alcohol drink alcohol drink alcohol drink alcohol drink alcohol drink alcohol   ",
                            "table service table service table service table service table service table service table service   ",
                            "classy ambience classy ambience classy ambience classy ambience classy ambience classy ambience     ",
                            "good for kids great for family good for kids great for family good for kids great for family kids   "]

    def append_final_reviews(self, review):
        review_file = open(learning_data_root+"generated_reviews.txt", "a")
        review_file.write(review + "\n")

    def generate_text(self, predictions, threshold, length_of_sequence):
        complete_review = ""
        for i in range(predictions.shape[0]):
            if predictions[i] > threshold:
                predicted_text = self.generate_text_intern(self.predictionTextPieces[i], length_of_sequence)
                complete_review = complete_review + predicted_text
        self.append_final_reviews(complete_review)
        return complete_review
        # Adar maybe a safe function to append the complete review into a text file

    def generate_text_intern(self, sentence, length_of_sequence):
        # Turns the sentence into integer for the model
        pattern = [self.char_to_int[char] for char in sentence]
        for i in range(length_of_sequence):
            x = np.reshape(pattern, (1, len(pattern), 1))
            x = x / float(self.n_vocab)
            prediction = self.model.predict(x, verbose=0)
            index = np.argmax(prediction)
            result = self.int_to_char[index]
            seq_in = [self.int_to_char[value] for value in pattern]
            sys.stdout.write(result)
            pattern.append(index)
            pattern = pattern[1:len(pattern)]
        # Turns the prediction into readable text
        prediction_list = [self.int_to_char[value] for value in pattern]
        predicted_text = ''.join(map(str, prediction_list))
        return predicted_text

