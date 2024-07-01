#!/usr/bin/env python

import gradio as gr

from settings import (
    DEFAULT_IMAGE_RESOLUTION,
    DEFAULT_NUM_IMAGES,
    MAX_IMAGE_RESOLUTION,
    MAX_NUM_IMAGES,
    MAX_SEED,
)
from utils import randomize_seed_fn

examples = [
    [
        "images/canny/canny_demo.jpg",
        "BEAUTIFUL PORTRAIT PAINTINGS BY EMMA UBER",
    ],
    [
        "images/canny/canny_demo2.jpg",
        "Serious Dog Portraits",
    ],
    [
        "images/canny/canny_demo3.jpg",
        "Cheese and Nuts.Oil on Linen.27x46cm. Private Collection",
    ],
]

def create_demo(process):
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                image = gr.Image()
                prompt = gr.Textbox(label="Prompt")
                run_button = gr.Button("Run")
                with gr.Accordion("Advanced options", open=False):
                    num_samples = gr.Slider(
                        label="Number of images", minimum=1, maximum=MAX_NUM_IMAGES, value=DEFAULT_NUM_IMAGES, step=1
                    )
                    image_resolution = gr.Slider(
                        label="Image resolution",
                        minimum=256,
                        maximum=MAX_IMAGE_RESOLUTION,
                        value=DEFAULT_IMAGE_RESOLUTION,
                        step=256,
                    )
                    canny_low_threshold = gr.Slider(
                        label="Canny low threshold", minimum=0, maximum=1.0, value=0.1, step=0.05
                    )
                    canny_high_threshold = gr.Slider(
                        label="Canny high threshold", minimum=0, maximum=1.0, value=0.2, step=0.05
                    )
                    num_steps = gr.Slider(label="Number of steps", minimum=1, maximum=100, value=20, step=1)
                    guidance_scale = gr.Slider(label="Guidance scale", minimum=0.1, maximum=30.0, value=7.5, step=0.1)
                    seed = gr.Slider(label="Seed", minimum=0, maximum=MAX_SEED, step=1, value=0)
                    randomize_seed = gr.Checkbox(label="Randomize seed", value=True)
                    a_prompt = gr.Textbox(label="Additional prompt", value="high-quality, extremely detailed, 4K")
                    n_prompt = gr.Textbox(
                        label="Negative prompt",
                        value="longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality",
                    )
            with gr.Column():
                result = gr.Gallery(label="Output", show_label=False, columns=2, object_fit="scale-down")

        gr.Examples(
            examples=examples,
            inputs=[
                image,
                prompt,
                guidance_scale,
                seed,
            ],
            outputs=result,
            fn=process,
        )

        inputs = [
            image,
            prompt,
            a_prompt,
            n_prompt,
            num_samples,
            image_resolution,
            num_steps,
            guidance_scale,
            seed,
            canny_low_threshold,
            canny_high_threshold,
        ]
        prompt.submit(
            fn=randomize_seed_fn,
            inputs=[seed, randomize_seed],
            outputs=seed,
            queue=False,
            api_name=False,
        ).then(
            fn=process,
            inputs=inputs,
            outputs=result,
            api_name=False,
        )
        run_button.click(
            fn=randomize_seed_fn,
            inputs=[seed, randomize_seed],
            outputs=seed,
            queue=False,
            api_name=False,
        ).then(
            fn=process,
            inputs=inputs,
            outputs=result,
            api_name="canny",
        )
    return demo


if __name__ == "__main__":
    from model import Model

    model = Model(task_name="Canny")
    demo = create_demo(model.process_canny)
    demo.queue().launch()
