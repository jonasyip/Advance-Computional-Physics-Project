import numpy as np
from nbody_system import system, body
from matplotlib import pyplot as plt
import matplotlib.animation

path = r"C:\Users\Student\OneDrive\Bristol University\Physics Year 4\Advanced Computational Physics\Advance-Computional-Physics-local-machine-1\mini_project\Direct approach\Python"
filename = "frames.npy"
filepath = "%s\%s" % (path, filename)

frames = np.load(filepath, allow_pickle=True)
total_frames = len(frames)

def animate(i):
    snapshot = frames[i]
    x = []
    y = []
    z = []
    for body1 in snapshot:
        x.append(body1[2])
        y.append(body1[3])
        z.append(body1[4])
    graph._offsets3d = (x, y, z)
    title.set_text('step={}'.format(i))



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim((-1E10, 1E10))
ax.set_ylim((-1E10, 1E10))
ax.set_zlim((-1E10, 1E10))
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

snapshot0 = frames[0]
x = []
y = []
z = []
for body1 in snapshot0:
    x.append(body1[2])
    y.append(body1[3])
    z.append(body1[4])
graph = ax.scatter(x, y, z)

title = ax.set_title('step=0')



ani = matplotlib.animation.FuncAnimation(fig, animate, (total_frames-1), interval=2, blit=False)
plt.show()