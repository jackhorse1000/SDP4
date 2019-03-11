# How to use Spencer

## How to SSH into Spencer

1. Make sure the raspberry pi is powered on
2. Log on to your dice computer
3. Go on a dice machine and do
   * In terminal type

````terminal
ssh student@squirtle
````

* You will then be prompted for a password
  * password = "password"

## How to sshfs(file mount) Spencer

1. Make sure the raspberry pi is powered on
2. Log on to your dice computer
3. Use the terminal to do the following
   1. In your home directory create a file called mount, if one already exists you can skip this step

````terminal
mkdir mount
````

Now do the following command so that the Pi's file system is on dice

````terminal
sshfs student@squirtle: mount
````

Then go into mount

````
cd mount
````

You should now see the contents of the pi

**The file system is now mounted wooo!**

### Retrieve from Git

**Inside the mount** directory **after you have mounted(used sshfs)** create a directory with you name, if you have done this just go into the directory

````terminal
mkdir jack
cd jack
````

Now clone the repo and go into it

````terminal
git clone https://github.com/jackhorse1000/SDP4.git
cd SDP
````

You may need to change branch to get the code you want to test use

````
git checkout <branch-name>
````

Current branch is *feature/step-nav* But this could change so Ask!

### Running and using the Server

Now to run the server,

**After using ssh** to connect to the Pi, navigate to the directory where the server is. For me it would be

````
cd jack/SDP/src/
````

To run the server use the following command

````
python3 server.py
````

Use Caesar's phone or your own Android to connect to Spencer.
When using the app click the **Connect** Button from there I hope it is easy enough to understand

### Putting the App on your phone

* Clone the repo

````terminal
git clone https://github.com/jackhorse1000/SDP4.git
````

* Open Android Studio
* From Android Studio open the folder App/ inside the cloned repo
* Then connect your phone and run it