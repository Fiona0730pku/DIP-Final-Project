# DIP Final Project

## Description

A project on ticket serial number detection and recognition.

My program identifies single digits by sending them through a network graph with parameters trained on TensorFlow, and will load the graph during each inference.

## Dataset

The dataset I use to train single digit recognition is the Chars74K dataset: http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/.

As numbers on tickets are all printed in a fixed format, I use only part of the dataset: 62992 synthesised characters from the computer to do the training task.

##Run the model

Filenames are read from `annotation.txt` and images are loaded from `./train_data` directory

Make sure to change `annotation.txt` in `read_write_text.py` and `./train_data` in `crop.py` if any of these two are altered during test session.

It is also necessary to modify the `checkpoints` file in `model_dump_10`(10 numbers)and`model_dump_62`(10 numbers and 26 uppercase and lowercase alphabets). `model_checkpoint_path:"/.../model_dump_xx/model.ckpt-xxx"`should be changed into the correct local path, and the same thing should also be done to `all_model_checkpoint_paths`.

Make sure `segments` directory and `prediction.txt` are created in the local directory in order to save segmented images and recognition result of single digits.

Then we can run the whole program by running

```python
$ python3 main.py
```

## Environment

- TensorFlow 1.12.0
- Python 3.6.5