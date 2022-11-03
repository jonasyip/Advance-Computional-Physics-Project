import numpy as np
from nbody_system import system, body
from matplotlib import pyplot as plt
import matplotlib.animation

path = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\Cython_2"
filename = "frames.npy"
filepath = "%s\%s" % (path, filename)

frames = np.load(filepath, allow_pickle=True)
total_frames = len(frames)

def animate(i):
    snapshot = frames[i]
    x = []
    y = []
    z = []
    for body in snapshot:
        x.append(body.x)
        y.append(body.y)
        z.append(body.z)
    graph._offsets3d = (x, y, z)
    title.set_text('time={}'.format(i))



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

snapshot0 = frames[0]
x = []
y = []
z = []
for body1 in snapshot0:
    x.append(body1.x)
    y.append(body1.y)
    z.append(body1.z)
graph = ax.scatter(x, y, z)

title = ax.set_title('time=0')

ani = matplotlib.animation.FuncAnimation(fig, animate, (total_frames-1), interval=200, blit=False)
plt.show()