from valoreader import Valoreader
import time

def main():

    flag= True

    reader= Valoreader(None)

    while flag:

        print("\n[1] Check Manually (Single-check)\n[2] Check text file (Multi-check - Coming soon)\n[3] Check excel file (Multi-check)\n[4] Exit\n")
        reader.openWebsite()

        choice= int(input(""))

        if choice == 1:
            
            username= input("Enter User: ")
            password= input("Enter Password: ")

            reader.sendCreds(username, password)
            data= reader.retrieveInfo()

            if data != -1:

                reader.openDataBook()
                reader.writeData(data)
                reader.closeDataBook()

                print("Check your databook!")
                time.sleep(5)

            else:

                print("Wrong username or password")

        elif choice == 2:
            pass

        elif choice == 3:

            path= input("Input the file path: ")

            reader._file = path

            reader.openfile()

        else:

            flag= False

if __name__ == "__main__":

    main()
