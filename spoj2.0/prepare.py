import chardet
import os

def find_encoding(fname):
    r_file = open(fname, 'rb').read()
    result = chardet.detect(r_file)
    charenc = result['encoding']
    return charenc

def preprocess(document_text):
    # remove the leading numbers from the string, remove non-alphanumeric characters, make everything lowercase
    terms = [term.lower() for term in document_text.strip().split()[1:]]
    return terms

def process_files(folder_path):
    vocab = {}
    documents = []
    inverted_index = {}

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            my_encoding = find_encoding(file_path)

            with open(file_path, 'r', encoding=my_encoding, errors='replace') as f:
                document_text = f.read()
                # preprocess the entire document text
                tokens = preprocess(document_text)
                documents.append(tokens)
                tokens = set(tokens)
                for token in tokens:
                    if token not in vocab:
                        vocab[token] = 1
                    else:
                        vocab[token] += 1

                    if token not in inverted_index:
                        inverted_index[token] = [len(documents) - 1]
                    else:
                        inverted_index[token].append(len(documents) - 1)

    # reverse sort the vocab by the values
    vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))

    print('Number of documents: ', len(documents))
    print('Size of vocab: ', len(vocab))
    print('Sample document: ', documents[0])

    # save the vocab in a text file
    with open('spoj2.0/tf-idf-spoj/vocab.txt', 'w', encoding='utf-8', errors='replace') as f:
        for key in vocab.keys():
            f.write("%s\n" % key)

    # save the idf values in a text file
    with open('spoj2.0/tf-idf-spoj/idf-values.txt', 'w', encoding='utf-8', errors='replace') as f:
        for key in vocab.keys():
            f.write("%s\n" % vocab[key])

    # save the documents in a text file
    with open('spoj2.0/tf-idf-spoj/documents.txt', 'w', encoding='utf-8', errors='replace') as f:
        for document in documents:
            f.write("%s\n" % ' '.join(document))

    # save the inverted index in a text file
    with open('spoj2.0/tf-idf-spoj/inverted-index.txt', 'w', encoding='utf-8', errors='replace') as f:
        for key in inverted_index.keys():
            f.write("%s\n" % key)
            f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))

folder_path = 'spoj2.0\Qdata'
process_files(folder_path)