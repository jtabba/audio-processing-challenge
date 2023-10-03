import os
import whisper
import re
import csv
from multiprocessing import Process
from datetime import datetime
from toolz import partition


# Path to the directory containing the audio files
directory = "audio_challenge/audio"
# AI model used to transcribe the audio files
model = whisper.load_model("base")


def process_audio_files(files_batch):
    for file in files_batch:
        file_path = os.path.join(directory, file)

        try:
            #  Skip irrelevant files
            if os.path.isfile(file_path) and file_path.endswith(".wav"):
                result = model.transcribe(file_path)["text"].strip().split(' ')

                words_count = 1
                consecutive_count = 1
                longest_consecutive_count = 1

                data = {
                    "Filename": file,
                    "Timestamp": datetime.now(),
                    "Words_Out_of_Order": False,
                    "Longest_Consecutive_Count": 0,
                    "Count_of_Audible_Words": 0
                }

                # Once we have the transcribed data we need to analyse its individual words
                for i in range(len(result)):
                    if i == len(result) - 1:
                        break

                    current_char = re.sub(r'[,|.| ]', '', result[i])
                    next_char = re.sub(r'[,|.| ]', '', result[i + 1])

                    if current_char.isnumeric():
                        # If the current character is a number add to the number of words and check if the next character is the next number in the sequence - if not then change the order data
                        current_num = int(current_char)
                        next_num = int(next_char)

                        words_count += 1

                        if next_num == current_num + 1:
                            consecutive_count += 1
                        else:
                            data["Words_Out_of_Order"] = True

                    else:
                        # If it is not a number skip and save the current consecutive count
                        longest_consecutive_count = consecutive_count
                        consecutive_count = 0
                        data["Words_Out_of_Order"] = True

                    data["Longest_Consecutive_Count"] = longest_consecutive_count if longest_consecutive_count != 1 else consecutive_count
                    data["Count_of_Audible_Words"] = words_count

                print(file_path, result, data)

                # Write the data to a csv file
                with open('output.csv', 'a') as csvfile:
                    field_names = data.keys()
                    writer = csv.writer(csvfile)

                    if os.stat('output.csv').st_size == 0:
                        writer.writerow(field_names)

                    writer.writerow(data.values())
            else:
                continue
        except Exception as e:
            print('An error has occurred: ', e)


if __name__ == '__main__':
    files = os.listdir(directory)
    # Partition the files into groups of 4 for multiprocessing
    queue = list(partition(4, files))

    for files_batch in queue:
        p = Process(target=process_audio_files, args=(files_batch,))
        p.start()
        p.join()

    print('Finished processing files')
