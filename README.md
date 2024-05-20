# SteganographyProject
A simple website where users can input two files and hide one within the other using steganography.

Users can register with their first and last name, email, and their chosen password. To upload files or view their own posts or account info, users must be logged in, but they can view all uploads/posts without being logged in.

The upload page prompts users to choose a carrier file and a secret file to be hidden within the carrier. They can then choose a mode for the periodicity, the starting bit, the periodicity, and a name for the upload/post. 

The starting bit represents the first bit in the carrier file to start substituting from. It is recommended to choose a starting bit that skips enough bits for the header of the carrier file.

The periodicity represents the number of bits to skip when substituting the bits in the carrier file with the bits of the secret file. Single mode signifies to skip the same number of bits every time, but multiple mode signifies to skip a different number of bits each time, according to the list that is defined in the periodicity input.

Uses Python/Flask for backend functionality and HTML, CSS, JavaScript, and Bootstrap for frontend functionality. 

Planning on using a cloud-based filesystem to store uploaded files in the future.
