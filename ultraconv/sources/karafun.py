import xml.etree.ElementTree as ET
import os

def extract_file(path, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(path, 'rb') as f:
        file_data = f.read()
    
    magic = file_data[:3]
    if magic != b'\x01\xce\xd7':
        raise ValueError("Invalid file format")
    
    nb_files = file_data[3]
    print(f"Number of files: {nb_files}")

    def write_file(id, out_path):
        with open(out_path, 'wb') as out_f:
            start_offset = 4 + nb_files * 5 # header + file table
            while start_offset < len(file_data):
                file_id = int.from_bytes(file_data[start_offset:start_offset+1], 'big')
                file_size = int.from_bytes(file_data[start_offset+2:start_offset+5], 'big')
                start_offset += 9 # 1 byte for file type, 1 bytes for id, 1 null, 3 bytes for size, 4 null bytes
                if file_id == id:
                    out_f.write(file_data[start_offset:start_offset+file_size])
                start_offset += file_size
 
    # first file is the XML file
    xml_path = os.path.join(out_dir, 'output.xml')
    write_file(1, xml_path)

    # read xml to fine the name and type of other files
    xmldoc = ET.parse(xml_path)
    files = xmldoc.getroot().findall('./files/file')
    for f in files:
        id = int(f.get('index'))
        if id != 1:
            out_path = os.path.join(out_dir, f.get('label'))
            write_file(id, out_path)

# extract_file(input_file, output_directory)
