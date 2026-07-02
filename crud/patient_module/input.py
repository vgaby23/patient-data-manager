# Making sure the input field has value
def mandatory_field(input_sentence):
    while True:
        input_field = input(f"Enter {input_sentence}: ").strip()

        if input_field:
            break
        else:
            print(f"Error: This field is mandatory. Please enter {input_sentence}")

    return input_field