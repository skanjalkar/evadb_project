import openai

def read_text_line(path, num_token=1000):
    """#write description here
    Args:
        path ([type]): [description]
        num_token (int, optional): [description]. Defaults to 1000.
    Yields: None
    """
    # For simplicity, we only keep letters.
    whitelist = set(".!?abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890 %")

    with open(path, "r") as f:
        line_itr = 0
        for line in f.readlines():
            line_itr = line_itr + 1
            if line_itr % 10 == 0:
                print("line: " + str(line_itr))
            for i in range(0, len(line), num_token):
                cut_line = line[i : min(i + 1000, len(line))]
                cut_line = "".join(filter(whitelist.__contains__, cut_line))
                yield cut_line

            if line_itr == 1000:
                break


def write_dict_to_files(data_dict, directory_path):
    """#write description here
    Args: data_dict: map of data which contains key value pari to be written to seperate files
          directory_path: path of directory where files will be written
    Yields: None
    """
    import os

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Iterate through the dictionary and write each key-value pair to a separate file
    for key, value in data_dict.items():
        file_path = os.path.join(directory_path, f"{key}.txt")
        with open(file_path, "w") as file:
            file.write(str(value))