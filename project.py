import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from moviepy.editor import *
from selenium.webdriver.chrome.options import Options
import pyautogui
import pyperclip

import shutil
import random
import os
from pytube import YouTube
def search_keyword():
    keywordslist=["shinchan in hindi","Taarak Mehta ka Ooltah Chashmah"]
    return random.choice(keywordslist)

def check_file(video):
    with open("C:\\Users\\vdhaw\\OneDrive\\Desktop\\data.txt","r") as file:
        data=file.readlines()
      
        if any(line.strip()==video for line in data):
            return True
        else:
            with open("C:\\Users\\vdhaw\\OneDrive\\Desktop\\data.txt","a+") as file:
                file.write(video+"\n")
         


def check_download():
    downloadfile=open("C:\\Users\\vdhaw\\OneDrive\\Desktop\\download.txt","r")
    datafile=open("C:\\Users\\vdhaw\\OneDrive\\Desktop\\data.txt","r")
    downloaddata=downloadfile.readlines()
    for line in datafile:
        if line not in downloaddata:
            file1=open("C:\\Users\\vdhaw\\OneDrive\\Desktop\\download.txt","a")
            file1.write(line)
            break
        else:
            continue

    
    
def download(link):
    file1=open("C:\\Users\\vdhaw\\OneDrive\\Desktop\\download.txt","w")
    #filedata=list(file1.readlines())
    #return filedata[len(filedata)-1]
    #yt = YouTube(filedata[len(filedata)-1])
    #video_stream = yt.streams.get_highest_resolution()
    #video_stream.download("C:\\Users\\vdhaw\\OneDrive\\Desktop\\video")
    yt = YouTube(link)
    video_stream = yt.streams.get_highest_resolution()
    desired_file_path = "C:\\Users\\vdhaw\\OneDrive\\Desktop\\video"
    video_stream.download(output_path=desired_file_path)


    
    
def getvideo(driver):
    driver.get("https://www.youtube.com")
    driver.implicitly_wait(5)
    search=driver.find_element(By.NAME,"search_query")
    x=search_keyword()
    search.send_keys(x)
    wait=WebDriverWait(driver,10)
    wait
    search.send_keys(Keys.RETURN)
    
    wait.until(EC.title_contains(x))
    y=driver.title
    if x+" - YouTube"==y:
        print("search done")
        wait.until(EC.presence_of_all_elements_located((By.XPATH,"//span[@id='text'  and contains(@aria-label,'hour')]")))
        """videos=driver.find_elements(By.XPATH,"//span[@id='text'  and contains(@aria-label,'hour') or   ]/ancestor::a" )"""


        videos=driver.find_elements(By.XPATH,"//a[@id='video-title']" )


        """for video in videos:
            selected=video.get_attribute("href")
            check_file(selected)
    
        check_download()"""
        wait
        for video in videos:
            title_checker=video.get_attribute("aria-label").lower()
            if x.lower() in title_checker:
                index=title_checker.find("ago")
                title_checker=title_checker[(index+4):-1]
    
                if (title_checker.find("hour")!=-1 or (int(title_checker[0:2])>=20 and title_checker.find("minute")!=-1)):
                    selected=video.get_attribute("href")
                    if check_file(selected):
                        continue
                    else:
                        check_file(selected)
                        download(selected)
                        break        

    else:
        print("not found")
"""//span[contains(@aria-label,'hour')]/ancestor::ytd-thumbnail/following-sibling::div/child::div/child::div/child::h3/child::a"""        

def upload_video(driver):
    folder_path = "C:\\Users\\vdhaw\\OneDrive\\Desktop\\video"
    driver.get("https://studio.youtube.com")
    
    wait=WebDriverWait(driver,10)
    
    


    file_names = os.listdir(folder_path)
    sent=str()
    k=len(file_names)
    i=1
    while i<=k:
        names=f"subclip_{i}.mp4"
        sent=f"{os.path.join(folder_path, names)}"
        time.sleep(0.3)
        sent = sent.replace('\\', '\\\\')
        time.sleep(0.3)
        if os.path.exists(sent):

            a=driver.find_element(By.XPATH,"//ytcp-button[@id='create-icon']")
            a.click()
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//yt-formatted-string[normalize-space()='Upload videos']")))
            button.click()
            time.sleep(0.3)
        
            files = wait.until(EC.element_to_be_clickable((By.XPATH, "//ytcp-button[@id='select-files-button']")))
            
            
            
            upload_input =driver.find_element(By.XPATH, "//*[@id='content']/input")
            upload_input.send_keys(sent)

            wait.until(EC.presence_of_element_located((By.XPATH,"//ytcp-social-suggestions-textbox[@id='title-textarea']//div[@id='textbox']")))
            wait.until(EC.element_to_be_clickable((By.XPATH,"//ytcp-social-suggestions-textbox[@id='title-textarea']//div[@id='textbox']")))
            time.sleep(5)
            try:

                element=driver.find_element(By.XPATH,"//div[@class='error-short style-scope ytcp-uploads-dialog' and text()='Daily upload limit reached']")
                if element.is_displayed():
                    print("daily limit reached at",names)
                    time.sleep(3)
                    driver.quit()
                    return
                
            except:   
                
                    sent = sent.replace('\\\\','\\')
                    os.remove(sent)
                    cross=wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='close-button-area style-scope ytcp-uploads-dialog']//ytcp-icon-button[@id='close-button']//tp-yt-iron-icon[@class='remove-defaults style-scope ytcp-icon-button']")))
                    cross.click()
                    time.sleep(50)

                        
                    print("upload complete",names)
                    i+=1


            
                

        else:
            k=k+1
            i+=1
            print("file not found",names)
            
        
        
      

def editor():
    print("starting")
    folder_path = "C:\\Users\\vdhaw\\OneDrive\\Desktop\\video"
    files = os.listdir(folder_path)
    for file in files:
    # Check if the file is a video file (you can customize this check based on the file extension)
        if file.endswith(".mp4"):
        # Perform actions on the video file
         video_path = os.path.join(folder_path, file)

    clip = VideoFileClip(video_path)
    print(video_path)
    shorts_size = (1080, 1920)
    white_bg = ColorClip(size=shorts_size, color=(255, 255, 255)).set_duration(clip.duration)
    x_pos = (shorts_size[0] - clip.size[0]) // 2
    print("done")
    final_clip = CompositeVideoClip([white_bg, clip.set_position((x_pos, 'center'))])
    max_duration = 55
    num_full_subclips = int(clip.duration // max_duration)
    subclips = []
    output_directory = "C:\\Users\\vdhaw\\OneDrive\\Desktop\\video\\"


    print("done2")
    

    for i in range(num_full_subclips):
        # Calculate start and end time for subclip
        start_time = i * max_duration
        end_time = (i + 1) * max_duration
        
        # Create subclip
        subclip = final_clip.subclip(start_time, end_time)
        subclips.append(subclip)
        print(f"Subclip {i + 1}: Duration={subclip.duration}, FPS={subclip.fps}, Size={subclip.size}")

    for i, subclip in enumerate(subclips, start=1):
        subclip.write_videofile(output_directory + f"subclip_{i}.mp4", fps=subclip.fps)

    time.sleep(100)
    os.remove(video_path) 

def clear_folder():
    shutil.rmtree("C:\\Users\\vdhaw\\OneDrive\\Desktop\\video")
    os.makedirs("C:\\Users\\vdhaw\\OneDrive\\Desktop\\video")

 

ops = webdriver.ChromeOptions()
ops.headless=True
ops.add_argument('--log-level=3')
ops.add_argument("user-data-dir=C:\\Users\\vdhaw\\AppData\\Local\\Google\\Chrome\\User Data\\")
ops.binary_location="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"



driver=webdriver.Chrome(options=ops)
driver.implicitly_wait(10)


folder_path = "C:\\Users\\vdhaw\\OneDrive\\Desktop\\video"
file_names = os.listdir(folder_path)

if len(file_names)==0:
    getvideo(driver)
    editor()
    upload_video(driver)


else:
    upload_video(driver)