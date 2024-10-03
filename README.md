# SteganographyProject
A simple website where users can input two files and hide one within the other using steganography.

## About 
- Users can register with their first and last name, email, and their chosen password.
- To upload files or view their own posts or account info, users must be logged in, but they can view all uploads/posts without being logged in.

- The upload page prompts users to choose a carrier file and a secret file to be hidden within the carrier.
- They can then choose a mode for the periodicity, the starting bit, the periodicity itself, and a name for the upload/post. 

- The starting bit represents the first bit in the carrier file to start substituting from.
- It is recommended to choose a starting bit that skips enough bits for the header of the carrier file.

- The periodicity represents the number of bits to skip when substituting the bits of the carrier file with the bits of the secret file.
- Single mode signifies to skip the same number of bits every time.
- Multiple mode signifies to skip a different number of bits each time, according to the list that is defined in the periodicity input.

## How to run
- Access hosted website [here](http://ec2-3-87-94-23.compute-1.amazonaws.com:8080/).
- To run from repository:
  - Download the repository and open the folder in Visual Studio or your preferred IDE. 
  - Install dependencies by typing 'pip install -r requirements.txt' in the terminal.
  - Run application by typing 'flask run' in the terminal.
  - Navigate to the development server at localhost:5000.
  - The application should be open and ready to use.

## Tools and Frameworks
- HTML, CSS, JavaScript, Bootstrap (frontend/user interface)
- Python, Flask (backend)

