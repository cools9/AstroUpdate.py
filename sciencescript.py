from cryptography.fernet import Fernet

class ScienceScript:
    def __init__(self, ip_address, hostname):
        self.ip_address = ip_address
        self.hostname = hostname
        self.file_structure = """
        file_name{
            password,
            key,
            contribute_num
        }
        file_name.contents{
            filecontents
        }
        """

    def create_notebook(self, filename, password, key, contribute_num):
        self.password = password
        self.key = key
        self.filename = filename

        # Replace placeholders in the file_structure with provided values
        encrypted_structure = self.file_structure.replace('password', password)
        encrypted_structure = encrypted_structure.replace('key', key)
        encrypted_structure = encrypted_structure.replace('contribute_num', str(contribute_num))

        # Encrypt the updated file structure
        fernet = Fernet(key)
        encrypted_structure = fernet.encrypt(encrypted_structure.encode())

        # Write the encrypted structure to the file
        with open(filename, 'xb') as notebook:
            notebook.write(encrypted_structure)

        return key

    def read_notebook(self, filename, password, key):
        self.password = password
        self.key = key
        self.filename = filename

        # Decrypt the file structure
        fernet = Fernet(key)
        with open(filename, 'rb') as notebook:
            decrypted_structure = fernet.decrypt(notebook.read()).decode()

        # Extract contribute_num from the decrypted structure
        contribute_num_start = decrypted_structure.find('contribute_num') + len('contribute_num') + 1
        contribute_num_end = decrypted_structure.find('\n', contribute_num_start)
        contribute_num = decrypted_structure[contribute_num_start:contribute_num_end].strip()

        # Check if contribute_num matches the stored IP address
        if contribute_num == self.ip_address:
            # Extract and print contents if the IP matches
            contents_start = decrypted_structure.find('filecontents') + len('filecontents') + 1
            contents = decrypted_structure[contents_start:].strip()
            print("Notebook Contents:")
            print(contents)
        else:
            print("You are not authorized to view this notebook.")