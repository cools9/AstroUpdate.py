import cProfile
import os

from CTkMenuBar import CTkTitleMenu , CustomDropdownMenu
import customtkinter as ctk

def main():
    import CTkMenuBar
    from CTkMessagebox import CTkMessagebox
    import tkinter
    from tkinter import TOP,BOTTOM,LEFT,RIGHT
    from PIL import Image
    import requests
    import sympy as sympy
    from bs4 import BeautifulSoup
    from astropy.time import Time
    import customtkinter
    from math import sin,sqrt,log,tan,cos



    #customtkinter.set_default_color_theme("C:\\Users\\rishabh\\PycharmProjects\\phthon bla\\venv\\Lib\\site-packages\\customtkinter\\assets\\themes\\Oceanix.json")
    class Functionalities:
        @staticmethod
        def image_of_the_day():
            # Define the URL for the APoD
            apod_url = "https://apod.nasa.gov/apod/astropix.html"

            # Get today's date in ISO format
            today = Time.now()
            date_str = today.iso.split()[0]

            # Build the URL for today's APoD
            apod_url = f"{apod_url}?date={date_str}"

            # Send a GET request and parse the HTML
            response = requests.get(apod_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                img_element = soup.find("img")
                image_url = "https://apod.nasa.gov/apod/" + img_element["src"]
                title = img_element["alt"]
                explanation = soup.find("p").text

                return f"Title: {title}\nImage URL: {image_url}\nExplanation: {explanation}"
            else:
                return "Failed to retrieve the Astronomy Picture of the Day"

        def evaluate_math_expression(expression, variable=None):
            try:
                if variable:
                    # If a variable is specified, use sympy for symbolic math
                    x = sympy.symbols(variable)
                    parsed_expression = sympy.sympify(expression)
                    result = sympy.simplify(parsed_expression)
                else:
                    # If no variable is specified, use math for numeric calculations
                    result = eval(expression)
                return result
            except Exception as e:
                return str(e)

        def ask_ai_a_question(self, prompt1):
            from transformers import GPT2LMHeadModel, GPT2Tokenizer

            # Load the pre-trained GPT-2 model and tokenizer
            model_name = "gpt2"
            model = GPT2LMHeadModel.from_pretrained(model_name)
            tokenizer = GPT2Tokenizer.from_pretrained(model_name)

            def generate_text(prompt, max_length=100):
                input_ids = tokenizer.encode(prompt, return_tensors="pt")

                # Generate text based on the input prompt
                output = model.generate(input_ids, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2)

                generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
                return generated_text

            print(generate_text(prompt1))

        def fits_file_reader(self, fits_file_path):
            from astropy.io import fits

            header_info = ""
            data_info = ""

            # Open the FITS file
            hdul = fits.open(fits_file_path)
            

            # Extract header information
            header = hdul[0].header
            header_info += "Header Information:\n"
            for key, value in header.items():
                # Provide explanations for some common header keywords
                if key == "NAXIS":
                    header_info += f"Number of Dimensions: {value}\n"
                elif key == "BITPIX":
                    header_info += f"Data Type: {value} (32-bit floating point)\n"
                elif key.startswith("NAXIS"):
                    dimension = int(key.lstrip("NAXIS"))
                    header_info += f"Dimension {dimension} Size: {value}\n"
                elif key == "OBJECT":
                    header_info += f"Target Object: {value}\n"
                elif key == "DATE-OBS":
                    header_info += f"Date of Observation: {value}\n"
                # You can add more explanations for other header keywords as needed
                else:
                    header_info += f"{key}: {value}\n"

            # Extract and format data
            data = hdul[0].data
            data_info += "Data:\n"
            data_info += str(data)

            # Close the FITS file
            hdul.close()

            return header_info, data_info


    class GUIFUNCTIONS:
        def calculate(input):
            # Function to handle math calculations based on the input
            try:
                result = Functionalities.evaluate_math_expression(input)
                CTkMessagebox ( title="Answer" , message=f"   {result}" )
            except Exception as e:
                CTkMessagebox ( title="Error" , message=f"{str(e)}" , icon="cancel" )

        def file_data(input):
            functionalities = Functionalities()  # Create an instance of the class
            return functionalities.fits_file_reader(fits_file_path=input)
        def ai_ui(input):
            root = ctk.CTkToplevel()
            root.geometry ( "400x500" )

            chat_log = ctk.CTkTextbox ( root , state="disabled" )
            chat_log.pack ( fill="both" , expand=True )

            # Assuming Functionalities is a class
            functionalities_instance = Functionalities ()  # Creating an instance of the class

            def send_message():
                message = user_input.get ()
                chat_log.configure ( state="normal" )
                chat_log.insert ( "end" , f"You: {message}\n" )

                bot_response = functionalities_instance.ask_ai_a_question (
                    prompt1=message )  # Calling the method on the instance
                chat_log.insert ( "end" , f"Bot: {bot_response}\n" )

                chat_log.configure ( state="disabled" )
                user_input.delete ( 0 , "end" )

            user_input = ctk.CTkEntry ( root )
            user_input.pack ( side="left" , fill="x" , expand=True )

            send_button = ctk.CTkButton ( root , text="Send" , command=send_message )
            send_button.pack ( side="right" )
            root.title("Ask AI")
            root.mainloop ()

    window=customtkinter.CTk()
    menu = CTkTitleMenu ( master=window )
    button1=menu.add_cascade ( "Features" )
    button3=menu.add_cascade("Theme")
    button2=menu.add_cascade("Edit")



    title_frame=customtkinter.CTkFrame(window,width=900,height=200,corner_radius=20,border_color="red")
    title_frame.configure(fg_color="transparent")
    title_frame.pack(side=TOP,pady=20,padx=20)
    label=customtkinter.CTkLabel(title_frame,text="AstroUpdate",width=900,height=int(100),font=("Arial", 70, "bold"))
    label.pack()


    general_tools=customtkinter.CTkFrame(window,width=900,height=500,corner_radius=20,border_color="red")
    general_tools.pack(pady=20,padx=10)
    tabview = customtkinter.CTkTabview(general_tools,width=1400,height=500)
    tabview.configure(fg_color="transparent")
    tabview.pack(padx=20, pady=20)

    tabview.add("Astronomical Image Of The Day")  # add tab at the end
    tabview.add("Calculator")  # add tab at the end
    tabview.add("Fits File Reader")
    tabview.add("AstroChat")
    tabview.set("Astronomical Image Of The Day")  # set currently visible tab
    tabview.add("ScienceScript")

    dropdown1 = CustomDropdownMenu ( widget=button1 )
    dropdown1.add_option ( option="Open FITS File" )
    dropdown1.add_option ( option="Open Calculator",command=lambda: tabview.set("Calculator") )
    dropdown1.add_option(option="Ask GPT2",command=lambda:GUIFUNCTIONS.ai_ui('bla'))

    dropdown2=CustomDropdownMenu(widget=button3)
    def light_mode():
        customtkinter.set_appearance_mode("light")
    def dark_mode():
        customtkinter.set_appearance_mode("dark")
    mode=dropdown2.add_submenu("Mode")
    mode.add_option("Light",command=light_mode)
    mode.add_option ( "Dark",command=dark_mode)
    dropdown2.add_separator()
    theme=dropdown2.add_submenu("Theme")
    path = "themes\\"
    files = os.listdir ( path )

    for file in files:
        theme.add_option(file,command=lambda:    customtkinter.set_default_color_theme(f"themes\\{file}"))
    """
    button = customtkinter.CTkButton(master=tabview.tab("tab 1"))
    button.pack(padx=20, pady=20)
    """
    #printing the Astronomical image of the day
    IOTD = Functionalities.image_of_the_day()
    textbox = customtkinter.CTkTextbox(tabview.tab("Astronomical Image Of The Day"),width=900,height=400)
    textbox.insert("0.0", IOTD)
    textbox.configure(state="disabled")
    textbox.pack()

    calculation_box=customtkinter.CTkTextbox(tabview.tab("Calculator"),width=900,height=300)
    calculation_box.pack()
    calculate_button = customtkinter.CTkButton(tabview.tab("Calculator"), width=200, height=50, corner_radius=50, text="Calculate", command=lambda: GUIFUNCTIONS.calculate(calculation_box.get("0.0", "end")))
    calculate_button.pack(side=BOTTOM)

    #showing the fits file
    fits_file_frame=customtkinter.CTkFrame(tabview.tab("Fits File Reader"),width=900,height=100,corner_radius=20,border_color="red")
    fits_file_frame.configure(fg_color="transparent")
    fits_file_frame.pack(side=BOTTOM)

    fits_file_content=customtkinter.CTkTextbox(fits_file_frame,width=900,height=300,corner_radius=20)
    fits_file_content.configure(state="disabled")
    fits_file_content.pack()

    fits_file_tools=customtkinter.CTkFrame(fits_file_frame)
    fits_file_tools.configure(fg_color="transparent")
    fits_file_tools.pack(side=BOTTOM)
    fits_file_directory=customtkinter.CTkEntry(fits_file_tools,placeholder_text='enter file location',width=200,height=50)
    fits_file_directory.pack(side=LEFT)
    fits_file_button = customtkinter.CTkButton(
        fits_file_tools,
        text="Fits File Reader",
        corner_radius=50,
        height=50,
        command=lambda: display_fits_data(fits_file_directory.get())
    )
    fits_file_button.pack()

    def display_fits_data(fits_file_path):
        functionalities_instance = Functionalities()  # Create an instance of Functionalities
        fits_data = functionalities_instance.fits_file_reader(fits_file_path)
        # Clear any existing content
        fits_file_content.configure(state="normal")
        fits_file_content.delete("1.0", "end")
        # Insert the new data
        fits_file_content.insert("1.0", fits_data)
        fits_file_content.configure(state="disabled")

    #AstroChatUI
    astrochat_frame=customtkinter.CTkFrame(tabview.tab("AstroChat"),corner_radius=30)

    astrochat_frame.pack()

    astrochat_tab=customtkinter.CTkTabview(astrochat_frame,corner_radius=50)
    astrochat_tab.pack(side=LEFT,pady=10,padx=10)
    astrochat_tab.add("Friends")
    astrochat_tab.add("Group Chat")

    add_image=customtkinter.CTkImage(light_image=Image.open('C:\\Users\\rishabh\\Desktop\\Desktop\\AstroUpdate\\plus.png'),
                                      dark_image=Image.open('C:\\Users\\rishabh\\Desktop\\Desktop\\AstroUpdate\\plus.png'),
                                      size=(30,30))

    add_friend=customtkinter.CTkButton(astrochat_tab.tab("Friends"),width=250,height=50,corner_radius=30,image=add_image,text="ADD FRIEND")
    add_friend.pack(side=BOTTOM)

    astrochat_mainframe=customtkinter.CTkScrollableFrame(astrochat_frame,width=700,height=500,corner_radius=50)
    astrochat_mainframe.pack(side=LEFT,pady=10,padx=10)

    mesage=customtkinter.CTkFrame(astrochat_mainframe)
    mesage.place(x=500,y=100)
    mesage.pack(side=BOTTOM)
    i=0
    for i in range(10):
        i+1
        label1=customtkinter.CTkLabel(astrochat_mainframe,text='hi')
        label1.pack(side=BOTTOM)
    message_text=customtkinter.CTkTextbox(mesage,width=200,height=100,corner_radius=20)
    message_text.pack(side=LEFT)
    send_image=customtkinter.CTkImage(light_image=Image.open('C:\\Users\\rishabh\\Desktop\\Desktop\\AstroUpdate\\send.png'),
                                      dark_image=Image.open('C:\\Users\\rishabh\\Desktop\\Desktop\\AstroUpdate\\send.png'),
                                      size=(30,30))
    message_button=customtkinter.CTkButton(mesage,image=send_image,width=100,height=100,corner_radius=30,text="send")
    message_button.pack(side=RIGHT)

    #ScienceScript

    def create_notebook_authenication():
        from cryptography.fernet import Fernet
        def generate_file(filename , password , contribute_num):
            print(f"{filename},{password},{contribute_num}")
            file_struct = f"""
            [
                {password},
                {contribute_num}
            ]
            contents[
                filecontents
            ]
            """
            print(file_struct)

            file_data = file_struct.replace ( 'filecontents' ,
                                              'some content' )  # Replace 'some content' with actual file content
            file_data = file_data.replace ( 'password' , password )
            file_data = file_data.replace ( 'contribute_num' , str ( contribute_num ) )
            # Assuming 'filename_text' contains the text extracted from the Tkinter Text widget
            filename = filename.strip ().replace ( '\n' , '' ).replace ( '\r' , '' )

            key_key = 'jCbIqLoVhw_oIWyLhVh_NQrwSMp0bhdqgqK_Fd_AIAY='
            key = key_key.encode ()  # Keys need to be in bytes

            # Create a Fernet object with the key
            cipher_suite = Fernet ( key )

            # Encrypt the data
            encrypted_data = cipher_suite.encrypt ( file_data.encode () )

            # Write the encrypted data to a file
            with open ( f"notebook\\{filename}.notes" , 'wb' ) as file:
                file.write ( encrypted_data )

        pop = customtkinter.CTkToplevel(window)

        create_notebook_frame = customtkinter.CTkScrollableFrame(pop, width=500, height=500)
        create_notebook_frame.pack(anchor=tkinter.CENTER)

        script_label = customtkinter.CTkLabel(create_notebook_frame, text="Create Notebook", font=("Consolas", 24, "bold"))
        script_label.pack(side=TOP, pady=20, padx=20)

        entry = customtkinter.CTkEntry(create_notebook_frame,placeholder_text='Filename', width=500, height=125)
        entry.pack(pady=20, padx=20)

        entry1 = customtkinter.CTkEntry(create_notebook_frame,placeholder_text='Password', width=500, height=125)
        entry1.pack(pady=20, padx=20)

        entry2 =customtkinter.CTkEntry(create_notebook_frame,placeholder_text="Enter The Names Of The People Who Can Contribute",width=500,height=125)
        entry2.pack(pady=20,padx=20)

        filename1=entry.get()
        contribute_num1=entry2.get()
        password1=entry1.get()
        print(filename1,contribute_num1,password1)




        generate_key_button = customtkinter.CTkButton (
            create_notebook_frame , text='Create' , image=add_image ,
            width=500 , height=166 ,
            command=lambda: generate_file ( entry.get() , entry1.get() , entry2.get() )
        )
        generate_key_button.pack ( pady=10 , padx=10 )

        pop.resizable(0,0)
        pop.title("Create Notebook")
        pop.geometry("500x500")
        pop.mainloop()





    sci_script_label=customtkinter.CTkLabel(tabview.tab("ScienceScript"),text="Your Notebooks",font=("Consolas", 24, "bold"))
    sci_script_label.pack(side=TOP,pady=20,padx=20)

    sci_script_options=customtkinter.CTkFrame(tabview.tab("ScienceScript"))
    sci_script_options.pack(side=BOTTOM)
    create_sci_script=customtkinter.CTkButton(sci_script_options,image=add_image,text="Create ScienceScript Notebook",command=create_notebook_authenication)
    create_sci_script.pack(side=LEFT,pady=20,padx=20)
    open_sci_script = customtkinter.CTkButton ( sci_script_options , image=add_image ,
                                                  text="Open ScienceScript Notebook" ,
                                                  command=create_notebook_authenication )
    open_sci_script.pack ( side=LEFT , pady=20 , padx=20 )
    delete_sci_script = customtkinter.CTkButton (sci_script_options, image=add_image ,
                                                  text="Delete ScienceScript Notebook" ,
                                                  command=create_notebook_authenication )
    delete_sci_script.pack ( side=LEFT , pady=20 , padx=20 )

    window.title("AstroUpdate")
    window.geometry("900x700")
    window.mainloop()

cProfile.run('main()',filename='output.txt')