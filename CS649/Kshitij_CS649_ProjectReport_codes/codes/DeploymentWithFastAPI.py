from fastapi import FastAPI
import tensorflow as tf
import numpy as np
import pickle
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StructType, StructField, IntegerType, StringType
from numpy.random import choice

from mido import Message, MidiFile, MidiTrack

spark = SparkSession.builder.getOrCreate()

app = FastAPI()

with open(r"./X_rdd.pickle", "rb") as input_file:
   X_rdd = pickle.load(input_file)

with open(r"./y_rdd.pickle", "rb") as input_file:
   y_rdd = pickle.load(input_file)

x=X_rdd.map(lambda x: x).collect()
y=y_rdd.map(lambda x: x).collect()[0]

def tune_to_midi(tune, midi_name='new_tune', debug_mode=False):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    for note in tune:
        if debug_mode:
            track.append(Message('note_on', note=note, time=64))
            track.append(Message('note_off', note=note, time=128))
        else:
            track.append(Message('note_on', note=note['note'], velocity=note['velocity'], time=note['time']))
            track.append(Message('note_off', note=note['note'], time=note['pause']))

    mid.save(midi_name + '.mid')

def tune_generator(model):
    for i in range(3):
        start = np.random.randint(0, len(X)-1)
        pattern = X[start]
        prediction_output = []

        for note_index in range(100):
            prediction_input = np.reshape(pattern, (1, len(pattern), 3))
            prediction = model.predict(prediction_input, verbose=0)
            prediction_output.append(prediction.astype(int)[0])
            pattern = np.append(pattern, prediction, axis = 0)
            pattern = pattern[1:len(pattern)]

        notes = spark.DataFrame(prediction_output, columns=['time', 'note', 'velocity'])
        notes['pause'] = 180
        notes_dict = notes.to_dict('records')
        tune_to_midi(notes_dict, midi_name=name + str(i))
        

# Load the pre-trained TensorFlow model
model = tf.keras.models.load_model('./lstm.h5')

@app.post("/generate_tune")
def generate_tune():
    # Generate a tune using the tune_generator function
    tune_generator(model, name='generated_tune')

    return {"message": "Tune generated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
