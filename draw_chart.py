import matplotlib.pyplot as plt
from datetime import datetime

def draw_chart(timestamp, rsi, pair):
    time = datetime.now()
    print(f"time: {time}")
    # Plot RSI vs. time
    plt.figure(figsize=(12, 6))
    plt.plot(time, rsi, label='RSI')
    plt.xlabel('Time')
    plt.ylabel('RSI')
    plt.title(f'RSI vs. Time for {pair}')
    plt.legend()
    plt.grid()
    plt.show()
   