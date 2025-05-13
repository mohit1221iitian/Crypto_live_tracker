import requests
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.animation import FuncAnimation

times = []  # Renamed from `time` to `times`
btcu = []
ethu = []
btci = []
ethi = []
max=10
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
fig.set_tight_layout(True)

# Fetch live prices function
def fetch_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    parameters = {'ids': 'bitcoin,ethereum', 'vs_currencies': 'usd,inr'}
    try:
        response = requests.get(url, params=parameters)  # Fixed the typo
        data = response.json()  # Fixed the typo here too
        return data['bitcoin']['usd'], data['bitcoin']['inr'], data['ethereum']['usd'], data['ethereum']['inr']
    except Exception as e:
        print('API ERROR', e)
        return None, None, None, None

# Animation function to update the graph
def animate(i):
    btcu_val, btci_val, ethu_val, ethi_val = fetch_prices()  # Renamed the variables to avoid confusion
    if btcu_val is None or ethu_val is None or btci_val is None or ethi_val is None:
        return
    
    # Get the current time in HH:MM:SS format
    curr_time = time.strftime('%H:%M:%S')
    times.append(curr_time)

    # Append the fetched data to respective lists
    btcu.append(btcu_val)
    btci.append(btci_val)
    ethu.append(ethu_val)
    ethi.append(ethi_val)

    timeo=times[-max:]
    btcuo=btcu[-max:]
    btcio=btci[-max:]
    ethio=ethi[-max:]
    ethuo=ethu[-max:]
    # Clear previous plot data and redraw
    ax1.clear()
    ax2.clear()

    # Plot data on respective axes
    ax1.plot(timeo, btcuo, label='BTC_USD')
    ax1.plot(timeo, ethuo, label='ETH_USD')
    ax2.plot(timeo, btcio, label='BTC_INR')
    ax2.plot(timeo, ethio, label='ETH_INR')

    # Add titles, labels, and legends
    ax1.set_title("Live Crypto Tracker (USD)")
    ax2.set_title("Live Crypto Tracker (INR)")
    ax1.set_ylabel('USD')
    ax2.set_ylabel('INR')
    ax2.set_xlabel('Time')

    ax1.legend()
    ax2.legend()
    for label in ax2.get_xticklabels():
        label.set_rotation(45)
    # Adjust layout for better spacing
    fig.tight_layout()  # Fixed the layout adjustment method

# Create the animation
ani = FuncAnimation(fig, animate, interval=1000)

# Show the plot
plt.show()
