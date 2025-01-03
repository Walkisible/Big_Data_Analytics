## Assignment 1: Preparation -- Install Spark

## Download assignment ที่ 1 ผ่าน:

https://github.com/Walkisible/Big_Data_Analytics/tree/main/Assignment01

Guide line สำหรับการติดตั้ง Spark บน google colab: https://github.com/Walkisible/Big_Data_Analytics/blob/main/Spark_install.ipynb

## README

การติดตั้งเพื่อ implement Spark สามารถทำได้หลายวิธีโดยวิธีที่ง่ายและสะดวกที่สุดคือ การ implement บน google colab ที่ provide distrubution basis ไว้ให้แล้วทำให้ users สามารถไป implement ได้เลย

อย่างไรก็ตาม ใน class จะอธิบายการ implement ไว้ให้ 2 วิธีคือการสร้าง local VM เพื่อ compute แบบ distributed กับวิธีที่ 2 คือการไป implement บน google colab

## วิธีที่ 2 -- รันบน local computer

ขั้นตอนแรก: ให้ทุกคนติดตั้ง Anaconda ก่อน เพื่อลง Environments สำหรับการใช้ภาษา Python บน คอมพิวเตอร์ส่วนตัว หากใครมี Anaconda แล้ว ให้ไปติดตั้ง Spark บนคอมพิวเตอร์ตาม OS ที่กำหนดในวิธี 1A หรือ 1B (ให้ติดตั้งและเลือกสร้าง env บน Python 3)

- Anaconda for windows: https://docs.anaconda.com/anaconda/install/windows/
- Anaconda for mac OS: https://docs.anaconda.com/anaconda/install/mac-os/
  **วิธีที่ 1A -- Install Spark บน Windows**
  1.1 เข้าออนไลน์คอร์ส BerkeleyX: CS100.1x Introduction to Big Data with Apache Spark (ปัจจุบันเป็น archived)
  https://courses.edx.org/courses/BerkeleyX/CS100.1x/1T2015/
  1.2. เข้าที่ tab “Course” เลือก “Setting up the Course Software Environment” จากนั้นอ่านและ install software ด้านล่างนี้โดยดูคำแนะนำการติดตั้งซอฟต์แวร์ได้ตามวิดีโอในหัวข้อนี้ (เลือก download software)
  Download & install VirtualBox – เลือก version ใหม่ล่าสุดจาก Website

* ในกรณีที่ใช้ Windows 10 หลังติดตั้งเสร็จแล้ว ให้เลือกค่า “Run this program in compatibility mode for Windows 7” สำหรับ VirtualBox
  Download & install Vagrant – เลือกversion ใหม่ล่าสุดจาก Website
  Download & install Virtual Machine
  download file https://github.com/spark-mooc/mooc-setup/archive/master.zip ไว้ที่ “user directory” เช่น c:\users\boonserm\myvagrant จากนั้น Unzip file แล้ว copy “Vagrantfile” ไว้ที่ “user directory”
  Run software:
  run cmd (command prompt – run as administrator)
  เปลี่ยนไดเร็กทอรีไปที่ user directory
  run “vagrant up” แล้วรอจนกว่าจะ Download เสร็จ จึงค่อย Start sparkvm ใน VM Machine จากนั้น ให้เข้าไปที่ http://localhost:8001 เพื่อรัน Jupyter Notebook
  ศึกษาหัวข้อ “Basic Instructions for Using the Virtual Machine” ตามวิดีโอ
  ศึกษาหัวข้อ “Running Your First Notebook” โดยการ upload file “Assignment1_StudentID.ipynb” (Spark iPython notebook file) และทดลองรันโปรแกรมตามคำอธิบายทีละขั้นตอน (อย่างไรก็ดี ออนไลน์คอร์สนี้ปัจจุบันปิดคอร์สแล้ว ทำให้ไม่สามารถ “submit” ตาม “Part 5: Export/ download and submit” ได้)

  **วิธีที่ 1B -- Install Spark บน mac OS**
  Download VM Virtual Box version 6.1.30 by clicking this link Download & install VirtualBox and then select the OS X hosts.
  1.1 Unarchive VirtualBox-6.1.30-148432-OSX.dmg and then click run the .pkg file
  Download Vagrant version 2.2.19 by clicking this link Download & install Vagrant and then select 64-bit.
  2.1 Unarchive vagrant_2.2.19_x86_64.dmg and then click run the .pkg file
  Download & install Virtual Machine from the github link by clicking this link https://github.com/spark-mooc/mooc-setup/archive/master.zip and then unzip this zipfile.
  Open “Terminal” and compile ‘pwd’ to check the directory. It always starts with an own user directory likewise /Users/student’s_OSX_username. If your directory path is not the same as this example, you must change the directory path by using ‘cd /Users/student’s_OSX_username’.
  Create directory for vagrant software on /Users/student’s_OSX_usernameby compile ‘mkdir myvagrant’ on terminal.
  Copy the ‘Vagrantfile’ from downloaded files from 3 to /Users/student’s_OSX_username/myvagrant by using ‘cp directory path of Vagrantfile /Users/student’s_OSX_username/myvagrant’
  Run command ‘vagrant up’ on terminal which the directory path located is on /Users/student’s_OSX_username/myvagrant and then wait until the downloading process will be completed. It spends time about 10 minutes depending on your internet speed.
  Starting ‘sparkvm’ on Oravle VM Virtual Box and then go to http://localhost:8001 on a web browser.
  If you cannot start sparkvm from 8, please verify security of the VM Virtual Box by this process. System Preference> Security & Privacy > Allow ‘VM Virtual Box’> Restart MacOS.
  Upload file Assignment1_StudentID.ipynb to http://localhost:8001 and then compile the jupyter notebook to complete this assignment.

### วิธีที่ 2 -- รันบน Google Colab

ใช้ jupyter-notebook ของ Colab (Colaboratory เป็น Jupyter notebook environment ที่อยู่บน Cloud ของ Google เราสามารถใช้เขียนและรันโปรแกรมผ่านเว็บเบราว์เซอร์ได้โดยไม่ต้องเซ็ตอัพใดๆ เป็นบริการฟรี สะดวกสำหรับทดสอบโปรแกรม -- ต้องมี google account)

1. Login เข้า Google drive ของตนเอง
2. ลาก folder ที่ download มา ไปไว้ที่ Google drive (ใน directory ที่ต้องการ)
3. เปิด folder
4. เปิดไฟล์ Assingment1_StudentID.ipynb ด้วย google colaboratory
5. ทำการ insert code จากไฟล์ "Spark_installation.ipynb" ซึ่งใน file จะมีวิธีการ install Spark และการสร้าง SparkContext อยู่แล้วให้ทำการ copy ตัว code มาวางใน file Assingment1_StudentID ใน Part 0 ได้เลย (ทำตาม instruction ในไฟล์ได้เลย)
6. ศึกษาหัวข้อ “Running Your First Notebook” โดยทดลองรันโปรแกรมตามคำอธิบายทีละขั้นตอน (อย่างไรก็ดี ออนไลน์คอร์สนี้ปัจจุบันปิดคอร์สแล้ว ทำให้ไม่สามารถ “submit” ตาม “Part 5: Export/ download and submit” ได้)


## วิธีส่งงาน:
1. หน้า “Assignment1_StudentID.ipynb” --> ให้ทำการสั่ง print หน้า web page แล้วเลือก save เป็น pdf file (แนะนำ Google Chrome) ให้เห็นผลการรัน แล้วส่งไฟล์ pdf พร้อมทั้ง source code มาที่ CourseVille โดยตั้งชื่อไฟล์เป็น “Assignment1_6XXXXXXX21.pdf” เมื่อ “6XXXXXXX21” คือรหัสประจำตัวนิสิต
2. คะแนนของแต่ละ assignment จะมาจากจำนวน test passed ที่ทำ อย่างไรก็ตาม source code ชุดนี้ maintain มานานหลายปีและอาจจะมีบางส่วนที่ assert ไม่ตรง เนื่องด้วย versioning และ distribution behavior อาจจะส่งผลให้แม้จะได้ result ที่ถูกต้อง แต่ก็ test failed ได้, นิสิตสามารถแจ้ง TA ได้เลยนะครับ TA จะทำการ check และให้คะแนนตามคำตอบที่ถูกต้อง
