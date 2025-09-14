import gradio as gr

# --- Backend Logic ---
def calculator(num1, num2, operation):
    try:
        num1 = float(num1)
        num2 = float(num2)

        if operation == "Add":
            return num1 + num2
        elif operation == "Subtract":
            return num1 - num2
        elif operation == "Multiply":
            return num1 * num2
        elif operation == "Divide":
            if num2 == 0:
                return "Error: Division by zero!"
            return num1 / num2
        else:
            return "Unknown Operation"
    except ValueError:
        return "Error: Please enter valid numbers!"

# --- Gradio Frontend ---
with gr.Blocks() as demo:
    gr.Markdown("<h2 style='text-align: center;'> Simple Calculator (Created By Akash)</h2>")

    with gr.Row():
        num1 = gr.Textbox(label="Number 1", placeholder="Enter first number")
        num2 = gr.Textbox(label="Number 2", placeholder="Enter second number")

    operation = gr.Radio(["Add", "Subtract", "Multiply", "Divide"], label="Choose Operation")

    calculate_btn = gr.Button("Calculate", variant="primary")
    result = gr.Textbox(label="Result", interactive=False)

    # Link button click to function
    calculate_btn.click(fn=calculator, inputs=[num1, num2, operation], outputs=result)

# Run the app
demo.launch()