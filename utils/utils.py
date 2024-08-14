def print_number_of_trainable_model_parameters(model):
    trainable_model_params = 0
    all_model_params = 0
    for _, param in model.named_parameters():
        all_model_params += param.numel()
        if param.requires_grad:
            trainable_model_params += param.numel()
    return f"trainable model parameters: {trainable_model_params}\nall model parameters: {all_model_params}\npercentage of trainable model parameters: {100 * trainable_model_params / all_model_params:.2f}%"


def preprocess_function(example, tokenizer):
    start_prompt = "Provide a description of the YouTube thumbnail given the following video title.\n\n"
    end_prompt = "\n\nThumbnail description: "
    prompt = [start_prompt + title + end_prompt for title in example["prompt"]]
    example["input_ids"] = tokenizer(
        prompt, padding="max_length", truncation=True, max_length=128
    ).input_ids
    example["labels"] = tokenizer(
        example["response"], padding="max_length", truncation=True, max_length=128
    ).input_ids

    return example
