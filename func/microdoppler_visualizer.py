
import numpy as np
import mmwave.dsp as dsp
from mmwave.dataloader import DCA1000
import matplotlib.pyplot as plt

plt.close("all")

def microdoppler_visualizer(uDoppler):
    from matplotlib.widgets import Slider, Button
            
    uDoppler_time = uDoppler.transpose(2,1,0)
    uDoppler_rang = uDoppler.transpose(1,0,2)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    plt.subplots_adjust(left=0.25, bottom=0.25)

    img1 = ax1.imshow(uDoppler_rang[0], aspect='auto')
    ax1.set_title('uDoppler Plot')
    
    img2 = ax2.imshow(uDoppler_time[0], aspect='auto')
    ax2.set_title('Range Doppler Plot')
        
    axcolor = 'white'

    range_idx = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    time_idx = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

    srange = Slider(range_idx, 'Range', 1, uDoppler.shape[1]-1, valinit=0, valstep=1)    
    trange = Slider(time_idx, 'Time', 1, uDoppler.shape[2]-1, valinit=0, valstep=1)    
            
    def update(val):
        r = int(srange.val)
        img1.set_data(uDoppler_rang[r])
        t = int(trange.val)
        img2.set_data(uDoppler_time[t])
        img1.autoscale()
        img2.autoscale()
        fig.canvas.draw_idle()
    srange.on_changed(update)
    trange.on_changed(update)
    
    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    
    def reset(event):
        srange.reset()
        trange.reset()
    button.on_clicked(reset)
    
    plt.show()

    
def stitch_visualizer(uDoppler, chirp_period, doppler_resolution, title='uDoppler w/ range selection', cmap_plot='jet'):
    plt.figure()
    plt.imshow(uDoppler,origin='lower',aspect='auto',extent=(0,chirp_period*uDoppler.shape[1],-uDoppler.shape[1]*doppler_resolution/2,uDoppler.shape[1]*doppler_resolution/2),cmap=cmap_plot)
    plt.title(title)
    plt.ylabel("Doppler (m/s)")
    plt.xlabel("Time (s)")


def range_azimuth_visualizer(x):
    from matplotlib.widgets import Slider, Button
    
    x = x/x.max() # Scale to [0,1]

    fig, ax1 = plt.subplots(1,1)

    img1 = ax1.imshow(x[0], aspect='auto', vmin=0.0, vmax=1.0)
    ax1.set_title('Range Azimuth Plot')
    fig.colorbar(img1)
    axcolor = 'white'

    plt.subplots_adjust(left=0.25, bottom=0.25)

    time_idx = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    
    trange = Slider(time_idx, 'Time', 1, x.shape[0]-1, valinit=0, valstep=1)    

    def update(val):

        t = int(trange.val)
        img1.set_data(x[t])
        # img1.autoscale()

        fig.canvas.draw_idle()
    trange.on_changed(update)
    
    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    
    def reset(event):
        trange.reset()
    button.on_clicked(reset)
    
    plt.show()
    

def classification_data_visualizer(x, label=None):
    from matplotlib.widgets import Slider, Button
    
    # x = x/x.max() # Scale to [0,1]

    fig, ax1 = plt.subplots(1,1)

    # img1 = ax1.imshow(x[0], aspect='auto', vmin=0.0, vmax=1.0)
    img1 = ax1.imshow(x[0], aspect='auto')
    ax1.set_title('MicroDoppler Spectrogram Plot')
    fig.colorbar(img1)
    axcolor = 'white'

    plt.subplots_adjust(left=0.25, bottom=0.25)

    time_idx = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

    trange = Slider(time_idx, 'Sample', 1, x.shape[0]-1, valinit=0, valstep=1)    

    def update(val):

        t = int(trange.val)
        img1.set_data(x[t])
        ax1.set_title('MicroDoppler Spectrogram Plot: ' + label[t] + ' ' + str(t))
        # img1.autoscale()

        fig.canvas.draw_idle()
    trange.on_changed(update)
    
    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    
    def reset(event):
        trange.reset()
    button.on_clicked(reset)
    
    plt.show()


def feature_viewer(x, nFeatures, n_row, n_col, title='PCA Features'):
    """ Grid view of features extracted using PCA

    """
    fig, axs = plt.subplots(4, 4, sharex='all', sharey='all', figsize=(10, 10))
    fig.suptitle(title, fontsize=16, x=0.55, y=0.95)

    fig.subplots_adjust(hspace = 0.15, wspace=.15)

    axs = axs.ravel()
    for i in range(nFeatures):
        axs[i].imshow(np.reshape(x[i], (n_row,n_col) ,'F'), aspect='auto', cmap='jet')
        axs[i].set_title('Feature ' + str(i+1))
        axs[i].axis('off')

    plt.show()