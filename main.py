import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk


# define variables
offset = 0
N = 100
psi = [0+0j] * N
mid = N // 2
psi[mid + offset] = 0.39
psi[mid-1 + offset] = 0.24
psi[mid-2 + offset] = 0.065
psi[mid+1 + offset] = 0.24
psi[mid+2 + offset] = 0.065
v = [0+0j] * N
opn = 0.0
m = 1
history = []
ts = 10
steps = 100



def calc():
    # ensure progressbar range matches this run
    prog['maximum'] = ts * steps
    prog['value'] = 0

    for k in range(ts * steps):
        # update progress bar (and allow GUI to refresh)
        prog['value'] = k + 1
        menu.update_idletasks()

        # store a snapshot (make a copy)
        history.append(psi.copy())
        # reset per-step arrays
        dx = [0+0j] * len(psi)
        dy1 = [0+0j] * len(psi)
        dy2 = [0+0j] * len(psi)

        # adds the potential energy
        for i in range(len(dx)):
            dx[i] = dx[i] + (v[i] * psi[i])

        # adds the kinetic energy (first derivative-like)
        for i in range(len(dy1)):
            if i == 0:
                dy1[i] = ((psi[i+1] - psi[i]) + 0)/2
            elif i == len(dy1)-1:
                dy1[i] = ((psi[i] - psi[i-1]) + 0)/2
            else:
                dy1[i] = ((psi[i] - psi[i-1]) + (psi[i+1] - psi[i]))/2

        # adds it again (second derivative-like) and combine into dx
        for i in range(len(dy2)):
            if i == 0:
                dy2[i] = ((dy1[i+1] - dy1[i]) + 0)/2
            elif i == len(dy2)-1:
                dy2[i] = ((dy1[i] - dy1[i-1]) + 0)/2
            else:
                dy2[i] = ((dy1[i] - dy1[i-1]) + (dy1[i+1] - dy1[i]))/2

            dy2[i] = dy2[i] * -(1/(2*m))
            dx[i] = dx[i] + dy2[i]

        # applies it to psi
        for i in range(len(psi)):
            psi[i] = psi[i] + (dx[i]*complex(0,1))/ts



def plot():
    # prepare 2D heatmap of probability density |psi|^2
    if len(history) == 0:
        # no history yet — use current psi as a single time step
        Z = np.array([[abs(ampl) for ampl in psi]])  # shape (1, N)
    else:
        Z = np.array([[abs(ampl) for ampl in state] for state in history])  # shape (T, N)
    T = Z.shape[0]

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(Z, origin='lower', aspect='auto', extent=[0, N-1, 0, max(T-1, 0)], cmap='viridis', interpolation='nearest')
    ax.set_xlabel('position index')
    ax.set_ylabel('time step')
    ax.set_title('Probability density |psi| (2D)')
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('|psi|^2')
    plt.show()



def calcnplot():
    global ts, steps, history, m, offset
    m = int(mb.get())
    ts = int(tsb.get())
    steps = int(stepb.get())
    offset = int(offb.get())
    reset_history()
    calc()
    plot()

def reset_history():
    global history, psi, mid, offset, opn, N
    prog['value'] = 0
    N = int(nb.get())
    opn = 0
    history = []
    # reset psi to the original localized initial state
    psi = [0+0j] * N
    mid = N // 2
    psi[mid + offset] = 0.39
    psi[mid-1 + offset] = 0.24
    psi[mid-2 + offset] = 0.05
    psi[mid+1 + offset] = 0.24
    psi[mid+2 + offset] = 0.05
    if pot_var.get() == 1:
        v[int(N//4)] = 1
        v[int(N//4)*3] = 1
    else:
        v[int(N//4)] = 0
        v[int(N//4)*3] = 0

# Gui
menu = tk.Tk()
icon = tk.PhotoImage(file="psi.png")
menu.title("Quantum simulator")
menu.iconphoto(False, icon)
tk.Label(menu, text='Time scale').grid(row=0, column=0)
tk.Label(menu, text='Steps').grid(row=1, column=0)
tk.Label(menu, text='Mass').grid(row=2)
tk.Label(menu, text='Offset').grid(row=3)
tk.Label(menu, text="pot walls").grid(row=0, column=2)
tk.Label(menu, text="N").grid(row=1, column=2)
tsb = tk.Spinbox(menu, from_=1, to=1000,)
stepb = tk.Spinbox(menu, from_=1, to=10000)
mb = tk.Scale(menu, from_=1, to=10, orient=tk.HORIZONTAL)
offb = tk.Scale(menu, from_=-((N/2)-3), to=((N/2)-3), orient=tk.HORIZONTAL)
nb = tk.Spinbox(menu, from_=10, to=500)
pot_var = tk.IntVar()
pot = tk.Checkbutton(menu, text="Enable", variable=pot_var)
# create progressbar with menu as parent and determinate mode
prog = ttk.Progressbar(menu, orient='horizontal', length=170, mode='determinate')
tsb.grid(row=0, column=1)
stepb.grid(row=1, column=1)
mb.grid(row=2, column=1)
offb.grid(row=3, column=1)
nb.grid(row=1, column=3)
pot.grid(row=0, column=3)
prog.grid(row=4, column=3)
Bt = tk.Button(menu, text ="calculate", command = calcnplot)
Bt.grid(row=4)
tk.mainloop()