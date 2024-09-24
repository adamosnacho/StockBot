import time
import yfinance as yf
from matplotlib import pyplot as plt
from bot import predict  # Using your custom bot library

# Run the prediction function with the specified time frame
score, lastFrame, bestFrame, futureFrame = predict("MSFT", 30)

if lastFrame and futureFrame:
    # Create x-axis values centered at 0: negative for lastFrame, positive for futureFrame
    last_len = len(lastFrame)
    future_len = len(futureFrame)
    combined_data = lastFrame + futureFrame
    x_values = list(range(-last_len + 1, 1)) + list(range(1, future_len + 1))

    # Create x-values for bestFrame to overlay on the left side of the lastFrame
    best_x_values = list(range(-last_len + 1, 1))

    # Create the initial plot
    plt.figure(figsize=(14, 6))
    plt.plot(x_values, combined_data, marker='o', linestyle='-', color='blue', label='Stock Prices')

    # Overlay the bestFrame on top of lastFrame with a different color
    plt.plot(best_x_values, bestFrame, marker='o', linestyle='--', color='green', label='Best Frame Match')

    # Mark the transition point between lastFrame and futureFrame
    plt.axvline(x=0, color='red', linestyle='--', label='Past | Future')

    # Display the score in the plot title for easy reference
    plt.title(f"MSFT Stock Prediction (Score: {score})")
    plt.xlabel("Time relative to start, minutes")
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Fetch live stock price and update the plot in real-time
    current_prices = []
    start_time = time.time()

    while time.time() - start_time < 1800:  # Run for 5 minutes (300 seconds)
        # Get the latest stock price using yfinance
        msft_data = yf.download('MSFT', period='1d', interval='1m')
        current_price = msft_data['Open'][-1]  # Get the last available closing price

        # Store current price for plotting
        current_prices.append(current_price)

        # Plotting current prices against the x-values
        # The x-values for the current prices are set relative to the end of the prediction range
        plt.plot([i for i in range(len(current_prices))], current_prices,
                 marker='x', linestyle='-', color='orange', label='Current Price')

        # Update the plot
        plt.pause(60)  # Update every 10 seconds

    plt.show()
