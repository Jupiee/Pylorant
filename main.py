from valoreader import Valoreader

def main():

    path= input("Input the file path: ")

    reader= Valoreader(path)
    reader.openWebsite()
    reader.openfile()

if __name__ == "__main__":

    main()
