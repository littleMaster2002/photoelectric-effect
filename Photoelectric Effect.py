import tkinter
import time
import math

# Set starting point and dimensions of photons.
startX = 271
startY = 54
radius = 14
movement = 5

# The metal used for this simulation is sodium. Below are the properties of sodium.
thresholdFrequency = 5.50e14
maximumWavelength = 3e8 / thresholdFrequency

# counters will be used to determine whether a particle is a photon (0) or an electron (1).
counters = [0]
# particles will be used to store all the particles created by the program (both photons and electrons)
# Stored in the same sequence as the counters
particles = []
# iteration will be used to show the effect of changing intensity on the number of photoelectrons emitted.
iteration = 0

window = tkinter.Tk()
window.title("Photoelectric Effect")
window.geometry("800x600")

canvas = tkinter.Canvas(window)
canvas.configure(bg="black")
canvas.pack(fill="both", expand=True)
# Create the metal.
canvas.create_rectangle(5, 260, 25, 340, fill="grey", width=2)
# Create the light source from which photons will be emitted
# angled at 45 degrees to the vertical and aimed directly towards the metal
points = [
    [257,40],
    [285,68],
    [313,40],
    [285,12]
    ]
canvas.create_polygon(points,fill="red")

# Create two sliders so the user can adjust wavelength and intensity settings during the running of the program
# User can only select wavelengths between 400 nm and 700 nm (visible light).
a = tkinter.Scale(window,from_=400,to=700,orient=tkinter.HORIZONTAL,label='Wavelength')
a.pack()

b = tkinter.Scale(window,from_=1,to=10,orient=tkinter.HORIZONTAL,label='Intensity')
b.pack()

# Create an exit button for the user.
def endProgram():
    window.destroy()

button = tkinter.Button(window, text = "Exit", command = endProgram)
button.pack()

def movingParticle(counters,iteration):
# Use while loop in order to continuously update the position of particles.
    while True:
# Extract the values for wavelength and intensity selected by the user.
        wavelength = int(a.get())
        wavelength = wavelength / 1000000000
        intensity = int(b.get())
# The number of photons created depends on the intensity - higher intensity means more photons emitted as the rate will be higher.
        if iteration % (20-intensity) == 0:
            particles.append(canvas.create_oval(startX-radius,startY-radius,startX+radius,
                                        startY+radius,fill="blue", width=4))
            counters.append(0)
# For all of the particles that have been created so far...
        for i in range(len(particles)):
# ...if the particle is a photon, move it diagonally towards the metal at a fixed speed...
            if counters[i] == 0:
                canvas.move(particles[i],-movement,movement)
                particlePos = canvas.coords(particles[i])
                xl,yl,xr,yr = particlePos
# ...or if the particle is an electron, move it horizontally away from the metal...
            if counters[i] == 1:
# ...only if the frequency of the incoming radiation is above the threshold frequency.
                if wavelength < maximumWavelength:
# The speed at which the particle moves away is determined by the wavelength of the incoming radiation (the lower the wavelength, the faster the movement, since there is more energy).
                    canvas.move(particles[i],movement-((wavelength-400e-9)*1e7),0)
# Colour all electrons green.
                    canvas.itemconfig(particles[i],fill="green")
                    particlePos = canvas.coords(particles[i])
                    try:
                        xl,yl,xr,yr = particlePos
                    except ValueError:
                        pass
                if wavelength > maximumWavelength:
                    canvas.delete(particles[i])
# Update the counter for a particle by determining when it reaches the metal. 
            if xl == 22:
                counters[i] += 1
# Increment the iteration by 1 at the end of each run.
        iteration += 1
        window.update()

movingParticle(counters,iteration)
