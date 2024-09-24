import yfinance as yf
import sys

def evaluateFrame(lastFrame, frame):
    score = 0

    for i in range(len(frame) - 1):
        l = frame[i]
        n = frame[i + 1]
        dF = l - n

        l = lastFrame[i]
        n = lastFrame[i + 1]
        dLF = l - n

        score += abs(dF - dLF) * (i + 1)

    return score

def predict(ticker: str, timeFrame = 30):
    msft = yf.Ticker(ticker)

    stock = msft.history(period="1d", interval="1m")["Open"].tolist()
    lastFrame = stock[-timeFrame : -1]
    lastFrame.append(stock[-1])
    print("Last frame")
    print(lastFrame)
    print()
    best = sys.maxsize # initialize best at max integer size
    bestIndex = 0
    bestShift = 0
    bestFrame = []
    for i in range(len(stock) - 2 * timeFrame + 1):
        frame = stock[i : i + timeFrame]
        score = evaluateFrame(lastFrame, frame)
        shift = sum(frame) / len(frame) - sum(lastFrame) / len(lastFrame)
        if score <= best:
            best = score
            bestFrame = frame
            bestIndex = i
            bestShift = shift

    print("Best frame")
    print(bestFrame)
    print("Best score i =", bestIndex, "last =", len(stock) - 1, "shift =", bestShift)
    print(best)
    futureFrame = stock[bestIndex + timeFrame + 1 : bestIndex + timeFrame * 2 + 1]
    for i in range(len(futureFrame) - 1):
        futureFrame[i] -= bestShift
        bestFrame[i] -= bestShift

    return best, lastFrame, bestFrame, futureFrame


if __name__ == "__main__":
    print(predict("MSFT"))