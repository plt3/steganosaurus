# steganosaurus
> Pure Python implementation of least significant bit steganography method

## Installation:
- Clone repo with `git clone https://github.com/plt3/steganosaurus`
- Or download zip by clicking the green "Code" button in the top right and choosing "Download ZIP"

### Installing Dependencies:
- Install dependencies with `pip install -r requirements.txt` while in project home directory (using a virtual environment is preferred)

## CLI Instructions:
- Run `python3 cli.py -h` in project home directory to see help message

### To hide a message into an image:
- To hide "hello world" into a copy of /path/to/image/file.png that will be saved at /path/to/image/file_message.png:
```
python3 cli.py --encode --message "hello world" /path/to/image/file.png
```  
- To hide "hello world" into a copy of /path/to/image/file.png that will be saved at /path/to/save.png:
```
python3 cli.py --encode --message "hello world" --outputfile /path/to/save.png /path/to/image/file.png
```  
- To hide all text stored in /path/to/text/file.txt into a copy of /path/to/image/file.png that will be saved at /path/to/image/file_message.png:
```
python3 cli.py --encode --inputfile /path/to/text/file.txt /path/to/image/file.png
```  

### To extract the hidden message from an image:
- To print message hidden in /path/to/image/file.png to stdout:
```
python3 cli.py --decode /path/to/image/file.png
```  
- To write message hidden in /path/to/image/file.png to /path/to/text/file.txt:
```
python3 cli.py --decode --outputfile /path/to/text/file.txt /path/to/image/file.png
``` 

## Programmatic Instructions:
#### NOTE: Must be in a Python script in project home directory for imports to work
- To hide messages in images:
```python
from Steganography import Encoder

encode = Encoder("hello world")  # create Encoder object with "hello world" message

encode.createCodeImage("myImage.png")  # hide "hello world" in copy of myImage.png saved at myImage_message.png

encode.setMessage("New message")  # change message to hide in future images
encode.createCodeImage("myImage.png", outputFile="message.png")  # hide message in message.png
```
- To decode messages from images:
```python
from Steganography import Decoder

decode = Decoder("message.png")  # create Decoder object for message.png file

message = decode.decodeImage()  # assign entire decoded message from message.png to message variable
print(message)

decode.setFilename('/new/image.png'). # change file path for future decoding

```
