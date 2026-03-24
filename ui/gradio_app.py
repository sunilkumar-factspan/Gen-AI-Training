import gradio as gr

def respond_to_input(user_input):
    return f"You entered: {user_input}"

gr.Interface(fn=respond_to_input, inputs="text", outputs="text").launch()

