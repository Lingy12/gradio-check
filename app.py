import os
import gradio as gr
import numpy as np
from datasets import load_from_disk
import sys

os.environ['GRADIO_TEMP_DIR'] = './tmp'
# Path to the datasets and annotations directories
datasets_path = sys.argv[1]
port = sys.argv[2]
name = sys.argv[3]
print(datasets_path)
annotations_path = "./annotations"

annotations_path = os.path.join(annotations_path, name + '.txt')
# Function to load datasets

# Function to save annotations
def save_annotation(label, id, text, saving_path):
    # Code to save the annotation in the annotations folder
    labeled_set = set()
    with open(saving_path, 'a') as f:
        f.write(id + ',' + label + ',' + text + '\n')

    with open(saving_path, 'r') as f:
        lines = f.readlines()
        num_of_labels = len(lines)
        for line in lines:
            id, _,_ = line.split(',', maxsplit=2)
            labeled_set.add(id)
    print(label)
    selected_index = np.random.choice(len(ds))
    while selected_index in labeled_set:
        selected_index = np.random.choice((len(ds)))

    id = gr.Text(ds[selected_index]['UTT_ID'])
    text = gr.Text(ds[selected_index]['transcription'])

    audio = gr.Audio((ds[selected_index]['audio']['sampling_rate'], ds[selected_index]['audio']['array']))
    pg = gr.Text(f'{num_of_labels}/{len(ds)}')
    return id, text, audio, pg


# Loading datasets
ds = load_from_disk(datasets_path)
print(ds)
# Gradio Interface
with gr.Blocks(theme='soft') as demo:

    if os.path.exists(annotations_path):
        with open(annotations_path, 'r') as f:
            lines = f.readlines()
            num_of_labels = len(lines)
    else:
        num_of_labels = 0
    with gr.Row():
        gr.Text('You are annotating: ' + datasets_path, label='dataset path', show_label=True)
        path = gr.State(annotations_path)
        selected_index = np.random.choice(len(ds))
        id = gr.Textbox(ds[selected_index]['UTT_ID'], label='id', show_label=True)
        pg = gr.Text(f'{num_of_labels}/{len(ds)}', label='label progress', show_label=True)

    with gr.Row():
        text = gr.Text(ds[selected_index]['transcription'], label='transcription', show_label=True,interactive=True )
        audio = gr.Audio((ds[selected_index]['audio']['sampling_rate'], ds[selected_index]['audio']['array']))

    with gr.Row():
        valid_btn = gr.Button('Valid')
        invalid_btn = gr.Button('Invalid')

    valid_btn.click(fn=save_annotation, inputs=[valid_btn, id, text, path], outputs=[id, text, audio, pg])
    invalid_btn.click(fn=save_annotation, inputs=[invalid_btn, id, text, path], outputs=[id, text, audio, pg])


#demo.queue()
demo.launch(server_name='0.0.0.0',server_port=int(port),share=False)
